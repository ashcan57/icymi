import xbmc, xbmcgui, xbmcaddon
import os, zipfile, shutil, urllib.request, tempfile

DROPBOX_URL = "https://www.dropbox.com/scl/fi/2ga9ygf46he0880urrvfe/dab21.zip?rlkey=qzqgft3qhl80kucl4mzel581x&st=m844txli&dl=1"

addon = xbmcaddon.Addon()

def download_build(url, target):
    xbmcgui.Dialog().notification("ICYMI Installer", "Downloading build...", xbmcgui.NOTIFICATION_INFO)
    urllib.request.urlretrieve(url, target)

def extract_build(zip_path, destination):
    xbmcgui.Dialog().notification("ICYMI Installer", "Installing build...", xbmcgui.NOTIFICATION_INFO)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(destination)

def main():
    dialog = xbmcgui.Dialog()
    confirm = dialog.yesno("ICYMI Installer",
                            "This will replace your Kodi userdata and add-ons.\nContinue?")
    if not confirm:
        dialog.notification("ICYMI Installer", "Installation cancelled", xbmcgui.NOTIFICATION_INFO)
        return

    # Determine Kodi userdata path
    userdata = xbmc.translatePath('special://userdata')
    temp_zip = os.path.join(tempfile.gettempdir(), "icy_build.zip")

    try:
        download_build(DROPBOX_URL, temp_zip)
        # Extract into userdata folder (overwrite existing files)
        extract_build(temp_zip, userdata)
        dialog.notification("ICYMI Installer", "Build installed successfully!", xbmcgui.NOTIFICATION_INFO)
        xbmc.executebuiltin("ReloadSkin()")  # optional: refresh Kodi
    except Exception as e:
        dialog.notification("ICYMI Installer", f"Error: {e}", xbmcgui.NOTIFICATION_ERROR)

if __name__ == "__main__":
    main()

