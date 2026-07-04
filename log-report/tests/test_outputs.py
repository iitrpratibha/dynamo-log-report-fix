import json
import re
from collections import Counter
from pathlib import Path

REPORT = Path("/app/report.json")
# /tests is read-only for the agent, so we recompute the answers from our own copy of the log.
TRUSTED_LOG = Path("/tests/access.log")

REQUEST_LINE = re.compile(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ')


def expected():
    paths, ips, total = Counter(), set(), 0
    for line in TRUSTED_LOG.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        total += 1
        ips.add(line.split()[0])
        match = REQUEST_LINE.search(line)
        if match:
            paths[match.group(1)] += 1
    return total, len(ips), paths.most_common(1)[0][0]


def load_report():
    assert REPORT.exists(), f"no report at {REPORT}"
    try:
        return json.loads(REPORT.read_text())
    except json.JSONDecodeError as exc:
        raise AssertionError(f"{REPORT} is not valid JSON: {exc}")


def test_report_is_json_object():
    """Criterion 1: report.json exists and is a single JSON object."""
    data = load_report()
    assert isinstance(data, dict), "report.json must be a single JSON object"


def test_total_requests():
    """Criterion 2: total_requests matches the request count in the log."""
    total, _, _ = expected()
    data = load_report()
    assert data.get("total_requests") == total, \
        f"total_requests should be {total}, got {data.get('total_requests')!r}"


def test_unique_ips():
    """Criterion 3: unique_ips matches the distinct client IP count."""
    _, ips, _ = expected()
    data = load_report()
    assert data.get("unique_ips") == ips, \
        f"unique_ips should be {ips}, got {data.get('unique_ips')!r}"


def test_top_path():
    """Criterion 4: top_path is the most-requested path."""
    _, _, top = expected()
    data = load_report()
    assert data.get("top_path") == top, \
        f"top_path should be {top!r}, got {data.get('top_path')!r}"
