## Payment Transaction Gateway API Tests

The code in this repository implements integration tests, covering most of the possible scenarios of <br/>
interaction with [Codemonsters Payment Gateway Demo API](https://github.com/eMerchantPay/codemonsters_api_full) "POST /payment_transactions" endpoint. <br/>
It can be considered a test app verifying that the API satisfies basic functional requirements.

### Environment setup

A Linux host is required as mentioned in the [Codemonsters Payment Gateway Demo API](https://github.com/eMerchantPay/codemonsters_api_full) readme instructions. <br/>
Make sure you have a successfully running API (system under test) following the instructions from the repository above. <br/>
In order to run the tests script you need to have the following dependencies installed: <br/>
* Python3 (Interpreter version 3.10)
* pytest 7.2.2 - can be installed by executing ``` sudo apt-get install python3-pytest ``` in the terminal
* requests 2.28.2 - can be installed by executing ``` sudo apt-get install python3-requests ``` in the terminal

After retrieving the code from this repository navigate to the directory of the project and execute ``` python3 -m pytest -v ``` <br/>
in the terminal. Expected result: <br/>
![Alt text](/Docs/Images/Tests_passing.png?raw=true)
