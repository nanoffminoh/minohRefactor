MINOH REFACTOR

model:
	Stats: the stat block of 7 stats used by other multiple classes
	Guest: the guests logged into the hotel. Contains stats used in the teams, and methods necessary for advancing his route when the player wants.
	GuestList: lists of guests, includes methods for easier manipulation
	Reward: the rewards the player can obtain through RD and exploration
	RewardList: list of rewards, includes methods for doing queries, sorting, etc.
	Inventory: the items, passive stats, files, etc the player has
	FilesList: its own separate class used by the files screen.
	DailyEvent: some events happen out of order, the daily event class allows you
                    to schedule or have events that happen on a given day when conditions are met.
	DailyEventList: list of daily events
	Relationship: when two guests are in a relationship they get a stat bonus if they're on the same team.
	RelationshipList: (you may be seeing a pattern here)
	Wardrobe: contains the articles of clothing asterion can wear.

access:
	team.py: functions that manage the teams during sessions, such as calculating the team rewards, determining the reward to get
	ui.py: functions that get data from the model to the screens
	permanent.py: functions that modify the save file variables along with persistent variables
	loader.py: functions that load data from the presets file
	others.py: other functions used in game that don't really touch on the model

tests:
	""""unit"""" tests for the model and access classes/functions
	yeah there's some with like ten asserts per test, sue me

presets.py: data such as initial stats for the guests, possible rewards, item descriptions, etc.

renpy_functions.py: emulates renpy variables that can't be used during testing because renpy sucks ass and shits itself when you try to import the random library

renpy_variables.py: the variables to be used in game (excludes the character objects), including persistent variables.