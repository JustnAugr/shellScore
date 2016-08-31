#!/usr/bin/env python3
import http.client
import json
import click
import sys

connection = http.client.HTTPConnection('api.football-data.org')
apikey = open('apikey.txt').read() #hidden for github upload, to get your own go to http://api.football-data.org
headers = { 'X-Auth-Token': apikey}


def get_comps():
	connection.request('GET', '/v1/competitions', None, headers )
	response = json.loads(connection.getresponse().read().decode())
	comp_list=[]
	for comp in response:
		comp_list.append([comp['id'],comp['caption']])
	return comp_list


def get_teams(comp_list):
	team_list=[]
	for id in comp_list:
		url = '/v1/competitions/' + str(id[0]) + '/teams'
		connection.request('GET',url, None, headers)
		response = json.loads(connection.getresponse().read().decode())
		for team in response['teams']:
			team_list.append([team['_links']['self']['href'], team['name']])
	return team_list

def get_team_fixt(team):
	team_id = team[0]
	team_name = team[1]
	url = team_id + '/fixtures/'
	connection.request('GET',url, None, headers)
	response = json.loads(connection.getresponse().read().decode())
	click.clear()
	upcoming_fixt = []
	past_fixt = []
	for fixture in response['fixtures']:
		if str(fixture['result']['goalsHomeTeam']) == 'None':
			fixture_string = '%s | %s -     %s' % (fixture['date'][:10].ljust(2,' '), fixture['homeTeamName'].ljust(25,' '), fixture['awayTeamName'])
			upcoming_fixt.append(fixture_string)
		else:
			fixture_string = '%s %s - %s %s' % (fixture['homeTeamName'].ljust(23,' '), fixture['result']['goalsHomeTeam'], 
				str(fixture['result']['goalsAwayTeam']).ljust(4, ' '), fixture['awayTeamName'])
			past_fixt.append(fixture_string)
	print('-'.ljust(80,'-'))		
	print('Past Fixtures'.rjust(45,' '))
	print('-'.ljust(80,'-'))
	for fixture in past_fixt:
		print('%s %s' % (' '.ljust(12,' '),fixture))
	print('-'.ljust(80,'-'))
	print('Upcoming Fixtures'.rjust(47,' '))
	print('-'.ljust(80,'-'))
	for fixture in upcoming_fixt:
		print(fixture)
	print('-'.ljust(80,'-'))
	while True:
		if click.confirm('Would you like to see the players currently listed for %s' % team_name):
			get_team_players(team)
		elif click.confirm('\nWould you like to return to the main menu?'):
			main(False)

def get_team_players(team):
	team_id = team[0]
	team_name = team[1]
	url = team_id + '/players/'
	connection.request('GET',url, None, headers)
	response = json.loads(connection.getresponse().read().decode())
	print('\n-'.ljust(124,'-'))
	print('Squad list'.rjust(60,' '))
	print('-'.ljust(124,'-'))
	print('%s | %s | %s | %s | %s | %s | %s' % ('#'.ljust(2,' '), 'Name'.ljust(25,' '), 'DOB'.ljust(10,' '), 'Nationality'.ljust(15,' '),
	 'Position'.ljust(20,' '), 'Transfer Value'.ljust(15,' '), 'Contract expiry'))
	print('-'.ljust(124,'-'))
	for player in response['players']:
		if str(player['contractUntil']) == 'None':
			print('%s | %s | %s | %s | %s | %s EU | %s' % (str(player['jerseyNumber']).ljust(2,' '), player['name'].ljust(25,' '), 
				player['dateOfBirth'], player['nationality'].ljust(20,' '), player['position'].ljust(20,' '), 
				player['marketValue'][:len(player['marketValue'])-1].ljust(15,' '), 'Unavailable'))
		elif str(player['jerseyNumber']) == 'None':
			print('%s | %s | %s | %s | %s | %s EU | %s' % ('?'.ljust(2,' '), player['name'].ljust(25,' '), player['dateOfBirth'], 
				player['nationality'].ljust(20,' '), player['position'].ljust(20,' '), player['marketValue'][:len(player['marketValue'])-1].ljust(15,' '), player['contractUntil']))
		else:
			print('%s | %s | %s | %s | %s | %s EU | %s' % (str(player['jerseyNumber']).ljust(2,' '), player['name'].ljust(25,' '), 
				player['dateOfBirth'], player['nationality'].ljust(20,' '), player['position'].ljust(20,' '), player['marketValue'][:len(player['marketValue'])-1].ljust(15,' '), player['contractUntil']))
	print('-'.ljust(124,'-'))
	while True:
		if click.confirm('Would you like to see the fixtures currently listed for %s' % team_name):
				get_team_fixt(team)
		elif click.confirm('\nWould you like to return to the main menu?'):
			main(False)

