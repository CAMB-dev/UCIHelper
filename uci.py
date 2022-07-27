import json
import requests
import os
#Disable SSL Warning
import urllib3
urllib3.disable_warnings()
from prettytable import PrettyTable
x = PrettyTable()
x.field_names = ['Name','Area','Task','Types','DateDonated']

print('''
	UCI Datasets Helper.
	This may the last thing I leave. Goodbye.
	Please wait while initializing data
	''')
datas = None
if os.path.exists('cache.json'):
	print('Existing cache file detected.')
	while True:
		comm = input('Would you want to download new list ? (y/n): ')
		if comm == 'y' or comm == 'yes':
			datas = json.loads(requests.get('https://archive-beta.ics.uci.edu/api/datasets-donated/find?limit=999',verify=False).text)
			print('Dataset list download successfully.')
			break
		elif comm == 'n' or comm == 'no':
			f = open('cache.json','r')
			datas = json.loads(f.read())
			f.close()
			break;
		else:
			print('Invalid choice !')
else:
	datas = json.loads(requests.get('https://archive-beta.ics.uci.edu/api/datasets-donated/find?limit=999',verify=False).text)
	print('Dataset list download successfully.')

if datas['error'] == False and datas['statusCode'] == 200:
	print('Dataset list parse successfully.')
	while True:
		comm = input('command: ')
		if comm == 'listall':
			print('Total: {0}'.format(str(datas['payload']['count'])))
			for item in datas['payload']['rows']:
				x.add_row([item['Name'][:100],item['Area'],str(item['Task'])[:60],item['Types'],item['DateDonated']])
			print(x)
			x.clear_rows()
		if comm == 'cache':
			f = open('cache.json','w')
			f.write(json.dumps(datas))
			f.close()
			print('Done.')
		if comm == 'listallc':
			f = open('cache.json','r')
			datas = json.loads(f.read())
			print('Total: {0}'.format(str(datas['payload']['count'])))
			for item in datas['payload']['rows']:
				x.add_row([item['Name'][:100],item['Area'],str(item['Task'])[:60],item['Types'],item['DateDonated']])
			print(x)
			x.clear_rows()
		if comm[:6] == 'search':
			keyword = comm[6:]
			index = 6
			for i in keyword:
				if i != ' ':
					break
				else:
					index += 1
			keyword = comm[index:]
			results = []
			for item in datas['payload']['rows']:
				if keyword.lower() in item['Name'].lower():
					results.append(item['Name'])
			print('Search: {0} results'.format(str(len(results))))
			for item in results:
				print(item)
		if comm[:6] == 'getres':
			keyword = comm[6:]
			index = 6
			for i in keyword:
				if i != ' ':
					break
				else:
					index += 1
			keyword = comm[index:]
			results = []
			for item in datas['payload']['rows']:
				if item['Name'] == keyword:
					results.append(item)
			print('There are {0} results list below:'.format(str(len(results))))
			for item in results:
				print('Name: {0}'.format(item['Name']))
				print('Abstract: {0}'.format(item['Abstract']))
				print('DownloadURL: {0}'.format('https://archive.ics.uci.edu/ml/{0}'.format(item['URLFolder'].replace('../',''))))
				print('Area: {0}'.format(item['Area']))
				print('Task: {0}'.format(item['Task']))
				print('Types: {0}'.format(item['Types']))
				print('DateDonated: {0}'.format(item['DateDonated']))
				print('User: {0}'.format(item['user']['user']))
				print('AuthorName: {0} {1}'.format(item['user']['firstName'],item['user']['lastName']))
		if comm == 'exit':
			print('bye')
			exit(0)
else:
	print('Failed to download dataset list, please try again later.')