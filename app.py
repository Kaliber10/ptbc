#!/usr/bin/env python
import tkinter as tk

import algorithms
import algorithms.type_matchup as type_matchup
import matchup_generator

root = tk.Tk()
root.title("ptbc")

frm_selections = tk.Frame(root)
frm_selections.grid(row=1, column=0)

frm_chart = tk.Frame(root)
frm_chart.grid(row=1,column=1)

frm_algs = tk.Frame(root)
frm_algs.grid(row=2, column=0)

frm_results = tk.Frame(root, bg="#C70039")
frm_results.grid(row=2, column=1)

frm_controls = tk.Frame(root)
frm_controls.grid(row=0, columnspan=2)

matchup_list = matchup_generator.find_valid_matchups('types')
alg_list = matchup_generator.find_valid_plugins(algorithms)

def fill_chart(matchup_data : dict):
	# should I create a system where it doesn't delete everything, instead it will delete everything it doesn't need
	# and update what's left. If it needs more it adds more.
	for i in frm_chart.grid_slaves():
		i.grid_forget()
	for i in range(len(matchup_data['header'])):
		e_top = tk.Label(frm_chart, text=matchup_data['header'][i], relief=tk.RAISED, bg="#CACACA", width=3)
		e_left = tk.Label(frm_chart, text=matchup_data['header'][i], relief=tk.RAISED, bg="#CACACA", width=3)
		e_top.grid (row=0, column=i+1)
		e_left.grid (row=i+1, column=0)
	# The horizontal is the defense. The vertical is the offense.
	for i in range(len(matchup_data['matchup'])):
		for j in range(len(matchup_data['matchup'][i])):
			e = tk.Label(frm_chart, text=str(matchup_data['matchup'][i][j]), relief=tk.GROOVE, width=3)
			#Can I use highlight instead of relief for the labels?
			# Add color to the label. If it is 2x, then use green, if it is 0.5x, then use red.
			# This makes it more clear to the user what the matchup is.
			if matchup_data['matchup'][i][j] == 2:
				e['bg'] = "#5EFF5B"
			if matchup_data['matchup'][i][j] == 0.5:
				e['bg'] = "#FF3535"
			e.grid(row=i+1, column=j+1)


option_list = []
v = tk.IntVar(frm_selections, 0)
def update_chart():
	idata = matchup_list[v.get()]['matchup']
	type_data = type_matchup.generate_data(idata)
	fill_chart(type_matchup.generate_matchups(type_data['data']))

def create_table(frame : tk.Frame, alg : list, keys : list, max_len : int):
	tk.Label(frame, text="DEF", relief=tk.RAISED, bg="#CACACA", width=6).grid(row=0, column=1)
	tk.Label(frame, text="OFF", relief=tk.RAISED, bg="#CACACA", width=6).grid(row=0, column=2)
	for ind, val in enumerate(keys):
		tk.Label(frame, text=str(val), relief=tk.RAISED, width=max_len).grid(row=ind+1, column=0)
		tk.Label(frame, text=str(alg[0][val]), width=6).grid(row=ind+1, column=1)
		tk.Label(frame, text=str(alg[1][val]), width=6).grid(row=ind+1, column=2)

def update_table():
	idata = matchup_list[v.get()]['matchup']
	type_data = type_matchup.generate_data(idata)
	for i in range(len(alg_list)):
		frame = tk.Frame(frm_results)
		frame.grid(row=0, column=i)
		alg = alg_list[i]['class']()
		result = alg.generate_scores(type_data['data'])
		create_table(frame, result, type_data['data'].keys(), type_data['meta']['max_length'])

lbl_selection = tk.Label(frm_selections, textvariable=v)
lbl_selection.grid()
for num, value in enumerate(matchup_list):
    option_list.append(tk.Radiobutton(frm_selections, text=value['name'], variable=v, value=num, indicator=0))
    option_list[-1].grid()
other_list = []
for num, value in enumerate(alg_list):
	other_list.append(tk.Checkbutton(frm_algs, text=value['name'], variable=num))
	other_list[-1].grid()
update_button = tk.Button(frm_controls, text="Update", command=update_chart)
update_button.grid(row=0, column=0)
quit_button = tk.Button(frm_controls, text='Quit', command=root.quit)
quit_button.grid(row=0, column=1)
update_chart()
update_table()
root.mainloop()