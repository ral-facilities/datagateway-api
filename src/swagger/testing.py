import requests

AUTHORIZATION_HEADER = {"Authorization": "Bearer 25fa63a6-85d2-11e9-8530-dcbd99df7bb4"}

print(requests.get("http://localhost:5000/datafiles/1",headers=AUTHORIZATION_HEADER).json())