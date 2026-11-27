import json
import subprocess
import urllib.error
import urllib.request

token = subprocess.run(
    ["security", "find-internet-password", "-s", "github.com", "-w"],
    capture_output=True, text=True,
).stdout.strip()

HDRS = {"Authorization": "token " + token, "Accept": "application/vnd.github+json"}


def api(path):
    req = urllib.request.Request("https://api.github.com" + path, headers=HDRS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, {}


for name in ("arsenbrsoyan987-eng.github.io", "vitok"):
    code, repo = api("/repos/arsenbrsoyan987-eng/" + name)
    print(f"{name}: {code}")
    if code == 200:
        print("  pages:", repo.get("has_pages"), "| size:", repo.get("size"))
