import enum
import json

def generate_def_score():
    print("## Generating Defensive Scores ##")
    for val in Types:
        total = len(Types)
        rlist = tdata[val.name]['resistances']
        wlist = tdata[val.name]['weaknesses']
        ilist = tdata[val.name]['immunities']
        score = 0.5 * len(rlist) + 2 * len(wlist) + (total - len(rlist) - len(wlist) - len(ilist))
        print(val.name + " : " + str(total - score))

def generate_off_score():
    print("## Generating Offensive Scores ##")
    for val in Types:
        total = len(Types)
        slist = tdata[val.name]['super']
        nlist = tdata[val.name]['not']
        dlist = tdata[val.name]['doesnt']
        score = 2 * len(slist) + 0.5 * len(nlist) + (total - len(slist) - len(nlist) - len(dlist))
        print(val.name + " : " + str(score - len(Types)))

#Open json file
#TODO Make it so it can open different json files
f = open('Type_Matchup.json')
#TODO Add exception handler for json files
idata = json.load(f)['matchups'] #Initial data from JSON

#Generate the names of the types for the enum.
type_list = {}
tdata = {} # Collected data populated with Types values
for index, value in enumerate(idata):
    type_list[value['name']] = index
    tdata[value['name']] = {'resistances' : [], 'weaknesses' : [], 'immunities' : [], 'super' : [], 'not' : [], 'doesnt' : []}

Types = enum.Enum('Types', type_list)

#Generate the dictionary with Types enums

#TODO Validate that all types in resistances/weaknesses/immunities are eligible types.
#TODO Validate the format of the json file for the program needs.
#TODO Add a value in type dictionary for defense and offense score.
#TODO Add a check to validate that the defense arrays match the offense arrays
for val in Types:
    for r in idata[val.value]['resistances']:
        # If the type is not in there, does it exception?
        tdata[val.name]['resistances'].append(Types[r])
        tdata[r]['not'].append(Types[val.name])
    for w in idata[val.value]['weaknesses']:
        tdata[val.name]['weaknesses'].append(Types[w])
        tdata[w]['super'].append(Types[val.name])
    for i in idata[val.value]['immunities']:
        tdata[val.name]['immunities'].append(Types[i])
        tdata[i]['doesnt'].append(Types[val.name])

#TODO Generate a type chart in ascii
generate_def_score()
generate_off_score()

#TODO Create an algorithm file so that people can create and share their own