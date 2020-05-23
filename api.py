import requests

import socket

CLIENT_ID  = "YOUR UID"
CLIENT_SECRET = "YOUR SECRET" 


response = requests.post('https://api.intra.42.fr/oauth/token',[('grant_type','client_credentials'),
					('client_id', CLIENT_ID),
					('client_secret',CLIENT_SECRET)])
if response.ok :
    token = response.json()['access_token']
    print('Token:', token)
else :
	print("token error")
	exit(1)

url = 'https://api.intra.42.fr/v2/cursus/1/cursus_users?'
param_second_generation = {
        'range[begin_at]' : '2019-03-20T00:00:00.000Z,2019-03-30T00:00:00.000Z',
        'page[number]' : '0',
        'page[size]' : '100',
        'filter[campus_id]' : '16'
        }
param_first_generation = {
        'range[begin_at]' : '2018-10-02T00:00:00.000Z,2018-10-15T00:00:00.000Z',
        'page[number]' : '0',
        'page[size]' : '100',
        'filter[campus_id]' : '16'
        }
header = {
        'Authorization': 'Bearer {0}'.format(token)
        }

users = []
size = 100
while size == 100:
    res = requests.get(url, params=param_second_generation, headers=header)
    param_second_generation['page[number]'] = str(int(param_second_generation['page[number]']) + 1)
    if res.ok:
        size = len(res.json())
        for n in res.json():
            user = {'id': n['user']['id'], 'login' : n['user']['login'], 'level' : n['level']}
            if user not in users:
                users.append(user)
    else:
        print('error')

i = 0
levels = 0
last = None
rank = 0
for n in sorted(users, key=lambda k: k['level'], reverse=True):
    if float(n['level']) >= 1:
        if last != n['level']:
            rank += i + 1
            i = 0
        else:
            i += 1
        last = n['level']
        print('{:<6} {:<4} {:<10} {:<0.2f}'.format(n['id'], rank, n['login'], float(n['level'])))
        levels += float(n['level'])
print('Users: {} Total: {:.2f} Average: {:.2f}'.format(rank + i, levels, levels / (rank + i)))
