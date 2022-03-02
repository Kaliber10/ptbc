#!/usr/bin/env python3
if __name__ == '__main__':
   import type_matchup
else:
   import algorithms.type_matchup as type_matchup

class Raw_Calc():

    def generate_def_score(self):
        score = {}
        total = len(type_matchup.Types)
        for val in type_matchup.Types:
            rlist = type_matchup.Type_Data[val]['resistances']
            wlist = type_matchup.Type_Data[val]['weaknesses']
            ilist = type_matchup.Type_Data[val]['immunities']
            score[val] = total - (0.5 * len(rlist) + 2 * len(wlist) + (total - len(rlist) - len(wlist) - len(ilist)))
        return score

    def generate_off_score(self):
        score = {}
        total = len(type_matchup.Types)
        for val in type_matchup.Types:
            slist = type_matchup.Type_Data[val]['super']
            nlist = type_matchup.Type_Data[val]['not']
            dlist = type_matchup.Type_Data[val]['doesnt']
            score[val] = (2 * len(slist) + 0.5 * len(nlist) + (total - len(slist) - len(nlist) - len(dlist))) - total
        return score

    def generate_scores(self):
        def_score = self.generate_def_score()
        off_score = self.generate_off_score()
        return [def_score, off_score]