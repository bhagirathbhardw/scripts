import json 
import requests 
import pandas as pd

api_token = 'INSERT_TERANET_API_TOKEN_HERE'
auth_url = 'https://us-svc.leanix.net/services/mtm/v1/oauth2/token' 
request_url = 'https://teranet.leanix.net/services/pathfinder/v1/graphql' 

# Get the bearer token - see https://dev.leanix.net/v4.0/docs/authentication
response = requests.post(auth_url, auth=('apitoken', api_token),
 data={'grant_type': 'client_credentials'})
response.raise_for_status() 
access_token = response.json()['access_token']
auth_header = 'Bearer ' + access_token
header = {'Authorization': auth_header}

# General function to call GraphQL given a query
def call(query):
  data = {"query" : query}
  json_data = json.dumps(data)
  response = requests.post(url=request_url, headers=header, data=json_data)
  response.raise_for_status()
 return response.json()

def setQualitySeal(id) :
  query = """
    mutation {
      updateFactSheet(id: "%s", 
                      patches: [{op: add, path: "/qualitySeal", value: "approve"}]) {
        factSheet {
          id
        } 
      }
    }
  """ % (id)
  response = call(query)
 print (response)

#Read from a CSV file called Book1.csv in the same directory as the script with just one column set as ID and the IDs of the Factsheets below it.

df = pd.read_csv('Book1.csv',sep=';')
for index, row in df.iterrows():
  setQualitySeal(row['id'])