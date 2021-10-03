import json
from urllib.request import Request, urlopen

from config.constants import APPROVED, DENIED
from config.secret import GITHUB_OAUTH_TOKEN
from utils.payment_requests import get_audit_results, get_payment_request_details, is_issue_eligible_for_processing

"""
TODO
- Ensure we aren't paying out duplicate issues
- Create payment receipt markdown file
- Update auth token to have proper permissions
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

    spacer = '-' * 20
    print(f'\n{spacer} Audit Results {spacer}')

    for auditor, responses in audit_results.items():
        print(f'\n{auditor}:')

        for response in responses:
            amount = response['amount']
            user = response['user']
            assessment = response['assessment']
            print(f'{amount} | {user} | {assessment}')


def fetch(*, url, headers):
    """
    Fetch API data and return as Python object
    """

    request = Request(url, headers=headers)
    response = urlopen(request)
    results = json.loads(response.read())

    return results


def process_payment(*, payment_request_details, audit_results, issue_number):
    """
    Process issue payment sending payments to each user
    For issues where all payments have been denied those will be logged as well

    For each payment recipient:
        sending payment (MOCK THIS FOR NOW - DO THIS LAST)
        writing results to a CSV file
        removing "Payment Due" label and adding the proper payment status label
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

                    if assessment == APPROVED:
                        approvals += 1
                    elif assessment == DENIED:
                        denials += 1

        if approvals > denials and approvals != 0:
            print(f'Pay {requested_user} {requested_amount} coins for issue #{issue_number}')


def run():
    """
    Run main application
    """

    payment_due_issues = fetch(
        url='https://api.github.com/repos/thenewboston-developers/Management/issues?labels=Payment+Due',
        headers={
            'Authorization': f'token {GITHUB_OAUTH_TOKEN}'
        }
    )

    for payment_due_issue in payment_due_issues:
        payment_request_details = get_payment_request_details(payment_due_issue)
        issue_number = payment_due_issue['number']
        comments = fetch(
            url=f'https://api.github.com/repos/thenewboston-developers/Management/issues/{issue_number}/comments',
            headers={
                'Authorization': f'token {GITHUB_OAUTH_TOKEN}'
            }
        )
        audit_results = get_audit_results(comments)

        if not is_issue_eligible_for_processing(audit_results):
            continue

        display_payment_details(
            payment_request_details=payment_request_details,
            audit_results=audit_results
        )

        spacer = '-' * 20
        print(f'\n{spacer} Payments Needed {spacer}\n')

        process_payment(
            payment_request_details=payment_request_details,
            audit_results=audit_results,
            issue_number=issue_number
        )


if __name__ == '__main__':
    run()
