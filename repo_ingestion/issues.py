import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_issues(owner, repo, max_issues=5):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }

    params = {
        "state": "open",
        "per_page": max_issues,
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)

    # 👇 graceful error handling
    if response.status_code != 200:
        return [{
            "title": "GitHub API Error",
            "body": f"Status {response.status_code}: {response.text}"
        }]

    issues = response.json()

    return [
        {
            "title": issue.get("title", ""),
            "body": issue.get("body", "")
        }
        for issue in issues
        if "pull_request" not in issue
    ]
