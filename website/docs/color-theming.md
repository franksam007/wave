---
title: Color Theming
---


Wave ships with prebuilt themes that are ready to be used. These include:

* `default`
* `neon`
* `h2o-dark`
* `benext`
* `ember`
* `fuchasia`
* `kiwi`
* `lighting`
* `monokai`
* `nature`
* `nord`
* `oceanic`
* `one-dark-pro`
* `solarized`
* `winter-is-coming`

Setting a theme is very simple:

```py
q.page['meta'] = ui.meta_card(box='', theme='h2o-dark')
```

## Custom user-defined themes

Having only predefined color palettes keeps you from matching your Wave app to your specific color brand, so we have added custom, user-defined palettes.

When using custom colors, first a new `ui.theme` needs to be registered within the `themes` attribute in `ui.meta_card`. It takes the name of the theme and 4 main colors as arguments:

* `primary` - Accent color for primary buttons, checkboxes etc.
* `text` - Default text color.
* `card` - Card background color.
* `page` - Base background color behind cards.

After the theme is successfully registered, you can use it in the same fashion as predefined themes, by setting `ui.meta_card`'s `theme` attribute.

```py
q.page['meta'] = ui.meta_card(
    box='',
    themes=[
        ui.theme(
            name='my-awesome-theme',
            primary='#13ebe7',
            text='#e8e1e1',
            card='#12123b',
            page='#070b1a',
        )
    ],
    theme='my-awesome-theme'
)
```

:::tip
You can register multiple themes, which might be handy for switching between the light / dark mode of your app.
:::

### Theme generator

Wave ships with a simple app that allows you to pick colors and see how they work together instantly.

This Wave app provides:

* Immediate visual feedback.
* Color contrast warnings when a particular contrast ratio is less than [4.5](https://www.w3.org/TR/UNDERSTANDING-WCAG20/visual-audio-contrast-contrast.html).
* Quick theme copy-pasting.

Simply run:

```sh
./venv/bin/wave run examples.theme_generator
```

Then visit <http://localhost:10101/demo>.

![theme-generator](assets/theme-generator.gif)

We would love to see all the beautiful themes our community came up with so don't hesitate and post the screenshots into our [show and tell](https://github.com/h2oai/wave/discussions/categories/show-and-tell) Github Discussions section! The best ones might even be included as predefined themes within Wave itself in the future.

## Can individual colors be changed?

In general, the answer is no. Wave tries to be smart and do all the minor decisions for you, e.g. picking a color for primary/secondary buttons, checkboxes, etc. This way, a consistent UX is ensured and you can focus solely on the product itself rather than wasting time on nitpicking small stuff.

However, some cards allow changing colors of particular parts, for example, icons, but this is more of an exception rather than a strict rule.

If full control over colors/typography etc. is needed, going with regular HTML/CSS/JS is probably a better choice.
