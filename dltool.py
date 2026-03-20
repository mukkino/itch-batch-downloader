# download pretty a file

import os
import shutil
import time

import dateparser
import requests

from datetime import datetime

# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', usepercent=True, decimals=1, fill='X', debugon=False):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        usepercent  - Optoinal  : display percentage (Bool)
        decimals    - Optional  : positive number of decimals in percent complete (Int), ignored if usepercent = False
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """

    prefix = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] " + prefix

    # length is calculated by terminal width
    twx, twy = shutil.get_terminal_size()
    length = twx - 1 - len(prefix) - len(suffix) -4
    if usepercent:
        length = length - 6
    if total == 0:
        filledLength = int(length * iteration // 1)
    else:
        filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    
     # process percent
    if usepercent:
        if total == 0:
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(1)))
        else:
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='', flush=True)
    else:
        print('\r%s |%s| %s' % (prefix, bar, suffix), end='', flush=True)

    # Print New Line on Complete
    if iteration == total:
        print(flush=True)

def download_a_file(url, filename="", session=None, cookies=None, rename_old=True, skip_if_identical=True, debugon=False):
    # returns true if the file was downloaded
    if cookies is None and session is not None:
        cookies = session.cookies
    if session is None:
        session = requests.Session()

    dlurl = url  # keep the original string for later use
    newDownloads = 0

    # Detect Cloudflare‑mirrored URLs
    is_cloudflare = dlurl.startswith("https://itchio-mirror.") or dlurl.startswith("https://r2.cloudflarestorage.com")

    if is_cloudflare:
        # Direct GET because of the time constraint
        data = session.get(dlurl, stream=True, cookies=cookies)
    else:
        data = session.head(dlurl)
    if data.status_code != 200:
        return False

    datadownloaded = 0

    # figure out file name
    raw_name = ""
    cd = data.headers.get("content-disposition")
    if cd and "filename=" in cd:
        raw_name = cd.split("filename=")[-1].strip('";\'')
    else:
        # Fallback: last path component of the URL (without query string)
        raw_name = dlurl.split("/")[-1].split("?")[0]

    # final path
    if filename == "" or os.path.isdir(filename):
        # ``filename`` is a directory (or empty) → put the file inside it
        dest_dir = filename if os.path.isdir(filename) else os.getcwd()
        final_path = os.path.join(dest_dir, raw_name)
    else:
        # Caller supplied an explicit file name
        final_path = filename

    # Skip‑if‑identical logic (only for non‑Cloudflare URLs, because we don’t have reliable metadata for the signed URLs)
    if not is_cloudflare and os.path.exists(final_path) and skip_if_identical:
        try:
            dltime = data.headers["last-modified"]
            datalength = int(data.headers["content-length"])
            stats = os.stat(final_path)
            if (dateparser.parse(dltime).timestamp() == stats.st_mtime and datalength == stats.st_size):
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"[INFO] File {final_path} already fully downloaded - skipping")
                return False
        except Exception:
            # If any header is missing we just fall through to a fresh download
            pass

    # Store data stream / GET
    if is_cloudflare:
        # We initialized with GET
        data_stream = data
    else:
        # For the normal CDN case we now do the real GET
        data_stream = session.get(dlurl, stream=True, cookies=cookies)
        if data_stream.status_code != 200:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} GET request failed ({data_stream.status_code})")
            return False

    # Rename old file if requested (only when a *file* exists, not a dir)
    if os.path.exists(final_path) and rename_old:
        now = datetime.now()
        ts = now.strftime("%Y%m%d%H%M%S")
        old_name = f"{final_path}_{ts}.old"
        print(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            + " "
            + f"[INFO] Renaming {final_path} → {old_name}"
        )
        if os.path.exists(old_name):
            os.remove(old_name)
        os.rename(final_path, old_name)

    # start download
    if debugon:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ " " + f"[DEBUG] Starting download of {dlurl} → {final_path}")
    else:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ " "+ f"[INFO] Starting download of {final_path}")

    incompletefilename = final_path + ".incomplete"
    starttime = time.time()
    datadownloaded = 0

    # Get the expected length (might be missing for Cloudflare URLs)
    try:
        datalength = int(data_stream.headers.get("content-length", 0))
    except Exception:
        datalength = 0

    with open(incompletefilename, "wb") as f:
        for chunk in data_stream.iter_content(chunk_size=8192):
            if not chunk:
                continue
            f.write(chunk)
            datadownloaded += len(chunk)
            difftime = time.time() - starttime
            if difftime == 0:
                kbs = (datadownloaded / 1) / 1024
            else:
                kbs = (datadownloaded / difftime) / 1024
            suffix = os.path.basename(final_path)
            prefix = f"{round(datadownloaded/1024/1024,1)}/{round(datalength/1024/1024,1)} MB ({round(kbs,1)} KB/s)"
            printProgressBar(datadownloaded, datalength, suffix=suffix, prefix=prefix, usepercent=False, debugon=debugon)

    # finish download
    os.rename(incompletefilename, final_path)

    # check size
    sizeondisk = os.path.getsize(final_path)
    if debugon:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] " + "filename: {}, disk: {}, http: {}".format(filename, sizeondisk, datalength))
    if datalength and sizeondisk != datalength:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] Size on Disk differs from HTTP")
        return False

    # touch up timestamp
    dltime = data.headers.get("last-modified")
    if dltime:
        ts = int(dateparser.parse(dltime).timestamp())
        os.utime(final_path, (ts, ts))

    # done
    return True
