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
	kindList = ['doc', 'md', 'image', 'svg', 'pdf', 'audio', 'video', 'script']
	for item in ADD_LIST:
		kindList.append(item)
	kindString = ''
	for item in kindList:
		kindString += item + ' | '
	kindStringFormatted = '[ {} ]'.format(kindString[:-3])
	print'''
## kind ##

Allows you to search by kind/category of file:

{}
'''.format(kindStringFormatted)

def kindx():
	print(r'''
## kindx ##

Allows you to search by a regex pattern, like:

kindx:'\.(ts|js)$'
''')

def kindz():
	print('''
## kindz ##

Allows you to search a list of file extensions seperated by commas (no spaces), such as: 

kindz:css,html,js

Additionally, you can use the form: 

kindz:'css|html|js'

If you use pipes as seperators, instead of commas, be sure to ecapsulate the entire value in quotes, as seen above.
''')

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
- log \t\tcreate a log from your search results.  Full path required.
''')

def types():
	print'''
Search by a configured set of file types. For example:

[ css | html | js | tsx ]

'''

def log():
	print('''
## log ##

Creates a log file from your search results.
if no file path is given, it defaults to the current directory.

Alternatively, you can use the shorthand of 'log:t' or 
'log:true', and it will create a markdown log file for you, 
in the current directory. In the short form, you can also specify json format, like so:

srch - kind:doc log:json

Example with name only: 
srch - kind:doc log:logfile.txt

Example using file path:
srch - kind:doc log:~/Documents/bacon-bits/demoSearch/log.txt

Example using shorthand:
srch - kind:doc log:t

* The shorthand version will result in a markdown file called 'log.md'
''')

def example():
	print('''
process working!
''')