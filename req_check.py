import sys
import requests

path = sys.argv[1] if len(sys.argv) > 1 else "requirements.txt"

total_p = []
nf_p = []
nf_v = []
oldest = None

for line in open(path):
    line = line.split("#")[0].strip()
    if not line or line.startswith("-"):
        continue

    if "==" in line:
        name, version = line.split("==", 1)
    else:
        name, version = line, None

    total_p.append(name)

    r = requests.get(f"https://pypi.org/pypi/{name}/json", timeout=10)
    if r.status_code == 404:
        nf_p.append(name)
        continue

    if version is None:
        continue

    releases = r.json()["releases"]
    if version not in releases:
        nf_v.append(f"{name}=={version}")
        continue

    files = releases[version]
    if files:
        uploaded = files[0]["upload_time"]
        if oldest is None or uploaded < oldest[0]:
            oldest = (uploaded, name, version)

print("Dependencies checked:", len(total_p))
print("Packages not on PyPI:", len(nf_p))
print("Versions not on PyPI:", len(nf_v))
print(f"Oldest pinned release: {oldest[1]}=={oldest[2]}")