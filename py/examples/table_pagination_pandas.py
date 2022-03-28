# Table / Pagination / Pandas
# Use a paginated #table to display large (100k+ rows) tabular data using pandas dataframe.
# #form #table #pagination #pandas
# ---

import os
from typing import List
from h2o_wave import main, app, Q, ui
import pandas as pd


all_issues_df = pd.DataFrame(
    [[i + 1, 'Closed' if i % 2 == 0 else 'Open'] for i in range(100)],
    columns=['text', 'status']
)
rows_per_page = 10
total_rows = len(all_issues_df)


def df_to_table_rows(df: pd.DataFrame) -> List[ui.TableRow]:
    return [ui.table_row(name=str(r[0]), cells=[str(r[0]), r[1]]) for r in df.itertuples(index=False)]


def get_df(q: Q):
    # Make a deep copy in order to not mutate the original df which serves as our baseline.
    df = all_issues_df.copy()

    if q.client.sort:
        # Reverse values since default sort of Wave table is different from Pandas.
        ascending = [not v for v in list(q.client.sort.values())]
        df = df.sort_values(by=list(q.client.sort.keys()), ascending=ascending)
    # Filter out all rows that do not contain searched string in `text` cell.
    if q.client.search:
        df = df[df.text.apply(str).str.contains(q.client.search)]
    # Filter out rows that do not contain filtered column value.
    if q.client.filters:
        # We want only rows that have no filters applied or their col value matches active filters.
        query = ' & '.join([f'({not bool(filters)} | {col} in {filters})' for col, filters in q.client.filters.items()])
        df = df.query(query)

    return df


@app('/demo')
async def serve(q: Q):
    if not q.client.initialized:
        q.page['meta'] = ui.meta_card(box='')
        q.page['form'] = ui.form_card(box='1 1 -1 -1', items=[
            ui.table(
                name='table',
                columns=[
                    ui.table_column(name='text', label='Text', sortable=True, searchable=True, link=False),
                    ui.table_column(name='status', label='Status', filterable=True),
                ],
                rows=df_to_table_rows(get_df(q)[0:rows_per_page]),
                resettable=True,
                downloadable=True,
                pagination=ui.table_pagination(total_rows, rows_per_page),
                # Make sure to register the necessary events for the feature you want to support, e.g. sorting.
                # All the registered events have to be handled by the developer.
                # `page_change` event is required to be handled for pagination to work.
                events=['sort', 'filter', 'search', 'page_change', 'download', 'reset']
            )
        ])
        q.client.initialized = True

    # Check if user triggered any table action and save it to local state for allowing multiple
    # actions to be performed on the data at the same time, e.g. sort the filtered data etc.
    if q.events.table:
        table = q.page['form'].items[0].table
        if q.events.table.sort:
            q.client.sort = q.events.table.sort
            q.client.page_offset = 0
        if q.events.table.filter:
            q.client.filters = q.events.table.filter
            q.client.page_offset = 0
        if q.events.table.search is not None:
            q.client.search = q.events.table.search
            q.client.page_offset = 0
        if q.events.table.page_change:
            q.client.page_offset = q.events.table.page_change.get('offset', 0)
        if q.events.table.reset:
            q.client.search = None
            q.client.sort = None
            q.client.filters = None
            q.client.page_offset = 0
            table.pagination = ui.table_pagination(total_rows, rows_per_page)

        offset = q.client.page_offset or 0
        df = get_df(q)

        if q.events.table.download:
            # Create and upload a CSV file for downloads.
            df.to_csv('data_download.csv')
            download_url, = await q.site.upload(['data_download.csv'])
            # Clean up.
            os.remove('data_download.csv')
            q.page['meta'].script = ui.inline_script(f'window.open("{download_url}")')

        # Update table pagination according to the new row count.
        if q.client.search is not None or q.client.filters:
            table.pagination = ui.table_pagination(len(df), rows_per_page)

        table.rows = df_to_table_rows(df[offset:offset + rows_per_page])

    await q.page.save()
