import json
import subprocess
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
        return e.code, (json.loads(body) if body else {})


code, repo = api("/repos/arsenbrsoyan987-eng/vtoroe-dyhanie")
print("доступ к репозиторию:", code)
if code == 200:
    print("  default branch:", repo.get("default_branch"))
    print("  permissions:", repo.get("permissions"))

code, me = api("/user")
print("\nсоздание репозиториев доступно:", "да" if code == 200 else code)
