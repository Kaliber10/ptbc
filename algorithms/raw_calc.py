#!/usr/bin/env python3
if __name__ == '__main__':
   from type_matchup import Type_Matchup
else:
   from algorithms.type_matchup import Type_Matchup

class Raw_Calc():

    def generate_def_score(self):
        score = {}
        total = len(Type_Matchup.Types)
        for val in Type_Matchup.Types:
            rlist = Type_Matchup.Type_Data[val]['resistances']
            wlist = Type_Matchup.Type_Data[val]['weaknesses']
            ilist = Type_Matchup.Type_Data[val]['immunities']
            score[val] = total - (0.5 * len(rlist) + 2 * len(wlist) + (total - len(rlist) - len(wlist) - len(ilist)))
        return score

    def generate_off_score(self):
        score = {}
        total = len(Type_Matchup.Types)
        for val in Type_Matchup.Types:
            slist = Type_Matchup.Type_Data[val]['super']
            nlist = Type_Matchup.Type_Data[val]['not']
            dlist = Type_Matchup.Type_Data[val]['doesnt']
            score[val] = (2 * len(slist) + 0.5 * len(nlist) + (total - len(slist) - len(nlist) - len(dlist))) - total
        return score

    def generate_scores(self):
        def_score = self.generate_def_score()
        off_score = self.generate_off_score()
        return [def_score, off_score]