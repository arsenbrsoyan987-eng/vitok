import json
import subprocess
import time
import urllib.error
import urllib.request

token = subprocess.run(
    ["security", "find-internet-password", "-s", "github.com", "-w"],
    capture_output=True, text=True,
).stdout.strip()

HDRS = {"Authorization": "token " + token, "Accept": "application/vnd.github+json"}
REPO = "/repos/arsenbrsoyan987-eng/vitok"


def api(path):
    req = urllib.request.Request("https://api.github.com" + path, headers=HDRS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode()
            return r.status, (json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        return e.code, {}


for attempt in range(6):
    code, runs = api(REPO + "/actions/runs?per_page=1")
    if code != 200:
        print("runs:", code, runs.get("message"))
        break
    items = runs.get("workflow_runs", [])
    if not items:
        print("запусков пока нет")
    else:
        run = items[0]
        print(f"[{attempt}] {run['name']}: {run['status']} / {run['conclusion']}")
        if run["status"] == "completed":
            print("  detail:", run["html_url"])
            break
    time.sleep(12)

code, pages = api(REPO + "/pages")
print("\nPages:", code)
if code == 200:
    print("  url:", pages.get("html_url"))
    print("  status:", pages.get("status"))
