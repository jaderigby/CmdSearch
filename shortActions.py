import sys, Run
import messages as msg

args = sys.argv[1:]

if len(args) == 0:
    msg.preamble()
    msg.statusMessage()

else:
    Run.execute(args)