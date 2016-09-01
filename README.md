# shellScore
written using http://api.football-data.org/index, a great API

##Description
A Python based project revolving around getting the scores, league, and player data for Football (or soccer) competitions around the world. Initially for personal use a means of staying updated on when my favorite teams are playing, and being able to easily find results at a few keystrokes.


![alt text](http://i.imgur.com/61JZT3D.gif "shellScore Demo by Justin Auger")
##Use
After running the program you can use `> search` to search the database, `> comps` to see a list of supported competitions, `> help` for a quick recap on what you can do, and `> exit`,


###Searching
`> TEAM/COMPETITION LOCATION` is the current formatting, where you enter what team or competition you'd like information about, followed by what information you'd like to get about it. 

Options include: Table, Standings, Schedule, Fixtures, Squad, Players, and Team. (Any portion of these words can be entered and on submit, it will autocomplete and try to find the closest match. So "fix" would autocomplete to "fixtures")

You can also just enter `> TEAM/COMPETITION` and the program will then guide you through possible choices with Yes/No confirmation prompts, and help menus.

####Example
`> barc fix` would lead to FC Barcelona's fixture list, as would `> barc sched`, or typing `> Barcelona` and then selecting from the menu.


###Other
[check me out @ justnaugr.github.io](http://justnaugr.github.io) & check out my other, bigger project [pyFootball](https://github.com/JustnAugr/pyFootball), a simulation based Football game
