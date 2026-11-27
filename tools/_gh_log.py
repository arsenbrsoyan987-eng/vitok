import json
import subprocess
import urllib.error
import urllib.request

token = subprocess.run(
    ["security", "find-internet-password", "-s", "github.com", "-w"],
    capture_output=True, text=True,
).stdout.strip()

HDRS = {"Authorization": "token " + token, "Accept": "application/vnd.github+json"}
JOB = "/repos/arsenbrsoyan987-eng/vitok/actions/jobs/"


def api(path):
    req = urllib.request.Request("https://api.github.com" + path, headers=HDRS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, {}


code, jobs = api("/repos/arsenbrsoyan987-eng/vitok/actions/runs/46010821591/jobs")
if code == 200 and jobs.get("jobs"):
    job_id = jobs["jobs"][0]["id"]
    code, log = api(JOB + str(job_id) + "/logs")
    print("логи:", code)
    if code == 200:
        text = log.get("raw", "")
        for line in text.splitlines():
            if "error" in line.lower() or "Error" in line:
                print("  ", line[:300])
    else:
        print("  ", log.get("message"))
