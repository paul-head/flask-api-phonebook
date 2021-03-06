import requests


BASE = "http://127.0.0.1:5000/"

data_put = {"first_name": "new", "last_name": "NEWE", "phone_number": "33333"}
data_patch = {"first_name": "newPATCHED and again", "last_name": "oh noooooo"}


# res_get = requests.get(BASE + '/api/4')
res_put = requests.put(BASE + 'api/1', data_put)
# res_patch = requests.patch(BASE + 'api/5', data_patch)
# res_del = requests.delete(BASE + 'api/101')

