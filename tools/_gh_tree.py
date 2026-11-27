import json
import subprocess
import urllib.request

token = subprocess.run(
    ["security", "find-internet-password", "-s", "github.com", "-w"],
    capture_output=True, text=True,
).stdout.strip()

HDRS = {"Authorization": "token " + token, "Accept": "application/vnd.github+json"}
REPO = "/repos/arsenbrsoyan987-eng/vtoroe-dyhanie"


def api(path):
    req = urllib.request.Request("https://api.github.com" + path, headers=HDRS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode()
            return r.status, (json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        return e.code, {}


code, tree = api(REPO + "/git/trees/main")
print("дерево main:", code)
if code == 200:
    for item in tree.get("tree", []):
        print(f"  {item['type']:<4} {item['path']}")

code, branches = api(REPO + "/branches")
print("\nветки:", code)
if code == 200:
    for b in branches:
        print("  ", b["name"])

code, pages = api(REPO + "/pages")
print("\nPages:", code)
if code == 200:
    print("  source:", pages.get("source"))
    print("  cname:", pages.get("cname"))
    print("  https_enforced:", pages.get("https_enforced"))
    print("  build_type:", pages.get("build_type"))
