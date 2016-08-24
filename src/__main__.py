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
		connection.request('GET',url, None, headers )
		response = json.loads(connection.getresponse().read().decode())
		for team in response['teams']:
			if str(team['shortName'])== 'None':
				team_list.append([team['_links']['self']['href'], team['name']])
			else:
				team_list.append([team['_links']['self']['href'], team['shortName']])
	return team_list
def test():
	print("TEST")
	sys.exit()

def main(flag):
	global comp_list
	global team_list
	print('Welcome to shellScore. Please wait while we load leagues and teams.')
	if flag:
		comp_list = get_comps()
		team_list = get_teams(comp_list)
		comp_team_list = comp_list + team_list
		
	choice = click.prompt('What competition or team would you like information about?')
	team_comp = choice.split()
	try:
		team_comp[1]
	except IndexError:
		team_comp = "".join(team_comp)
	else:
		team_comp = "".join(choice.split()[:-1])
	command ="".join(choice.split()[-1])
	for comp in comp_list:
		if team_comp.lower() in comp[1].lower():
			if click.confirm('Is this the competition you wanted: %s? ' % comp[1]):
				if command == 'table' or 'standings':
					get_league_table(comp)
					#todo
				elif command == 'fixtures' or 'schedule':
					get_league_fixt(comp)
					#todo
		else:
			for team in team_list:
				if team_comp.lower() in team[1].lower():
					if click.confirm('Is this the team you wanted? %s ' % team[1]):                 #todo add a full name function to confirm it's the right one
						if command == 'fixtures' or command == 'schedule':
							#get_team_fixt(team)
							#todo
							test()
							break
						elif command == 'players' or command == 'squad' or command == 'team':
							#get_team_players(team)
							#todo
							test()
							break

						elif command == team_comp:
							teamchoice = click.prompt('Would you like to see the fixtures for %s, or their squad?' % team[1], type=click.Choice(['fixtures', 'schedule', 'players','squad']))
							if teamchoice == 'fixtures' or teamchoice == 'schedule':
								test()
								#get_team_fixt(team)
								#todo
							elif teamchoice == 'squad' or teamchoice == 'players':
								test()
								#get_team_players(team)
								#todoq
						else:
							print('Enter a valid command for a team next time, or just enter the team name.')
					else:
						pass
				else:
					pass
			else:
				print('Unable to find that team/competition. Please try again.\n')
				main(False)

if __name__ == '__main__':
	main(True)
