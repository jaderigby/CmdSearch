import messages as msg
import helpers, re, ast, json

settings = helpers.get_settings()

def execute(ARGS):
	argDict = helpers.arguments(ARGS)

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

	primaryPat = '''[\w,.?!;:'"(){{}}[\]<>`~*@#&$%^| +\-]'''
	fileOnlyPat = '''\/?{}*'''.format(primaryPat)
	hiddenFileOnlyPat = '''\/?\.{}*'''.format(primaryPat)
	hiddenFileSuffixPat = '''{}*'''.format(primaryPat)

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
	if settings:
		if 'kind' in settings:
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
	folder = key_set(argDict, 'dir', False)

	# assign either 'name' or 'file' as name
	name = key_set(argDict, 'name', False)
	if not name:
		name = key_set(argDict, 'file', False)

	contains = key_set(argDict, 'contains', False)
	if 'h' in argDict:
		hidden = key_set(argDict, 'h', False)
	else:
		hidden = key_set(argDict, 'hidden', False)
	only = key_set(argDict, 'only', False)
	dir = key_set(argDict, 'from', False)
	cmdGiven = key_set(argDict, 'cmd', False)
	if not cmdGiven:
		cmdGiven = key_set(argDict, 'c', False)
	log = key_set(argDict, 'log', False)

	# normalize 'true' to short form
	if hidden == 'true':
		hidden = 't'
	if only == 'true':
		only = 't'
	
	cmdList = []

	termList = []
	optionList = []
	suffixList = []

	if folder:
		if not contains and not name:
			termList.append('-g')
			sugarized = """\/?{PATTERN}*{FOLDER}{PATTERN}*\/""".format(PATTERN = primaryPat, FOLDER = folder)
			termList.append(sugarized)
		elif not contains and name:
			termList.append('-g')
			sugarized = """\/?{PATTERN}*{FOLDER}{PATTERN}*\/{FILE_ONLY_PAT}{NAME}{PATTERN}*\..{{1,15}}""".format(PATTERN = primaryPat, FOLDER = folder, FILE_ONLY_PAT= fileOnlyPat, NAME= name)
			termList.append(sugarized)
		elif contains and not name:
			termList.append('-G')
			sugarized = """\/?{PATTERN}*{FOLDER}{PATTERN}*\/""".format(PATTERN = primaryPat, FOLDER = folder)
			termList.append(sugarized)
			termList.append(contains)
		elif contains and name:
			termList.append('-G')
			sugarized = """\/?{PATTERN}*{FOLDER}{PATTERN}*\/{FILE_ONLY_PAT}{NAME}{PATTERN}*\..{{1,15}}""".format(PATTERN = primaryPat, FOLDER = folder, FILE_ONLY_PAT= fileOnlyPat, NAME= name)
			termList.append(sugarized)
			termList.append(contains)
	
	else:
		if not contains and not hidden:
			# print("\n-!contains & !hidden-")
			if not extensionRegex and name:
				termList.append('-g')
				# sugarized = '''{}.*\.{{1,15}}'''.format(name)
				sugarized = """{FILE_ONLY_PAT}{NAME}{PRIMARY_PAT}*\..{{1,15}}""".format(FILE_ONLY_PAT= fileOnlyPat, NAME= name, PRIMARY_PAT= primaryPat)
				termList.append(sugarized)
			elif not name and extensionRegex:
				termList.append('-g')
				sugarized = kindObj[extensionRegex]
				termList.append(sugarized)
			elif name and extensionRegex:
				termList.append('-g')
				# sugarized = '''{}.*{}'''.format(name, kindObj[extensionRegex])
				# sugarized = '''\/?[\w.&!@#$%^&*()+{{}}[\]:;|<>,?\-`~'"]*{}[\w.&!@#$%^&*()+{{}}[\]:;|<>,?\-`~'"]*{}'''.format(name, kindObj[extensionRegex])
				sugarized = """{FILE_ONLY_PAT}{NAME}{PRIMARY_PAT}*{KIND}""".format(FILE_ONLY_PAT= fileOnlyPat, NAME= name, PRIMARY_PAT= primaryPat, KIND= kindObj[extensionRegex])
				termList.append(sugarized)
		
		elif contains and not hidden:
			# print("\n-contains & !hidden-")
			if not name and not extensionRegex and contains:
				termList.append(contains)
			elif not extensionRegex and name and contains:
				termList.append('-G')
				sugarized = """{FILE_ONLY_PAT}{NAME}{PRIMARY_PAT}*\..{{1,15}}""".format(FILE_ONLY_PAT= fileOnlyPat, NAME= name, PRIMARY_PAT= primaryPat)
				termList.append(sugarized)
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
				sugarized = """{FILE_ONLY_PAT}{NAME}{PRIMARY_PAT}*{KIND}""".format(FILE_ONLY_PAT= fileOnlyPat, NAME= name, PRIMARY_PAT= primaryPat, KIND= kindObj[extensionRegex])
				termList.append(sugarized)
				termList.append(contains)

		elif not contains and hidden:
			# print("\n-!contains & hidden-")
			if name and not extensionRegex:
				# print('name & hidden & !kind')
				termList.append('-g')
				# sugarized = '''{}.*\.{{1,15}}'''.format(name)
				sugarized = """\.{FILE_ONLY_PAT}{NAME}{PRIMARY_PAT}*""".format(FILE_ONLY_PAT= fileOnlyPat, NAME= name, PRIMARY_PAT= primaryPat)
				termList.append(sugarized)
			elif not name and extensionRegex:
				termList.append('-g')
				sugarized = kindObj[extensionRegex]
				termList.append(sugarized)
			elif name and extensionRegex:
				# print('name & hidden & kind')
				termList.append('-g')
				# sugarized = '''{}.*{}'''.format(name, kindObj[extensionRegex])
				# sugarized = '''\/?[\w.&!@#$%^&*()+{{}}[\]:;|<>,?\-`~'"]*{}[\w.&!@#$%^&*()+{{}}[\]:;|<>,?\-`~'"]*{}'''.format(name, kindObj[extensionRegex])
				sugarized = """\.{FILE_ONLY_PAT}{NAME}{PRIMARY_PAT}*{KIND}""".format(FILE_ONLY_PAT= fileOnlyPat, NAME= name, PRIMARY_PAT= primaryPat, KIND= kindObj[extensionRegex])
				termList.append(sugarized)

		elif contains and hidden:
			print("\n-contains & hidden-")
			if name:
				termList.append('-G')
				# sugarized = '''{}.*\.{{1,15}}'''.format(name)
				sugarized = """\.{FILE_ONLY_PAT}{NAME}{PRIMARY_PAT}*""".format(FILE_ONLY_PAT= fileOnlyPat, NAME= name, PRIMARY_PAT= primaryPat)
				termList.append(sugarized)
				termList.append(contains)
			elif not name and extensionRegex:
				termList.append('-G')
				sugarized = kindObj[extensionRegex]
				termList.append(sugarized)
				termList.append(contains)
			elif name and extensionRegex:
				termList.append('-G')
				# sugarized = '''{}.*{}'''.format(name, kindObj[extensionRegex])
				# sugarized = '''\/?[\w.&!@#$%^&*()+{{}}[\]:;|<>,?\-`~'"]*{}[\w.&!@#$%^&*()+{{}}[\]:;|<>,?\-`~'"]*{}'''.format(name, kindObj[extensionRegex])
				sugarized = """\.{FILE_ONLY_PAT}{NAME}{PRIMARY_PAT}*{KIND}""".format(FILE_ONLY_PAT= fileOnlyPat, NAME= name, PRIMARY_PAT= primaryPat, KIND= kindObj[extensionRegex])
				termList.append(sugarized)
				termList.append(contains)
	
	optionList.append('-o')

	if hidden == 't':
		optionList.append('--hidden')

	if extType:
		addType = "--" + extType
	
	dirsOnly = False

	if folder and not name and not contains:
		if only == 't':
			dirsOnly = True
		elif cmdGiven:
			dirsOnly = True
	else:
		if only == 't':
			optionList.append('-l')
	
	if log:
		optionList.append('--ignore-dir')
		optionList.append('cmdsearch-logs')

	if dir:
		# capture first character for match later, after normalization below
		firstChar = dir[1:]

		# normalize instances where tilde for user path is used
		dir = dir.replace('~/', helpers.path('user'))
		dir = dir.replace('~', helpers.path('user'))

		backTrackPat = re.compile('../')
		match = re.findall(backTrackPat, dir)
		if not firstChar == '/' and match:
			for item in range(len(match)):
				dir = helpers.run_command_output('cd {} && pwd'.format(dir), False)[:-1] + '/'
	else:
		currentLocation = helpers.run_command_output('pwd', False)[:-1] + '/'
		dir = currentLocation

	suffixList.append(dir)
	
	#=======================
	# Build the command list
	#=======================

	cmdList.append('ag')

	# if extType:
	# 	cmdList.append(addType)

	for term in termList:
		cmdList.append(term)

	for opt in optionList:
		cmdList.append(opt)
	
	if len(suffixList) > 0:
		for item in suffixList:
			cmdList.append(item)

	results = helpers.run_command_output_search(cmdList)

	#===================
	# Output the results
	#===================

	resultsFormatted = []
	resultsFormattedUnique = []
	if dirsOnly:
		pat = re.compile("ERR")
		for item in results.splitlines():
			match = re.search(pat, item)
			item = re.sub(fileOnlyPat + '$', '', item)
			if not match:
				resultsFormatted.append(item)
		
		resultsFormattedUnique = list(set(resultsFormatted))
		
		for item in resultsFormattedUnique:
			print(helpers.decorate('green', item))

		if len(resultsFormatted) == 0:
			msg.no_results()

	else:
		pat = re.compile("ERR")
		for item in results.splitlines():
			match = re.search(pat, item)
			if not match:
				print(helpers.decorate('green', item))

		if results == '':
			msg.no_results()
	
	if dirsOnly:
		if cmdGiven:
			if len(resultsFormattedUnique) == 1:
				helpers.run_command('{} {}'.format(cmdGiven, resultsFormattedUnique[0]))
			elif len(resultsFormattedUnique) > 0:
				selection = helpers.user_selection("Selection: ", resultsFormattedUnique)
				if selection != 'exit':
					helpers.run_command('{} {}'.format(cmdGiven, resultsFormattedUnique[selection - 1]))

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
			logPat = re.compile('(.*\.)(md|json)')
			match = re.search(logPat, log)
			if match:
				logFormat = match.group(2)
			logFile = log
			logRoot = helpers.run_command_output('pwd', False).replace('\n', '') + '/cmdsearch-logs'
			helpers.run_command('mkdir -p {}'.format(logRoot), False)
			logPath = logRoot + '/' + logFile
		if results:
			if logFormat == 'md':
				searchData = '__Date:__ {}\n'.format(currDate)
				searchData += '__Time:__ {}\n'.format(currTime.strftime("%H:%M:%S"))
				searchData += '__Search:__ `{}`\n\n'.format(searchQuery)
				for item in results.splitlines():
					match = re.search(pat, item)
					if not match:
						searchData += '\n* `{}`'.format(item)
			elif logFormat == 'json':
				newObj = {}
				newObj['date'] = '{}'.format(currDate)
				newObj['time'] = '{}'.format(currTime.strftime("%H:%M:%S"))
				newObj['search'] = searchQuery.replace('\n', '')
				newObj['searchResults'] = []
				for item in results.splitlines():
					match = re.search(pat, item)
					if not match:
						newObj['searchResults'].append(item)
				searchData = json.dumps(newObj, indent=4)
			else:
				searchData = results

			logPathFormatted = logPath.replace('\n', '')
			print(helpers.decorate('cyan', '''
LOG: {}
'''.format(logPathFormatted)))
			helpers.write_file(logPathFormatted, searchData)

	msg.done()