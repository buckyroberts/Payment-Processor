from config.settings import AUDITORS


def get_audit_results(comments):
    """
    Parse GitHub API comments into list of dictionaries
    """

    audit_results = {auditor: [] for auditor in AUDITORS}

    for comment in comments:
        comment_body = comment['body']
        username = comment['user']['login']

        # Not a valid auditor
        if username not in AUDITORS:
            continue

        # If we already have results for this auditor
        if audit_results[username]:
            continue

        audit_results[username] = parse_comment_body_for_payment_data(comment_body)

    return audit_results


def get_payment_request_details(issue):
    """
    Filter out the payment requests from a GitHub issue
    """

    lines = issue.get('body').splitlines()
    payment_requests = [line for line in lines if line.startswith('[payment_request|') and line.endswith(']')]
    payment_requests = [parse_payment_request(payment_request) for payment_request in payment_requests]

    return {
        'creator': issue['user']['login'],
        'payment_requests': payment_requests
    }


def parse_comment_body_for_payment_data(comment_body):
    """
    Parse a GitHub comment body and return a list of payment request dicts
    """

    lines = comment_body.splitlines()
    results = [line for line in lines if line.startswith('[payment_request|') and line.endswith(']')]
    results = [parse_payment_request_response(payment_request) for payment_request in results]
    return results


def parse_payment_request(payment_request):
    """
    Parse payment request line of text into dictionary
    """

    results = payment_request.replace('[payment_request|', '').replace(']', '')
    amount, user = results.split('|')

    return {
        'amount': int(amount),
        'user': user
    }


def parse_payment_request_response(payment_request_response):
    """
    Parse payment request response line of text into dictionary
    """

    results = payment_request_response.replace('[payment_request|', '').replace(']', '')
    amount, user, assessment = results.split('|')

    return {
        'amount': int(amount),
        'user': user,
        'assessment': assessment
    }
