#!/usr/bin/env python3
"""Смена названия сайта и домена во всех файлах проекта.

Примеры:
    python3 tools/rename.py --brand "ВИТОК" --domain "vitok.ru" --dry-run
    python3 tools/rename.py --brand "ВИТОК" --domain "vitok.ru"
    python3 tools/rename.py --brand "ВТОРОЕ ДЫХАНИЕ"

Скрипт меняет только точные вхождения старого названия и старого домена,
поэтому безопасен для повторного запуска.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FILES = [
    "index.html",
    "privacy.html",
    "README.md",
    "assets/js/main.js",
    "robots.txt",
    "sitemap.xml",
]

OLD_BRAND = "ВИТОК"
OLD_DOMAIN = "vtoroe-dyhanie.ru"


def detect_domain(text):
    found = re.search(r"https://([a-z0-9.-]+\.[a-z]{2,})/", text)
    return found.group(1) if found else OLD_DOMAIN


def main():
    parser = argparse.ArgumentParser(description="Сменить название сайта и домен")
    parser.add_argument("--brand", help="новое название сайта")
    parser.add_argument("--domain", help="новый домен без схемы, например vitok.ru")
    parser.add_argument("--dry-run", action="store_true", help="только показать, что изменится")
    args = parser.parse_args()

    if not args.brand and not args.domain:
        parser.error("укажите --brand и/или --domain")

    if args.domain:
        args.domain = re.sub(r"^https?://", "", args.domain).strip("/").lower()

    index = ROOT / "index.html"
    current_domain = detect_domain(index.read_text(encoding="utf-8")) if index.exists() else OLD_DOMAIN

    total = 0
    for name in FILES:
        path = ROOT / name
        if not path.exists():
            print(f"  пропуск: {name} (нет файла)")
            continue

        text = path.read_text(encoding="utf-8")
        original = text
        brand_hits = 0
        domain_hits = 0

        if args.brand:
            brand_hits = text.count(OLD_BRAND)
            text = text.replace(OLD_BRAND, args.brand)

        if args.domain and current_domain != args.domain:
            domain_hits = text.count(current_domain)
            text = text.replace(current_domain, args.domain)

        if text != original:
            total += brand_hits + domain_hits
            if not args.dry_run:
                path.write_text(text, encoding="utf-8")
            print(f"  {name}: название ×{brand_hits}, домен ×{domain_hits}")
        else:
            print(f"  {name}: без изменений")

    mode = "будет заменено" if args.dry_run else "заменено"
    print(f"\nИтого {mode} вхождений: {total}")
    if args.dry_run:
        print("Это пробный прогон. Уберите --dry-run, чтобы применить.")
    else:
        print("Проверьте index.html: строки с canonical, og:url, og:image.")


if __name__ == "__main__":
    sys.exit(main())
