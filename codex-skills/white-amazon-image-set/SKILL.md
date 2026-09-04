---
name: white-amazon-image-set
description: Create or redesign clean white-background Amazon listing image sets, including compliant 1:1 main images, secondary feature infographics, lifestyle-use collages, and A+ visuals. Use when the user asks for Amazon product images, white-background ecommerce layouts, listing-image prompts, consistent typography hierarchy, product feature graphics, or a coordinated image set derived from product and reference images.
---

# White Amazon Image Set

Build a coordinated Amazon image set with product fidelity, restrained typography, strong hierarchy, and generous white space. Treat supplied product images as identity references and supplied style images as layout references unless the user says otherwise.

## Workflow

1. Classify the asset before designing:
   - **Main image**: use a 1:1 pure-white canvas; show only the product or an allowed apparel model; omit text, badges, diagrams, effects, borders, and extra props.
   - **Secondary listing image**: allow headlines, feature icons, lifestyle context, callouts, and restrained product effects.
   - **A+ image**: use the requested module size or the reference aspect ratio; never assume 1:1.
2. Inspect every input image. Lock the product's shape, materials, colors, controls, accessories, proportions, and supplied claims.
3. Select one composition pattern from this skill. Do not mix every pattern into one image.
4. Write all required copy verbatim before composing. Do not invent specifications, performance claims, certifications, medical claims, or included accessories.
5. Generate or edit the visual. For text-heavy images, prefer generating the photography without text and applying typography deterministically when possible.
6. Verify product fidelity, spelling, hierarchy, alignment, whitespace, and Amazon asset-type constraints.

## Learned Visual System

Use this system when the user asks to match the style learned from the massage-roller references `4.png` and `7.png`.

### Canvas and background

- Default listing-image canvas: square 1:1, ideally 2000-2048 px.
- Use pure white `#FFFFFF` for main images.
- For secondary images, use white to very light neutral gray, approximately `#F5F5F5` to `#FFFFFF`.
- Keep backgrounds bright and low-noise. Use only soft, realistic contact shadows under the product.
- Reserve 6-8% outer safe margins for copy and icons.

### Core color palette

- Primary headline deep teal: `#063B4C`.
- Darker headline alternative: `#062832`.
- Primary body text and icons: `#080A0B` to `#111111`.
- Secondary body text: `#262626` to `#333333`.
- Dividers: `#D5D9DB` at low visual weight.
- Background: `#FFFFFF`; secondary-image neutral: `#F5F5F5`.
- Keep normal text monochrome except for the deep-teal headline.
- Allow blue, red, or green only as small product-derived functional accents, such as LEDs, heat, or battery visualization. Do not reuse these accents decoratively in headings or peer icons.

### Typography

- Use one clean modern sans-serif family throughout. Prefer Arial, Helvetica, Inter, or a similar neutral grotesk.
- Use sentence case or title case. Avoid condensed display fonts, italics, outlines, bevels, and decorative effects.
- Use weight 700-800 for main headlines and key numbers, 600-700 for feature headings, and 400-500 for body copy.
- Keep line spacing compact for headlines and relaxed for explanatory copy.
- Left-align major headlines and paragraphs. Center only repeated metric cells when the grid benefits from it.

Use proportional sizes so the hierarchy survives different square resolutions:

| Level | Size as % of canvas width | 2000 px reference | Color and weight |
| --- | ---: | ---: | --- |
| Main headline | 3.8-4.8% | 76-96 px | Deep teal, 700-800 |
| Lead/subheadline | 2.0-2.6% | 40-52 px | Black, 400-500 |
| KPI numeral | 4.8-6.2% | 96-124 px | Black, 700-800 |
| KPI unit/short label | 1.6-2.1% | 32-42 px | Black, 500-700 |
| Feature heading | 2.0-2.5% | 40-50 px | Black, 600-700 |
| Feature description | 1.5-1.9% | 30-38 px | Dark gray, 400 |

