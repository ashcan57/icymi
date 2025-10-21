import os, zipfile, hashlib

def zipdir(path, zipname):
    with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.zip') or file == 'build_repo.py':
                    continue
                z.write(os.path.join(root, file),
                        os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

def get_version(addon_path):
    with open(os.path.join(addon_path, 'addon.xml'), 'r', encoding='utf-8') as f:
        for line in f:
            if 'version=' in line:
                return line.split('version="')[1].split('"')[0]
    return '0.0.0'

def build_repo(base_path):
    addon_dirs = [d for d in os.listdir(base_path)
                  if os.path.isdir(d) and d.startswith(('plugin.', 'repository.'))]
    addons_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<addons>\n'
    for d in addon_dirs:
        addon_path = os.path.join(base_path, d)
        version = get_version(addon_path)
        zip_name = f"{d}-{version}.zip"
        zip_path = os.path.join(base_path, d, zip_name)
        zipdir(addon_path, zip_path)
        with open(os.path.join(addon_path, 'addon.xml'), 'r', encoding='utf-8') as f:
            addons_xml += f.read().strip() + '\n'
    addons_xml += '</addons>'
    with open(os.path.join(base_path, 'addons.xml'), 'w', encoding='utf-8') as f:
        f.write(addons_xml)
    md5 = hashlib.md5(addons_xml.encode('utf-8')).hexdigest()
    with open(os.path.join(base_path, 'addons.xml.md5'), 'w') as f:
        f.write(md5)

if __name__ == "__main__":
    build_repo('.')
    print("Repository built successfully!")




