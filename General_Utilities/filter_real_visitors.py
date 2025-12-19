# FEATURES
# Works with apache log format %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"
#
# Bot/crawler exclusion: Hard filters out UAs with bot/crawler keywords.
# Score filter: Only visitors with score > 6 included.
# Sorted output: Visitors sorted by number of requests.
# Top 3 non-asset URLs per visitor.
# Unique visitor count by IP at the top.
# All HTML URLs ranked by number of unique visitors at the end.

import re
import sys
from datetime import datetime
from collections import defaultdict

# Regex to detect bot/crawler UAs
BOT_UA_REGEX = re.compile(
    r'(bot|crawler|crawl|spider|slurp|wget|curl|python|scrapy|httpclient|headless|phantom|selenium|playwright|puppeteer)',
    re.IGNORECASE
)

def ua_looks_like_bot(ua):
    return bool(BOT_UA_REGEX.search(ua))

# Apache log regex for your format
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) (?P<proto>[^"]+)" '
    r'(?P<status>\d+) (?P<bytes>\d+) '
    r'"(?P<referer>[^"]*)" "(?P<ua>[^"]*)"'
)

ASSET_EXTENSIONS = (
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif",
    ".svg", ".woff", ".woff2", ".ico"
)

TIME_FORMAT = "%d/%b/%Y:%H:%M:%S %z"

def parse_time(t):
    return datetime.strptime(t, TIME_FORMAT)

def is_asset(path):
    return path.lower().endswith(ASSET_EXTENSIONS)

def score_visitor(v):
    if len(v["times"]) < 2:
        return None

    times = sorted(v["times"])
    deltas = [
        (times[i+1] - times[i]).total_seconds()
        for i in range(len(times)-1)
    ]

    avg_delta = sum(deltas) / len(deltas)
    score = 0

    # Timing analysis
    if avg_delta > 1.0:
        score += 3
    if avg_delta < 0.2:
        score -= 3

    # Assets loaded
    if v["assets"] >= 2:
        score += 3
    else:
        score -= 2

    # HTML pages requested
    if v["html"] >= 2:
        score += 2

    # Path diversity
    if len(v["paths"]) >= 3:
        score += 2

    return score

def main(logfile):
    visitors = defaultdict(lambda: {
        "times": [],
        "assets": 0,
        "html": 0,
        "paths": set(),
        "path_counts": defaultdict(int)
    })

    # Dictionary to count unique visitors per URL
    url_visitors = defaultdict(set)

    # Parse log
    with open(logfile, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = LOG_PATTERN.search(line)
            if not m:
                continue

            ip = m.group("ip")
            ua = m.group("ua")

            # Hard exclude bots/crawlers
            if ua_looks_like_bot(ua):
                continue

            path = m.group("path")
            t = parse_time(m.group("time"))

            key = (ip, ua)
            v = visitors[key]

            v["times"].append(t)
            v["paths"].add(path)

            if is_asset(path):
                v["assets"] += 1
            else:
                v["html"] += 1
                v["path_counts"][path] += 1
                url_visitors[path].add(ip)  # track unique visitor per URL

    # Count unique visitors by IP
    unique_ips = set(ip for (ip, ua) in visitors.keys())
    total_unique_ips = len(unique_ips)
    print(f"\nTotal unique visitors (by IP, after excluding bots): {total_unique_ips}\n")

    # Collect scored visitors
    results = []

    for (ip, ua), v in visitors.items():
        score = score_visitor(v)
        if score is not None and score > 5:  # omit score ≤ 5
            # Only include non-asset URLs
            html_paths = {p: c for p, c in v["path_counts"].items() if not is_asset(p)}
            top_paths = sorted(
                html_paths.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            top_paths = [p[0] for p in top_paths]

            results.append({
                "ip": ip,
                "ua": ua,
                "score": score,
                "requests": len(v["times"]),
                "assets": v["assets"],
                "html": v["html"],
                "top_paths": top_paths
            })

    # Sort visitors by number of requests descending
    results.sort(key=lambda x: x["requests"], reverse=True)

    # Print visitor details
    print("Likely REAL visitors (score > 5, sorted by request count):\n")
    for r in results:
        print(f"IP: {r['ip']}")
        print(f"Requests: {r['requests']}")
        print(f"Score: {r['score']}")
        print(f"Assets: {r['assets']}  HTML: {r['html']}")
        print(f"Top 3 URLs visited: {', '.join(r['top_paths'])}")
        print(f"UA: {r['ua']}")
        print("-" * 60)

    # Rank all HTML URLs by number of unique visitors
    url_ranking = sorted(
        ((url, len(ips)) for url, ips in url_visitors.items()),
        key=lambda x: x[1],
        reverse=True
    )

    print("\nAll HTML URLs ranked by unique visitors:\n")
    for url, count in url_ranking:
        print(f"{url}: {count} unique visitors")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python filter_real_visitors.py access.log")
        sys.exit(1)

    main(sys.argv[1])
