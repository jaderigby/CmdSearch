import messages as msg
import helpers, re

# settings = helpers.get_settings()

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

	dir = key_set(argDict, 'dir', False)
	hidden = key_set(argDict, 'hidden', '')
	h = key_set(argDict, 'h', '')
	name = key_set(argDict, 'name', False)
	pattern = key_set(argDict, 'input', False)
	contains = key_set(argDict, 'contains', False)
	cmdList = []

	cmdList.append('ag')

	if hidden == 'true' or h == 'true':
		cmdList.append('--hidden')

	cmdList.append('-o')
	if name:
		cmdList.append('-g')
		cmdList.append(name)
	elif pattern:
		cmdList.append('-g')
		cmdList.append(pattern)
	elif contains:
		cmdList.append(contains)

	if dir == '~/':
		dir = dir.replace('~/', helpers.root())
	elif not dir:
		dir = helpers.run_command_output('pwd', False)[:-1] + '/'
	cmdList.append(dir)

	results = helpers.run_command_output_search(cmdList)

	pat = re.compile("ERR")
	for item in results.splitlines():
		match = re.search(pat, item)
		if not match:
			print(bcolors.OKGREEN + (item) + bcolors.ENDC)

	if results == '':
		msg.no_results()
	msg.done()
