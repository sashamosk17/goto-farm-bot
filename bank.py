import requests
from config import BANK_HOST, TRADING_TOKEN

def ask_money(from_id, amount, description):
    try:
        answer = requests.post(BANK_HOST + '/api/ask', json={
            'token': TRADING_TOKEN,
            'account_id': from_id,
            'amount': amount,
            'description': description
        })

        return answer.json()
    except:
        try:
            return answer.json()
        except:
            return None


def verify_transaction(transaction_id, code):
    try:
        answer = requests.post(BANK_HOST + '/api/verify', json={
            "transaction_id": transaction_id,
            "code": code
        })

        return answer.json()
    except:
        try:
            return answer.json()
        except:
            return None
