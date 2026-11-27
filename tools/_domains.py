import socket
import subprocess

domains = [
    "vitok.ru", "vitok.online", "vitok.club", "vitok.space", "vitok.team",
    "vitok.pro", "vitok.site", "vitok.sport", "vitok.net", "vitok.org",
    "vitok.icu", "vitok.su", "vitok.store", "vitok.co", "vitok.app",
    "vitok.moscow", "vitok.school", "vitok.fitness",
]

for d in domains:
    ns = subprocess.run(["dig", "+short", d, "NS"], capture_output=True, text=True).stdout.strip()
    a = subprocess.run(["dig", "+short", d, "A"], capture_output=True, text=True).stdout.strip()
    if not ns and not a:
        state = "DNS нет → вероятно свободен"
    elif not ns and a:
        state = "есть A, но нет NS → странно"
    else:
        state = "занят"
    print(f"{d:<16} {state}")
