import requests

def fetch_issues(owner, repo, max_issues=10):
    """
    Fetches open GitHub issues.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {
        "state": "open",
        "per_page": max_issues
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    issues = []
    for issue in response.json():
        if "pull_request" not in issue:
            issues.append({
                "number": issue["number"],
                "title": issue["title"],
                "body": issue["body"] or "",
                "labels": [l["name"] for l in issue["labels"]]
            })

    return issues



