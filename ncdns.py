#!/usr/bin/env python3

usage= 'Usage: updateNCIP <domain> <password> <subdomain- More than one can be defined> [-a | --ip <specifiedip>] [--help to bring up this message]'

# Import argv and getopt to handle arguments. 
from sys import argv, exit
from getopt import gnu_getopt, GetoptError
# Imports url handler for obtaining ip.
from urllib.request import urlopen
from urllib.error import URLError
# To parse webpage.
from html.parser import HTMLParser
# Regex to check for validity of ip.
import re

#Notice the below regex has 4 groups at ipRegex.fullmatch.group() between 1 and 4, inclusive.
ipRegex = re.compile(r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})')

#Extend HTMLParser with NCParser. 
class NCParser(HTMLParser):
	# We don't define handle_endtag because we don't use it. 	

	def __init__(self):
		HTMLParser.__init__(self)
		self.text = ''

	def __str__(self):
		return self.text

	def handle_starttag(self, tag, attrs):
		if 		tag == 'response' \
				or tag=='responses' \
				or tag == 'debug': return
		
		self.text += tag + ': '

	def handle_data(self, data):
		self.text += data + '\n'

	def handle_comment(self, data):
		self.text += 'Comment: ' + data + '\n'

# We use a skeleton template to build our url.
# Template: 
# https://dynamicdns.park-your-domain.com/update?host=[host]&domain=[domain_name]&password=[ddns_password]&ip=[your_ip]
def getURL(domain, password, ip, host):
	return \
			r'https://dynamicdns.park-your-domain.com/update?host=' + host \
			+ r'&domain=' + domain \
			+ r'&password=' + password \
			+ r'&ip=' + ip

def validIP(ip):
	match = ipRegex.fullmatch(ip)
	# Following line short circuits to stop errors. 
	if match is None \
		or [i for i in range(1,5) if int(match.group(i)) >= 256] != []:
		
		return False
	
	return True

def main():

	########################################################################
	# Validation
	########################################################################

	# The ip defaults to public ip by the browser link.
	# The ip is assumed public unless an option changes it. 
	ip = ''

	# gnu_getopt returns a tuple of 2 lists,
	# where the first is a list of tuples for options,
	# and the other is a list of arguments.  
	try:
		opts, args = gnu_getopt(argv, 'a:', ['ip=', 'help'])
	except GetoptError:
		exit(usage)

	# Since opts is a tuple of lists where the first is the flag
	# and the second is the argument for the flag (if requested),
	# we can write a for loop for this. 
	for opt, optArg in opts:
		#In case opt is help.
		if opt == '--help':
			print(usage)
			exit(0)
		#in case ip specified. 
		elif opt == '-a' or opt == '--ip':
			if not validIP(optArg):
				exit('You need to enter a valid IP.')
			ip = optArg
		

	# args includes the way the program is called as well as arguments. 
	# Since we want 3 arguments, we check for an argument size of 4 or more.
	if len(args) < 4: exit(usage)

	########################################################################
	# Work
	########################################################################

	domain = args[1]
	password = args[2]

	# urls is a dictionary of hosts, and the corresponding html responses.
	try: 
		urls = { host : \
				urlopen(getURL(domain, password, ip, host), \
				timeout = 10 ).read().decode('utf-8') \
				for host in args[3:] }	
	except URLError:
		exit('Couldn\'t connect to NameCheap servers. ')


	########################################################################
	# Output
	########################################################################

	for host, response in urls.items():
		ncParser = NCParser()
		
		ncParser.feed(response)

		print('Host: ' + host)
		print('' + str(ncParser) + '\n')


if __name__ == '__main__': main()
