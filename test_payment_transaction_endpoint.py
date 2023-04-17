import pytest
import requests
from config import sut_settings
import json
from requests.auth import HTTPBasicAuth

#url = sut_settings['urlSettings']['baseUrl'] + "/payment_transactions"

class Tests:
    # Send a valid payment transaction request and expect an approved response
    def test_valid_payment_transaction_returns_success(self, username, password, config_data_load):
        response = requests.post(config_data_load.url,
                                 auth=HTTPBasicAuth(username, password),
                                 headers={"Content-Type": "application/json"},
                                 json=config_data_load.payment_transaction_payload)

        assert response.status_code == 200

        parsed_response = json.loads(response.content)

        assert parsed_response["status"] == "approved"
        assert parsed_response["usage"] == "Coffeemaker"
        assert parsed_response["amount"] == 500
        assert parsed_response["message"] == "Your transaction has been approved."
        assert parsed_response["unique_id"] and len(parsed_response["unique_id"]) > 0
        assert parsed_response["transaction_time"] and len(parsed_response["transaction_time"]) > 0


    # Send a valid void transaction request and expect an approved response
    def test_valid_void_transaction_returns_success(self, username, password, config_data_load):
        # In order to void transaction we generate a payment transaction to use the unique id
        # generated from the API
        response = requests.post(config_data_load.url,
                                 auth=HTTPBasicAuth(username, password),
                                 headers={"Content-Type": "application/json"},
                                 json=config_data_load.payment_transaction_payload)
        parsed_response = json.loads(response.content)
        unique_id = parsed_response["unique_id"]

        void_request_body = {
            "payment_transaction": {
                "reference_id": unique_id,
                "transaction_type": "void"
            }
        }
        void_response = requests.post(config_data_load.url,
                                      auth=HTTPBasicAuth(username, password),
                                      headers={"Content-Type": "application/json"},
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
    def test_valid_payment_transaction_invalid_authentication_returns_access_denied(self, config_data_load):
        response = requests.post(config_data_load.url,
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer Y29kZW1vbnN0ZXI6bXk1ZWNyZXQta2V5Mm8ybw=="})

        assert response.status_code == 401
        assert response.content.decode("utf-8") == "HTTP Basic: Access denied.\n"


    # Send a void transaction pointing to a non-existent payment transaction and expect (422)
    def test_void_transaction_non_existent_payment_returns_invalid_reference(self, username, password, config_data_load):
        void_request_body = {
            "payment_transaction": {
                "reference_id": "",
                "transaction_type": "void"
            }
        }
        void_response = requests.post(config_data_load.url,
                                      auth=HTTPBasicAuth(username, password),
                                      headers={"Content-Type": "application/json"},
                                      json=void_request_body)

        assert void_response.status_code == 422

        parsed_void_response = json.loads(void_response.content)
        error_responses = parsed_void_response["reference_id"]

        assert len(error_responses) > 0
        assert error_responses[0] == "Invalid reference transaction!"
        assert error_responses


    # Send a void transaction pointing to an existent void transaction and expect (422)
    def test_void_transaction_existent_void_transaction_returns_invalid_reference(self, username, password, config_data_load):
        # In order to void transaction we generate a payment transaction to use the unique id
        # generated from the API
        response = requests.post(config_data_load.url,
                                 auth=HTTPBasicAuth(username, password),
                                 headers={"Content-Type": "application/json"},
                                 json=config_data_load.payment_transaction_payload)
        parsed_response = json.loads(response.content)
        unique_id = parsed_response["unique_id"]

        # To make sure we attempt to void an existing void transaction later
        # create a valid one voiding the payment transaction from the previous step
        void_request_body = {
            "payment_transaction": {
                "reference_id": unique_id,
                "transaction_type": "void"
            }
        }

        void_response = requests.post(config_data_load.url,
                                      auth=HTTPBasicAuth(username, password),
                                      headers={"Content-Type": "application/json"},
                                      json=void_request_body)

        parsed_void_response = json.loads(void_response.content)
        existent_unique_id = parsed_void_response["unique_id"]

        # Attempt to void the existing void transaction from the previous step
        void_request_existent_void_transaction_body = {
            "payment_transaction": {
                "reference_id": existent_unique_id,
                "transaction_type": "void"
            }
        }
        void_response_existent_void_transaction = requests.post(config_data_load.url,
                                                                auth=HTTPBasicAuth(username, password),
                                                                headers={"Content-Type": "application/json"},
                                                                json=void_request_existent_void_transaction_body)

        assert void_response_existent_void_transaction.status_code == 422

        parsed_void_response_existent_void_transaction = json.loads(void_response_existent_void_transaction.content)
        error_responses = parsed_void_response_existent_void_transaction["reference_id"]

        assert len(error_responses) > 0
        assert error_responses[0] == "Invalid reference transaction!"
        assert error_responses
