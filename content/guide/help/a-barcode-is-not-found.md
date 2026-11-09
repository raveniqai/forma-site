---
title: A barcode is not found
summary: What to do when the scanner finds nothing.
order: 10
---

# A barcode is not found

Sometimes a scan reads the bars cleanly and Forma still cannot log the food. This page explains what each message means and the quickest way to log the meal anyway.

## When to use it

- The scanner read the bars, but Forma says the barcode is not in the database.
- Open Food Facts knows the product but has no nutrition figures for it.
- The lookup could not finish because the food database could not be reached.
- The camera will not start at all, so there is nothing to scan with.

## Step by step

1. Tap **Enter it by hand** on the message.
2. Type the food's name, the grams, and the protein, carbs and fat from the label.
3. Check the numbers, then save.
4. Or tap **Search instead** and search for the food by name in `Search foods`.
5. Tap a result.
6. Change the Grams if you need to, check the numbers, and save.

> **Tip:** If the bars will not read at all, type the digits printed under the bars into the **Digits under the bars** field and tap **Look up**. A barcode has 6 to 14 digits. **Look up** waits until you have typed at least 6 digits. If the entry is too long or has anything but digits, Forma says so instead of searching.

## What each message means

- **"That barcode isn't in Open Food Facts."** The product is missing from the public database. Enter it by hand once, and the next scan finds it. Where meal photos can be read (Apple Intelligence on iPhones that support it, or Forma Power), the message says "That barcode isn't in the database" instead. It adds that a photo of the label is read for the numbers but does not keep the barcode; only a hand entry keeps it.
- **"Open Food Facts knows this product but has no nutrition figures for it."** The product exists in the database, but without usable numbers. Enter them by hand from the label.
- **"Couldn't reach Open Food Facts."** The phone is offline or the database did not answer. Nothing is broken: your own foods and the bundled USDA table still work, and scanning works again when you are back online. After a lookup that could not finish, Forma does not keep the digits; when you are online again, scan once more or type them in.
- **"That doesn't look like a barcode (6 to 14 digits)."** The digits you typed were not a plausible barcode. Check for a missed digit or a letter that slipped in.

## Good to know

- **Enter it by hand** opens the same form as **Manual**. Forma works out the calories from the protein, carbs and fat you type, and you see the numbers before anything is saved.
- A hand entry made after a scan keeps the barcode with the food, as long as the entry is one food. The next scan of that package finds it in your own library straight away, even with no signal.
- In `Search foods`, your own foods come first, then the bundled USDA table, then packaged foods from Open Food Facts.
- A scan checks your own foods first (instant, works with no signal), then Open Food Facts.
- A result never saves itself. Whatever a scan finds lands on the confirm sheet first, where you check the portion and the numbers.
- Scanning runs entirely on your phone with Apple's barcode scanner. The camera is used only while the scanning screen is open; nothing is recorded or kept. Only the barcode itself, or the words you type in a food search, goes out to Open Food Facts.
- If the camera has not been allowed yet, the scan pane shows **Allow the camera to scan** with a button to allow it. If the camera is turned off for Forma in iOS Settings, it shows that with an **Open Settings** button. On a device that cannot scan barcodes, it asks you to type the digits instead.
- Where meal photos can be read, photographing a product's nutrition label (**Photograph its label**) reads the numbers, which you check before saving. It does not attach the barcode. Use **Enter it by hand** if you want the next scan of that package to find the food.

## Related

- [Log food: search, scan or by hand](/guide/eat/log-food/)
- [Ways to log your food](/guide/your-way/ways-to-log-food/)
- [Troubleshooting](/guide/help/troubleshooting/)
- [Saved meals and repeating a meal](/guide/eat/saved-meals/)
