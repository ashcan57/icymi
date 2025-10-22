ICYMI Kodi repo - ready to push to GitHub

Instructions:
1. Unzip or push the contents of this zip to the root of your GitHub repo 'ahcan57/icymi' (main branch).
2. Do NOT include the large dab21.zip in the repo root. Upload dab21.zip as a Release asset in GitHub Releases (v1.0.0).
   Release URL should be:
   https://github.com/ashcan57/icymi/releases/download/v1.0.0/dab21.zip
3. Enable GitHub Pages: Settings → Pages → Deploy from branch 'main' → / (root). Wait a few minutes.
4. Verify in browser:
   https://ashcan57.github.io/icymi/addons.xml
   https://ashcan57.github.io/icymi/addons.xml.md5
   https://ashcan57.github.io/icymi/repository.icymi/addon.xml
5. In Kodi: Settings → File Manager → Add Source → https://ashcan57.github.io/icymi/ (include trailing slash)
   Then Add-ons → Install from zip → repository.icymi.zip (should appear) → Install from repository → ICYMI Repository → ICYMI

If Kodi still says 'Can't retrieve directory information', try removing the source in Kodi and re-adding it, and clear Kodi cache/databases.
