import os, base64

repo = r'C:\Users\Sarath Babu\OneDrive\Documents\AI Agents\Paperclip Project\sarathbabu123'
def b64(img_path):
    with open(os.path.join(repo, img_path), 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')

char_b64 = b64('char.png')
avatar_b64 = b64('avatar.png')

for svg in ['banner.svg', 'banner-light.svg']:
    path = os.path.join(repo, svg)
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    data = data.replace('href="./char.png"', f'href="{char_b64}"')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)

path = os.path.join(repo, 'lanyard.svg')
with open(path, 'r', encoding='utf-8') as f:
    data = f.read()
data = data.replace('href="./avatar.png"', f'href="{avatar_b64}"')
with open(path, 'w', encoding='utf-8') as f:
    f.write(data)

readme = os.path.join(repo, 'README.md')
with open(readme, 'r', encoding='utf-8') as f:
    rdata = f.read()

rdata = rdata.replace('github-readme-stats.vercel.app', 'github-readme-stats-git-masterrstaa-rickstaa.vercel.app')
with open(readme, 'w', encoding='utf-8') as f:
    f.write(rdata)

print("Done replacing base64 and URLs.")
