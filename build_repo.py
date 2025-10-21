import os
import zipfile
import hashlib
import xml.etree.ElementTree as ET

# ──────────────────────────────
# Utilities
# ──────────────────────────────

def get_version(addon_xml_path):
    """Extract version from addon.xml"""
    try:
        tree = ET.parse(addon_xml_path)
        root = tree.getroot()
        return root.attrib.get("version", "0.0.0")
    except Exception:
        import re
        with open(addon_xml_path, "r", encoding="utf-8") as f:
            text = f.read()
        m = re.search(r'version=["\']([\d\.]+)["\']', text)
        return m.group(1) if m else "0.0.0"

def zip_addon(addon_dir, zip_path):
    """Zip an add-on folder correctly for Kodi"""
    addon_name = os.path.basename(addon_dir)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(addon_dir):
            for file in files:
                if file.endswith(".zip") or file == "build_repo.py":
                    continue
                full_path = os.path.join(root, file)
                # Ensure the top-level folder in ZIP is the add-on folder name
                arcname = os.path.join(addon_name, os.path.relpath(full_path, addon_dir))
                z.write(full_path, arcname)

# ──────────────────────────────
# Main builder
# ──────────────────────────────

def build_repo(base_path="."):
    print("\033[96mBuilding Kodi repository...\033[0m")

    addon_dirs = [
        d for d in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, d))
        and (d.startswith("plugin.") or d.startswith("repository."))
    ]

    addons_xml_parts = []
    built_zips = []

    for d in addon_dirs:
        addon_path = os.path.join(base_path, d)
        addon_xml_file = os.path.join(addon_path, "addon.xml")
        if not os.path.isfile(addon_xml_file):
            print(f"\033[93mWarning: {addon_xml_file} missing, skipping {d}\033[0m")
            continue

        version = get_version(addon_xml_file)
        zip_name = f"{d}-{version}.zip"
        zip_path = os.path.join(addon_path, zip_name)

        zip_addon(addon_path, zip_path)
        built_zips.append(zip_name)

        with open(addon_xml_file, "r", encoding="utf-8") as f:
            addons_xml_parts.append(f.read().strip())

    addons_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<addons>\n" +
        "\n".join(addons_xml_parts) +
        "\n</addons>"
    )

    # Write addons.xml and md5
    with open(os.path.join(base_path, "addons.xml"), "w", encoding="utf-8") as f:
        f.write(addons_xml)

    md5 = hashlib.md5(addons_xml.encode("utf-8")).hexdigest()
    with open(os.path.join(base_path, "addons.xml.md5"), "w", encoding="utf-8") as f:
        f.write(md5)

    # Report
    print("\033[92mRepository built successfully!\033[0m")
    for z in built_zips:
        print(f"   • {z}")

    return addons_xml

# ──────────────────────────────
# Sanity check
# ──────────────────────────────

if __name__ == "__main__":
    addons_xml = build_repo(".")
    try:
        ET.fromstring(addons_xml)
        print("\033[92m✅ addons.xml sanity check passed — valid XML!\033[0m")
    except ET.ParseError as e:
        print("\033[91m❌ addons.xml sanity check failed:\033[0m")
        print(f"   {e}")










