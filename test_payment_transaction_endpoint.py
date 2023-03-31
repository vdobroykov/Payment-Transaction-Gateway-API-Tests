import requests
from config import config
import json

data = {
    "payment_transaction": {
        "card_number": "4200000000000000",
        "cvv": "123",
        "expiration_date": "06/2019",
        "amount": "500",
        "usage": "Coffeemaker",
        "transaction_type": "sale",
        "card_holder": "Panda Panda",
        "email": "panda@example.com",
        "address": "Panda Street, China"
    }
}

url = config['urlSettings']['baseUrl'] + "/payment_transactions"
authorizationType = config['authorization']['authorizationType']
authorizationToken = config['authorization']['authorizationToken']


# Send a valid payment transaction request and expect an approved response
def test_valid_payment_transaction():
    response = requests.post(url,
                             headers={"Content-Type": "application/json",
                                      "Authorization": authorizationType + " " + authorizationToken},
                             json=data)

    assert response.status_code == 200

    parsed_response = json.loads(response.content)

    assert parsed_response["status"] == "approved"
    assert parsed_response["usage"] == "Coffeemaker"
    assert parsed_response["amount"] == 500
    assert parsed_response["message"] == "Your transaction has been approved."
    assert parsed_response["unique_id"] and len(parsed_response["unique_id"]) > 0
    assert parsed_response["transaction_time"] and len(parsed_response["transaction_time"]) > 0


# Send a valid void transaction request and expect an approved response
def test_valid_void_transaction():
    response = requests.post(url,
                             headers={"Content-Type": "application/json",
                                      "Authorization": authorizationType + " " + authorizationToken},
                             json=data)
    parsed_response = json.loads(response.content)
    unique_id = parsed_response["unique_id"]

    void_request_body = {
        "payment_transaction": {
            "reference_id": unique_id,
            "transaction_type": "void"
        }
    }
    void_response = requests.post(url,
                                  headers={"Content-Type": "application/json",
                                           "Authorization": authorizationType + " " + authorizationToken},
                                  json=void_request_body)

    assert void_response.status_code == 200

    parsed_void_response = json.loads(void_response.content)

    assert parsed_void_response["status"] == "approved"
    assert parsed_void_response["usage"] == "Coffeemaker"
    assert parsed_void_response["amount"] == 500
    assert parsed_void_response["message"] == "Your transaction has been voided successfully"
    assert parsed_void_response["unique_id"] and len(parsed_void_response["unique_id"]) > 0
    assert parsed_void_response["transaction_time"] and len(parsed_void_response["transaction_time"]) > 0


# Send a valid payment transaction with an invalid authentication and expect an appropriate response (401)
def test_valid_payment_transaction_invalid_authentication():
    response = requests.post(url,
                             headers={"Content-Type": "application/json",
                                      "Authorization": "Bearer Y29kZW1vbnN0ZXI6bXk1ZWNyZXQta2V5Mm8ybw=="},
                             json=data)

    assert response.status_code == 401
    assert response.content.decode("utf-8") == "HTTP Basic: Access denied.\n"


# Send a void transaction pointing to a non-existent payment transaction and expect (422)
def test_void_transaction_non_existent_payment():
    void_request_body = {
        "payment_transaction": {
            "reference_id": "",
            "transaction_type": "void"
        }
    }
    void_response = requests.post(url,
                                  headers={"Content-Type": "application/json",
                                           "Authorization": authorizationType + " " + authorizationToken},
                                  json=void_request_body)

    assert void_response.status_code == 422

    parsed_void_response = json.loads(void_response.content)
    error_responses = parsed_void_response["reference_id"]

    assert len(error_responses) > 0
    assert error_responses[0] == "Invalid reference transaction!"
    assert error_responses


# Send a void transaction pointing to an existent void transaction and expect (422)
def test_void_transaction_existent_void_transaction():
    response = requests.post(url,
                             headers={"Content-Type": "application/json",
                                      "Authorization": authorizationType + " " + authorizationToken},
                             json=data)
    parsed_response = json.loads(response.content)
    unique_id = parsed_response["unique_id"]

    void_request_body = {
        "payment_transaction": {
            "reference_id": unique_id,
            "transaction_type": "void"
        }
    }
    void_response = requests.post(url,
                                  headers={"Content-Type": "application/json",
                                           "Authorization": authorizationType + " " + authorizationToken},
                                  json=void_request_body)

    parsed_void_response = json.loads(void_response.content)
    existent_unique_id = parsed_void_response["unique_id"]

    void_request_existent_void_transaction_body = {
        "payment_transaction": {
            "reference_id": existent_unique_id,
            "transaction_type": "void"
        }
    }
    void_response_existent_void_transaction = requests.post(url,
                                                            headers={"Content-Type": "application/json",
                                                                     "Authorization": authorizationType + " " + authorizationToken},
                                                            json=void_request_existent_void_transaction_body)

    assert void_response_existent_void_transaction.status_code == 422

    parsed_void_response_existent_void_transaction = json.loads(void_response_existent_void_transaction.content)
    error_responses = parsed_void_response_existent_void_transaction["reference_id"]

    assert len(error_responses) > 0
    assert error_responses[0] == "Invalid reference transaction!"
    assert error_responses