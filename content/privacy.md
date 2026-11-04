# Privacy Policy

Last updated: {{effective_date}}

{{app_name}} ("Forma", "the app") is made by {{publisher}}. Contact: [{{support_email}}](mailto:{{support_email}}).

<!-- TODO-OWNER: the support email is not yet confirmed (see site.config.json). Confirm the mailbox works before publishing. -->

## The short version
- Forma has **no ads**, **no tracking** and **no analytics**, and you do not create an account.
- **Core** keeps your data **on your phone**. The only copy that leaves it is a backup to **your own private iCloud**.
- **Power** (optional, paid) adds **Garmin watch data** and **online AI help** through Forma's own server. Those two features do send data off your phone, as described in [Garmin data and AI](#garmin-data-and-ai). Both are off until you switch them on.
- **Garmin data and anything made from it is never sent to the AI service.** It is not sold and is not used to train or improve any AI model.
- The app looks up foods on **Open Food Facts** when you scan a barcode or search for a food.
- You can **export** or **delete** your data, and **withdraw AI consent**, in Settings at any time. Deleting also deletes your Power account on our server.

## What Forma stores, and where
Everything you enter or connect: profile (height, birth date, sex, goal), weigh-ins, body measurements, workouts and sets, meals and foods you saved, supplements, injuries you log, check-in notes, targets and settings. It is stored in the app's database on your phone.

