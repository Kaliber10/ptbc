#!/usr/bin/env python3
import json
import math
import os
import sys
import importlib
import inspect
import pkgutil

import algorithms

import algorithms.type_matchup as tm

def find_valid_plugins(pkg_space):
    #1. Find the plugins in the folder
    #2. Import said modules/plugins
    #3. Find the classes of the modules.
    #4. Import the class. Try and Exception. If no exception, put it in the valid list.
    discovered_plugins = {}
    valid_plg = []
    for finder, name, ispkg in pkgutil.iter_modules(pkg_space.__path__, pkg_space.__name__ + "."):
        try:
            discovered_plugins[name] = importlib.import_module(name)
        except Exception as e:
            print ("The plugin " + name + " had an exception when importing.", file=sys.stderr)
            print ("  " + str(e), file=sys.stderr)
        except:
            print("The plugin " + name + " had an exception when importing.", file=sys.stderr)
    #Find the classes of a module.
    for name, module in discovered_plugins.items():
        for cls in inspect.getmembers(module, inspect.isclass):
            # Check if the algorithm has "generate_scores" method.
            if hasattr(cls[1], "generate_scores") and inspect.isfunction(cls[1].generate_scores):
                fun_spec = inspect.getfullargspec(cls[1].generate_scores)
                if len(fun_spec.args) ==  2:
                    # Get the class from the module, which is an algorithm.
                    #ModuleNotFoundError could appear.
                    try:
                        valid_plg.append({"name" : cls[1].__name__, "class" : getattr(module, cls[1].__name__)})
                        #valid_plg[cls[1].__name__] = getattr(module, cls[1].__name__)
                    except Exception as e:
                        print("Exception while verifying algorithm.", file=sys.stderr)
                        print(e, file=sys.stderr)
                        continue
    del discovered_plugins
    return valid_plg

def find_valid_matchups(path):
    # This will return the list of all valid json files and their data.
    valid_types = []
    # Find all json files in /types.
    with os.scandir(str(path)) as ot:
        for entry in ot:
            if entry.name.endswith(".json"):
                try:
                    file_in = open(path + '/' + entry.name)
                    # There could be additional entries to the json in the future.
                    data_in = json.load(file_in)['matchups']
                    # Determine if the data is valid.
                    valid, errs = tm.validate_input(data_in)
                    # If the json file is not valid for any reason, it will not be added
                    # to the list.
                    if valid:
                        # This will store the file name for reference later as well as the
                        # data in said file.
                        valid_types.append({"name":entry.name,"matchup":data_in})
                    else:
                        # Print the file that had errors and the files that occurred so
                        # that they may be fixed.
                        print("Errors found in " + entry.name, file=sys.stderr)
                        print(*errs, sep='\n', file=sys.stderr)
                except FileNotFoundError as e:
                    # In the case where the file gets deleted while going through
                    # the list.
                    print(e, file=sys.stderr)
                    continue
                except json.decoder.JSONDecodeError as e:
                    # There were json syntax errors file which prevent loading.
                    print("Error Found in " + entry.name + ":\n" + str(e) + "\nIgnoring file...", file=sys.stderr)
                    continue
                except KeyError as e:
                    # There was not 'matchups' entry in the file.
                    print("Error Found in " + entry.name, file=sys.stderr)
                    print("Missing " + str(e) + " Value.", file=sys.stderr)
                    print("Ignoring file...", file=sys.stderr)
                except Exception as e:
                    # An unexpected Error was found.
                    print("Error Found in " + entry.name, file=sys.stderr)
                    print(e, file=sys.stderr)
                    print("Ignoring file...", file=sys.stderr)
                    continue
    return valid_types

