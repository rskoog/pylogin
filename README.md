# pylogin
A Python utility similar to RANCID's clogin.

I recently ran into an issue where I needed to push changes to a lot of devices that didn't have a prompt any 
existing utility would recognize.  After finding the [paramiko-expect](https://github.com/fgimian/paramiko-expect) library by fgimian, I decided to make a utility similar to clogin, but that would easily allow the user to specify different prompts to match.  It does require a python version of at least 2.7 due to the argparse requirement.

### Install 
You will first need to verify that you have python version 2.7 installed. RHEL 6 for example still uses Python 2.6 and needs to remain that way.  If you don't have version 2.7 you will need to do a local install.
```
[skoog@bounty pylogin]$ python -V
Python 2.6.6
[skoog@bounty pylogin]$ python2.7 -V
Python 2.7.10
[skoog@bounty pylogin]$ which python
/usr/bin/python
[skoog@bounty pylogin]$ which python2.7
/usr/local/bin/python2.7
```
Next you need to install the libary dependency for the install of python being used and dowload the script.
```
python2.7 -m pip install git+https://github.com/fgimian/paramiko-expect.git
wget https://github.com/rskoog/pylogin/blob/master/pylogin.py
./pylogin.py --help
```

### Usage
```
[skoog@bounty pylogin]$ ./pylogin.py --help
usage: pylogin.py [-h] [-c COMMAND] [-p PASSWORD] [-prompt PROMPT]
                  [-pagerprompt PAGERPROMPT]
                  [-enablepassprompt ENABLEPASSPROMPT]
                  [-enablepass ENABLEPASS] [-t TIMEOUT] [-u USERNAME]
                  [-x COMMANDFILE]
                  router [router ...]

pylogin a python script with expect prompt handling and behavior similar to
rancid's clogin

positional arguments:
  router                One or my routers to connect to.

optional arguments:
  -h, --help            show this help message and exit
  -c COMMAND            Command to be run on each router list on the command-
                        line. Multiple commands maybe listed by separating
                        them with semi-colons (;)
  -p PASSWORD           Password to be used for the device. The script will
                        prompt if not given one.
  -prompt PROMPT        Prompt that pylogin should expect for a new line,
                        defaults to Cisco IOS like.
  -pagerprompt PAGERPROMPT
                        Prompt given by pager if enabled, defaults to Cisco
                        IOS like.
  -enablepassprompt ENABLEPASSPROMPT
                        Password prompt given by the device when the enable
                        command is sent. The default is cisco ios compatible.
  -enablepass ENABLEPASS
                        Enable password, defaults to the same as password.
  -t TIMEOUT            Time pylogin should allow to connect to the device.
  -u USERNAME           Username to be used for the device, defaults to
                        current user.
  -x COMMANDFILE        Specifies a file with commands to run on each device.
                        Theymust not expect additional input. This option
                        overrides -c
```

#### Example Usage with a Sentry Commander PDU device:

```
[skoog@bounty pylogin]$ ./pylogin.py -c 'show syslog' -prompt 'Switched CDU: ' 
Password:


Sentry Switched CDU Version 6.1e

Location: Your-House

Switched CDU: show syslog

   SYSLOG Configuration

      Primary Host:    1.1.1.1
      Secondary Host:
      Port:            514

   Command successful

Switched CDU: exit

Session ended
```

#### Cisco Router.
```
[skoog@bounty pylogin]$ ./pylogin.py -c 'enable;show version' rtr
Password:


*Mybanner*


rtr>enable
password:
rtr#show version
Cisco IOS Software, 2800 Software (C2800NM-ADVSECURITYK9-M), Version 12.4(24)T2, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2009 by Cisco Systems, Inc.
Compiled Mon 19-Oct-09 17:38 by prod_rel_team

ROM: System Bootstrap, Version 12.4(13r)T, RELEASE SOFTWARE (fc1)

rtr uptime is 12 weeks, 2 hours, 26 minutes
System returned to ROM by power-on
System restarted at 09:29:31 EDT Tue Jun 23 2015
System image file is "flash:c2800nm-advsecurityk9-mz.124-24.T2.bin"


This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

Cisco 2811 (revision 53.51) with 247808K/14336K bytes of memory.
Processor board ID XXXXXXXXXXX
2 FastEthernet interfaces
1 Serial interface
1 Virtual Private Network (VPN) Module
DRAM configuration is 64 bits wide with parity enabled.
239K bytes of non-volatile configuration memory.
62720K bytes of ATA CompactFlash (Read/Write)

Configuration register is 0x2102

rtr#
rtr#exit
```
