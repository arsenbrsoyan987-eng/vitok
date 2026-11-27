import json
import subprocess
import urllib.error
import urllib.request

token = subprocess.run(
    ["security", "find-internet-password", "-s", "github.com", "-w"],
    capture_output=True, text=True,
).stdout.strip()

HDRS = {"Authorization": "token " + token, "Accept": "application/vnd.github+json"}
RUN = "/repos/arsenbrsoyan987-eng/vitok/actions/runs/46010821591"


def api(path):
    req = urllib.request.Request("https://api.github.com" + path, headers=HDRS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, {}


code, jobs = api(RUN + "/jobs")
print("jobs:", code)
for job in jobs.get("jobs", []):
    print(f"  {job['name']}: {job['conclusion']}")
    for step in job.get("steps", []):
        mark = "OK " if step["conclusion"] == "success" else f"{step['conclusion'] or '—'}"
        print(f"    [{mark}] {step['name']}")
