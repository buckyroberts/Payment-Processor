import json
from urllib.request import Request, urlopen

from config.secret import GITHUB_OAUTH_TOKEN
from utils.payment_requests import get_audit_results, get_payment_request_details, is_issue_eligible_for_processing

"""
TODO
- Ensure we aren't paying out duplicate issues
"""


def display_payment_details(*, payment_request_details, audit_results):
    """
    Display formatted payment details (for development)
    """

    print('\nCreator:')
    print(payment_request_details['creator'])

    print('\nPayment Requests:')
    for payment_request in payment_request_details['payment_requests']:
        amount = payment_request['amount']
        user = payment_request['user']
        print(f'{amount} | {user}')

    spacer = '-' * 40
    print(f'\n{spacer}')

    for auditor, responses in audit_results.items():
        print(f'\n{auditor}:')

        for response in responses:
            amount = response['amount']
            user = response['user']
            assessment = response['assessment']
            print(f'{amount} | {user} | {assessment}')


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


def process_payment(*, payment_request_details, audit_results, issue_number):
    """
    Process payment including:
    - calculating all payment recipients and amounts
    - sending payments to each
    - writing results to a CSV file after each payment has been sent
    - updating the GitHub issue with the proper label
    """

    payment_requests = payment_request_details['payment_requests']

    for payment_request in payment_requests:
        requested_amount = payment_request['amount']
        requested_user = payment_request['user']

        approvals = 0
        denials = 0

        for auditor, responses in audit_results.items():

            for response in responses:
                amount = response['amount']
                user = response['user']
                assessment = response['assessment']

                if amount == requested_amount and user == requested_user:

                    # TODO: Constants
                    if assessment == 'approved':
                        approvals += 1
                    elif assessment == 'denied':
                        denials += 1

        if approvals > denials and approvals != 0:
            print(f'Pay {requested_user} {requested_amount} coins for issue #{issue_number}')


def run():
    """
    Run main application
    """

    payment_due_issues = fetch(
        'https://api.github.com/repos/thenewboston-developers/Management/issues?labels=Payment+Due'
    )

    for payment_due_issue in payment_due_issues:
        payment_request_details = get_payment_request_details(payment_due_issue)
        issue_number = payment_due_issue['number']
        comments = fetch(
            f'https://api.github.com/repos/thenewboston-developers/Management/issues/{issue_number}/comments'
        )
        audit_results = get_audit_results(comments)

        if not is_issue_eligible_for_processing(audit_results):
            continue

        process_payment(
            payment_request_details=payment_request_details,
            audit_results=audit_results,
            issue_number=issue_number
        )

        display_payment_details(
            payment_request_details=payment_request_details,
            audit_results=audit_results
        )


if __name__ == '__main__':
    run()
