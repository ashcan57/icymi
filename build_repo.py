import os, zipfile, hashlib
from xml.etree import ElementTree as ET

def get_version(addon_xml_path):
    try:
        tree = ET.parse(addon_xml_path)
        root = tree.getroot()
        return root.attrib.get('version', '0.0.0')
    except Exception:
        # fallback: look for version in text
        with open(addon_xml_path, 'r', encoding='utf-8') as f:
            text = f.read()
        import re
        m = re.search(r'version=["\']([\d\.]+)["\']', text)
        return m.group(1) if m else '0.0.0'

def zip_addon(addon_dir, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(addon_dir):
            for file in files:
                if file.endswith('.zip') or file == 'build_repo.py':
                    continue
                full = os.path.join(root, file)
                arcname = os.path.relpath(full, os.path.join(addon_dir, '..'))
                z.write(full, arcname)

def build_repo(base_path='.'):
    addon_dirs = [d for d in os.listdir(base_path)
                  if os.path.isdir(os.path.join(base_path, d)) and (d.startswith('plugin.') or d.startswith('repository.'))]
    addons_xml_parts = []
    for d in addon_dirs:
        addon_path = os.path.join(base_path, d)
        addon_xml_file = os.path.join(addon_path, 'addon.xml')
        if not os.path.isfile(addon_xml_file):
            print(f"Warning: {addon_xml_file} missing, skipping {d}")
            continue
        version = get_version(addon_xml_file)
        zip_name = f"{d}-{version}.zip"
        zip_path = os.path.join(addon_path, zip_name)
        zip_addon(addon_path, zip_path)
        with open(addon_xml_file, 'r', encoding='utf-8') as f:
            addons_xml_parts.append(f.read().strip())
    addons_xml = '<?xml version="1.0" encoding="UTF-8"?>\\n<addons>\\n' + '\\n'.join(addons_xml_parts) + '\\n</addons>'
    with open(os.path.join(base_path, 'addons.xml'), 'w', encoding='utf-8') as f:
        f.write(addons_xml)
    md5 = hashlib.md5(addons_xml.encode('utf-8')).hexdigest()
    with open(os.path.join(base_path, 'addons.xml.md5'), 'w', encoding='utf-8') as f:
        f.write(md5)
    print("Built addons.xml and md5, and created addon zip files.")

if __name__ == '__main__':
    build_repo('.')
