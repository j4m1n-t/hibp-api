import argparse, hashlib, os, requests
from dotenv import load_dotenv

class HIBPClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://haveibeenpwned.com/api/v3"
        self.headers = {
            'hibp-api-key': self.api_key
        }

    def check_email_breaches(self, email, truncate_response=True):
        url = f"{self.base_url}/breachedaccount/{email}?truncateResponse={str(truncate_response).lower()}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return []
        else:
            response.raise_for_status()
    
    def display_email_breaches(self, breach):
        print(f"Breach Name: {breach.name}")

    def check_password_pwned(self, password):
        sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1_password[:5], sha1_password[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url)
        if response.status_code == 200:
            hashes = (line.split(':') for line in response.text.splitlines())
            for hash_suffix, count in hashes:
                if hash_suffix == suffix:
                    return int(count)
        return 0

    def get_all_breaches(self):
        url = f"{self.base_url}/breaches"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_breach_details(self, breach_name):
        url = f"{self.base_url}/breach/{breach_name}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_subscription_status(self):
        url = f"{self.base_url}/enumeration/latest"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def display_breaches(self, breaches):
        for breach in breaches:
            print(f"Name: {breach['Name']}")
            print(f"Title: {breach['Title']}")
            print(f"Domain: {breach['Domain']}")
            print(f"Date: {breach['BreachDate']}")
            print(f"Data Compromised: {', '.join(breach['DataClasses'])}")
            print("-" * 40)

    def display_subscription_status(self, status):
        print(f"Subscription Status: {status}")

    def perform_full_check(self, email, password, truncate_response=True):
        print(f"Checking breaches for email: {email}")
        breaches = self.check_email_breaches(email, truncate_response=truncate_response)
        if breaches:
            self.display_breaches(breaches)
        else:
            print(f"No breaches found for email: {email}")

        print(f"Checking if password has been pwned...")
        password_count = self.check_password_pwned(password)
        if password_count > 0:
            print(f"Password has been pwned {password_count} times!")
        else:
            print("Password has not been pwned.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HIBP Python Client to interact with Have I Been Pwned API.")
    
    parser.add_argument(
        "--email",
        type=str,
        help="The email address to check for breaches and pastes."
    )
    parser.add_argument(
        "--password",
        type=str,
        help="The password to check if it has been pwned."
    )
    parser.add_argument(
        "--all-breaches",
        action="store_true",
        help="List all breaches."
    )
    parser.add_argument(
        "--breach-details",
        type=str,
        help="Get details of a specific breach by name."
    )
    parser.add_argument(
        "--subscription-status",
        action="store_true",
        help="Get the current subscription status."
    )
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="Truncate the response when checking breaches."
    )

    args = parser.parse_args()

    # Initialize the HIBP client
    dotenv_path = os.path.expanduser("~/hibp-api/.env")
    load_dotenv(dotenv_path)
    api_key = os.getenv('HIBP_API_KEY')
    if not api_key:
        raise ValueError("API key not found in .env file. Please set the HIBP_API_KEY variable.")

    hibp_client = HIBPClient(api_key=api_key)

    # Perform actions based on provided arguments
    if args.email and args.password:
        hibp_client.perform_full_check(email=args.email, password=args.password, truncate_response=args.truncate)
    elif args.all_breaches:
        all_breaches = hibp_client.get_all_breaches()
        print(f"Total Breaches: {len(all_breaches)}")
        hibp_client.display_breaches(all_breaches)
    elif args.breach_details:
        breach_details = hibp_client.get_breach_details(args.breach_details)
        print(breach_details)
    elif args.subscription_status:
        subscription = hibp_client.get_subscription_status()
        hibp_client.display_subscription_status(subscription)
    elif args.email:
        emails = hibp_client.check_email_breaches()
        hibp_client.display_email_breaches(emails)
    elif args.password:
        password = hibp_client.check_password_pwned()
        hibp_client.display_password_pwned(password)
    else:
        parser.print_help()
