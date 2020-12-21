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
			if DICT[KEY] == 'true':
				DICT[KEY] = 't'
			return DICT[KEY]
		else:
			return DEFAULT

	#=========
	# patterns
	#=========

	fileOnlyPat = '''\/?[\w.&!@#$%^&*()+{{}}[\]:;|<>,?\-`~'" ]*'''
	hiddenFileOnlyPat = '''\/?\.[\w.&!@#$%^&*()+{{}}[\]:;|<>,?\-`~'"]*'''
	hiddenFileSuffixPat = '''[\w.&!@#$%^&*()+{{}}[\]:;|<>,?\-`~'"]*'''

	# uses the GitHub flavor of acceptable markdown extensions
	kindObj = {}
	kindObj['doc'] = "\.(doc|docx|pdf|md|mkd|mkdn|mdown|markdown|rtf|txt)$"
	kindObj['md'] = "\.(md|mkd|mkdn|mdown|markdown)$"
	kindObj['image'] = "\.(jpeg|jpg|jpe|jif|jfif|jfi|png|gif|webp|tiff|tif|psd|raw|arw|cr2|nrw|k25|bmp|dib|heif|heic|ind|indd|indt|jp2|j2k|jpf|jpx|jpm|mj2)$"
	kindObj['svg'] = "\.(svg|svgz|eps|ai)$"
	kindObj['pdf'] = "\.(pdf)$"
	kindObj['audio'] = "\.(pcm|wav|aiff|mp3|aac|ogg|wma|flac|alac|mpa|aif|m4a|mid|mogg|sdt|flp|aimppl|4mp|mui|l|toc|bun|nbs|sf2|sfk|dm|m4r|ovw|vyf)$"
	kindObj['video'] = "\.(webm|mpg|mp2|mpeg|mpe|mpv|ogg|mp4|m4p|m4v|avi|wmv|mov|qt|flv|swf|avchd)$"
	kindObj['script'] = "\.(js|tsx|ts|py|json)$"
	kindObj['kindx'] = ''
	kindObj['kindz'] = ''
	for item in settings['kind']:
		item = ast.literal_eval(json.dumps(item))
		kindObj[item['name']] = item['pattern']

	extensionRegex = key_set(argDict, 'kind', False)
	extensionPattern = key_set(argDict, 'kindx', False)
	extensionList = key_set(argDict, 'kindz', False)

	if extensionPattern:
		kindObj['kindx'] = extensionPattern
		extensionRegex = 'kindx'
	
	if extensionList:
		extensionList = extensionList.replace(',', '|')
		kindzPattern = r'\.({})$'.format(extensionList)
		kindObj['kindz'] = kindzPattern
		extensionRegex = 'kindz'

	extType = key_set(argDict, 'type', False)
	name = key_set(argDict, 'name', False)
	contains = key_set(argDict, 'contains', False)
	hidden = key_set(argDict, 'hidden', '')
	h = key_set(argDict, 'h', '')
	only = key_set(argDict, 'only', False)
	dir = key_set(argDict, 'dir', False)
	log = key_set(argDict, 'log', False)
	
	cmdList = []

	termList = []
	optionList = []
	suffixList = []

	if not contains:
		if not extensionRegex and name:
			termList.append('-g')
			# sugarized = '''{}.*\.{{1,15}}'''.format(name)
			sugarized = '''(({FILE_ONLY_PAT}{NAME}{FILE_ONLY_PAT}\..{{1,15}})|({HIDDEN_FILE_ONLY_PAT}{NAME}{HIDDEN_FILE_SUFFIX_PAT}))'''.format(FILE_ONLY_PAT= fileOnlyPat, NAME= name, HIDDEN_FILE_ONLY_PAT= hiddenFileOnlyPat, HIDDEN_FILE_SUFFIX_PAT= hiddenFileSuffixPat)
			termList.append(sugarized)
		
		elif not name and extensionRegex:
			termList.append('-g')
			sugarized = kindObj[extensionRegex]
			termList.append(sugarized)
		
		elif name and extensionRegex:
			termList.append('-g')
			# sugarized = '''{}.*{}'''.format(name, kindObj[extensionRegex])
			# sugarized = '''\/?[\w.&!@#$%^&*()+{{}}[\]:;|<>,?\-`~'"]*{}[\w.&!@#$%^&*()+{{}}[\]:;|<>,?\-`~'"]*{}'''.format(name, kindObj[extensionRegex])
			sugarized = '''(({FILE_ONLY_PAT}{NAME}{FILE_ONLY_PAT}{KIND})|({HIDDEN_FILE_ONLY_PAT}{NAME}{HIDDEN_FILE_SUFFIX_PAT}))'''.format(FILE_ONLY_PAT= fileOnlyPat, NAME= name, KIND= kindObj[extensionRegex], HIDDEN_FILE_ONLY_PAT= hiddenFileOnlyPat, HIDDEN_FILE_SUFFIX_PAT= hiddenFileSuffixPat)
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
			# sugarized = '''{}.*{}'''.format(name, kindObj[extensionRegex])
			# sugarized = '''\/?[\w.&!@#$%^&*()+{{}}[\]:\"';|<>,?\-`~]*{}[\w.&!@#$%^&*()+{{}}[\]:\"';|<>,?\-`~]*{}'''.format(name, kindObj[extensionRegex])
			sugarized = '''(({FILE_ONLY_PAT}{NAME}{FILE_ONLY_PAT}{KIND})|({HIDDEN_FILE_ONLY_PAT}{NAME}{HIDDEN_FILE_SUFFIX_PAT}))'''.format(FILE_ONLY_PAT= fileOnlyPat, NAME= name, KIND= kindObj[extensionRegex], HIDDEN_FILE_ONLY_PAT= hiddenFileOnlyPat, HIDDEN_FILE_SUFFIX_PAT= hiddenFileSuffixPat)
			termList.append(sugarized)
			termList.append(contains)
	
	optionList.append('-o')

	if hidden == 't' or h == 't':
		optionList.append('--hidden')

	if extType:
		addType = "--" + extType
	
	if hidden:
		optionList.append('--hidden')
	
	if only == 't':
		optionList.append('-l')
	
	if log:
		optionList.append('--ignore-dir')
		optionList.append('cmdsearch-logs')

	if dir == '~/':
		dir = dir.replace('~/', helpers.root())
	elif dir == '~':
		dir = dir.replace('~', helpers.root())
	elif not dir:
		dir = helpers.run_command_output('pwd', False)[:-1] + '/'
	dir = re.sub('~/', helpers.root(), dir)
	suffixList.append(dir)
	
	#=======================
	# Build the command list
	#=======================

	cmdList.append('ag')

	if extType:
		cmdList.append(addType)

	for term in termList:
		cmdList.append(term)

	for opt in optionList:
		cmdList.append(opt)
	
	if len(suffixList) > 0:
		for item in suffixList:
			cmdList.append(item)

	results = helpers.run_command_output_search(cmdList)

	pat = re.compile("ERR")
	for item in results.splitlines():
		match = re.search(pat, item)
		if not match:
			print(bcolors.OKGREEN + (item) + bcolors.ENDC)

	if results == '':
		msg.no_results()
	
	if log:
		from datetime import date, datetime
		
		currDate = date.today()
		currTime = datetime.now()
		searchQuery = helpers.format_search_query()
		logPath = helpers.run_command_output('pwd', False)
		logFile = ''
		logFormat = 'txt'
		searchData = ''
		if log == 'true' or log == 't' or log == 'json' or log == 'md':
			logFormat = 'md'
			logFile = 'log.md'
			logRoot = helpers.run_command_output('pwd', False).replace('\n', '') + '/cmdsearch-logs'
			helpers.run_command('mkdir -p {}'.format(logRoot), False)
			if log == 'json':
				logFormat = 'json'
				logFile = 'log.json'
			logPath = logRoot + '/' + logFile
		else:
			logFile = log.split('/')[-1]
			logRoot = log.replace(logFile, '')
			logRoot = logRoot.replace('cmdsearch-logs/', '')[:-1]
			helpers.run_command('cd {} && mkdir -p {}'.format(logRoot, 'cmdsearch-logs'), False)
			logPath = logRoot + 'cmdsearch-logs/' + logFile
		if results:
			if logFormat == 'md':
				searchData = '__Date:__ {}\n'.format(currDate)
				searchData += '__Time:__ {}\n'.format(currTime.strftime("%H:%M:%S"))
				searchData += '__Search:__ `{}`\n\n'.format(searchQuery)
				for item in results.splitlines():
					searchData += '\n* `{}`'.format(item)
			elif logFormat == 'json':
				newObj = {}
				newObj['date'] = '{}'.format(currDate)
				newObj['time'] = '{}'.format(currTime.strftime("%H:%M:%S"))
				newObj['search'] = searchQuery.replace('\n', '')
				newObj['searchResults'] = []
				for item in results.splitlines():
					newObj['searchResults'].append(item)
				searchData = json.dumps(newObj, indent=4)
			else:
				 searchData = results

			logPathFormatted = logPath.replace('\n', '')
			print((bcolors.OKCYAN + '''
LOG: {}
''' + bcolors.ENDC).format(logPathFormatted))
			helpers.write_file(logPathFormatted, searchData)

	msg.done()
