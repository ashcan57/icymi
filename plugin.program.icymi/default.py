# Minimal safe example that shows the Dropbox build URL to the user.
try:
    import xbmcgui
    import xbmc
except Exception:
    # Running outside Kodi for testing
    xbmcgui = None
    xbmc = None

BUILD_URL = "https://www.dropbox.com/scl/fi/2ga9ygf46he0880urrvfe/dab21.zip?rlkey=qzqgft3qhl80kucl4mzel581x&st=m844txli&dl=1"

def main():
    message = ("Your ICYMI build is available at:\n\n"
               f"{BUILD_URL}\n\n"
               "For safety, please download and install manually, or extend this script carefully.")
    if xbmcgui:
        xbmcgui.Dialog().ok("ICYMI Build Installer", message)
    else:
        print(message)

if __name__ == '__main__':
    main()
