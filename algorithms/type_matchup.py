#!/usr/bin/env python
import sys

#Error Codes:
#1 :
#2 :
class Type_Matchup ():

    Types = [] # Types Names
    Type_Data = {} # Collected data populated with Types values
    Max_Char_Length = 0
    
    @staticmethod
    def _max_length():
        max_len = 0
        for t in Type_Matchup.Types:
            max_len = max(max_len, len(t))
        Type_Matchup.Max_Char_Length = max_len
        
    # Validate the data given. This is called to check if a json file is valid. If not,
    # the file will be removed from the list.
    # Ensure that:
    # There are no duplicate entries between Resistances, Weaknesses and Immunities
    # Every value in Resistances, Weaknesses and Immunities has an equivalent type.
    def validate_input (input):
        valid = False
        error_list = []
        
        if type(input) == list:
            v_types = [x['name'] for x in input if 'name' in x]
            # 0 is resistances
            # 1 is weaknesses
            # 2 is immunities
            key_list = {t:[False, False, False] for t in v_types}
            for index, value in enumerate (v_types):
                if 'resistances' in input[index]:
                    key_list[0] = True
                    for r_val in input[index]['resistances']:
                        if not r_val in v_types:
                            if r_val.upper() in (t_val.upper() for t_val in v_types):
                                error_list.append ("Wrong casing for type " + t_val + " in 'resistances'")
                            else:
                                error_list.append (r_val + " does not exist in the list of types.")       
                else:
                    if 'resistances'.upper() in (key.upper() for key in input[index].keys):
                        error_list.append ("Wrong casing for 'resistances' in type " + v_types[index])
                    else:
                        error_list.append ("Missing entry 'resistances' in type " + v_types[index])
                        
                if 'weaknesses' in input[index]:
                    key_list[1] = True
                    for w_val in input[index]['weaknesses']:
                        if not w_val in v_types:
                            if w_val.upper() in (t_val.upper() for t_val in v_types):
                                error_list.append ("Wrong casing for type " + t_val + " in 'weaknesses'")
                            else:
                                error_list.append (w_val + " does not exist in the list of types.")
                else:
                    if 'weaknesses'.upper() in (key.upper() for key in input[index].keys):
                        error_list.append ("Wrong casing for 'weaknesses' in type " + v_types[index])
                    else:
                        error_list.append ("Missing entry 'weaknesses' in type " + v_types[index])
                        
                if 'immunities' in input[index]:
                    key_list[2] = True
                    for i_val in input[index]['immunities']:
                        if not i_val in v_types:
                            if i_val.upper() in (t_val.upper() for t_val in v_types):
                                error_list.append ("Wrong casing for type " + t_val + " in 'immunities'")
                            else:
                                error_list.append (i_val + " does not exist in the list of types.")
                else:
                    if 'immunities'.upper() in (key.upper() for key in input[index].keys):
                        error_list.append ("Wrong casing for 'immunities' in type " + v_types[index])
                    else:
                        error_list.append ("Missing entry 'immunities' in type " + v_types[index])
                #Check for duplicate entries
                for index, value in enumerate (v_types):
                    if key_list[value][0]:
                        for r_val in input[index]['resistances']:
                            if key_list[value][1]:
                                if r_val.upper() in (w_val.upper() for w_val in input[index]['weaknesses']):
                                    error_list.append ("Duplicate Entry " + r_val + " in Resistances and Weaknesses.")
                            if key_list[value][2]:
                                if r_val.upper() in (i_val.upper() for i_val in input[index]['immunities']):
                                    error_list.append ("Duplicate Entry " + r_val + " in Resistances and Immunities.")
                    if key_list[value][1]:
                        for w_val in input[index]['weaknesses']:
                            if key_list[value][2]:
                                if w_val.upper() in (i_val.upper() for i_val in input[index]['immunities']):
                                    error_list.append ("Duplicate Entry " + w_val + " in Weaknesses and Immunities.")

            del v_types
        else:
            error_list.append ("The input is not a dictionary.")
        
        # If there are any errors added, then the input must not be valid.
        if len(error_list) > 0:
            valid = False
        else:
            valid = True
        return valid, error_list

    @staticmethod
    def generate_data (input):
        for index, value in enumerate (input):
            Type_Matchup.Types.append(value['name'])
            # Change to Super, Reduced, None
            Type_Matchup.Type_Data[value['name']] = {'resistances' : [],
                                        'weaknesses' : [],
                                        'immunities' : [],
                                        'super' : [],
                                        'not' : [],
                                        'doesnt' : []}

        #Populate the dictionary with Types list and input data.
        for index, value in enumerate (Type_Matchup.Types):
            try:
                for r in input[index]['resistances']:
                    if r.upper() in (t.upper() for t in input[index]['weaknesses']):
                        print ("Duplicate Entry " + r + " in Resistances and Weaknesses", file=sys.stderr)
                        sys.exit(1)
                    if r.upper() in (t.upper() for t in input[index]['immunities']):
                        print ("Duplicate Entry " + r + " in Resistances and Immunities", file=sys.stderr)
                        sys.exit(1)
                    if r.upper() in (t.upper() for t in Type_Matchup.Type_Data[value]['resistances']):
                        print ("Warning : " + r + " is duplicated in Resistances.", file=sys.stderr)
                    # If the type is not in there, it will exception on a KeyError
                    # KeyError as e will return the key it is looking for.
                    try:
                        Type_Matchup.Type_Data[value]['resistances'].append(r)
                        Type_Matchup.Type_Data[r]['not'].append(value)
                    except KeyError:
                        print("Type " + r + " does not exist", file=sys.stderr)
                        sys.exit()
                for w in input[index]['weaknesses']:
                    if w.upper in (t.upper() for t in input[index]['immunities']):
                        print ("Duplicate Entry " + w + " in Weaknesses and Immunities", file=sys.stderr)
                    try:
                        Type_Matchup.Type_Data[value]['weaknesses'].append(w)
                        Type_Matchup.Type_Data[w]['super'].append(value)
                    except KeyError:
                        print("Type " + w + " does not exist")
                        sys.exit()
                for i in input[index]['immunities']:
                    try:
                        Type_Matchup.Type_Data[value]['immunities'].append(i)
                        Type_Matchup.Type_Data[i]['doesnt'].append(value)
                    except KeyError:
                        print("Type " + i + " does not exist")
                        sys.exit()
            except KeyError as e:
                print("Missing '" + str(e) + "' Entry")
                sys.exit()
        Type_Matchup._max_length()