#!/usr/bin/env python3

class Raw_Calc():

    def generate_def_score(self, input):
        score = {}
        total = len(input.keys())
        for val in input.keys():
            rlist = input[val]['resistances']
            wlist = input[val]['weaknesses']
            ilist = input[val]['immunities']
            score[val] = total - (0.5 * len(rlist) + 2 * len(wlist) + (total - len(rlist) - len(wlist) - len(ilist)))
        return score

    def generate_off_score(self, input):
        score = {}
        total = len(input.keys())
        for val in input.keys():
            slist = input[val]['super']
            nlist = input[val]['reduced']
            dlist = input[val]['none']
            score[val] = (2 * len(slist) + 0.5 * len(nlist) + (total - len(slist) - len(nlist) - len(dlist))) - total
        return score

    def generate_scores(self, input):
        def_score = self.generate_def_score(input)
        off_score = self.generate_off_score(input)
        return [def_score, off_score]