#!usr/bin/env python3

class Type_Matchup ():
    Type_Data = {}
    Types = []
    def generate_data (self,input):
        for index, value in enumerate (input):
            self.Types.append(value['name'])
            self.Type_Data[value['name']] = {'resistances' : [],
                                        'weaknesses' : [],
                                        'immunities' : [],
                                        'super' : [],
                                        'not' : [],
                                        'doesnt' : []}

        for index, value in enumerate (self.Types):
            try:
                for r in input[index]['resistances']:
                    # If the type is not in there, it will exception on a KeyError
                    # KeyError as e will return the key it is looking for.
                    try:
                        self.Type_Data[value]['resistances'].append(r)
                        self.Type_Data[r]['not'].append(value)
                    except KeyError:
                        print("Type " + r + " does not exist")
                        exit()
                for w in input[index]['weaknesses']:
                    try:
                        self.Type_Data[value]['weaknesses'].append(w)
                        self.Type_Data[w]['super'].append(value)
                    except KeyError:
                        print("Type " + w + " does not exist")
                        exit()
                for i in input[index]['immunities']:
                    try:
                        self.Type_Data[value]['immunities'].append(i)
                        self.Type_Data[i]['doesnt'].append(value)
                    except KeyError:
                        print("Type " + i + " does not exist")
                        exit()
            except KeyError as e:
                print("Missing '" + str(e) + "' Entry")
                exit()