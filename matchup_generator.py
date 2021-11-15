import json
import math
import os
import sys

import importlib
import inspect
import pkgutil

import algorithms

from algorithms.type_matchup import Type_Matchup

#1. Find the plugins in the folder
#2. Import said modules/plugins
#3. Find the classes of the modules.
#4. Check that the classes are a subclass of Algorithm, and aren't Algorithm itself.
#5. Import the class. Try and Exception. If no exception, put it in the valid list.
def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

discovered_plugins = {
    name : importlib.import_module(name)
    for finder, name, ispkg
    in iter_namespace(algorithms)
}
valid_algs = {}
for name, module in discovered_plugins.items():
    #Find the classes of a module.
    for cls in inspect.getmembers(module, inspect.isclass):
        # Check if the algorithm has "generate_scores" method.
        if hasattr(cls[1], "generate_scores") and inspect.isfunction(cls[1].generate_scores):
            # Get the class from the module, which is an algorithm.
            try:
                valid_algs[cls[1].__name__] = getattr(module, cls[1].__name__)
                
            except:
                print("Exception", file=sys.stderr)
                continue

#ModuleNotFoundError could appear.

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
    # Validate the input. Move to another function?
    # Ensure that a list is returned of length 2. One entry for defense scores and one
    # entry for offense scores.
    if type(scores) == list:
        if len(scores) != 2:
            return None
    else:
        return None
    # Ensure that the entries are dictionaries with the same length as the number
    # of types.
    if type(scores[0]) == dict or type(scores[1]) == dict:
        if len(scores[0]) != len(Type_Matchup.Types) or len(scores[1]) != len(Type_Matchup.Types):
            return None
    else:
        return None
    max_len = Type_Matchup.Max_Char_Length
    print(" " * max_len, end="")
    print("|  DEF |  OFF |")
    for val in Type_Matchup.Types:
        filler = max_len - len(val)
        fill_def = 6 - len(str(scores[0][val]))
        fill_off = 6 - len(str(scores[1][val]))
        print(val + " " * filler, end="|")
        print(" " * math.floor(fill_def/2) + str(scores[0][val]) + " " * math.ceil(fill_def/2), end="|")
        print(" " * math.floor(fill_off/2) + str(scores[1][val]) + " " * math.ceil(fill_off/2) + "|")

#Find all json files in types.
valid_type = []
with os.scandir('types') as ot:
    for entry in ot:
        if entry.name.endswith(".json"):
            try:
                file_in = open('types/' + entry.name)
                #There could be additional entries to the json in the future.
                data_in = json.load(file_in)['matchups']
                #check if the input is valid.
                valid, errs = Type_Matchup.validate_input(data_in)
                if valid:
                    #Add files to a list. A file from that list can be chose.
                    valid_type.append({"name":entry.name,"matchup":data_in})
                else:
                    print("Errors found in " + entry.name, file=sys.stderr)
                    print(errs, file=sys.stderr)
            except FileNotFoundError as e:
                print(e, file=sys.stderr)
                continue
            except json.decoder.JSONDecodeError as e:
                #There were errors in the json file itself.
                print("Error Found in " + entry.name + ":\n" + str(e) + "\nIgnoring...", file=sys.stderr)
                continue
            except KeyError as e:
                #The setup for the json file was not compatible.
                print("Missing '" + str(e) + "' Value.", file=stderr)
            except BaseException as e:
                #Unknown Error found.
                print(e, file=sys.stderr)
                print("Some Error Found", file=sys.stderr)
                continue

# If there are no valid type matchups or algorithms, then exit the program
# as it can't run.
to_exit = False
if len(valid_type) == 0:
    print("No Valid Entry Found For Type Matchups!")
    to_exit = True

if len(valid_algs) == 0:
    print("No Valid Entry Found For Algorithms!")
    to_exit = True

if to_exit:
    print("Exiting...")
    sys.exit(0)

for index, item in enumerate(valid_type):
    print (str(index) + ": " + str(item['name']))

print("Enter a number to select a matchup\nType 'exit' to quit.")
user = 0
while True:
    try:
        user = input('--> ')
        if user.lower() == 'exit':
            sys.exit(0)
        user = int(user)
        if user > len(valid_type) - 1 or user < 0:
            print("Enter a valid value")
        else:
            break
    except ValueError:
        print(str(user) +" is not a number!", file=sys.stderr)
    
idata = valid_type[user]['matchup']
alg_list = list(valid_algs)
for index, name in enumerate(alg_list):
    print(str(index) + ": " + str(name))

print("Enter a number to select an algorithm\nType 'exit' to quit.")
user = 0
while True:
    try:
        user = input('--> ')
        if user.lower() == 'exit':
            sys.exit(0)
        user = int(user)
        if user > len(alg_list) - 1 or user < 0:
            print("Enter a valid value")
        else:
            user = alg_list[user]
            break
    except ValueError:
        print(str(user) +" is not a number!", file=sys.stderr)

Type_Matchup.generate_data (idata)
generate_matchups()
print(user)
alg = valid_algs[user]()
#TODO Try to handle generate_scores exceptioning as best as possible. Can
#     test by just raising exceptions in the algorithm file.
try:
    result = alg.generate_scores()
except:
    print("Exception")
    sys.exit(0)

generate_table(result)