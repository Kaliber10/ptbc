#!/usr/bin/env python3

class No_Score():

    def generate_def_score(self):
        score = {}
        l = []
        dict = {}
        total = len(l)
        for val in l:
            rlist = dict[val]['resistances']
            wlist = dict[val]['weaknesses']
            ilist = dict[val]['immunities']
            score[val] = total - (0.5 * len(rlist) + 2 * len(wlist) + (total - len(rlist) - len(wlist) - len(ilist)))
        return score

    def generate_off_score(self):
        score = {}
        l = []
        total = len(l)
        for val in l:
            slist = dict[val]['super']
            nlist = dict[val]['not']
            dlist = dict[val]['doesnt']
            score[val] = (2 * len(slist) + 0.5 * len(nlist) + (total - len(slist) - len(nlist) - len(dlist))) - total
        return score