def get_comp_table(comp):
	comp_id = comp[0]
	comp_name = comp[1]
	url = '/v1/competitions/' + str(comp_id) + '/leagueTable/'
	connection.request('GET',url, None, headers)
	response = json.loads(connection.getresponse().read().decode())
	try:
		response['standing']
	except KeyError:
		print('\nSorry, that competition\'s standings weren\'t available. Try again at a later date and we might have updated!')
		search_db()
	else:
		print('\n-'.ljust(78,'-'))	
		print(' %s| %s|  %s|  %s|  %s|  %s|  %s|  %s|  %s| %s |' % ('Pos'.ljust(3,' '),'Name'.ljust(26,' '),'P'.ljust(2, ' '),'W'.ljust(2,' '),'D'.ljust(2,' '),'L'.ljust(2,' '),'GF'.ljust(3,' '),'GA'.ljust(3,' '),'GD'.ljust(3,' '),'PTs'.ljust(3,' ')))
		for table_place in response['standing']:
			#      pos, name, win, draw, loss, GF, GA, GD, points
			#       1    2     3     4    5     6   7   8   9
			if str(table_place['goalDifference'])[0] == '-':
				print('%s | %s | %s| %s| %s| %s|%s|%s|%s| %s|' % (str(table_place['position']).center(3,' '), table_place['teamName'].ljust(25,' '), 
					str(table_place['playedGames']).center(3,' '), str(table_place['wins']).center(3,' '), 
					str(table_place['draws']).center(3,' '), str(table_place['losses']).center(3,' '), str(table_place['goals']).center(5,' '), str(table_place['goalsAgainst']).center(5,' '), 
					str(table_place['goalDifference']).center(5,' '), str(table_place['points']).ljust(4,' ')))
			else:
				print('%s | %s | %s| %s| %s| %s|%s|%s|%s| %s|' % (str(table_place['position']).center(3,' '), table_place['teamName'].ljust(25,' '), 
					str(table_place['playedGames']).center(3,' '), str(table_place['wins']).center(3,' '), 
					str(table_place['draws']).center(3,' '), str(table_place['losses']).center(3,' '), str(table_place['goals']).center(5,' '), str(table_place['goalsAgainst']).center(5,' '), 
					('+' + str(table_place['goalDifference'])).center(5,' '), str(table_place['points']).ljust(4,' ')))
		print('-'.ljust(77,'-'))		
	while True:
		if click.confirm('Would you like to see the fixtures currently listed for %s' % comp_name):
			get_comp_fixt(comp)
		elif click.confirm('\nWould you like to return to the main menu?'):
			main(False)


def get_comp_fixt(comp):
	comp_id = comp[0]
	comp_name = comp[1]
	url = '/v1/competitions/' + str(comp_id) + '/fixtures/'
	connection.request('GET',url, None, headers)
	response = json.loads(connection.getresponse().read().decode())
	upcoming_fixt = []
	past_fixt = []
	for fixture in response['fixtures']:
		if fixture['status'] == 'SCHEDULED':
			fixture_string = '%s | %s -     %s' % (fixture['date'][:10].ljust(2,' '), fixture['homeTeamName'].ljust(25,' '), fixture['awayTeamName'])
			upcoming_fixt.append(fixture_string)
		elif fixture['status'] == 'FINISHED':
			fixture_string = '%s %s - %s %s' % (fixture['homeTeamName'].ljust(23,' '), fixture['result']['goalsHomeTeam'], 
				str(fixture['result']['goalsAwayTeam']).ljust(4, ' '), fixture['awayTeamName'])
			past_fixt.append(fixture_string)
	print('\n--'.ljust(80,'-'))		
	print('Past Fixtures'.rjust(45,' '))
	print('-'.ljust(80,'-'))
	for fixture in past_fixt:
		print('%s %s' % (' '.ljust(12,' '),fixture))
	print('-'.ljust(80,'-'))
	print('Upcoming Fixtures'.rjust(47,' '))
	print('-'.ljust(80,'-'))
	for fixture in upcoming_fixt:
		print(fixture)
	print('-'.ljust(80,'-'))
	while True:
		if click.confirm('Would you like to see the league table for %s' % comp_name):
			get_comp_table(comp)
		elif click.confirm('\nWould you like to return to the main menu?'):
			main(False)

