import enum
import json
import math

# Generate the matchup chart for the types.
# This is not algorithm dependent.
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

def generate_def_score():
    for val in Types:
        total = len(Types)
        rlist = tdata[val.name]['resistances']
        wlist = tdata[val.name]['weaknesses']
        ilist = tdata[val.name]['immunities']
        score = 0.5 * len(rlist) + 2 * len(wlist) + (total - len(rlist) - len(wlist) - len(ilist))
        #print(val.name + " : " + str(total - score))
        tdata[val.name]['def_score'] = total - score

def generate_off_score():
    for val in Types:
        total = len(Types)
        slist = tdata[val.name]['super']
        nlist = tdata[val.name]['not']
        dlist = tdata[val.name]['doesnt']
        score = 2 * len(slist) + 0.5 * len(nlist) + (total - len(slist) - len(nlist) - len(dlist))
        #print(val.name + " : " + str(score - total))
        tdata[val.name]['off_score'] = score - total

def offensive_weight(val):
    if val >= 1.0:
        return 2
    else:
        return 1

def defensive_weight(val):
    if val >= 1.0:
        return 2
    else:
        return 1

def generate_table():
    generate_def_score()
    generate_off_score()
    arr = [[0 for x in range(2)] for y in range(len(Types))]
    #arr = [[0] * 2] * len(Types) This is wrong, for some reason updating one value updates them all.
    for val in Types:
        total = len(Types)
        d_score = 0
        rlist = tdata[val.name]['resistances']
        wlist = tdata[val.name]['weaknesses']
        ilist = tdata[val.name]['immunities']
        for i in rlist:
            d_score += 0.5 / offensive_weight(tdata[i.name]['off_score'])
        for i in wlist:
            d_score += 2 + offensive_weight(tdata[i.name]['off_score']) - 1
        d_score += total - len(rlist) - len(wlist) - len(ilist)
        arr[val.value][0] = total - d_score
    for val in Types:
        total = len(Types)
        o_score = 0
        slist = tdata[val.name]['super']
        nlist = tdata[val.name]['not']
        dlist = tdata[val.name]['doesnt']
        for i in slist:
            o_score += 2 + defensive_weight(tdata[i.name]['def_score']) - 1
        for i in nlist:
            o_score += 0.5 / defensive_weight(tdata[i.name]['def_score'])
        o_score += total - len(slist) - len(nlist) - len(dlist)
        arr[val.value][1] = o_score - total
    max_len = 0
    for val in Types:
        max_len = max(max_len, len(val.name))
    print(" " * max_len, end="")
    print("|  DEF |  OFF |")
    for val in Types:
        filler = max_len - len(val.name)
        fill_def = 6 - len(str(arr[val.value][0]))
        fill_off = 6 - len(str(arr[val.value][1]))
        print(val.name + " " * filler, end="|")
        print(" " * math.floor(fill_def/2) + str(arr[val.value][0]) + " " * math.ceil(fill_def/2), end="|")
        print(" " * math.floor(fill_off/2) + str(arr[val.value][1]) + " " * math.ceil(fill_off/2) + "|")
        

#TODO Weighted score: Everything over 1 has a higher weight.
#Open json file
#TODO Make it so it can open different json files
#TODO Have a folder for the json files and algorithms. User can select any file in that folder.
try:
    f = open('Type_Matchup.json')
except:
    print("Failed to open file")
    exit()
#TODO Add exception handler for json files
try:
    idata = json.load(f)['matchups'] #Initial data from JSON
except json.decoder.JSONDecodeError as e:
    print(e)
    exit()
except KeyError as e:
    print("Missing '" + str(e) + "' value")
    exit()

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

#TODO Validate the format of the json file for the program needs.
#TODO Add a check to validate that the defense arrays match the offense arrays
#TODO Add a check to validate that a resistance can't also be a weakness/immunities, etc
for val in Types:
    try:
        for r in idata[val.value]['resistances']:
            # If the type is not in there, it will exception on a KeyError
            # KeyError as e will return the key it is looking for.
            try:
                tdata[val.name]['resistances'].append(Types[r])
                tdata[r]['not'].append(Types[val.name])
            except KeyError:
                print("Type " + r + " does not exist")
                exit()
        for w in idata[val.value]['weaknesses']:
            try:
                tdata[val.name]['weaknesses'].append(Types[w])
                tdata[w]['super'].append(Types[val.name])
            except KeyError:
                print("Type " + w + " does not exist")
                exit()
        for i in idata[val.value]['immunities']:
            try:
                tdata[val.name]['immunities'].append(Types[i])
                tdata[i]['doesnt'].append(Types[val.name])
            except KeyError:
                print("Type " + i + " does not exist")
                exit()
    except KeyError as e:
        print("Missing '" + str(e) + "' Entry")
        exit()

#TODO for algorithm file, run through a queue of equations to get to the final one.
#TODO create an algorithm array to store all the scores generated to be used by other algorithms.
generate_table()

generate_matchups()

#TODO Create an algorithm file so that people can create and share their own