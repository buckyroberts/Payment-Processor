import json
from urllib.request import Request, urlopen

from config.secret import GITHUB_OAUTH_TOKEN


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


def get_payment_requests(issue):
    """
    Filter out the payment requests from a GitHub issue
    """

    lines = issue.get('body').splitlines()
    payment_requests = [line for line in lines if line.startswith('[payment_request|') and line.endswith(']')]
    return payment_requests


def get_payment_request_data(issue):
    """
    Return payment request data
    """

    for payment_request in get_payment_requests(issue):
        print(payment_request)


def run():
    """
    Run main application
    """

    issues = fetch('https://api.github.com/repos/thenewboston-developers/Management/issues?labels=Payment+Due')

    for issue in issues:
        get_payment_request_data(issue)


if __name__ == '__main__':
    run()
