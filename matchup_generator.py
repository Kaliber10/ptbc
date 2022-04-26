#!/usr/bin/env python3
import json
import math
import os
import sys
import importlib
import inspect
import pkgutil
import threading
import time

import algorithms

def _max_length(input):
    max_len = 0
    for t in input:
        max_len = max(max_len, len(t))
    return max_len
    
# Validate the data given. This is called to check if a json file is valid. If not,
# the file will be removed from the list.
# Ensure that:
# There are no duplicate entries between Resistances, Weaknesses and Immunities
# Every value in Resistances, Weaknesses and Immunities has an equivalent type.
def validate_input (input):
    valid = False
    error_list = []
    
    if type(input) == list:
        if len(input) > 40:
            error_list.append("More than 40 types is not allowed.\n")
        # Make this a lower(), so that casing is not important. Adjust the validate.
        l_type_names = [x['name'] for x in input if 'name' in x]
        v_types = [x['name'].lower() for x in input if 'name' in x]
        # This is just an example, it should be integrated better
        # It could be nice enough to find the duplicates for you.
        t_name_set = set(v_types)
        if len(t_name_set) != len(v_types):
            err_string = "Duplicate Types Given in List.\n"
            dup_set = set()
            dup_dict = {}
            for index, value in enumerate(v_types):
                if value in dup_dict:
                    dup_dict[value].append(index)
                    dup_set.add(value)
                else:
                    dup_dict[value] = [index]
            if len(dup_set) > 0:
                for item in dup_set:
                    for i in dup_dict[item]:
                        err_string += l_type_names[i] + ","
            # Remove the last comma
            err_string = err_string[0:-1]
            error_list.append(err_string)
            del err_string, dup_set, dup_dict
        del t_name_set
        # 0 is resistances
        # 1 is weaknesses
        # 2 is immunities
        #There doesn't need to be a key_list for each type, Since it runs in one go.
        key_list = {t:[False, False, False] for t in v_types}
        for index, value in enumerate (v_types):
            if 'resistances' in input[index]:
                key_list[value][0] = True
                for r_val in input[index]['resistances']:
                    if not r_val.lower() in v_types:
                        error_list.append (r_val + " in resistance of " + l_type_names[index] + " does not exist in the list of types.")       
            else:
                if 'resistances'.upper() in (key.upper() for key in input[index].keys()):
                    error_list.append ("Wrong casing for 'resistances' in type " + l_type_names[index] + ".")
                else:
                    error_list.append ("Missing entry 'resistances' in type " + l_type_names[index] + ".")
                    
            if 'weaknesses' in input[index]:
                key_list[value][1] = True
                for w_val in input[index]['weaknesses']:
                    if not w_val.lower() in v_types:
                        error_list.append (w_val + " in weakness of " + l_type_names[index] + " does not exist in the list of types.")
            else:
                if 'weaknesses'.upper() in (key.upper() for key in input[index].keys()):
                    error_list.append ("Wrong casing for 'weaknesses' in type " + l_type_names[index] + ".")
                else:
                    error_list.append ("Missing entry 'weaknesses' in type " + l_type_names[index] + ".")
                    
            if 'immunities' in input[index]:
                key_list[value][2] = True
                for i_val in input[index]['immunities']:
                    if not i_val.lower() in v_types:
                        error_list.append (i_val + " in immunities of " + l_type_names[index] + " does not exist in the list of types.")
            else:
                if 'immunities'.upper() in (key.upper() for key in input[index].keys()):
                    error_list.append ("Wrong casing for 'immunities' in type " + l_type_names[index] + ".")
                else:
                    error_list.append ("Missing entry 'immunities' in type " + l_type_names[index] + ".")
        #Check for duplicate entries
        for index, value in enumerate (v_types):
            if key_list[value][0]:
                for r_val in set(input[index]['resistances']):
                    count = 0
                    for r2_val in input[index]['resistances']:
                        if r_val.upper() == r2_val.upper():
                            count = count + 1
                    if count > 1:
                        error_list.append ("Duplicate Entry " + r_val + " in Resistances in entry " + l_type_names[index] + ".")
                    if key_list[value][1]:
                        if r_val.upper() in (w_val.upper() for w_val in set(input[index]['weaknesses'])):
                            error_list.append ("Duplicate Entry " + r_val + " in Resistances and Weaknesses in entry " + l_type_names[index] + ".")
                    if key_list[value][2]:
                        if r_val.upper() in (i_val.upper() for i_val in set(input[index]['immunities'])):
                            error_list.append ("Duplicate Entry " + r_val + " in Resistances and Immunities in entry " + l_type_names[index] + ".")
                    del count
            if key_list[value][1]:
                for w_val in set(input[index]['weaknesses']):
                    count = 0
                    for w2_val in input[index]['weaknesses']:
                        if w_val.upper() == w2_val.upper():
                            count = count + 1
                    if count > 1:
                        error_list.append ("Duplicate Entry " + w_val + " in Weaknesses in entry " + l_type_names[index] + ".")
                    if key_list[value][2]:
                        if w_val.upper() in (i_val.upper() for i_val in set(input[index]['immunities'])):
                            error_list.append ("Duplicate Entry " + w_val + " in Weaknesses and Immunities in entry " + l_type_names[index] + ".")
                    del count
            if key_list[value][2]:
                for i_val in set(input[index]['immunities']):
                    count = 0
                    for i2_val in input[index]['immunities']:
                        if i_val.upper() == i2_val.upper():
                            count = count + 1
                    if count > 1:
                        error_list.append ("Duplicate Entry " + i_val + " in Immunities in entry " + l_type_names[index] + ".")
                    del count
        del v_types, key_list, l_type_names
    else:
        error_list.append ("The input is not a list.")
    
    # If there are any errors added, then the input must not be valid.
    if len(error_list) > 0:
        valid = False
    else:
        valid = True
    return valid, error_list

