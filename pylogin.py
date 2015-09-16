#!/usr/local/bin/python2.7
#
# pylogin - a python version of rancid's clogin with a few added options.
#
#
# This script uses the paramiko expect library 
# https://github.com/fgimian/paramiko-expect
#
import getpass
import traceback
import paramiko
from paramikoe import SSHClientInteraction
import argparse

def main():
    # Setup a command parset to handle user input
    parser = argparse.ArgumentParser(description="pylogin a python script "
                                     "with expect prompt handling and "
                                     "behavior similar to rancid\'s clogin")
    parser.add_argument("-c", dest="command", type=str, help="Command to "
                        "be run on each router list on the command-line."
                        " Multiple commands maybe listed by separating "
                        "them with semi-colons (;)")
    parser.add_argument("-p", dest="password", type=str, help="Password to be "
                        "used for the device. The script will prompt if not "
                        "given one.")
    parser.add_argument("-prompt", dest="prompt", type=str, default=".*(>|#)", 
                        help="Prompt that pylogin should expect for a new "
                        "line, defaults to Cisco IOS like.")
    parser.add_argument("-pagerprompt", dest="pagerprompt", type=str, 
                        default=".*--More-- ", help="Prompt given by pager if "
                        "enabled, defaults to Cisco IOS like.")
    parser.add_argument("-enablepassprompt", dest="enablepassprompt", type=str,
                        default="password: ", help="Password prompt given by "
                        " the device when the enable command is sent. The "
                        "default is cisco ios compatible.") 
    parser.add_argument("-enablepass", dest="enablepass", type=str,
                        help="Enable password, defaults to the same as "
                        "password.")
    parser.add_argument("-t", dest="timeout", type=int, default=10, 
                        help="Time pylogin should allow to connect to the "
                        "device.")
    parser.add_argument("-u", dest="username", type=str, 
                        default=getpass.getuser() , help="Username to be "
                        "used for the device, defaults to current user.")
    parser.add_argument("-x", dest="commandFile", type=str, help="Specifies"
                        " a file with commands to run on each device. They" 
                        "must not expect additional input.  This option " 
                        "overrides -c")
    parser.add_argument("-r", dest="routerFile", type=str, help="Specifies a"
                        " file with a list of routers to apply the commands "
                        "against.  This option overrides the router argument.")
    parser.add_argument("router", metavar="router", type=str, 
                        nargs=argparse.REMAINDER, help="One or my routers to "
                        "connect to.") 
    args = parser.parse_args()
    # Prompt for pass if one wasn't given.
    if not args.password:
        password = getpass.getpass()
    else:
        password = args.password
    # Check to see if we were given an enable pass and if so set the enable
    # password, if none specified default to same as password.
    if args.enablepass:
        enablePassword = args.enablepass
    else:
        enablePassword = password
    if args.routerFile:
        routerFileObj = open(args.routerFile)
        routerList = routerFileObj.read().splitlines()
        routerFileObj.close()
    else:
        routerList = args.router
    # Counter to determine which router we are working with.
    routerId = 0

    # Build the prompt list
    expectPrompt = [args.prompt, args.pagerprompt, args.enablepassprompt] 

    # Use SSH client to login
    try:
        # Lets figure out what commands to Run
        if args.commandFile:
            # Commands were in a file specified with -x, open the file and read
            # all the lines.
            commandFileObj = open(args.commandFile) 
            commandsToRun = commandFileObj.read().splitlines()
            commandFileObj.close()
        else:
            # Commands specified with -c option separated by ';'
            commandsToRun = args.command.split(";")
        while routerId < len(routerList): 

            # Create a new SSH client object
            client = paramiko.SSHClient()

            # Set SSH key parameters to auto accept unknown hosts
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the host.
            client.connect(hostname=routerList[routerId], 
                           username=args.username, password=password)

            # Create a client interaction class which will interact with 
            # the host.
            interact = SSHClientInteraction(client, timeout=args.timeout, 
                                            display=True)
            # Counter to track which command we are running.
            commandId = 0
	    while commandId <= len(commandsToRun): 
                # Watch the ssh session until we need to do something
                interact.expect(expectPrompt)
                if interact.last_match == args.prompt:
                    #Our last command sent was successful, or we have our first
                    # prompt now we check to see if we need to run another.
                    if commandId < len(commandsToRun):
                        # We need to send a command
                        interact.send(commandsToRun[commandId])
                    # Advance the command counter
                    commandId +=1
                elif interact.last_match == args.pagerprompt:
                    # We received a pager prompt and need to handle it
                    interact.send(" ")
                elif interact.last_match == args.enablepassprompt:
                    # Then enable command was sent and we need to send a 
                    # password.
                    interact.send(enablePassword)
            # Send the exit command and expect EOF (a closed session)
            # This may need to be changed to support more devices
            interact.send('exit')
            interact.expect()
            # Advance to next router
            routerId +=1

    except Exception:
       traceback.print_exc()
    finally:
        try:
            client.close()
        except:
            pass

if __name__ == '__main__':
	main()
