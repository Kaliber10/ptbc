import json
import math
import sys

import importlib
import inspect
import pkgutil

import algorithms

from algorithms.type_matchup import Type_Matchup
from algorithms.algorithm import Algorithm

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
        # Check if the class is a subclass of the base Algorithm class and make sure it isn't from
        # importing the Algorithm class.
        if (issubclass (cls[1], Algorithm)) and not cls[1] == Algorithm:
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

## TODO handle case where None is returned, or there is too many or not enough
## values.
def generate_table(scores):
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

#Open json file
#TODO Make it so it can open different json files
#TODO Have a folder for the json files and algorithms. User can select any file in that folder.
try:
    f = open('Type_Matchup_6.json')
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
for name, cls in valid_algs.items():
    print (name)
    alg = cls()
    try:
        result = alg.generate_scores()
        generate_table(alg.generate_scores())
    except:
        print("Exception")
        continue