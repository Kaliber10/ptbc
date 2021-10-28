#!/usr/bin/env python
import sys

class Type_Matchup ():

    Types = [] # Types Names
    Type_Data = {} # Collected data populated with Types values

    @staticmethod
    def generate_data (input):
        for index, value in enumerate (input):
            Type_Matchup.Types.append(value['name'])
            Type_Matchup.Type_Data[value['name']] = {'resistances' : [],
                                        'weaknesses' : [],
                                        'immunities' : [],
                                        'super' : [],
                                        'not' : [],
                                        'doesnt' : []}

        #Populate the dictionary with Types list and input data.
        #TODO Add a check to validate that the defense arrays match the offense arrays
        #TODO Add a check to validate that a resistance can't also be a weakness/immunities, etc
        for index, value in enumerate (Type_Matchup.Types):
            try:
                for r in input[index]['resistances']:
                    # If the type is not in there, it will exception on a KeyError
                    # KeyError as e will return the key it is looking for.
                    try:
                        Type_Matchup.Type_Data[value]['resistances'].append(r)
                        Type_Matchup.Type_Data[r]['not'].append(value)
                    except KeyError:
                        print("Type " + r + " does not exist")
                        sys.exit()
                for w in input[index]['weaknesses']:
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