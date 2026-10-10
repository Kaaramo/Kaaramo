"""Récupère le calendrier public des contributions et écrit data/contributions.json (sans token)."""
import json
import re
from datetime import date, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USER = "Kaaramo"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "contributions.json"


def fetch():
    r = requests.get(f"https://github.com/users/{USER}/contributions", timeout=30,
                     headers={"User-Agent": "profile-readme-bot"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    counts = {}
    for tip in soup.select("tool-tip"):
        target = tip.get("for")
        txt = tip.get_text(" ", strip=True)
        m = re.match(r"(No|\d[\d,]*) contributions?", txt)
        if target and m:
            counts[target] = 0 if m.group(1) == "No" else int(m.group(1).replace(",", ""))

    days = []
    for td in soup.select("td.ContributionCalendar-day[data-date]"):
        days.append({
            "date": td["data-date"],
            "level": int(td.get("data-level", 0)),
            "count": counts.get(td.get("id"), 0),
        })
    days.sort(key=lambda d: d["date"])
    return days


def stats(days):
    total = sum(d["count"] for d in days)
    best = max(days, key=lambda d: d["count"]) if days else None
    longest = cur = 0
    for d in days:
        cur = cur + 1 if d["count"] > 0 else 0
        longest = max(longest, cur)
    current = 0
    for d in reversed(days):
        if d["count"] > 0:
            current += 1
        elif d["date"] == date.today().isoformat() and current == 0:
            continue  # la journée en cours ne casse pas la série
        else:
            break
    return {
        "total": total,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]} if best else None,
        "active_days": sum(1 for d in days if d["count"] > 0),
    }


if __name__ == "__main__":
    days = fetch()
    OUT.parent.mkdir(exist_ok=True)
    data = {"user": USER, "generated": date.today().isoformat(), "stats": stats(days), "days": days}
    OUT.write_text(json.dumps(data, indent=1), encoding="utf-8")
    print(f"{len(days)} jours, {data['stats']['total']} contributions")
