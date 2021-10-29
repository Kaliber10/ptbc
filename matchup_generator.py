import enum
import json
import math
import sys
from algorithms.type_matchup import Type_Matchup
from algorithms.raw_calc import Raw_Calc
from algorithms.weighted_calc import Weighted_Calc

# Generate the matchup chart for the types.
# This is not algorithm dependent.
def generate_matchups():
    temp_filler = "   "
    # Print the top of the table.
    print ("   |", end="")
    for type in Type_Matchup.Types:
        print (type[:3], end="|") # Print the first 3 characters of the type
    print("")
    # Print the left side of the table.
    for type in Type_Matchup.Types:
        print (type[:3], end="|")
        for opp_type in Type_Matchup.Types:
            if opp_type in Type_Matchup.Type_Data[type]['super']:
                print(" 2 |", end="")
            elif opp_type in Type_Matchup.Type_Data[type]['not']:
                print("0.5|", end="")
            elif opp_type in Type_Matchup.Type_Data[type]['doesnt']:
                print(" 0 |", end="")
            else:
                print(" 1 |", end="")

        print("")

def generate_table(scores):
    max_len = 0 
    for val in Type_Matchup.Types:
        max_len = max(max_len, len(val))
    print(" " * max_len, end="")
    print("|  DEF |  OFF |")
    for val in Type_Matchup.Types:
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
    sys.exit(1)
#TODO Add exception handler for json files
try:
    idata = json.load(f)['matchups'] #Initial data from JSON
except json.decoder.JSONDecodeError as e:
    print(e)
    sys.exit(1)
except KeyError as e:
    print("Missing '" + str(e) + "' value")
    sys.exit(1)

#TODO create an algorithm array to store all the scores generated to be used by other algorithms.
Type_Matchup.generate_data (idata)
generate_matchups()
rc = Raw_Calc()
wc = Weighted_Calc()
generate_table(rc.generate_scores())
generate_table(wc.generate_scores())

#TODO Create an algorithm file so that people can create and share their own