import requests


BASE = "http://127.0.0.1:5000/"

data = {"first_name": "new", "last_name": "NEWE", "phone_number": "33333"}

res = requests.put(BASE + 'api/101', data)
print(res.json())
