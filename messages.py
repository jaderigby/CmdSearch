import helpers, json

actionList = json.loads(helpers.read_file('{}/{}'.format(helpers.self_path(), 'action-list.json')))

def preamble():
	print('''
Simple wrapper for AG (The Silver Searcher). Because it uses ag, you will need to also install ag.
AG Man Page: https://www.mankier.com/1/ag
''')

def statusMessage():
	if len(actionList['actions']) > 0:
		print("")
		for item in actionList['actions']:
			print('''[ {} {} ]\t\t{}'''.format(actionList['alias'], item['name'], item['description']))
		print("")
	else:
		print('''
Search is working successfully!
''')

def no_results():
	print('''
:: No Results ::
''')

def done():
	print('''
[ Process Completed ]
''')

def example():
	print('''
process working!
''')