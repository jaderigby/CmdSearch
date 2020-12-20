import sys, addAction, helpers
import messages as msg
import Run
import Kind
import Args
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

elif action == "args":
	Args.execute()
# new actions start here
