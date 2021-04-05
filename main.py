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


def run():
    """
    Run main application
    """

    data = fetch('https://api.github.com/repos/thenewboston-developers/Management/issues?labels=Payment+Due')
    print(data)


if __name__ == '__main__':
    run()