With Core, we (the developer) cannot see it and do not receive it. With Power, only the specific data described in [Garmin data and AI](#garmin-data-and-ai) reaches our server.

The start date of your free trial is kept in your phone's Keychain and in your iCloud backup, so that reinstalling or restoring does not restart it.

## Garmin data and AI
This section applies only if you subscribe to **Forma Power** and then choose to use Garmin or online AI help. Without Power, none of it happens.

### Garmin data: what we do with it
- **Connecting.** You start it yourself in Settings > Devices > Garmin and sign in on Garmin's own page. Forma never sees your Garmin password.
- **What arrives.** Garmin sends our server data from your watch, for example activities, heart rate, sleep, heart-rate variability, stress, body battery, steps and weight. Which items arrive depends on your watch and your Garmin settings.
- **Use.** Only to show it to you in Forma and to coach you from it, next to your food and training. Some of it is copied to your phone so the app can show it.
- **Not sold, not advertised, not for AI training.** We do not sell Garmin data, share it for advertising, or use it to build advertising profiles. We do not use it, or anything derived from it, to train, evaluate or improve any AI model.

### Who holds or processes it
- **Garmin**, the source of the data, which you connect yourself. Garmin's own privacy policy applies to what Garmin holds.
- **Oracle Cloud Infrastructure**, the cloud provider that hosts Forma's server.
- **Forma's server**, run by {{publisher}}, on that hosting. It holds an open-source service called Open Wearables that stores your Garmin data under a random per-user identifier, not your name. The token that identifies your phone to the server is stored only as a hash.
- **Encrypted backups.** The server database is backed up every night, encrypted, and a limited number of the newest backups are kept.
- **No other party** receives your Garmin data. In particular, the AI service below does not.

### Online AI help: how it works
- **What it is.** Reads a meal photo, estimates a meal you describe, and powers Ask Coach (which is part of Power). Wording of coach messages can also use it.
- **What is sent, only when you use the feature:** the meal photo or description, the question you type to the coach, a substitute request (an exercise and candidate exercises), and a few facts that your phone worked out from your own logs, such as an average protein figure.
- **Never sent:** Garmin data or any other watch data, and anything derived from it. Also not your name, your diary or your history. Our server refuses requests that look like they contain watch data.
- **Route.** Your phone sends the request to Forma's server, which passes it to an online AI provider (currently Groq) and returns the answer. Forma's server keeps nothing you send: no photo, text or answer is stored. It logs only technical facts such as the time, the request type, the model used, and a daily count to enforce a usage limit.
- **The AI provider.** Groq receives the request while it answers it. What Groq does with it is covered by [Groq's privacy policy](https://groq.com/privacy-policy).

<!-- TODO-OWNER: confirm Groq's data-retention and training terms before publishing (the sources say they are unverified) and say so here. Also confirm the provider is still Groq at launch. -->

- **Where it runs instead.** Where Apple Intelligence is available on your iPhone, it does the task on the phone and nothing leaves it.
- **Everything the AI produces is a draft.** You check it. The numbers behind your targets are worked out on your phone, never by AI.

### AI consent, and how to withdraw it
Online AI help is **off until you agree**. When Power starts, and before the first online AI request, Forma shows a screen that says what is sent and where, with the buttons Allow and Not now. Nothing is sent until you tap Allow.

To withdraw, open **Settings > AI help** and switch off **Online AI help**. It takes effect at once. Forma then uses your iPhone or your own typing instead. You can switch it on again later.

### Your rights over Garmin and Power data
- **Access.** Garmin data shows in the app. To get a copy of what the server holds about you, write to [{{support_email}}](mailto:{{support_email}}).
- **Correct.** Garmin data comes from your watch; correct it at the source in Garmin's apps. For anything else, write to us.
- **Stop receiving.** **Settings > Devices > Garmin > Disconnect Garmin** stops new data. You can connect again later.
- **Delete.** **Settings > Data & backup > Delete all my data** also deletes your Power account on our server: your Garmin connection and the data stored for it, your registered phones, and the account itself. You can also write to us to ask for deletion.
- **Export.** **Settings > Data & backup > Export all my data** exports what is on your phone. For the server copy, write to us.
- **Withdraw consent.** Settings > AI help, as above.

<!-- TODO-OWNER: (1) retention period of server data for Power and of the nightly encrypted backups (the app/server do not state it); say how long deleted data can remain in backups. (2) confirm you can fulfil server-copy export and deletion requests sent to the support email, and how fast. (3) region of the hosting: deliberately not named here; decide whether to disclose it. -->

## Apple Health
If you allow it, Forma **reads** your body weight, body fat percentage and lean body mass from Apple Health so you do not type them. Forma **does not write** to Health. Health data is not used for advertising and is not sold.

Forma is also being extended so that the coach can read sleep, heart-rate variability and resting heart rate from Apple Health. This is **not in the current version**. When it is, it will be read **on your phone only**, and, like Garmin data, it and anything made from it will never be sent to the AI service. You can withdraw access any time in the Health app or iOS Settings.

## iCloud backup
Forma saves a copy of its database to a private area of **your** iCloud account (CloudKit private database). Only you can read it; we cannot. It is stored under your iCloud storage. "Delete all my data" can delete it too; you can also remove it in iOS Settings > Apple Account > iCloud > Manage Storage.

This is the only backup of the data on your phone. If you use Power, the server's own encrypted backups (see above) cover only what the server holds.

## Open Food Facts and USDA data
When you scan a barcode or type a food search, Forma sends that barcode or search text from your phone to Open Food Facts over HTTPS to get nutrition facts. No name, account or advertising identifier is sent. As with any web request, Open Food Facts can see your IP address, and Forma identifies itself by app name and version. Open Food Facts handles requests under [its own privacy policy](https://world.openfoodfacts.org/privacy). Results are cached on your phone. Open Food Facts data is available under the Open Database Licence.

Generic foods come from the USDA FoodData Central database, which is bundled in the app and needs no connection.

## Camera and photos
The camera is used to scan barcodes. The camera or the system photo picker can also be used to read a meal. Where Apple Intelligence on your iPhone can read it, the photo stays on your phone. With Power and your consent, a photo can instead go through Forma's server to the AI service, as described above. Photos are not sent anywhere else.

## Notifications and widgets
Reminders are scheduled on your phone. Widgets and the rest-timer Live Activity read a small snapshot the app keeps in your phone's secure storage. Nothing is sent to us.

## Subscriptions
Apple takes the payment and manages Forma Core and Forma Power subscriptions. We do not see your payment details. The app asks Apple (through the App Store on your phone) whether your subscription is active. For Power, the app also sends Apple's signed proof of the subscription to our server, so the server can confirm it, and receives a token that identifies your phone. The 14-day free trial is handled inside the app and asks for no payment details.

## Who receives data
- **Apple**: App Store and subscriptions (StoreKit), iCloud backup, Apple Health, and Apple Intelligence on your phone.
- **Garmin**: only if you connect it.
- **Oracle Cloud Infrastructure**: hosts Forma's server (Power only).
- **Groq**: the online AI provider (Power, with your consent only).
- **Open Food Facts**: food and barcode lookups.
- **USDA FoodData Central**: bundled food data; nothing is sent to it.

## What we do not do
We do not sell or share your data for advertising, do not track you across apps or websites, do not build advertising profiles, and do not use third-party analytics or crash-reporting SDKs. Apple may give us aggregated crash and usage statistics if you chose to share them with developers in iOS settings.

## Children
Forma is not directed at children. We do not knowingly collect data from children.

<!-- TODO-OWNER: confirm the wording and the age rating you choose in App Store Connect (the listing draft expects 4+). The original draft said "under 13 [adjust to your age rating/jurisdiction]". Decide with a lawyer whether to name an age. -->

## Your choices and rights
Export or delete your data in Settings > Data & backup. With Core we hold none of your data, so those tools answer requests to access, correct or delete. With Power, see [Your rights over Garmin and Power data](#your-rights-over-garmin-and-power-data), and you can write to [{{support_email}}](mailto:{{support_email}}) with any question or request.

<!-- TODO-OWNER: add jurisdiction-specific wording (for example the data protection law of the owner's country, GDPR / UK GDPR, CCPA) with a lawyer, if you want it. It is deliberately left out rather than guessed. -->

## Medical disclaimer
Forma gives information and suggestions, not medical advice. See the [Terms of Use](/terms/).

## Changes
If this policy changes we will update the date above and, for material changes, tell you in the app.
