import requests
from config import BANK_HOST, TRADING_TOKEN

def ask_money(from_id, amount, description):
    answer = requests.post(BANK_HOST + '/api/ask', json={
        'token': TRADING_TOKEN,
        'account_id': from_id,
        'amount': amount,
        'description': description
    })

    return answer.json()


def verify_transaction(transaction_id, code):
    answer = requests.post(BANK_HOST + '/api/verify', json={
        "transaction_id": transaction_id,
        "code": code
    })

    return answer.json()

def send_money(to_id, amount, description):
    answer = requests.post(HOST + '/api/send', json={
        'token': TRADING_TOKEN,
        'account_id': to_id,
        'amount': amount,
        'description': description
    })

    return answer.json()
