import pytest
from config import sut_settings

def pytest_addoption(parser):
    parser.addoption("--username", action="store")
    parser.addoption("--password", action="store")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    username_value = metafunc.config.option.username
    password_value = metafunc.config.option.password

    if 'username' in metafunc.fixturenames and username_value is not None:
        metafunc.parametrize("username", [username_value])

    if 'password' in metafunc.fixturenames and password_value is not None:
        metafunc.parametrize("password", [password_value])


@pytest.fixture
def payment_transaction_payload():
    return {
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
@pytest.fixture
def config_data_load():
    payment_transaction_data = {
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
    return ConfigData(sut_settings['urlSettings']['baseUrl'] + "/payment_transactions", payment_transaction_data)

class ConfigData:
    def __init__(self, url, payment_transaction_payload):
        self.url = url
        self.payment_transaction_payload = payment_transaction_payload