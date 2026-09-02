import datetime as dt
import json
import os
import re
import urllib.request


USERNAME = "Nausheen2206"
COLORS = ["#1F2937", "#164E63", "#0E7490", "#10B981", "#FBBF24", "#F97316"]


def fetch_contributions(username):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return fetch_public_contributions(username)

    query = {
        "query": "query($login:String!) { user(login:$login) { contributionsCollection { contributionCalendar { weeks { contributionDays { date contributionCount } } } } } }",
        "variables": {"login": username},
    }
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps(query).encode("utf-8"),
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-contribution-board",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            payload = json.load(response)
        weeks = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
        return {
            day["date"]: day["contributionCount"]
            for week in weeks
            for day in week["contributionDays"]
        }
    except (KeyError, OSError, json.JSONDecodeError):
        return fetch_public_contributions(username)


def fetch_public_contributions(username):
    url = f"https://github.com/users/{username}/contributions"
    request = urllib.request.Request(url, headers={"User-Agent": "profile-contribution-board"})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            html = response.read().decode("utf-8")
    except OSError as error:
        raise RuntimeError("Unable to fetch real GitHub contribution data") from error

    pattern = re.compile(
        r'data-date="(?P<date>[^"]+)".*?data-level="(?P<level>\d+)".*?'
        r'id="(?P<cell>contribution-day-component-[^"]+)".*?'
        r'<tool-tip[^>]*for="(?P=cell)"[^>]*>(?P<label>.*?)</tool-tip>',
        re.DOTALL,
    )
    contributions = {}
    for match in pattern.finditer(html):
        label = re.sub(r"<[^>]+>", "", match.group("label")).strip()
        count_match = re.search(r"(\d+) contribution", label)
        contributions[match.group("date")] = int(count_match.group(1)) if count_match else 0
    if not contributions:
        raise RuntimeError("GitHub contribution calendar returned no real data")
    return contributions


def contribution_level(count, maximum):
    if count == 0:
        return 0
    if maximum <= 4:
        return min(count, 5)
    return min(5, max(1, (count * 5 + maximum - 1) // maximum))


def build_svg(contributions, output_file="assets/contribution-game.svg"):
    today = dt.date.today()
    start = today - dt.timedelta(days=today.weekday() + 363)
    dates = [start + dt.timedelta(days=index) for index in range(364)]
    maximum = max(contributions.values(), default=1)
    total = sum(contributions.values())
    active_days = sum(value > 0 for value in contributions.values())
    cell = 18
    gap = 4
    graph_x = 70
    graph_y = 135
    parts = [
        '<svg width="1200" height="360" viewBox="0 0 1200 360" xmlns="http://www.w3.org/2000/svg">',
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#111827"/><stop offset="1" stop-color="#0D1117"/></linearGradient>',
        '<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#A855F7"/><stop offset="0.5" stop-color="#22D3EE"/><stop offset="1" stop-color="#10B981"/></linearGradient>',
        '<filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        '<style>.hot{animation:pulse 1.8s ease-in-out infinite}.scan{animation:scan 4s linear infinite}@keyframes pulse{50%{opacity:.65}}@keyframes scan{from{transform:translateX(0)}to{transform:translateX(1120px)}}</style>',
        "</defs>",
        '<rect width="1200" height="360" rx="18" fill="url(#bg)" stroke="#263244"/>',
        '<path d="M0 86H1200" stroke="#263244"/>',
        '<text x="42" y="45" fill="#E5E7EB" font-family="monospace" font-size="22" font-weight="700">CONTRIBUTION QUEST</text>',
        '<text x="42" y="70" fill="#94A3B8" font-family="monospace" font-size="12">Nausheen2206 // BUILDING IN PUBLIC</text>',
        '<text x="930" y="42" fill="#22D3EE" font-family="monospace" font-size="12">TOTAL XP</text>',
        f'<text x="930" y="70" fill="#FBBF24" font-family="monospace" font-size="24" font-weight="700">{total:,}</text>',
        '<rect x="42" y="101" width="1116" height="5" rx="2.5" fill="#1F2937"/>',
        '<rect class="scan" x="42" y="101" width="120" height="5" rx="2.5" fill="url(#bar)" filter="url(#glow)"/>',
        '<text x="42" y="128" fill="#64748B" font-family="monospace" font-size="10">LESS</text>',
        '<text x="1100" y="128" fill="#64748B" font-family="monospace" font-size="10">MORE</text>',
    ]

    for index, date in enumerate(dates):
        count = contributions.get(date.isoformat(), 0)
        level = contribution_level(count, maximum)
        x = graph_x + (index // 7) * (cell + gap)
        y = graph_y + (index % 7) * (cell + gap)
        class_name = ' class="hot"' if level >= 4 else ""
        parts.append(
            f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="{COLORS[level]}"{class_name}><title>{date.isoformat()}: {count} contributions</title></rect>'
        )

    parts.extend(
        [
            '<rect x="42" y="307" width="1116" height="1" fill="#263244"/>',
            f'<text x="42" y="334" fill="#A5B4FC" font-family="monospace" font-size="12">ACTIVE DAYS  {active_days}</text>',
            '<text x="310" y="334" fill="#22D3EE" font-family="monospace" font-size="12">STREAK MODE  ONLINE</text>',
            '<text x="930" y="334" fill="#10B981" font-family="monospace" font-size="12">LEVEL UP +SHIP</text>',
            "</svg>",
        ]
    )

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(parts))
    print(f"Contribution quest created: {output_file}")


if __name__ == "__main__":
    data = fetch_contributions(USERNAME)
    build_svg(data)
