import http.client
import json
import click
import sys


connection = http.client.HTTPConnection('api.football-data.org')
apikey = open('src/apikey.txt').read() #hidden for github upload, to get your own go to http://api.football-data.org
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
			if str(team['shortName'])== 'None':
				team_list.append([team['_links']['self']['href'], team['name']])
			else:
				team_list.append([team['_links']['self']['href'], team['shortName']])
	return team_list

def get_team_fixt(team):
	team_id = team[0]
	team_name = team[1]
	url = team_id + '/fixtures/'
	connection.request('GET',url, None, headers)
	response = json.loads(connection.getresponse().read().decode())
	click.clear()
	print('Fixtures')
	print('-'.ljust(29,'-'))
	for fixture in response['fixtures']:
		if str(fixture['result']['goalsHomeTeam']) == 'None':
			fixture_string = '%s %s - %s' % (fixture['date'][:9], fixture['homeTeamName'], fixture['awayTeamName'])
		else:
			fixture_string = '%s %s - %s %s' % (fixture['homeTeamName'], fixture['result']['goalsHomeTeam'], fixture['result']['goalsAwayTeam'], fixture['awayTeamName'])
		print(fixture_string)
	while True:
		if click.confirm('Would you like to return to the main menu?'):
			main(False)
		else:
			if click.confirm('Would you like to see the players currently listed for %s' % team_name):
				get_team_players(team)

def get_team_players(team):
	team_id = team[0]
	team_name = team[1]
	url = team_id + '/players/'
	connection.request('GET',url, None, headers)
	response = json.loads(connection.getresponse().read().decode())
	#todo finish this

def get_comp_table(comp):
	comp_id = comp[0]
	comp_name = comp[1]
	url = '/v1/competitions/' + comp_id + '/leagueTable/'
	connection.request('GET',url, None, headers)
	response = json.loads(connection.getresponse().read().decode())
	print('get_comp_table')
	#todo finish this

def get_comp_fixt(comp):
	comp_id = comp[0]
	comp_name = comp[1]
	url = '/v1/competitions/' + comp_id + '/fixtures/'
	connection.request('GET',url, None, headers)
	response = json.loads(connection.getresponse().read().decode())
	#todo finish this

def search_db():
	click.clear()
	choice = click.prompt('What competition or team would you like information about?')
	if choice.lower() == 'help':
		click.clear()
		print('help')
		search_db()

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
				print('another error')
	else:
		for n in range(len(team_comp)):
			for team in team_list:
				if team_comp.lower() in team[1].lower() and team[1][n:n+len(team_comp)].lower() == team_comp.lower():
					if click.confirm('Is this the team you wanted? %s ' % team[1]):  
						if command == 'fixtures' or command == 'schedule':
							get_team_fixt(team)
						elif command == 'players' or command == 'squad' or command == 'team':
							get_team_players(team)
						elif command == team_comp:
							teamchoice = click.prompt('Would you like to see the fixtures for %s, or their squad?' % team[1], type=click.Choice(['fixtures', 'schedule', 'players','squad']))
							if teamchoice == 'fixtures' or teamchoice == 'schedule':
								get_team_fixt(team)
							elif teamchoice == 'squad' or teamchoice == 'players':
								get_team_players(team)
						else:
							print('Enter a valid command for a team next time, or just enter the team name.')
		else:
			print('Unable to find that team/competition. Please try again. \n')
			#main(False)

def main(flag):
	global comp_list
	global team_list
	if not flag:
		click.clear()
	print('Welcome to shellScore. Please wait while we load leagues and teams.')
	if flag:
		comp_list = get_comps()
		team_list = get_teams(comp_list)
	

	while True:
		choice = click.prompt('\nWhat would you like to do?')
		if choice.lower() == 'help':
			print('\nhelp')
		elif choice.lower() == 'comps':
			print('\nHere are all available competitions: ')
			for comp in comp_list:
				print(comp[1])
		elif choice.lower() == 'teams':
			print('\nHere are all available teams: ')
			for team in team_list:
				print(team[1])
		elif choice.lower() == 'search':
			search_db()
		elif choice.lower() == 'exit':
			sys.exit()
		else:
			print('Sorry, that command wasn\'t recognized. Try one of these: help, search, comps, teams, exit')

if __name__ == '__main__':
	main(True)
