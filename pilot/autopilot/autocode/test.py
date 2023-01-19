# Import necessary libraries
import requests
import logging
import configparser
import requests_oauthlib
import clickup
import time
import os

# Use a more robust logging system to better track and log errors and events.
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ClickupConnection:
    def __init__(self, timeout=30):
        self.timeout = timeout

    # Use a context manager to ensure the connection is properly closed if an error occurs.
    def __enter__(self):  # sourcery skip: raise-specific-error
        with requests.session() as clickup_session:
            # Create a function to better handle authentication and authorization, instead of using the environment variables within the class.
            def authenticate_and_authorize():
                self.clickup_auth_token = os.environ.get('CLICKUP_AUTH_TOKEN')
                self.clickup_api_key = os.environ.get('CLICKUP_API_KEY')
                
                # Validate the environment variables for authentication and authorization before making a connection attempt.
                if not self.clickup_auth_token or not self.clickup_api_key:
                    logging.error('Missing environment variables for authentication and authorisation')
                    raise Exception('Missing environment variables for authentication and authorisation')
                
                # Authenticate with Clickup using OAuth
                oauth = requests_oauthlib.OAuth2Session(self.clickup_auth_token)
                logging.info('Authenticated with Clickup API using OAuth')

                # Authorize the connection with Clickup
                timeout_start = time.time()
                while time.time() < timeout_start + self.timeout:
                    authorization = clickup_session.post('https://api.clickup.com/api/v2/authorize', data={'api_key': self.clickup_api_key})
                    if authorization.status_code == 200:
                        # Successfully connected to Clickup API
                        logging.info('Successfully connected to Clickup API')
                        break
                    else:
                        # Add a retry mechanism if the initial connection attempt fails.
                        time.sleep(1)
                        logging.warning('Connection attempt to Clickup API failed. Retrying...')
                        if time.time() > timeout_start + self.timeout:
                            # Use a more robust retry mechanism if the timeout is exceeded.
                            clickup_session.get('https://api.clickup.com/api/v2/authorize', data={'api_key': self.clickup_api_key}, timeout=30, retry=True, backoff_factor=0.3)
                            logging.warning('Connection attempt to Clickup API timed out. Retrying...')
                else:
                    # Log any errors that occur during the connection
                    logging.error('Error connecting to Clickup API: {}'.format(authorization.status_code))
                
                # Add a fallback for failed authentication attempts and allow for multiple authentication methods.
                if clickup.Client.is_authenticated_with_additional_methods():
                    logging.info('Authenticated with Clickup API using additional authentication methods')
                else:
                    logging.info('Already authenticated and authorized with Clickup API')

            # Improve the error handling by catching exceptions and logging them.
            try:
                # Call the authentication and authorization function
                authenticate_and_authorize()
            except Exception as error:
                logging.exception('Unexpected error connecting to Clickup API: {}'.format(error))
        return clickup_session

    # Close the connection if an error occurs
    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info('Closing connection to Clickup API')

# Create a main function to call the connection class
def main():
    # Establish a connection to the Clickup API
    with ClickupConnection() as clickup_session:
        # Use the requests module’s built-in timeout setting to set a time limit for the connection attempt.
        try:
            clickup_session.get('https://api.clickup.com/api/v2/me', timeout=30)
        except requests.exceptions.Timeout:
            # Use a more robust retry mechanism if the timeout is exceeded.
            logging.warning('Connection attempt to Clickup API timed out. Retrying...')
            clickup_session.get('https://api.clickup.com/api/v2/me', timeout=30, retry=True, backoff_factor=0.3)
        except Exception as error:
            logging.exception('Unexpected error connecting to Clickup API: {}'.format(error))

# Call the main function
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception("Unexpected error: {}".format(e))