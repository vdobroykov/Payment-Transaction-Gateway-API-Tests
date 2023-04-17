import pytest

def pytest_addoption(parser):
    parser.addoption("--username", action="store")
    parser.addoption("--password", action="store")
    parser.addoption("--base_url", action="store", default="http://localhost:3001")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    username_value = metafunc.config.option.username
    password_value = metafunc.config.option.password
    base_url_value = metafunc.config.option.base_url

    if 'username' in metafunc.fixturenames and username_value is not None:
        metafunc.parametrize("username", [username_value])

    if 'password' in metafunc.fixturenames and password_value is not None:
        metafunc.parametrize("password", [password_value])

    if 'base_url' in metafunc.fixturenames and base_url_value is not None:
        metafunc.parametrize("base_url", [base_url_value])


@pytest.fixture
def config_data_load(request):
    base_url_value = request.config.option.base_url
    username_value = request.config.option.username
    password_value = request.config.option.password

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
    
    return ConfigData(base_url_value,
                      username_value,
                      password_value,
                      "/payment_transactions",
                      payment_transaction_data)


class ConfigData:
    def __init__(self, base_url, username, password, payment_transaction_endpoint, payment_transaction_payload):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.payment_transaction_endpoint = payment_transaction_endpoint
        self.payment_transaction_payload = payment_transaction_payload