Apply these relationships rather than forcing every level into an image. Use at most four visible text levels per composition.

### Spacing and alignment

- Use a consistent left edge for headline, subheadline, and body copy.
- Keep the main headline 0.35-0.55 headline-heights above its subheadline.
- Keep copy blocks short: one or two headline lines and no more than two body lines where possible.
- Separate repeated feature cells with thin light-gray vertical rules, not boxes.
- Use equal column widths and align icon centers, baselines, and caption blocks.
- Avoid rounded cards, colored pills, heavy borders, shadows behind text, or scattered labels.

### Icons and information graphics

- Use simple black outline icons with consistent stroke thickness.
- At a 2000 px canvas, use approximately 4-7 px icon strokes.
- Pair one icon with one message. Keep icons optically similar in size.
- Use bold numerals as the primary information cue and smaller units beside or below them.
- Do not place every icon inside a colored circle. Let line icons sit directly on the white background.

## Composition Patterns

### Pattern A: Product-led specification infographic

Use for battery, charging, performance, modes, dimensions, or technical features.

- Place the large product hero in the upper 48-58% of the canvas.
- Keep the product centered or slightly elevated, with a soft contact shadow and ample white space.
- Place a one-line deep-teal headline below the hero, followed by a smaller black lead sentence.
- Build the primary metric row as 3-4 equal columns beneath the lead sentence.
- Use one black outline icon, one bold number or short label, and one explanatory caption per column.
- Add an optional secondary trust row with 2-3 benefits such as portability, reliability, or convenience.
- Separate columns with thin gray rules. Do not enclose the grid in cards.

### Pattern B: Lifestyle breadth with central product hero

Use to show audience range, multiple sports, or use scenarios.

- Divide the upper 42-50% into 3-4 equal vertical lifestyle panels.
- Use authentic, bright action photography with consistent lighting and white separators.
- Fade the lower edges of the lifestyle panels smoothly into white.
- Place the product hero across the middle, overlapping the fade area while remaining clearly separated from the people.
- Place a two-line deep-teal headline in the lower-left information zone.
- Add one short black supporting paragraph beneath it, ideally no more than two lines.
- Keep the lower-right area mostly open; do not fill it with decorative badges.

### Pattern C: Compliant main image

Use for Amazon image position 1.

- Use a 1:1 pure-white canvas with the product occupying approximately 85% of the frame.
- Center the product, preserve every physical detail, and use only a natural contact shadow.
- For apparel, use a natural professional standing pose when a model is requested; keep the garment fully visible and undistorted.
- Remove all text, icons, effects, inset images, packaging not included with the product, and lifestyle scenery.

## Prompt Construction

State these roles explicitly:

- `Edit target`: the image whose product identity and physical details must remain.
- `Product reference`: supporting views used to understand construction or accessories.
- `Style reference`: used only for composition, typography, color, lighting, or hierarchy.

Include:

1. Asset type and exact dimensions/aspect ratio.
2. Product invariants.
3. Selected composition pattern.
4. Exact text in quotation marks.
5. Typography levels and proportional sizes.
6. Deep-teal/black/white palette.
7. Forbidden changes and unsupported claims.

## Quality Gate

Before delivery, confirm:

- The product shape, controls, materials, colors, and included parts match the reference.
- The asset type is correct: main image, secondary image, or A+.
- All required text is exact, legible, and free of duplicated or invented words.
- The headline is deep teal; ordinary text and icons are black or dark gray.
- No more than four typography levels are visible.
- The product remains the strongest visual element.
- Icons share one line style and repeated cells align consistently.
- White space is intentional; no unnecessary cards, labels, glows, or decorative clutter were added.
- Human anatomy, hands, faces, and equipment interactions are plausible in lifestyle imagery.

## 中文名称与说明

- 中文名称：亚马逊白底图组
- 用途说明：创建或优化亚马逊白底商品图片组。
