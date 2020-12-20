import messages as msg
import helpers, re

# settings = helpers.get_settings()

def execute():
	msg.types()
	listOut = helpers.user_input("Full List: [y/n] ")
	results = helpers.run_command_output('ag --list-file-types', False)

	if listOut == 'y':
		pat = re.compile("--.+\n")
		matches = re.findall(pat, results)
		for item in matches:
			print('- {}'.format(item.replace('--', '')[:-1]))
	elif listOut == 'n':
		return