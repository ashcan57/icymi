#!/usr/bin/env python3
import os, hashlib, zipfile, xml.etree.ElementTree as ET, sys

ROOT = '.'                     # repo root (where this script lives)
ADDONS_DIR = os.path.join(ROOT, 'addons')
OUT_XML = os.path.join(ROOT, 'addons.xml')
MD5_FILE = OUT_XML + '.md5'

print(f"[INFO] Looking for zip files in: {ADDONS_DIR}")

if not os.path.isdir(ADDONS_DIR):
    print("[ERROR] 'addons/' directory does NOT exist.")
    sys.exit(1)

zip_files = [f for f in sorted(os.listdir(ADDONS_DIR)) if f.lower().endswith('.zip')]
if not zip_files:
    print("[WARN] No .zip files found in 'addons/'. Nothing to index.")
    sys.exit(0)

root = ET.Element('addons')

for zip_name in zip_files:
    zip_path = os.path.join(ADDONS_DIR, zip_name)
    print(f"[INFO] Processing {zip_name} …")
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            inner_xml = z.read('addon.xml')
        root.append(ET.fromstring(inner_xml))
    except Exception as e:
        print(f"[ERROR] Could not read addon.xml from {zip_name}: {e}")
        sys.exit(1)

# ---------- write addons.xml ----------
try:
    ET.ElementTree(root).write(OUT_XML, encoding='utf-8', xml_declaration=True)
    print(f"[SUCCESS] Created {OUT_XML}")
except Exception as e:
    print(f"[ERROR] Failed to write {OUT_XML}: {e}")
    sys.exit(1)

# ---------- write MD5 ----------
try:
    with open(OUT_XML, 'rb') as f:
        md5 = hashlib.md5(f.read()).hexdigest()
    with open(MD5_FILE, 'w') as f:
        f.write(md5)
    print(f"[SUCCESS] Created {MD5_FILE}")
except Exception as e:
    print(f"[ERROR] Failed to write MD5 file: {e}")
    sys.exit(1)