def validate_table(types, scores):
    # Validate the return from the plugin.
    # Ensure that a list is returned of length 2. One entry for defense scores and one
    # entry for offense scores.
    if type(scores) == list:
        if len(scores) != 2:
            return False, "The algorithm must return a list of length 2, and each index being a dictionary of each type, and a numeric value."
    else:
        return False, "The algorithm must return a list of length 2, and each index being a dictionary of each type, and a numeric value."
    # Ensure that the entries are dictionaries with the same length as the number
    # of types.
    if type(scores[0]) == dict or type(scores[1]) == dict:
        if len(scores[0]) != len(types['data'].keys()) or len(scores[1]) != len(types['data'].keys()):
            return False, "The dictionaries must be the same length as the number of Types."
        if sorted(types['data'].keys()) != sorted(list(scores[0].keys())) or sorted(types['data'].keys()) != sorted(list(scores[1].keys())):
            return False, "The dictionaries keys must be the Types."
        for val in scores[0].keys():
            if not isinstance(scores[0][val], (int, float)):
                return False, "Each entry must be a number."
        for val in scores[1].keys():
            if not isinstance(scores[1][val], (int, float)):
                return False, "Each entry must be a number."
    else:
        return False, "The algorithm must return a list of length 2, and each index being a dictionary of each type, and a numeric value."
    return True, ""

def generate_table(types, scores):
    max_len = types['meta']['max_length']
    print(" " * max_len, end="")
    print("|  DEF |  OFF |")
    for val in types['data'].keys():
        filler = max_len - len(val)
        fill_def = 6 - len(str(scores[0][val]))
        fill_off = 6 - len(str(scores[1][val]))
        print(val.capitalize() + " " * filler, end="|")
        print(" " * math.floor(fill_def/2) + str(scores[0][val]) + " " * math.ceil(fill_def/2), end="|")
        print(" " * math.floor(fill_off/2) + str(scores[1][val]) + " " * math.ceil(fill_off/2) + "|")

def pick_option (options, desc):
    # options is a list.
    selected = 0
    if len(options) > 1:
        for index, item in enumerate(options):
            print (str(index) + ": " + str(item), file=sys.stdout)
        print("Enter a number to select " + str(desc) + "\nType 'exit' to quit.", file=sys.stdout)
        while True:
            selected = input('--> ')
            if selected.lower() == 'exit':
                #print("Exiting...", file=sys.stdout)
                return None
            # Determine if the entered string is a number.
            if selected.isdigit():
                selected = int(selected)
                if selected > len(options) - 1 or selected < 0:
                    print (str(selected) + " is not a valid value!", file=sys.stdout)
                else:
                    break
            else:
                print(str(selected) + " is not a valid value!", file=sys.stdout)
    return selected

def main():
    alg_entries = find_valid_plugins(algorithms)
    matchup_list = find_valid_matchups('types')
    # If there are no valid type matchups or algorithms, then exit the program
    # as it can't run.
    to_exit = False
    if len(matchup_list) == 0:
        print ("No Valid Entry Found For Type Matchups!", file=sys.stdout)
        to_exit = True
    if len(alg_entries) == 0:
        print ("No Valid Entry Found For Algorithms!", file=sys.stdout)
        to_exit = True
    if to_exit:
        print("Exiting...", file=sys.stdout)
        sys.exit(0)
    selected_matchup = pick_option([x['name'] for x in matchup_list if x['name']], "a matchup")
    if selected_matchup == None:
        print("Exiting...", file=sys.stdout)
        sys.exit(0)
    alg = pick_option([x['name'] for x in alg_entries if x['name']], "an algorithm")
    if alg == None:
        print("Exiting...", file=sys.stdout)
        sys.exit(0)
    idata = matchup_list[selected_matchup]['matchup']
    data = tm.generate_data (idata)
    tm.generate_matchups(data['data'])
    print(alg_entries[alg]['name'])
    alg = alg_entries[alg]['class']()
    try:
        result = alg.generate_scores(data['data'])
    except Exception as e:
        print("There was an Exception in the algorithm.")
        print(e)
        sys.exit(1)
    is_valid, error = validate_table(data, result)
    if is_valid:
        generate_table(data, result)
    else:
        print("The algorithm return is not valid!", file=sys.stderr)
        print(error, file=sys.stderr)

if __name__ == "__main__":
    main()
