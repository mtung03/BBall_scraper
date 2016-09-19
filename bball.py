# bball.py

from lxml import html
import requests
import sys

def parse_args(arglist):
	arglist = arglist[1:]
	newlist = []
	j = 0
	for i in range(len(arglist)):
		curr_arg = arglist[i]
		if arglist[i][0] != '-':
			if i == 0:
				print "Invalid argument input.\nUsage: python bball.py -[player] -[stat] -[g/36/100/tot]"
			else:
				newlist[j-1] += (' ' + arglist[i])
		else :
			newlist.append(curr_arg)
			j += 1
	#print newlist
	return newlist



def set_url(args):
	url = 'http://www.basketball-reference.com/leagues/'
	year = args[3][1:]
	if args[2] == '-g':
		url += 'NBA_'+year+'_per_game.html'
	elif args[2] == '-36':
		url += 'NBA_'+year+'_per_minute.html'
	elif args[2] == '-100':
		url += 'NBA_'+year+'_per_poss.html'
	elif args[2] == '-tot':
		url += 'NBA_'+year+'_totals.html'
	else:
		print 'Invalid stat type input.\nUsage: python bball.py -[player] -[stat] -[g/36/100/tot]'
		return

	return url

def formatname(name):
	last = ''
	first = ''
	i = 0
	while name[i] != ' ':
		first += name[i]
		i += 1
	i += 1
	for j in range(i, len(name)):
		last += name[j]
	return last+ ',' + first

def get_stat(url, args):
	page = requests.get(url)
	tree = html.fromstring(page.content)

	# This will create a list of stats:
	headers = tree.xpath('//th[@class="tooltip"]/@tip')
	statindex = ''
	for i in range(len(headers)):
		if headers[i][0] == '<':
			j = 0
			while headers[i][j] != '>':
				j += 1
			headers[i] = headers[i][j+1:]
			while headers[i][j] != '<':
				j += 1
			headers[i] = headers[i][:j]
		if headers[i][:len(args[1][1:])] == args[1][1:]:
			statindex = i
			#print statindex

	if args[1] == '-stats':
		for i in headers:
			print i
		statindex = 'headers'
		return
	if statindex == '':
		print "Invalid stat.\nUsage: python bball.py -[player] -[stat] -[g/36/100/tot]"
		return

	playername = formatname(args[0][1:])
	path = '//td[@csk="'+ playername +'"]/../td['+str(statindex+6)+']/text()' #a/text()'
	#print path
	myplayer = tree.xpath(path)
	return myplayer

#//*[@id="totals"]/tbody/tr[4]/td[2]/a
# usage: python bball.py -[player] -[stat] -[g/36/100/tot]

args = parse_args(sys.argv)

if len(args) != 4:
	print 'Invalid input.\nUsage: python bball.py -[player] -[stat] -[g/36/100/tot] -[year]'

url = set_url(args)

stat = ''

stat = get_stat(url, args)

if stat != '' and stat != None:
	for i in stat:
		print i
