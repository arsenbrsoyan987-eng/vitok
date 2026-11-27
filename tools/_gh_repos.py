import json
import subprocess
import urllib.request

token = subprocess.run(
    ["security", "find-internet-password", "-s", "github.com", "-w"],
    capture_output=True, text=True,
).stdout.strip()

HDRS = {"Authorization": "token " + token, "Accept": "application/vnd.github+json"}


def api(path):
    req = urllib.request.Request("https://api.github.com" + path, headers=HDRS)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


code, repos = api("/user/repos?per_page=100&sort=updated")
print("репозитории:", code)
if isinstance(repos, list):
    for r in repos:
        print(f"  {r['name']:<28} pages={r.get('has_pages')} private={r['private']}")

for name in ("vtoroe-dyhanie", "vitok"):
    code, pages = api(f"/repos/arsenbrsoyan987-eng/{name}/pages")
    print(f"\nPages {name}: {code}")
    if code == 200:
        print("  url:", pages.get("html_url"))
        print("  cname:", pages.get("cname"))
        print("  branch:", (pages.get("source") or {}).get("branch"))
        print("  status:", pages.get("status"))
    else:
        print("  ", pages.get("message"))
