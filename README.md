# HIBP Python Client

A Python client for interacting with the [Have I Been Pwned (HIBP)](https://www.haveibeenpwned.com/) [API](https://haveibeenpwned.com/API/v3). This script allows you to check if an email address has been involved in any data breaches, determine if a password has been pwned, retrieve details of specific breaches, and more.

Features

* Check Email Breaches: Identify whether an email address has been compromised in any known data breaches.
* Check Password Pwned: Determine if a password has been exposed in any known data breaches using the k-Anonymity model.
* List All Breaches: Retrieve a list of all known breaches from the HIBP API.
* Get Breach Details: Fetch detailed information about a specific breach by its name.
* Check Subscription Status: Get the current subscription status of the API key.

### Prerequisites

* Python 3.x
* A Have I Been Pwned API key. You can obtain one from [here](https://haveibeenpwned.com/API/Key).
* A `.env` file with your HIBP API key.

### Installation

1. Clone the repository into your User Directory: 

        cd ~
        git clone https://github.com/j4m1n-t/hibp-api.git
        cd hibp-api

2. Create a virtual environment (optional but recommended):

        python3 -m venv venv
        source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:

        pip install -r requirements.txt

4. Set up your `.env` file:

    Create a `.env` file in the root directory with the following content:

        HIBP_API_KEY=your_hibp_api_key
5. Modify the `.env` location in `hibp-api.py`if necessary. By default, it is set to: 
        
        dotenv_path = os.path.expanduser("~/hibp-api/.env")

### Usage

Run the script with various arguments to perform different actions:

#### Check Email Breaches

    python hibp-api.py --email example@example.com

#### Check If a Password Has Been Pwned

    python hibp-api.py --password yourpassword123

#### Perform a Full Check (Email Breaches & Password Pwned)

    python hibp-api.py --email example@example.com --password yourpassword123

#### List All Breaches

    python hibp-api.py --all-breaches

#### Get Details of a Specific Breach

    python hibp-api.py --breach-details BreachName

#### Check Subscription Status

    python hibp-api.py --subscription-status

#### Truncate Response for Email Breaches (Default = True)

    python hibp-api.py --email example@example.com --truncate

### Command-Line Arguments
|Argument| Description|
|:--|:--|
|`--email`| The email address to check for breaches.|
|`--password`| The password to check if it has been pwned.|
|`--all-breaches`| List all breaches.|
|`--breach-details`| Get details of a specific breach by name.|
|`--subscription-status`| Get the current subscription status.|
|`--truncate`| Truncate the response when checking breaches (default: True).|

### Example Usage

#### Check if an email has been involved in any breaches and whether a password has been pwned:

    python hibp-api.py --email john.doe@example.com --password mysecurepassword

#### List all known breaches:

    python hibp-api.py --all-breaches

#### Get details of a specific breach:

    python hibp-api.py --breach-details LinkedIn

### License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/j4m1n-t/hibp-api/blob/main/LICENSE) file for details.

### Contact

For any questions or issues, please contact Jamin Thompson at j.thompson@j4m1n.me.

---