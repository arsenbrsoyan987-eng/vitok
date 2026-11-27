import json
import subprocess
import urllib.error
import urllib.request

token = subprocess.run(
    ["security", "find-internet-password", "-s", "github.com", "-w"],
    capture_output=True, text=True,
).stdout.strip()

HDRS = {
    "Authorization": "token " + token,
    "Accept": "application/vnd.github+json",
    "Content-Type": "application/json",
}


def api(path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request("https://api.github.com" + path, data=data, headers=HDRS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode()
            return r.status, (json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return e.code, json.loads(body)
        except json.JSONDecodeError:
            return e.code, {"raw": body[:300]}


code, res = api("/repos/arsenbrsoyan987-eng/vitok/pages", "POST",
                {"source": {"branch": "main", "path": "/"}})
print("включение Pages:", code)
if code in (200, 201):
    print("  url:", res.get("html_url"))
    print("  status:", res.get("status"))
else:
    print("  ", res.get("message"))

code, res = api("/repos/arsenbrsoyan987-eng/vitok/pages")
print("\nсостояние Pages:", code)
if code == 200:
    print("  url:", res.get("html_url"))
    print("  status:", res.get("status"))
    print("  source:", res.get("source"))
