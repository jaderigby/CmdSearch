import messages as msg
import helpers, re, ast, json

settings = helpers.get_settings()

def execute(ARGS):
	argDict = helpers.arguments(ARGS)

	class bcolors:
		HEADER = '\033[95m'
		OKBLUE = '\033[94m'
		OKCYAN = '\033[96m'
		OKGREEN = '\033[92m'
		WARNING = '\033[93m'
		FAIL = '\033[91m'
		ENDC = '\033[0m'
		BOLD = '\033[1m'
		UNDERLINE = '\033[4m'

	def key_set(DICT, KEY, DEFAULT):
		if KEY in DICT:
			return DICT[KEY]
		else:
			return DEFAULT

	#=========
	# patterns
	#=========

	# uses the GitHub flavor of acceptable markdown extensions
	kindObj = {}
	kindObj['doc'] = "\.(doc|docx|pdf|md|mkd|mkdn|mdown|markdown|rtf|txt)$"
	kindObj['md'] = "\.(md|mkd|mkdn|mdown|markdown)$"
	kindObj['image'] = "\.(jpeg|jpg|jpe|jif|jfif|jfi|png|gif|webp|tiff|tif|psd|raw|arw|cr2|nrw|k25|bmp|dib|heif|heic|ind|indd|indt|jp2|j2k|jpf|jpx|jpm|mj2)$"
	kindObj['svg'] = "\.(svg|svgz|eps|pdf|ai)$"
	kindObj['pdf'] = "\.(pdf)$"
	# audio = 
	kindObj['movie'] = "\.(webm|mpg|mp2|mpeg|mpe|mpv|ogg|mp4|m4p|m4v|avi|wmv|mov|qt|flv|swf|avchd)$"
	for item in settings['kind']:
		item = ast.literal_eval(json.dumps(item))
		kindObj[item['name']] = item['pattern']

	extensionRegex = key_set(argDict, 'kind', False)


	name = key_set(argDict, 'name', False)
	contains = key_set(argDict, 'contains', False)
	hidden = key_set(argDict, 'hidden', '')
	h = key_set(argDict, 'h', '')
	extType = key_set(argDict, 'type', False)
	dir = key_set(argDict, 'dir', False)
	
	cmdList = []

	termList = []
	optionList = []
	suffixList = []

	if not contains:
		if not extensionRegex and name:
			termList.append('-g')
			termList.append(name)
		
		elif not name and extensionRegex:
			termList.append('-g')
			sugarized = kindObj[extensionRegex]
			termList.append(sugarized)
		
		elif name and extensionRegex:
			termList.append('-g')
			sugarized = '{}.*{}'.format(name, kindObj[extensionRegex])
			# termList.append(name)
			termList.append(sugarized)
	
	elif contains:
		if not name and not extensionRegex and contains:
			termList.append(contains)
		elif not extensionRegex and name and contains:
			termList.append('-G')
			termList.append(name)
			termList.append(contains)
		elif not name and extensionRegex and contains:
			termList.append('-G')
			sugarized = kindObj[extensionRegex]
			termList.append(sugarized)
			termList.append(contains)

		elif name and extensionRegex and contains:
			termList.append('-G')
			sugarized = '{}.*{}'.format(name, kindObj[extensionRegex])
			termList.append(sugarized)
			termList.append(contains)
	
	optionList.append('-o')

	if hidden == 'true' or h == 'true':
		optionList.append('--hidden')

	# if extType:
	# 	addType = "--" + extType
	# 	optionList.append(addType)
	
	if hidden:
		optionList.append('--hidden')

	if dir == '~/':
		dir = dir.replace('~/', helpers.root())
	elif dir == '~':
		dir = dir.replace('~', helpers.root())
	elif not dir:
		dir = helpers.run_command_output('pwd', False)[:-1] + '/'
	dir = re.sub('~/', helpers.root(), dir)
	suffixList.append(dir)

		# if dir == '~/':
	# 	dir = dir.replace('~/', helpers.root())
	# elif not dir:
	# 	dir = helpers.run_command_output('pwd', False)[:-1] + '/'
	# cmdList.append(dir)
	
	#=======================
	# Build the command list
	#=======================

	cmdList.append('ag')

	for term in termList:
		cmdList.append(term)

	for opt in optionList:
		cmdList.append(opt)
	
	if len(suffixList) > 0:
		for item in suffixList:
			cmdList.append(item)

	

	# print("is list: ")
	# print(cmdList)
	# print("")
	results = helpers.run_command_output_search(cmdList)
	# print(results)

	pat = re.compile("ERR")
	for item in results.splitlines():
		match = re.search(pat, item)
		if not match:
			print(bcolors.OKGREEN + (item) + bcolors.ENDC)

	if results == '':
		msg.no_results()
	msg.done()
