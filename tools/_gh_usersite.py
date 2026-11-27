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
            return e.code, {"raw": body[:200]}


code, res = api("/user/repos", "POST", {
    "name": "arsenbrsoyan987-eng.github.io",
    "description": "ВИТОК — индивидуальная школа циклических видов спорта",
    "private": False,
    "has_issues": False,
    "has_wiki": False,
    "auto_init": False,
})
print("создание user site:", code, res.get("message", ""))
if code in (200, 201):
    print("  full_name:", res.get("full_name"))
