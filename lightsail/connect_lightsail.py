
import boto3

STATIC_IP_ADDRESS='54.203.12.154'
URL='http://54.203.12.154/wp-admin/'
USERNAME='user'
PASSWORD='h9grtxnyRPdz'

# Connecting to Lightsail using boto3
client = boto3.client('lightsail')

# Connect to the .pem
pem_key_path = 'LightsailDefaultKey-us-west-2.pem'
key = open(pem_key_path, 'r').read()

# Connect to the instance
region = 'us-west-2'

# Connect to the instance
response = client.get_instance(
    instanceName='WordPress-1'
)
print(response)

bitnami-wordpress.sh --admin_password "password"