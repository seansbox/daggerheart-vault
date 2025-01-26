import glob, os, shutil, zipfile, urllib.request, re

# Remove old icons directory
for file in glob.glob("*.png"):
    os.remove(file)

# Download and extract zip
urllib.request.urlretrieve('http://game-icons.net/archives/svg/zip/000000/transparent/game-icons.net.svg.zip', 'game-icons.net.svg.zip')
with zipfile.ZipFile('game-icons.net.svg.zip', 'r') as zip_ref: zip_ref.extractall('.')

# Flatten and move SVG files
for root, dirs, files in os.walk('icons/000000/transparent/1x1/'):
    for file in files:
        if file.endswith('.svg'):
            category = os.path.basename(root)
            new_name = f"{os.path.splitext(file)[0]}-{category}.svg"
            os.rename(os.path.join(root, file), new_name)

# Clean up SVGs
shutil.rmtree('icons'); os.remove('game-icons.net.svg.zip')

# Modify SVGs
for svg_file in os.listdir('.'):
    if svg_file.endswith('.svg'):
        with open(svg_file, 'r+') as file:
            content = file.read()
            content = re.sub(
              r'<path fill="#000" ([^/]+)/',
              r'<path stroke="#000000" stroke-width="40" stroke-linecap="round" stroke-linejoin="round" \1/><path fill="#FFFFFF" \1/', 
              content)
            content = re.sub(r'viewBox="0 0 512 512"', r'viewBox="-32 -32 576 576"', content)
            file.seek(0); file.write(content); file.truncate()