def search_db():
	choice = click.prompt('\nWhat competition or team would you like information about?')
	if choice.lower() == 'help':
		click.clear()
		print('help')
		search_db()
	elif choice.lower() == 'exit':
		main(False)

	team_comp = choice.split()
	try:
		team_comp[1]
	except IndexError:
		team_comp = ''.join(team_comp)
	else:
		team_comp = ''.join(choice.split()[:-1])
	command = ''.join(choice.split()[-1])
	for comp in comp_list:
		if team_comp.lower() in comp[1].lower():
			if click.confirm('Is this the competition you wanted: %s? ' % comp[1]):
				command_list = ['table','standings','fixtures','schedule']
				for cmd in command_list:
					if command.lower() in cmd:
						if click.confirm('You\'ve selected %s, is that correct?' % cmd):
							if cmd == 'table' or cmd == 'standings':
								get_comp_table(comp)
							elif cmd == 'fixtures' or cmd == 'schedule':
								get_comp_fixt(comp)
				else:
					while True:
						comp_choice = click.prompt('Would you like to the competition standings or the fixture list for %s?' % comp[1])
						comp_choice_list = ['standings','table','fixtures','schedule', 'exit']
						for poss_choice in comp_choice_list:
							if comp_choice.lower() in poss_choice:
								if click.confirm('You\'ve selected %s, is that correct?' % poss_choice):
									if poss_choice == 'standings' or poss_choice == 'table':
										get_comp_table(comp)
									elif poss_choice == 'fixtures' or poss_choice == 'schedule':
										get_comp_fixt(comp)
									elif poss_choice =='exit':
										main(False)
						else:
							print('Sorry, that choice was not recognized. Try one of these: standings, table, fixtures, schedule, exit')
	else:
		for n in range(30):
			for team in team_list:
				if team_comp.lower() in team[1].lower() and team[1][n:n+len(team_comp)].lower() == team_comp.lower():
					if click.confirm('Is this the team you wanted? %s ' % team[1]): 
						command_list = ['fixtures','schedule','players','team','squad']
						for cmd in command_list:
							if command.lower() in cmd:
								if click.confirm('You\'ve selected %s, is that correct?' % cmd):
									if cmd == 'fixtures' or cmd == 'schedule':
										get_team_fixt(team)
									elif cmd == 'players' or cmd == 'squad' or cmd == 'team':
										get_team_players(team)

						else:
							while True:
								team_choice = click.prompt('Would you like to view the fixtures for %s, or their squad?' % team[1])
								team_choice_list = ['fixtures', 'schedule', 'squad', 'players', 'team', 'exit']
								for poss_choice in team_choice_list:
									if team_choice.lower() in poss_choice:
										if click.confirm('You\'ve selected %s, is that correct?' % poss_choice):
											if poss_choice == 'fixtures' or poss_choice == 'schedule':
												get_team_fixt(team)
											elif poss_choice == 'squad' or poss_choice == 'players' or poss_choice == 'team':
												get_team_players(team)
											elif poss_choice == 'exit':
												main(False)
								else:
									print('Sorry, that choice was not recognized. Try one of these: fixtures, schedule, squad, players, team, exit')
		else:
			print('Unable to find that team/competition. Please try again. \n')
			search_db()


#todo add saving/loading favorites with a favorites file, clean up
def main(flag):
	global comp_list
	global team_list
	if not flag:
		click.clear()
		print('-'.ljust(70,'-'))
		print('Welcome to shellScore.'
				'\n                 _          _ _ __                    '
				'\n             ___| |__   ___| | / _\ ___ ___  _ __ ___ '
				'\n            / __| \'_ \ / _ \ | \ \ / __/ _ \| \'__/ _ \\'
				'\n            \__ \ | | |  __/ | |\ \ (_| (_) | | |  __/'
				'\n            |___/_| |_|\___|_|_\__/\___\___/|_|  \___|')
		print('-'.ljust(70,'-'))
	if flag:
		print('-'.ljust(70,'-'))
		print('Welcome to shellScore. Please wait while we load leagues and teams.'
				'\n                 _          _ _ __                    '
				'\n             ___| |__   ___| | / _\ ___ ___  _ __ ___ '
				'\n            / __| \'_ \ / _ \ | \ \ / __/ _ \| \'__/ _ \\'
				'\n            \__ \ | | |  __/ | |\ \ (_| (_) | | |  __/'
				'\n            |___/_| |_|\___|_|_\__/\___\___/|_|  \___|')
		print('-'.ljust(70,'-'))
	if flag:
		comp_list = get_comps()
		team_list = get_teams(comp_list)
	while True:
		choice = click.prompt('What would you like to do?')
		if choice.lower() == 'help':
			print('\nAvailable commands: help, comps, search, exit')
			print('-'.ljust(70,'-'))
		elif choice.lower() == 'comps':
			print('\nHere are all available competitions:\n')
			for comp in comp_list:
				print(comp[1])
			print('-'.ljust(100,'-'))
		elif choice.lower() == 'search':
			search_db()
		elif choice.lower() == 'exit':
			sys.exit()
		else:
			print('Sorry, that command wasn\'t recognized. Try one of these: help, search, comps, teams, exit')

if __name__ == '__main__':
	main(True)
