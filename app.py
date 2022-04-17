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

frm_results = tk.Frame(root)
frm_results.grid(row=2, column=1)

frm_controls = tk.Frame(root)
frm_controls.grid(row=0, columnspan=2)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

matchup_list = matchup_generator.find_valid_matchups('types')
alg_list = matchup_generator.find_valid_plugins(algorithms)

def fill_chart(matchup_data : dict):
	# should I create a system where it doesn't delete everything, instead it will delete everything it doesn't need
	# and update what's left. If it needs more it adds more.
	for i in frm_chart.grid_slaves():
		i.grid_forget()
	for i in range(len(matchup_data['header'])):
		e_top = tk.Label(frm_chart, text=matchup_data['header'][i], relief=tk.RAISED, bg="#CACACA", width=3, font=("TkDefaultFont", 12))
		e_left = tk.Label(frm_chart, text=matchup_data['header'][i], relief=tk.RAISED, bg="#CACACA", width=3, font=("TkDefaultFont", 12))
		e_top.grid (row=0, column=i+1)
		e_left.grid (row=i+1, column=0)
	# The horizontal is the defense. The vertical is the offense.
	for i in range(len(matchup_data['matchup'])):
		for j in range(len(matchup_data['matchup'][i])):
			e = tk.Label(frm_chart, text=str(matchup_data['matchup'][i][j]), relief=tk.GROOVE, width=3, font=("TkDefaultFont", 12))
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
cur_selection = tk.IntVar(frm_selections, 0)
def update_chart():
	idata = matchup_list[v.get()]['matchup']
	type_data = type_matchup.generate_data(idata)
	fill_chart(type_matchup.generate_matchups(type_data['data']))

def create_table(frame : tk.Frame, name : str, alg : list, keys : list, max_len : int):
	tk.Label(frame, text=name, font=("TkDefaultFont", 12)).grid(row=0, columnspan=3)
	tk.Label(frame, text="DEF", relief=tk.RAISED, bg="#CACACA", width=6, font=("TkDefaultFont", 12)).grid(row=1, column=1)
	tk.Label(frame, text="OFF", relief=tk.RAISED, bg="#CACACA", width=6, font=("TkDefaultFont", 12)).grid(row=1, column=2)
	for ind, val in enumerate(keys):
		tk.Label(frame, text=str(val), relief=tk.RAISED, width=max_len, font=("TkDefaultFont", 12)).grid(row=ind+2, column=0)
		tk.Label(frame, text=str(alg[0][val]), width=6, font=("TkDefaultFont", 12)).grid(row=ind+2, column=1)
		tk.Label(frame, text=str(alg[1][val]), width=6, font=("TkDefaultFont", 12)).grid(row=ind+2, column=2)

def update_table():
	option_list[cur_selection.get()]['state'] = tk.NORMAL
	option_list[cur_selection.get()]['bg'] = "SystemButtonFace"
	option_list[cur_selection.get()]['selectcolor'] = "SystemWindow"
	option_list[v.get()]['state'] = tk.DISABLED
	option_list[v.get()]['bg'] = "#88FF7E"
	option_list[v.get()]['selectcolor'] = "#88FF7E"
	cur_selection.set(v.get())
	idata = matchup_list[v.get()]['matchup']
	type_data = type_matchup.generate_data(idata)
	for i in frm_results.grid_slaves():
		i.grid_forget()
	selected_alg = [ind for ind, val in enumerate(other_list) if val[1].get() == 1]
	for i in range(len(selected_alg)):
		frame = tk.Frame(frm_results,highlightbackground="black", highlightthickness=2)
		frame.grid(row=0, column=i)
		alg = alg_list[selected_alg[i]]['class']()
		result = alg.generate_scores(type_data['data'])
		create_table(frame, alg_list[selected_alg[i]]['name'], result, type_data['data'].keys(), type_data['meta']['max_length'])

def configure_min_size():
	root.update()
	fin_width = 0
	fin_height = 0
	fin_width = max(frm_selections.winfo_width(), frm_algs.winfo_width()) + max(frm_chart.winfo_width(), frm_results.winfo_width())
	fin_height = frm_controls.winfo_height() + max(frm_selections.winfo_height(), frm_chart.winfo_height()) + max(frm_algs.winfo_height(), frm_results.winfo_height())
	root.minsize(width=fin_width, height=fin_height)

def update():
	update_button['bg'] = "SystemButtonFace"
	update_chart()
	update_table()
	configure_min_size()

def check_for_update():
	if v.get() != cur_selection.get():
		update_button['bg'] = "#FFFD58"


nn = len(max([n['name'] for n in matchup_list], key=len))
for num, value in enumerate(matchup_list):
    option_list.append(tk.Radiobutton(frm_selections, text=value['name'], variable=v, width = nn, value=num, indicator=0, command=check_for_update, font=("TkDefaultFont", 12)))
    option_list[-1].grid()
other_list = []
for num, value in enumerate(alg_list):
	ck_var = tk.IntVar()
	other_list.append([tk.Checkbutton(frm_algs, text=value['name'], variable=ck_var, font=("TkDefaultFont", 12)), ck_var])
	other_list[-1][0].grid()
update_button = tk.Button(frm_controls, text="Update", command=update)
update_button.grid(row=0, column=0)
quit_button = tk.Button(frm_controls, text='Quit', command=root.quit)
quit_button.grid(row=0, column=1)
update()
root.mainloop()