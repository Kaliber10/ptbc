#!/usr/bin/env python3
if __name__ == '__main__':
   from type_matchup import Type_Matchup
else:
   from algorithms.type_matchup import Type_Matchup
#from algorithm import Algorithm
#from type_matchup import Type_Matchup

class Weighted_Calc():

    _off_weight = 0.0
    _def_weight = 0.0

    def _offensive_weight(self, val):
        if val >= self._off_weight:
            return 2
        else:
            return 1
            
    def _defensive_weight(self, val):
        if val >= self._def_weight:
            return 2
        else:
            return 1

    def _weighted_average(self, o_input, dlist, outlier):
        off_list = []
        def_list = []
        for val in Type_Matchup.Types:
            off_list.append(o_input[val])
            def_list.append(dlist[val])
        off_list.sort()
        def_list.sort()

        _off_weight = abs(sum (off_list[outlier:len(off_list)-outlier])/len(off_list) - 2 * outlier)
        _def_weight = abs(sum (def_list[outlier:len(def_list)-outlier])/len(def_list) - 2 * outlier)

    def _generate_raw_def(self):
        score = {}
        total = len(Type_Matchup.Types)
        for val in Type_Matchup.Types:
            rlist = Type_Matchup.Type_Data[val]['resistances']
            wlist = Type_Matchup.Type_Data[val]['weaknesses']
            ilist = Type_Matchup.Type_Data[val]['immunities']
            score[val] = total - (0.5 * len(rlist) + 2 * len(wlist) + (total - len(rlist) - len(wlist) - len(ilist)))
        return score

    def _generate_raw_off(self):
        score = {}
        total = len(Type_Matchup.Types)
        for val in Type_Matchup.Types:
            slist = Type_Matchup.Type_Data[val]['super']
            nlist = Type_Matchup.Type_Data[val]['not']
            dlist = Type_Matchup.Type_Data[val]['doesnt']
            score[val] = (2 * len(slist) + 0.5 * len(nlist) + (total - len(slist) - len(nlist) - len(dlist))) - total
        return score

    def _generate_table(self, o_input, d_input):
        off_list = {}
        def_list = {}
        #arr = [[0 for x in range(2)] for y in range(len(Types))]
        for val in Type_Matchup.Types:
            total = len(Type_Matchup.Types)
            d_score = 0
            rlist = Type_Matchup.Type_Data[val]['resistances']
            wlist = Type_Matchup.Type_Data[val]['weaknesses']
            ilist = Type_Matchup.Type_Data[val]['immunities']
            for i in rlist:
                d_score += 0.5 / self._offensive_weight(o_input[i])
            for i in wlist:
                d_score += 2 + self._offensive_weight(o_input[i]) - 1
            # This algorithm should also compensate for being neutral effective against good types.
            d_score += total - len(rlist) - len(wlist) - len(ilist)
            def_list[val] = total - d_score
        for val in Type_Matchup.Types:
            total = len(Type_Matchup.Types)
            o_score = 0
            slist = Type_Matchup.Type_Data[val]['super']
            nlist = Type_Matchup.Type_Data[val]['not']
            dlist = Type_Matchup.Type_Data[val]['doesnt']
            for i in slist:
                o_score += 2 + self._defensive_weight(d_input[i]) - 1
            for i in nlist:
                o_score += 0.5 / self._defensive_weight(d_input[i])
            o_score += total - len(slist) - len(nlist) - len(dlist)
            off_list[val] = o_score - total
        return def_list, off_list

    def generate_scores(self):
        def_score = self._generate_raw_def()
        off_score = self._generate_raw_off()
        self._weighted_average(off_score, def_score, 2)
        def_score, off_score = self._generate_table(off_score, def_score)
        return [def_score, off_score]