
# itch batch downloader

A Python script that downloads all items bound to your itch.io account in batch.

## The downloader

- Retrieves items currently bound to your itch.io account/library.
- Attempts to download all available files it can access automatically.
- Optionally captures product pages as PNG and PDF.
- Downloads embedded videos.
- Preserves historical versions where possible.
- Supports interrupting and resuming batch download progress.

The goal of the tool is to create the most complete local archive possible of your itch.io purchases.

This script only downloads items bound to your account and does not bypass itch.io permissions.

---

# Features

- Batch download of items currently bound to your itch.io account/library.
- Resume interrupted batch downloads.
- Skip files that are already identical.
- Capture product pages as:
  - PNG screenshot
  - PDF print
- Download embedded videos.
- Preserve older PNG/PDF page captures instead of overwriting them.
- Filename sanitization is not yet fully implemented.
- Debug mode for detailed download tracking.

---

# Requirements

- [Python](https://www.python.org/downloads/) 3.9 or newer
- Python packages listed in `requirements.txt`
- Sufficient disk space for your library
- Exported itch.io cookies in Netscape cookies.txt format (saved as `cookies-itch.txt`). Note: browser cookies eventually expire. If the downloader suddenly stops seeing your purchases, re-export the cookies from your browser.

## Optional (only needed for some features)

### Google Chrome

Required for features that use Selenium browser automation.

If [Chrome](https://www.google.com/intl/en_au/chrome/) is not installed:

- Product page PDF snapshots will not be created (`create_pdf`)
- Product page PNG screenshots will not be created (`create_png`)

The rest of the downloader will still work (library scanning and file downloads).

If Chrome is not available you can disable these features in the configuration file:

```
create_pdf = OFF
create_png = OFF
```

---

### Microsoft Visual C++ Redistributable

Install the x64 version if you are using 64-bit Python (most systems). This is needed on Windows only and it's available [here](https://www.microsoft.com/en-gb/download/details.aspx?id=48145)

Some Python packages used by the downloader include native compiled components (for example `cryptography`, `cffi`, and other compiled wheels).

If the runtime is missing on Windows:

- the script may fail to start
- HTTPS connections used for downloading files may fail
- some dependencies may fail to import

On most Windows systems this runtime is already installed.

The script has primarily been tested on Windows, but most of the code is cross-platform and may also work on Linux and macOS, although those platforms have been tested less.

---

# Usage

## 1. Login to itch.io

Open:

[https://itch.io/[(https://itch.io/)

Log in to your account.

The script requires your authenticated session cookies in order to access your library and download owned content.

---

## 2. Export your itch.io cookies

Export the cookies for itch.io from your browser and save them to a text file.

Recommended browser extensions:

- [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) (Chrome / Chromium browsers)
- [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/) (Firefox)

Export **only itch.io cookies**. If you export all of the it will also work but it will be unsafe from a cybersecuroty standpoint.

Save the exported file in the same directory as the script and rename it to:

```
cookies-itch.txt
```

---

## 3. Configure the downloader

Edit the configuration file:

```
itch-batch-downloader.ini
```

Set at minimum:

- the download directory
- any optional behaviour flags

If the configuration file does not exist, run the script once and it will be created automatically.

The first run will exit after generating the default configuration.

---

## 4. Run the script

From the script directory run:

```
python itch-batch-downloader.py
```

or if your system uses python3:

```
python3 itch-batch-downloader.py
```

If unsure, try the first command.

---

# Debug mode

You can enable verbose debug output by editing the configuration file and setting:

```
debug_logs = ON
```

When debug mode is enabled the script prints additional information to the console.

---

# Stopping the script

Press:

```
CTRL + C
```

to safely interrupt the downloader.

---

# Tips and tricks

If you would like to associate free games with your account in batch, you can use tools such as [ItchClaim](https://github.com/Smart123s/ItchClaim).

If you purchased bundles, many items may not automatically appear under [My Purchases](https://itch.io/my-purchases)

You can use [Tampermonkey](https://www.tampermonkey.net/) scripts such as [itch-io-bundle-to-library](https://greasyfork.org/en/scripts/427686-itch-io-bundle-to-library) to add them automatically.

Chrome extension alternative might also work but I haven't tested them personally. Example: [itch.io Bundle Auto Add to Library](https://chromewebstore.google.com/detail/itchio-bundle-auto-add-to/pbolegaohnnpillkpklefebilhanameg)

---

# Honourable mention

This script was originally based on:

https://github.com/shakeyourbunny/itch-downloader
