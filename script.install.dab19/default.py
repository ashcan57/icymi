import xbmc, xbmcgui, xbmcaddon, xbmcvfs, os, sys, zipfile, shutil, urllib.request

ADDON = xbmcaddon.Addon()
# <-- KEEP THIS EXACT LINK – it forces a direct download from Dropbox -->
DROPBOX_URL = (
    "https://www.dropbox.com/scl/fi/90rsb9oal9dc3fp3g1l8s/dab19.zip?"
    "rlkey=5st59x4bq5xpvljnf0rlflu1z&st=80dmmhhx&dl=1"
)

def notify(msg):
    xbmcgui.Dialog().notification("DAB19 Installer", msg,
                                  xbmcgui.NOTIFICATION_INFO, 5000)

def download_zip(dest_path):
    try:
        urllib.request.urlretrieve(DROPBOX_URL, dest_path)
        return True
    except Exception as e:
        notify(f"Download failed: {e}")
        return False

def extract_zip(zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            for member in z.namelist():
                # Resolve the target location inside Kodi’s virtual FS
                target = xbmc.translatePath(member)
                target_dir = os.path.dirname(target)
                if not xbmcvfs.exists(target_dir):
                    xbmcvfs.mkdirs(target_dir)
                # Copy the file
                with z.open(member) as src, xbmcvfs.File(target, 'wb') as dst:
                    shutil.copyfileobj(src, dst)
        return True
    except Exception as e:
        notify(f"Extraction failed: {e}")
        return False

def main():
    tmp_zip = xbmc.translatePath('special://temp/dab19.zip')
    notify("Downloading DAB19 build…")
    if not download_zip(tmp_zip):
        return
    notify("Extracting files…")
    if not extract_zip(tmp_zip):
        return
    # Clean up the temporary zip
    xbmcvfs.delete(tmp_zip)
    notify("Installation complete – restarting Kodi.")
    xbmc.restart()

if __name__ == '__main__':
    main()