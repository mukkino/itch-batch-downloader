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
    if cookies == None and session != None:
        cookies = session.cookies
    if session == None:
        session = requests.Session()
    dlurl = url
    newDownloads = 0

    # check download if available and metadata
    data = session.head(dlurl)
    if data.status_code == 200:
        dltime = data.headers["last-modified"]
        datalength = int(data.headers["content-length"])

        if os.path.exists(filename) and skip_if_identical:
            stats = os.stat(filename)
            if dateparser.parse(dltime).timestamp() == stats.st_mtime and datalength == stats.st_size:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] File {} already fully downloaded and identical to online version, skipping".format(filename))
                return False

        datadownloaded = 0

        if filename == "":
            filename = data.headers["content-disposition"].split("'")[-1]
        shortfilename = filename.split(os.sep)[-1]
        incompletefilename = filename + ".incomplete"
        starttime = time.time()

        # rename old download if necessary
        now = datetime.now()
        date_time = now.strftime("%Y%m%d%H%M%S")
        if os.path.exists(filename) and rename_old:
            newOldName = filename + "_" + str(date_time)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] Renaming {} to {}.".format(filename, newOldName + ".old"))
            if os.path.exists(filename + ".old"):
                os.remove(filename + ".old")
            if os.path.exists(newOldName + ".old"):
                os.remove(newOldName + ".old")
            os.rename(filename, newOldName + ".old")

        # start download
        if debugon:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] Starting download of {} (-> {})".format(dlurl, filename))
        else:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] Starting download of {}".format(filename))
        with open(incompletefilename, "wb") as f:
            with session.get(dlurl, stream=True, cookies=cookies) as downloaddata:
                for chunk in downloaddata.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive
                        f.write(chunk)
                        datadownloaded += len(chunk)
                        difftime = time.time() - starttime
                        if difftime == 0:
                            kbs = (datadownloaded / 1) / 1024
                        else:
                            kbs = (datadownloaded / difftime) / 1024
                        mysuffix = "{} / {} MB ({} KB/s)".format(round(datadownloaded / 1024 / 1024, 1),
                                                                 round(datalength / 1024 / 1024, 1), round(kbs, 1))
                        printProgressBar(datadownloaded, datalength, suffix=shortfilename, prefix=mysuffix,
                                         usepercent=False, debugon=debugon)
        f.close()

        # finish download
        os.rename(incompletefilename, filename)
        newDownloads = newDownloads + 1

        # check size
        sizeondisk = os.path.getsize(filename)
        if debugon:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] " + "filename: {}, disk: {}, http: {}".format(filename, sizeondisk, datalength))
        if sizeondisk != datalength:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] Size on Disk differs from HTTP")
            return False

        # touch up timestamp
        timestamp = int(dateparser.parse(dltime).timestamp())
        os.utime(filename, (timestamp, timestamp))

        # done
        return True
    else:
        return False