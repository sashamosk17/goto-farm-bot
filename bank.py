import requests

host = 'https://bank.goto.msk.ru'
trading_token = '6e6f9b5a-45a0-4819-8b45-bfdb24d366c0'

def ask_money(from_id, amount, description):
    answer = requests.post(host + '/api/ask', json={
        'token': trading_token,
        'account_id': from_id,
        'amount': amount,
        'description': description
    })

    return answer.json()


def verify_transaction(transaction_id, code):
    answer = requests.post(host + '/api/verify', json={
        "transaction_id": transaction_id,
        "code": code
    })

    return answer.json()

def send_money(to_id, amount, description):
    answer = requests.post(host + '/api/send', json={
        'token': trading_token,
        'account_id': to_id,
        'amount': amount,
        'description': description
    })

    return answer.json()
