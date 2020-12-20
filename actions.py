import sys, addAction, helpers
import messages as msg
import Run
import Kind
# new imports start here

# settings = helpers.get_settings()

try:
	action = str(sys.argv[1])
except:
	action = None

args = sys.argv[2:]

if action == None:
	msg.preamble()
	msg.statusMessage()

elif action == '-action':
	addAction.execute(args)

elif action == '-profile':
	helpers.profile()

elif action == "-":
	Run.execute(args)

elif action == "kind":
	Kind.execute()
# new actions start here
