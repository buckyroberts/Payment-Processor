import json
from urllib.request import Request, urlopen

from config.secret import GITHUB_OAUTH_TOKEN
from utils.payment_requests import get_audit_results, get_payment_request_details


def fetch(url):
    """
    Fetch API data and return as Python object
    """

    request = Request(
        url,
        headers={
            'Authorization': f'token {GITHUB_OAUTH_TOKEN}'
        }
    )
    response = urlopen(request)
    results = json.loads(response.read())

    return results


def run():
    """
    Run main application
    """

    payment_due_issues = fetch(
        'https://api.github.com/repos/thenewboston-developers/Management/issues?labels=Payment+Due'
    )

    for payment_due_issue in payment_due_issues:
        payment_request_details = get_payment_request_details(payment_due_issue)
        print(payment_request_details)

        number = payment_due_issue['number']
        comments = fetch(f'https://api.github.com/repos/thenewboston-developers/Management/issues/{number}/comments')
        audit_results = get_audit_results(comments)
        print(audit_results)


if __name__ == '__main__':
    run()
