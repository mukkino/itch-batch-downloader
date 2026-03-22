# Changelog for itch-batch-downloader

## 0.1.2 (2026-03-22)

Acknowledgments - Thanks to sumitaghosh for this release
Important - UPX has not been used in this build
Added a sample/default itch-batch-downloader.ini file to the repository.
Added support in fetch_upload() for newer itch.io download button formats when data-upload_id is not present.
Added fallback parsing of /download/ links from the upload block and, if needed, from the whole page.
Added handling for Cloudflare-backed download URLs such as itchio-mirror.* and r2.cloudflarestorage.com.
Added filename fallback logic in dltool.py when Content-Disposition is missing, using the URL path instead.
Added support for treating the filename argument as either a directory or a full output path in dltool.py.
Added protocol normalization for iframe video URLs, including protocol-relative URLs like //....
Added extra repository ignore rules for .DS_Store, /Downloads, /env, and *.xz.
Changed fetch_upload() now accepts an extra full_page_soup argument and uses it as a fallback source for locating download buttons.
Changed Download URL resolution now branches between:
Changed the legacy POST {dlurl}/file/{upload_id} flow, and
Changed a direct JSON GET flow for newer endpoints.
Changed PDF generation was changed from a low-level Selenium command executor call to driver.print_page(...).
Changed PDF output filename construction was cleaned up to use an f-string.
Changed dltool.download_a_file() was reworked to:
Changed detect Cloudflare-style mirrors,
Changed use HEAD only for standard URLs,
Changed use direct GET for Cloudflare URLs,
Changed compute the final output path more flexibly,
Changed apply skip-if-identical only when reliable metadata is available.
Changed Dependency versions in requirements.txt were broadly refreshed to newer releases.
Changed The README was substantially expanded and refreshed:
Changed Python tested version updated from 3.10.7 to 3.14.3.
Changed UPX tested version updated from 3.96 to 5.1.1.
Changed Package installation instructions were rewritten.
Changed Minor util.py adjustments.
New guidance was added for Windows, macOS, and Linux packaging context.
New More tips, caveats, and external tooling references were added.
Fixed
Fixed download detection for pages that no longer expose the old data-upload_id attribute.
Fixed file download handling for Cloudflare mirror URLs that do not provide the same metadata as the legacy CDN flow.
Fixed cases where downloads could still proceed even when Content-Disposition was missing.
Fixed iframe video download URL construction so already absolute URLs are not blindly prefixed with https:.
Improved non-200 handling in dltool.py by returning early when HEAD or GET requests fail.
Improved old-file renaming logic to operate on the resolved final output path.
Improved timestamp restoration to only run when Last-Modified exists.
Documentation: README wording was updated in multiple places for clarity, grammar, and formatting. Configuration option descriptions were reformatted and emphasized. The known issues / caveats section was updated and expanded. Additional notes were added around claiming free games, browser extensions, cookie export, and compilation.

## 0.1.0 (2022-09-24)

- project forked from itch-downloader 0.5.3, initial release of itch-batch-downloader 0.1.0
- ability to download any purchased item (removed distinction between games and non-games)
- replaced code for downloading dumping webpages, screenshots and videos
- added support to export product page as .png and .pdf
- added support in tool (rather then external) for downloading iframe embedded videos, etc. within a product page
- file renaming for filesystem compatibility (unicode)
- logging system with debug info added (unicode, both for output to file and/or console)
- misc bug fixes, stability improvements and special cases handling

## 0.5.3 (2022-04-16)

- download now adds datestamp to archives
- renames already downloaded files appropriately
- added webpage screenshot of gamepage (user has to provide service url)
- added screenshot download option
- added operating system selection (not yet active)
- still hardcoded that only windows and android will be downloaded

## 0.5.2 (2022-04-12)

- added a primitive download continue (tracks download position and resumes download at number)
- fixed (hopefully) "SSL: DECRYPTION_FAILED_OR_BAD_RECORD_MAC"
- fixed missing content-disposition
- some reformatting

## 0.5.1 (2022-04-10)

- fixed config file reading
- some adjustments for win32 platform

## 0.5 (2022-04-10)

- first numbered revision
- configuration put into proper .ini file
- rewritten README.md
- Changelog.md
- displays xxx / number of games during downloading games
- proper requirements.txt

## unnamed revisions (2022-04-10)

- basic working revisions, ironed out bugs and such
- configuration baked into script
- total rewrite of bundle downloader
