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