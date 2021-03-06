# Once you have the Info.csv ready with all the changes you can use this script to import the changes back.
# Please keep in mind if you have added certain attributes in the exportRelationship.py, also adapt this script per the need.
# This works by default in line with the ApplicationtoITRelationship and changes in Technical Fit.
# Changes required :-
# 1. Provide : apiToken and adapt the base_url as per your instance.
# 2. Modify the runUpdate as per the requirement.
# 3. Test the script in Sandbox and on a small amount of data before making the bulk changes.

import json
import requests
import sys
import base64
import click
import pandas as pd

# Define Global variables here
# Required Global Variable : apiToken
apiToken = ""
# Update the Base URL of your LeanIX instance
base_url = 'https://demo-eu.leanix.net'

def getAccessToken(api_token):
    api_token = api_token
    auth_url = base_url+'/services/mtm/v1/oauth2/token'

    # Get the bearer token - see https://dev.leanix.net/v4.0/docs/authentication
    response = requests.post(auth_url, auth=('apitoken', api_token),
                             data={'grant_type': 'client_credentials'})
    response.raise_for_status()
    access_token = response.json()['access_token']
    return access_token

# Function to decipher the access_token
def getAccessTokenJson(access_token):
    payload_part = access_token.split('.')[1]
    # fix missing padding for this base64 encoded string.
    # If number of bytes is not dividable by 4, append '=' until it is.
    missing_padding = len(payload_part) % 4
    if missing_padding != 0:
        payload_part += '=' * (4 - missing_padding)
    payload = json.loads(base64.b64decode(payload_part))
    return payload

# runUpdate method to update FactSheet
def runUpdate(access_token):
    df = pd.read_csv('Info.csv', sep=';')
    df = df.fillna("")
    for index, row in df.iterrows():
        runMutation(row['App ID'],row['Relation ID'],row['ITComponent ID'],row['Attribute Value'], access_token)

# For updating an Attribute on relationship, you will need RelationshipID along with the FactSheetID and the targetFactSheet ID which we exported in exportRelationships.py
def runMutation(factSheetId,relationId,targetId,attributeValue, access_token):
    attribute = "technicalSuitability"
    path = "/relApplicationToITComponent/"+relationId
    print(attributeValue)
    patches = "{op: replace, path: \""+path+"\", value: \"{\\\""+attribute+"\\\": \\\""+attributeValue+"\\\",\\\"factSheetId\\\": \\\""+ targetId +"\\\"}\"}"
    query = """
    mutation{
        updateFactSheet(id: "%s",patches: [%s]) {
        factSheet {
        id
        name
        }
        }
      }
    """ % (factSheetId, patches)
    response_mutation = call("query", query, access_token)
    print(response_mutation)

# General function to call GraphQL given a query
def call(request_type, query, access_token):
    auth_header = 'Bearer ' + access_token
    header = {'Authorization': auth_header}
    request_url = base_url+'/services/pathfinder/v1/graphql'
    data = {request_type: query}
    json_data = json.dumps(data)
    response = requests.post(url=request_url, headers=header, data=json_data)
    response.raise_for_status()
    return response.json()

# start of main program
if __name__ == '__main__':
    access_token = getAccessToken(apiToken)
    access_token_json = getAccessTokenJson(access_token)
    print(access_token_json['principal']['username'])
    print(access_token_json['principal']['permission']['workspaceName'])
    if click.confirm('Do you want to continue?', default=True):
      runUpdate(access_token)