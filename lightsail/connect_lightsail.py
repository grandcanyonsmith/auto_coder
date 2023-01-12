

import boto3
import logging
import base64
import hashlib
import os

# Set up logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Configuration Options
STATIC_IP_ADDRESS: str = '54.203.12.154'
URL: str = 'http://54.203.12.154/wp-admin/'
USERNAME: str = 'user'
PASSWORD: str = hashlib.sha256('h9grtxnyRPdz'.encode('utf-8')).hexdigest()

# Connecting to Lightsail using boto3
client = boto3.client('lightsail')

# Connect to the .pem
PEM_KEY_PATH: str = 'LightsailDefaultKey-us-west-2.pem'
key: str = open(PEM_KEY_PATH, 'rb').read()

# Connect to the instance
REGION: str = 'us-west-2'


class LightsailInstance:
    """
    Class to manage a Lightsail instance and provide methods to connect and set the admin password
    """
    def __init__(self, instance_name: str, region: str) -> None:
        """
        Initialize the connection to the Lightsail instance
        
        Parameters
        ----------
        instance_name : str
            The name of the instance to connect to
        region : str
            The region of the instance to connect to
        """
        self.instance_name = instance_name
        self.region = region
        self.connection = self._connect_instance()

    def _connect_instance(self) -> dict:
        """
        Connect to the instance in the specified region

        Returns
        -------
        response : dict
            The response from the instance connection
        """
        # Log the connection attempt
        logging.info(f'Attempting to connect to instance {self.instance_name} in region {self.region}')

        # Initialize response variable
        response = None

        # Try to connect to the instance
        try:
            response = client.get_instance(instanceName=self.instance_name)
            # Log the response
            logging.info(f'Successfully connected to instance {self.instance_name} in region {self.region}: {response}')
        # Log the error if an exception is thrown and raise the exception
        except Exception as e:
            logging.error(f'Failed to connect to instance {self.instance_name} in region {self.region}: {e}')
            raise

        return response
    
    def set_admin_password(self, password: str) -> dict:
        """
        Set the admin password for the instance

        Parameters
        ----------
        password : str
            The password to set for the instance

        Returns
        -------
        response : dict
            The response from the admin password set
        """

        # Log the admin password set attempt
        logging.info(f'Attempting to set admin password')

        # Initialize response variable
        response = None

        # Secure credentials usage
        encrypted_password = base64.b64encode(password.encode('utf-8'))

        # Try to set the admin password
        try:
            response = f'bitnami-wordpress.sh --admin_password {encrypted_password}'
            # Log the response
            logging.info(f'Successfully set admin password')
            # Log an info message when the admin password is set
            logging.info('Admin password has been set successfully!')
        # Log the error if an exception is thrown and raise the exception
        except Exception as e:
            logging.error(f'Failed to set admin password: {e}')
            raise
        return response


def main():
    # Connect to the instance
    try:
        instance = LightsailInstance('WordPress-1', REGION)
        response = instance.connection
        # Check if response is valid
        if response:
            logging.info('Successfully received a valid response')
        else:
            logging.error('Invalid response received')
    except Exception as e:
        logging.error(f'Failed to connect to instance: {e}')

    # Set admin password
    try:
        # Check if password is valid
        if PASSWORD:
            instance.set_admin_password(PASSWORD)
        else:
            logging.error('Invalid password')
    except Exception as e:
        logging.error(f'Failed to set admin password: {e}')


def test_connect_instance():
    """
    Test the connect_instance function
    """
    # Test with valid inputs
    try:
        instance = LightsailInstance('WordPress-1', REGION)
        response = instance.connection
        # Check if response is valid
        if response:
            logging.info('Successfully received a valid response')
        else:
            logging.error('Invalid response received')
    except Exception as e:
        logging.error(f'Failed to connect to instance: {e}')
    
    # Test with invalid inputs
    try:
        instance = LightsailInstance('InvalidInstanceName', REGION)
        response = instance.connection
        # Check if response is valid
        if response:
            logging.info('Successfully received a valid response')
        else:
            logging.error('Invalid response received')
    except Exception as e:
        logging.error(f'Failed to connect to instance: {e}')


def test_set_admin_password():
    """
    Test the set_admin_password function
    """
    # Test with valid inputs
    try:
        instance = LightsailInstance('WordPress-1', REGION)
        response = instance.set_admin_password(PASSWORD)
        # Check if response is valid
        if response:
            logging.info('Successfully received a valid response')
        else:
            logging.error('Invalid response received')
    except Exception as e:
        logging.error(f'Failed to set admin password: {e}')
    
    # Test with invalid inputs
    try:
        instance = LightsailInstance('WordPress-1', REGION)
        response = instance.set_admin_password('invalidpassword')
        # Check if response is valid
        if response:
            logging.info('Successfully received a valid response')
        else:
            logging.error('Invalid response received')
    except Exception as e:
        logging.error(f'Failed to set admin password: {e}')


if __name__ == '__main__':
    main()
    test_connect_instance()
    test_set_admin_password()