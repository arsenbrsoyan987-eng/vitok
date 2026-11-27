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


code, repo = api("/repos/arsenbrsoyan987-eng/vitok")
if code == 200:
    print("репозиторий vitok уже существует")
else:
    code, repo = api("/user/repos", "POST", {
        "name": "vitok",
        "description": "ВИТОК — индивидуальная школа циклических видов спорта",
        "private": False,
        "has_issues": False,
        "has_wiki": False,
        "auto_init": False,
    })
    print("создание репозитория:", code)
    if code not in (200, 201):
        print(" ", repo.get("message"))

code, user = api("/user")
print("лимит API:", user.get("login"))
