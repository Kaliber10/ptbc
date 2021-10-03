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
        print(val.name + " : " + str(score - total))

def generate_matchups():
    temp_filler = "   "
    # Print the top of the table.
    print ("   |", end="")
    for type in Types:
        print (type.name[:3], end="|") # Print the first 3 characters of the type
    print("")
    # Print the left side of the table.
    for type in Types:
        print (type.name[:3], end="|")
        for opp_type in Types:
            if opp_type in tdata[type.name]['super']:
                print(" 2 |", end="")
            elif opp_type in tdata[type.name]['not']:
                print("0.5|", end="")
            elif opp_type in tdata[type.name]['doesnt']:
                print(" 0 |", end="")
            else:
                print(" 1 |", end="")
                
        print("")

#TODO Weighted score: Everything over 1 has a higher weight.
#Open json file
#TODO Make it so it can open different json files
#TODO Have a folder for the json files and algorithms. User can select any file in that folder.
f = open('Type_Matchup.json')
#TODO Add exception handler for json files
idata = json.load(f)['matchups'] #Initial data from JSON

#Generate the names of the types for the enum.
type_list = {}
tdata = {} # Collected data populated with Types values
for index, value in enumerate(idata):
    type_list[value['name']] = index
    tdata[value['name']] = {'resistances' : [],
                            'weaknesses' : [],
                            'immunities' : [],
                            'def_score'  : 0,
                            'super' : [],
                            'not' : [],
                            'doesnt' : [],
                            'off_score' : 0}

Types = enum.Enum('Types', type_list)

#Generate the dictionary with Types enums

#TODO Validate that all types in resistances/weaknesses/immunities are eligible types.
#TODO Validate the format of the json file for the program needs.
#TODO Add a value in type dictionary for defense and offense score.
#TODO Add a check to validate that the defense arrays match the offense arrays
#TODO Add a check to validate that a resistance can't also be a weakness/immunities, etc
for val in Types:
    try:
        for r in idata[val.value]['resistances']:
            # If the type is not in there, it will exception on a KeyError
            try:
                tdata[val.name]['resistances'].append(Types[r])
                tdata[r]['not'].append(Types[val.name])
            except KeyError:
                print("Type " + r + " does not exist")
                exit()
    except KeyError:
        print("Missing 'resistances' Entry")
        exit()
    try:
        for w in idata[val.value]['weaknesses']:
            try:
                tdata[val.name]['weaknesses'].append(Types[w])
                tdata[w]['super'].append(Types[val.name])
            except KeyError:
                print("Type " + w + " does not exist")
                exit()
    except KeyError:
        print("Missing 'weaknesses' Entry")
        exit()
    try:
        for i in idata[val.value]['immunities']:
            try:
                tdata[val.name]['immunities'].append(Types[i])
                tdata[i]['doesnt'].append(Types[val.name])
            except KeyError:
                print("Type " + i + " does not exist")
                exit()
    except KeyError:
        print("Missing 'immunities' Entry")
        exit()

#TODO for algorithm file, run through a queue of equations to get to the final one.
generate_def_score()
generate_off_score()

generate_matchups()

#TODO Create an algorithm file so that people can create and share their own