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
        
    @staticmethod
    def _check_for_dups(li):
        return None
        
    # Validate the data given. This is called to check if a json file is valid. If not,
    # the file will be removed from the list.
    # Ensure that:
    # There are no duplicate entries between Resistances, Weaknesses and Immunities
    # Every value in Resistances, Weaknesses and Immunities has an equivalent type.
    def validate_input (input):
        valid = False
        error_list = []
        
        
        if type(input) == list:
            # Should the casing requirement be removed, and just be handled. . .?
            # Make this a lower(), so that casing is not important. Adjust the validate.
            l_type_names = [x['name'] for x in input if 'name' in x]
            v_types = [x['name'].lower() for x in input if 'name' in x]
            # This is just an example, it should be integrated better
            # It could be nice enough to find the duplicates for you.
            t_name_set = set(v_types)
            if len(t_name_set) != len(v_types):
                err_string = "Duplicate Types Given in List\n"
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
                            error_list.append (r_val + " in resistance of " + value + " does not exist in the list of types.")       
                else:
                    if 'resistances'.upper() in (key.upper() for key in input[index].keys()):
                        error_list.append ("Wrong casing for 'resistances' in type " + l_type_names[index])
                    else:
                        error_list.append ("Missing entry 'resistances' in type " + l_type_names[index])
                        
                if 'weaknesses' in input[index]:
                    key_list[value][1] = True
                    for w_val in input[index]['weaknesses']:
                        if not w_val.lower() in v_types:
                            error_list.append (w_val + " in weakness of " + value + " does not exist in the list of types.")
                else:
                    if 'weaknesses'.upper() in (key.upper() for key in input[index].keys()):
                        error_list.append ("Wrong casing for 'weaknesses' in type " + l_type_names[index])
                    else:
                        error_list.append ("Missing entry 'weaknesses' in type " + l_type_names[index])
                        
                if 'immunities' in input[index]:
                    key_list[value][2] = True
                    for i_val in input[index]['immunities']:
                        if not i_val.lower() in v_types:
                            error_list.append (i_val + " in immunities of " + value + " does not exist in the list of types.")
                else:
                    if 'immunities'.upper() in (key.upper() for key in input[index].keys()):
                        error_list.append ("Wrong casing for 'immunities' in type " + l_type_names[index])
                    else:
                        error_list.append ("Missing entry 'immunities' in type " + l_type_names[index])
            #Check for duplicate entries
            for index, value in enumerate (v_types):
                if key_list[value][0]:
                    for r_val in set(input[index]['resistances']):
                        count = 0
                        for r2_val in input[index]['resistances']:
                            if r_val.upper() == r2_val.upper():
                                count = count + 1
                        if count > 1:
                            error_list.append ("Duplicate Entry " + r_val + " in Resistances in entry " + value + ".")
                        if key_list[value][1]:
                            if r_val.upper() in (w_val.upper() for w_val in set(input[index]['weaknesses'])):
                                error_list.append ("Duplicate Entry " + r_val + " in Resistances and Weaknesses in entry " + value + ".")
                        if key_list[value][2]:
                            if r_val.upper() in (i_val.upper() for i_val in set(input[index]['immunities'])):
                                error_list.append ("Duplicate Entry " + r_val + " in Resistances and Immunities in entry " + value + ".")
                        del count
                if key_list[value][1]:
                    for w_val in set(input[index]['weaknesses']):
                        count = 0
                        for w2_val in input[index]['weaknesses']:
                            if w_val.upper() == w2_val.upper():
                                count = count + 1
                        if count > 1:
                            error_list.append ("Duplicate Entry " + w_val + " in Weaknesses in entry " + value + ".")
                        if key_list[value][2]:
                            if w_val.upper() in (i_val.upper() for i_val in set(input[index]['immunities'])):
                                error_list.append ("Duplicate Entry " + w_val + " in Weaknesses and Immunities in entry " + value + ".")
                        del count
                if key_list[value][2]:
                    for i_val in set(input[index]['immunities']):
                        count = 0
                        for i2_val in input[index]['immunities']:
                            if i_val.upper() == i2_val.upper():
                                count = count + 1
                        if count > 1:
                            error_list.append ("Duplicate Entry " + i_val + " in Immunities in entry " + value + ".")
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
                    Type_Matchup.Type_Data[value]['resistances'].append(r)
                    Type_Matchup.Type_Data[r]['not'].append(value)
                for w in input[index]['weaknesses']:
                    Type_Matchup.Type_Data[value]['weaknesses'].append(w)
                    Type_Matchup.Type_Data[w]['super'].append(value)
                for i in input[index]['immunities']:
                    Type_Matchup.Type_Data[value]['immunities'].append(i)
                    Type_Matchup.Type_Data[i]['doesnt'].append(value)
            except KeyError as e:
                print("Missing '" + str(e) + "' Entry")
                sys.exit()
        Type_Matchup._max_length()