def generate_data (input):
    # Reset the data
    Types = []
    Type_Data = {}
    Type_Data['data'] = {}
    Type_Data['meta'] = {}
    for index, value in enumerate (input):
        Types.append(value['name'])
        # Change to Super, Reduced, None
        Type_Data['data'][value['name']] = {'resistances' : [],
                                    'weaknesses' : [],
                                    'immunities' : [],
                                    'super' : [],
                                    'reduced' : [],
                                    'none' : []}

    #Populate the dictionary with Types list and input data.
    for index, value in enumerate (Types):
        for r in input[index]['resistances']:
            Type_Data['data'][value]['resistances'].append(r)
            Type_Data['data'][r]['reduced'].append(value)
        for w in input[index]['weaknesses']:
            Type_Data['data'][value]['weaknesses'].append(w)
            Type_Data['data'][w]['super'].append(value)
        for i in input[index]['immunities']:
            Type_Data['data'][value]['immunities'].append(i)
            Type_Data['data'][i]['none'].append(value)
    
    Type_Data['meta']['max_length'] = _max_length(Types)
    del Types
    return Type_Data
    
# Generate the matchup chart for the types.
def generate_matchups(Data : dict):
    chart = {"header" : [],
             "matchup" : []}
    # Probably alphabetize the keys to make it easier
    # to find duplicates.
    for type in Data.keys():
        if type[0:3] in chart["header"]:
            chart["header"].append(type[0:2] + type[4])
            print("Error: Potential Duplicate Names")
        else:
            chart["header"].append(type[0:3])
    type_index_map = {type: index for index, type in enumerate(Data.keys())}
    for index, type in enumerate(Data.keys()):
        chart['matchup'].append([1 for i in Data.keys()])
        for j in Data[type]['super']:
            chart['matchup'][index][type_index_map[j]] = 2
        for j in Data[type]['reduced']:
            chart['matchup'][index][type_index_map[j]] = 0.5
        for j in Data[type]['none']:
            chart['matchup'][index][type_index_map[j]] = 0
    return chart

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
                    valid, errs = validate_input(data_in)
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

def thread_caller (input):
    input['result'] = input['algorithm'](input['data'])

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
    data = generate_data (idata)
    chart = generate_matchups(data['data'])
    print("   |", end="")
    for type in chart['header']:
        print (type.capitalize(), end="|")
    print("")
    for ind in range(len(chart['matchup'])):
        print (chart['header'][ind].capitalize(), end="|")
        for jnd in range(len(chart['matchup'][ind])):
            val = str(chart['matchup'][ind][jnd])
            if len(val) < 3:
                val = ' ' * math.ceil((3 - len(val)) / 2) + val + ' ' * math.floor((3 - len(val)) / 2)
            print (val + "|", end="")
        print("")
    print(alg_entries[alg]['name'])
    alg = alg_entries[alg]['class']()
    pass_info = {"data" : data["data"],
                 "result" : None,
                 "algorithm" : alg.generate_scores}
    x = threading.Thread(target=thread_caller, args=(pass_info,))
    start_time = time.perf_counter()
    try:
        x.start()
        success = False
        while True:
            if x.is_alive() and (time.perf_counter() - start_time >= 60):
                break
            elif not x.is_alive():
                break
        result = pass_info["result"]
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
