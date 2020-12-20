import messages as msg
import helpers

settings = helpers.get_settings()

def execute():
	addToList = []
	for item in settings['kind']:
		addToList.append(item['name'])
	msg.kinds(addToList)
