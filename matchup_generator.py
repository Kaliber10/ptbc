import enum
import json
import math
import sys
import algorithms.type_matchup as tm
from algorithms.raw_calc import Raw_Calc

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

# Generate a score.
# R = Resistances List
# W = Weaknesses List
# I = Immunities List
# S = Super Effective List
# N = Not Very Effective List
# D = Doesn't Effect List
# T = Types List
# $<X> Means value of <X>
# %<X> Means length of <X>
# ^<X>:<R/T> Means result of Algorithm <X>
# #<X> Means average value of Algorithm <X>
# Should everything be delimited by spaces?
# The final value is determined by the final line?
# Alg 1
# Return: Array
# loop T {%T - 0.5 * %R + 2 * %W + (%T - %R - %W - %I)}
# Equivalent to 0.5 * %R - %W + %I
# Alg 2
# Return: Array
# loop T {(2 * %S + 0.5 * %N + (%T - %S - %N - %D)) - %T}
# Alg 3
# Return: Value
# Variables : {off_list : Array}
# loop T { off_list.add {^1}}, Average(off_list)
# Alg 4
# Return: Value
# Variables : {def_list : Array}
# loop T { def_list.add {^2}}, Average (def_list)
# Alg 5
# loop T {loop R {0.5 / x}
def generate_def_score():
    for val in Types:
        total = len(Types)
        rlist = tdata[val.name]['resistances']
        wlist = tdata[val.name]['weaknesses']
        ilist = tdata[val.name]['immunities']
        score = 0.5 * len(rlist) + 2 * len(wlist) + (total - len(rlist) - len(wlist) - len(ilist))
        tdata[val.name]['def_score'] = total - score

def generate_off_score():
    for val in Types:
        total = len(Types)
        slist = tdata[val.name]['super']
        nlist = tdata[val.name]['not']
        dlist = tdata[val.name]['doesnt']
        score = 2 * len(slist) + 0.5 * len(nlist) + (total - len(slist) - len(nlist) - len(dlist))
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
def weighted_average():
    outlier = 2
    off_list = []
    def_list = []
    for val in Types:
        off_list.append(tdata[val.name]['off_score'])
        def_list.append(tdata[val.name]['def_score'])
    off_list.sort()
    def_list.sort()
    print(sum(off_list))
    print(sum(def_list))
    print(sum(off_list[outlier:len(off_list)-outlier])/len(off_list[outlier:len(off_list)-outlier]))
    print(sum(def_list[outlier:len(def_list)-outlier])/len(def_list[outlier:len(def_list)-outlier]))
    
def generate_table():
    generate_def_score()
    generate_off_score()
    weighted_average()
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
        # This algorithm should also compensate for being neutral effective against good types.
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
        
def generate_table2(scores):
    max_len = 0 
    for val in tm.Type_Matchup.Types:
        max_len = max(max_len, len(val))
    print(" " * max_len, end="")
    print("|  DEF |  OFF |")
    for val in tm.Type_Matchup.Types:
        filler = max_len - len(val)
        fill_def = 6 - len(str(scores[0][val]))
        fill_off = 6 - len(str(scores[1][val]))
        print(val + " " * filler, end="|")
        print(" " * math.floor(fill_def/2) + str(scores[0][val]) + " " * math.ceil(fill_def/2), end="|")
        print(" " * math.floor(fill_off/2) + str(scores[1][val]) + " " * math.ceil(fill_off/2) + "|")

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

#TODO create an algorithm array to store all the scores generated to be used by other algorithms.
#generate_table()

#generate_matchups()

tm.Type_Matchup.generate_data (idata)
rc = Raw_Calc()
generate_table2(rc.generate_scores())

#TODO Create an algorithm file so that people can create and share their own