import json
import subprocess
import urllib.request

out = subprocess.run(
    ["security", "find-internet-password", "-s", "github.com", "-w"],
    capture_output=True, text=True,
)
token = out.stdout.strip()
if not token:
    print("токен в связке ключей не найден")
    raise SystemExit(1)

req = urllib.request.Request(
    "https://api.github.com/user",
    headers={"Authorization": "token " + token, "Accept": "application/vnd.github+json"},
)
with urllib.request.urlopen(req, timeout=20) as r:
    scopes = r.headers.get("x-oauth-scopes", "")
    data = json.load(r)
    print("login:", data.get("login"))
    print("scopes:", scopes if scopes else "(не указаны — fine-grained токен)")
