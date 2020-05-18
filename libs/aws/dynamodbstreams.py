'''
dynamoDBstreams functions for WeirdAAL
'''

import boto3
import botocore
import pprint
import os
import sys

pp = pprint.PrettyPrinter(indent=5, width=80)

# from http://docs.aws.amazon.com/general/latest/gr/rande.html
regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'af-south-1', 'ap-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'cn-north-1', 'cn-northwest-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-south-1', 'eu-north-1', 'me-south-1', 'sa-east-1', 'us-gov-west-1', 'us-gov-east-1']

'''
Code to get the AWS_ACCESS_KEY_ID from boto3
'''
session = boto3.Session()
credentials = session.get_credentials()
AWS_ACCESS_KEY_ID = credentials.access_key


def list_dynamodbstreams():
    '''
    Use list_streams function in dynamodbstreams to list available streams
    '''
    print("### Printing DynamoDBstreams ###")
    try:
        for region in regions:
            client = boto3.client('dynamodbstreams', region_name=region)
            response = client.list_streams()
            if response.get('Streams') is None:
                print("{} likely does not have DynamoDB permissions\n" .format(AWS_ACCESS_KEY_ID))
            elif len(response['Streams']) <= 0:
                print("[-] ListStreams allowed for {} but no results [-]" .format(region))
            else:
                print("### {} DynamoDB Streams ###" .format(region))
                for streams in response['Streams']:
                    pp.pprint(streams)
                    print("\n")

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'InvalidClientTokenId':
            sys.exit("{} : The AWS KEY IS INVALID. Exiting" .format(AWS_ACCESS_KEY_ID))
        elif e.response['Error']['Code'] == 'AccessDenied':
            print('{} : Does not have the required permissions' .format(AWS_ACCESS_KEY_ID))
        elif e.response['Error']['Code'] == 'SubscriptionRequiredException':
            print('{} : Has permissions but isnt signed up for service - usually means you have a root account' .format(AWS_ACCESS_KEY_ID))
        else:
            print("Unexpected error: {}" .format(e))
    except KeyboardInterrupt:
        print("CTRL-C received, exiting...")
