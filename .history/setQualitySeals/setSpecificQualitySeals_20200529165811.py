import json 
import requests 
import pandas as pd

api_token = 'INSERT_YOUR_API_TOKEN_HERE'
#auth url depends on where your LeanIX region is, US-SVC, EU-SVC, CA-SVC etc.
auth_url = 'https://us-svc.leanix.net/services/mtm/v1/oauth2/token' 
#request url depends on what is the instance of your leanix workspace 'us.leanix.net', or if you have SSO then your custom instance 
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

#Reads from a CSV file called Book1.csv in the same directory as the script with just one column set as ID and the IDs of the Factsheets below it.

df = pd.read_csv('Book1.csv',sep=';')
for index, row in df.iterrows():
  setQualitySeal(row['id'])