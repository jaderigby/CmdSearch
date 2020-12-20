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

def kinds(ADD_LIST=[]):
	kindList = ['doc', 'md', 'image', 'svg', 'pdf', 'movie']
	for item in ADD_LIST:
		kindList.append(item)
	kindString = ''
	for item in kindList:
		kindString += item + ' | '
	kindStringFormatted = '[ {} ]'.format(kindString[:-3])
	print'''
Allows you to search by kind/category of file:

{}
'''.format(kindStringFormatted)

def args():
	print('''
Arguments:

- name \t\tsearch files by name (regex pattern). Use double backslash "\\" as escape character
- contains \tsearch for matching search string inside files
- kind \t\tfilter matches by kind. 
- only \t\tshort for "file only", this removes line matches on "contains"
- hidden \tinclude hidden files
- h \t\tshort version of "hidden"
- dir \t\tspecify directory to search. When argument is absent, search starts at current directory
''')

def types():
	print'''
Search by a configured set of file types. For example:

[ css | html | js | tsx ]

For an exhaustive list, do "srch list-types"
'''

def example():
	print('''
process working!
''')