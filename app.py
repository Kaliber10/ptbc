#!/usr/bin/env python
import tkinter as tk
from tkinter import ttk

import algorithms
import matchup_generator

root = tk.Tk()
root.title("ptbc")

frm_selections = tk.Frame(root)
frm_selections.grid(row=1, column=0)

f_contain_chart = tk.Frame(root)
f_contain_chart.grid(row=1,column=1, sticky=tk.NSEW)
scl_chart_v = ttk.Scrollbar(f_contain_chart, orient=tk.VERTICAL)
scl_chart_h = ttk.Scrollbar(f_contain_chart, orient=tk.HORIZONTAL)
can_chart = tk.Canvas(f_contain_chart, highlightthickness=0, yscrollcommand=scl_chart_v.set, xscrollcommand=scl_chart_h.set)
can_chart.grid(row=0, column=0, sticky=tk.NSEW)
scl_chart_v['command'] = can_chart.yview
scl_chart_h['command'] = can_chart.xview
scl_chart_v.grid(row=0, column=1, sticky=(tk.NS))
scl_chart_h.grid(row=1, column=0, sticky=(tk.EW))
frm_chart = tk.Frame(can_chart)
frm_chart.grid(row=0, column=0, sticky=(tk.NSEW))
f_contain_chart.columnconfigure(0, weight=1)
f_contain_chart.rowconfigure(0, weight=1)
can_chart.create_window(0, 0, window=frm_chart, anchor=tk.NW)

frm_algs = tk.Frame(root)
frm_algs.grid(row=2, column=0)

f_contain_results = tk.Frame(root)
f_contain_results.grid(row=2, column=1, sticky=tk.NSEW)
scl_results_v = ttk.Scrollbar(f_contain_results, orient=tk.VERTICAL)
scl_results_h = ttk.Scrollbar(f_contain_results, orient=tk.HORIZONTAL)
can_results = tk.Canvas(f_contain_results, highlightthickness=0, yscrollcommand=scl_results_v.set, xscrollcommand=scl_results_h.set)
can_results.grid(row=0, column=0, sticky=tk.NSEW)
scl_results_v['command'] = can_results.yview
scl_results_h['command'] = can_results.xview
scl_results_v.grid(row=0, column=1, sticky=(tk.NS))
scl_results_h.grid(row=1, column=0, sticky=(tk.EW))
frm_results = tk.Frame(can_results)
frm_results.grid(row=0, column=0, sticky=(tk.NSEW))
f_contain_results.columnconfigure(0, weight=1)
f_contain_results.rowconfigure(0, weight=1)
can_results.create_window(0,0, window=frm_results, anchor=tk.NW)

f_contain_offense = tk.Frame(root)
f_contain_offense.grid(row=1, column=2, sticky=tk.NSEW)
scl_offense_v = ttk.Scrollbar(f_contain_offense, orient=tk.VERTICAL)
scl_offense_h = ttk.Scrollbar(f_contain_offense, orient=tk.HORIZONTAL)
can_offense = tk.Canvas(f_contain_offense, highlightthickness=0, yscrollcommand=scl_offense_v.set, xscrollcommand=scl_offense_h.set)
can_offense.grid(row=0, column=0, sticky=tk.NSEW)
scl_offense_v['command'] = can_offense.yview
scl_offense_h['command'] = can_offense.xview
scl_offense_v.grid(row=0, column=1, sticky=(tk.NS))
scl_offense_h.grid(row=1, column=0, sticky=(tk.EW))
frm_offense = tk.Frame(can_offense)
frm_offense.grid(row=0, column=0, sticky=(tk.NSEW))
f_contain_offense.columnconfigure(0, weight=1)
f_contain_offense.rowconfigure(0, weight=1)
can_offense.create_window(0,0, window=frm_offense, anchor=tk.NW)

f_contain_defense = tk.Frame(root)
f_contain_defense.grid(row=2, column=2, sticky=tk.NSEW)
scl_defense_v = ttk.Scrollbar(f_contain_defense, orient=tk.VERTICAL)
scl_defense_h = ttk.Scrollbar(f_contain_defense, orient=tk.HORIZONTAL)
can_defense = tk.Canvas(f_contain_defense, highlightthickness=0, yscrollcommand=scl_defense_v.set, xscrollcommand=scl_defense_h.set)
can_defense.grid(row=0, column=0, sticky=tk.NSEW)
scl_defense_v['command'] = can_defense.yview
scl_defense_h['command'] = can_defense.xview
scl_defense_v.grid(row=0, column=1, sticky=(tk.NS))
scl_defense_h.grid(row=1, column=0, sticky=(tk.EW))
frm_defense = tk.Frame(can_defense)
frm_defense.grid(row=0, column=0, sticky=(tk.NSEW))
f_contain_defense.columnconfigure(0, weight=1)
f_contain_defense.rowconfigure(0, weight=1)
can_defense.create_window(0,0, window=frm_defense, anchor=tk.NW)

frm_controls = tk.Frame(root)
frm_controls.grid(row=0, columnspan=3)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

matchup_list = matchup_generator.find_valid_matchups('types')
alg_list = matchup_generator.find_valid_plugins(algorithms)

def fill_chart(matchup_data : dict):
	# should I create a system where it doesn't delete everything, instead it will delete everything it doesn't need
	# and update what's left. If it needs more it adds more.
	for i in frm_chart.grid_slaves():
		i.grid_forget()

	# Add a corner piece to the type chart for aesthetic.
	e_corner = tk.Label(frm_chart, relief=tk.RAISED, bg="#CACACA", width=3)
	e_corner.grid(row=0, column=0, sticky=tk.NSEW)

	for i in range(len(matchup_data['header'])):
		e_top = tk.Label(frm_chart, text=matchup_data['header'][i], relief=tk.RAISED, bg="#CACACA", width=3, font=("TkDefaultFont", 12))
		e_left = tk.Label(frm_chart, text=matchup_data['header'][i], relief=tk.RAISED, bg="#CACACA", width=3, font=("TkDefaultFont", 12))
		e_top.grid (row=0, column=i+1)
		e_left.grid (row=i+1, column=0)
		e_top.bind('<Button-1>', on_defensive_click)
		e_left.bind('<Button-1>', on_offensive_click)
	# The horizontal is the defense. The vertical is the offense.
	for i in range(len(matchup_data['matchup'])):
		for j in range(len(matchup_data['matchup'][i])):
			e = tk.Label(frm_chart, text=str(matchup_data['matchup'][i][j]), bg="#F0F0F0", relief=tk.GROOVE, width=3, font=("TkDefaultFont", 12))
			# TODO Can I use highlight instead of relief for the labels?
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
	type_data = matchup_generator.generate_data(idata)
	fill_chart(matchup_generator.generate_matchups(type_data['data']))
	matchup_data = matchup_generator.generate_matchups(type_data['data'])
	frm_offense.data = matchup_data
	# Calculate the defensive data from the offensive data
	frm_defense.data = {'header': matchup_data['header'], "matchup": []}
	for i, _ in enumerate(matchup_data["header"]):
		defense_matchup = []
		for j in matchup_data['matchup']:
			defense_matchup.append(j[i])
		frm_defense.data['matchup'].append(defense_matchup)
	construct_header(frm_defense, matchup_data["header"])
	construct_header(frm_offense, matchup_data['header'])

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
	type_data = matchup_generator.generate_data(idata)
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
	# A minimum of 400 by 300 pixels for both the matchup chart and the algorithm results is suitable.
	min_width = 400
	min_height = 300
	# The minimum width is calculated the maximum value of each column. The controls tab is irrelevant as it won't be bigger
	# than either of the two other selections.
	fin_width = max(frm_selections.winfo_reqwidth(), frm_algs.winfo_reqwidth()) + min_width
	# The minimum height is calculated with the maximum value of each row.
	fin_height = frm_controls.winfo_reqheight() + max(frm_selections.winfo_reqheight(), min_height) + max(frm_algs.winfo_reqheight(), min_height)
	root.columnconfigure(0, minsize=max(frm_selections.winfo_reqwidth(), frm_algs.winfo_reqwidth()))
	root.rowconfigure(1, minsize=max(frm_selections.winfo_reqheight(), min_height))
	root.rowconfigure(2, minsize=max(frm_algs.winfo_reqheight(), min_height))
	root.minsize(width=fin_width, height=fin_height)

def configure_chart_size():
	# Update the scrollregion of the canvas to be the size of the newly updated chart. The scrollregion needs to be updated everytime the
	# chart is changed.
	can_chart.config(scrollregion=(0,0,frm_chart.winfo_reqwidth(), frm_chart.winfo_reqheight()))

def configure_results_size():
	# Update the scrollregion of the canvas to be the size of the newly updated chart. The scrollregion needs to be updated everytime an update
	# happens. This requires calculating the requested size of the child frames. The parent frame (frm_results),
	# will only give the number of frames that are children of it. There is no command that will give the raw row length and column height.
	# The for loop gets the width and height from the children so that any category of the display size (font, spacing) can be changed and the
	# function would still get the correct number.
	wid = 0
	hei = 0
	for i in frm_results.grid_slaves():
		wid += i.winfo_reqwidth()
		hei = max(i.winfo_reqheight(), hei)
	can_results.config(scrollregion=(0,0,wid,hei))

def construct():
	update_button['bg'] = "SystemButtonFace"
	update_chart()
	update_table()
	# The after call has to be used to position the configure_chart_size call to happen after the screen has been updated.
	# Using an event generation did not successfully update the canvas size based on the frame size.
	# Add if statement that this only changes if the chart is actually updated.
	root.after(1, func=configure_chart_size)
	root.after(100, func=configure_results_size)

def check_for_update():
	if v.get() != cur_selection.get():
		update_button['bg'] = "#FFFD58"

def on_defensive_click(event):
	# This will work for the defensive stats of a type.
	grid_num = event.widget.grid_info()['column'] - 1
	if grid_num in selected_defense:
		r = selected_defense.index(grid_num) + 1
		selected_defense.remove(grid_num)
		highlight_column(grid_num + 1, False)
		remove_selection(frm_defense, r)
	else:
		selected_defense.append(grid_num)
		highlight_column(grid_num + 1, True)
		add_selection(frm_defense, frm_defense.data, grid_num)

def on_offensive_click(event):
	# This will work for the offensive stats of a type.
	grid_num = event.widget.grid_info()['row'] - 1
	if grid_num in selected_offense:
		r = selected_offense.index(grid_num) + 1
		selected_offense.remove(grid_num)
		highlight_row(grid_num + 1, False)
		remove_selection(frm_offense, r)
	else:
		selected_offense.append(grid_num)
		highlight_row(grid_num + 1, True)
		add_selection(frm_offense, frm_offense.data, grid_num)

def on_vertical_mousewheel(widget, event):
	# This checks if the total yview is 100%. If it is, don't scroll anymore.
	if widget.yview() == (0.0, 1.0):
		return
	widget.yview_scroll(int(-1*(event.delta/120)), "units")

def on_horizontal_mousewheel(widget, event):
	# This checks if the total xview is 100%. If it is, don't scroll anymore.
	if widget.xview() == (0.0, 1.0):
		return
	widget.xview_scroll(int(-1*(event.delta/120)), "units")

def bound_to_mousewheel(event, widget):
	widget.bind_all("<MouseWheel>", lambda event, widget=widget : on_vertical_mousewheel(widget, event))
	widget.bind_all("<Shift-MouseWheel>", lambda event, widget=widget : on_horizontal_mousewheel(widget, event))

def unbound_to_mousewheel(event, widget):
	widget.unbind_all("MouseWheel>")
	widget.unbind_all("<Shift-MouseWheel>")

def construct_header(frame : tk.Frame, type_names : list):
	"""Construct the header for the offense and defense.
	Use the matchup_data to fill the frame with the list of types.
	"""
	for i in frame.grid_slaves():
		i.destroy()
	e_corner = tk.Label(frame, relief=tk.RAISED, bg="#CACACA", width=3)
	e_corner.grid(row=0, column=0, sticky=tk.NSEW)
	for i in range(len(type_names)):
		e_top = tk.Label(frame, text=type_names[i], relief=tk.RAISED, bg="#CACACA", width=3, font=("TkDefaultFont", 12))
		e_top.grid (row=0, column=i+1)

def add_selection(frame : tk.Frame, matchup_data : dict, sel : int):

	r = len(frame.grid_slaves(column=0))

	# Create the label that indicates the type.
	h = tk.Label(frame, text=matchup_data['header'][sel], relief=tk.RAISED, bg="#CACACA", width=3, font=("TkDefaultFont", 12))
	h.grid(row=r, column=0)

	for j in range(len(matchup_data['matchup'][sel])):
		e = tk.Label(frame, text=str(matchup_data['matchup'][sel][j]), bg="#F0F0F0", relief=tk.GROOVE, width=3, font=("TkDefaultFont", 12))
		e.grid(row=r, column=j+1)

def remove_selection(frame : tk.Frame, r : int):

	l = len(frame.grid_slaves(column=0))

	# Remove the row that had be unselected.
	for i in frame.grid_slaves(row=r):
		i.destroy()

	# Shift every row below the unselected row.
	for i in range(r+1, l):
		for j in frame.grid_slaves(row=i):
			j.grid_configure(row=i-1)

def highlight_column(column : int, highlight : bool):
	"""Highlight a column.
	Update the elements of a column to be highlighted or not. Will not remove a highlight for a cell whose row is highlighted.
	"""

	# 0 : header
	# 1 : normal
	# 2 : super
	# 3 : not
	# 4 : foreground
	COLORS = {"selected" : ("#353535", "#d6d6d6", "#2CFF29", "#ff0000", "#ffffff"), "not_selected" : ("#CACACA", "#F0F0F0", "#5EFF5B","#FF3535", "#000000")}
	for i in frm_chart.grid_slaves(column=column):
		if i.grid_info()['row'] == 0:
			if highlight:
				i.configure(fg=COLORS['selected'][4], bg=COLORS['selected'][0], relief=tk.RIDGE)
			else:
				i.configure(fg=COLORS["not_selected"][4], bg=COLORS["not_selected"][0], relief=tk.RAISED)
		else:
			if highlight:
				if i['text'] == "2":
					i.configure(bg=COLORS['selected'][2])
				elif i['text'] == "0.5":
					i.configure(bg=COLORS['selected'][3])
				else:
					i.configure(bg=COLORS['selected'][1])
				i.configure(relief=tk.RIDGE, fg=COLORS["selected"][4])
			else:
				if i.grid_info()['row'] - 1 not in selected_offense:
					if i['text'] == "2":
						i.configure(bg=COLORS['not_selected'][2])
					elif i['text'] == "0.5":
						i.configure(bg=COLORS['not_selected'][3])
					else:
						i.configure(bg=COLORS['not_selected'][1])
					i.configure(relief=tk.GROOVE, fg=COLORS["not_selected"][4])
		i.configure(font="TkDefaultFont 12")

def highlight_row (row : int, highlight : bool):
	"""Highlight a row.
	Update the elements of a row to be highlighted or not. Will not remove a highlight for a cell whose column is highlighted.
	"""

	# 0 : header
	# 1 : normal
	# 2 : super
	# 3 : not
	# 4 : foreground
	COLORS = {"selected" : ("#353535", "#d6d6d6", "#2CFF29", "#ff0000", "#ffffff"), "not_selected" : ("#CACACA", "#F0F0F0", "#5EFF5B","#FF3535", "#000000")}
	for i in frm_chart.grid_slaves(row=row):
		if i.grid_info()['column'] == 0:
			if highlight:
				i.configure(fg=COLORS['selected'][4], bg=COLORS['selected'][0], relief=tk.RIDGE)
			else:
				i.configure(fg=COLORS["not_selected"][4], bg=COLORS["not_selected"][0], relief=tk.RAISED)
		else:
			if highlight:
				if i['text'] == "2":
					i.configure(bg=COLORS['selected'][2])
				elif i['text'] == "0.5":
					i.configure(bg=COLORS['selected'][3])
				else:
					i.configure(bg=COLORS['selected'][1])
				i.configure(relief=tk.RIDGE, fg=COLORS["selected"][4])
			else:
				if i.grid_info()['column'] - 1 not in selected_defense:
					if i['text'] == "2":
						i.configure(bg=COLORS['not_selected'][2])
					elif i['text'] == "0.5":
						i.configure(bg=COLORS['not_selected'][3])
					else:
						i.configure(bg=COLORS['not_selected'][1])
					i.configure(relief=tk.GROOVE, fg=COLORS["not_selected"][4])
		i.configure(font="TkDefaultFont 12")

nn = len(max([n['name'] for n in matchup_list], key=len))
for num, value in enumerate(matchup_list):
    option_list.append(tk.Radiobutton(frm_selections, text=value['name'], variable=v, width = nn, value=num, indicator=0, command=check_for_update, font=("TkDefaultFont", 12)))
    option_list[-1].grid(sticky=tk.EW)
other_list = []
for num, value in enumerate(alg_list):
	ck_var = tk.IntVar()
	other_list.append([tk.Checkbutton(frm_algs, text=value['name'], variable=ck_var, font=("TkDefaultFont", 12)), ck_var])
	other_list[-1][0].grid(sticky=tk.EW)
update_button = tk.Button(frm_controls, text="Update", command=construct)
update_button.grid(row=0, column=0)
quit_button = tk.Button(frm_controls, text='Quit', command=root.quit)
quit_button.grid(row=0, column=1)
construct()
# Call to configure the minimum size after the mainloop has started so that the width/height of the frames can be calculated correctly.
# This must be done with an .after call. An event generation occurs too early to get the proper width/height.
root.after(1, configure_min_size)
# Only bind the mousewheel when the mouse is within the area of widget.
can_chart.bind('<Enter>', lambda event, widget=can_chart: bound_to_mousewheel(event, widget))
can_chart.bind('<Leave>', lambda event, widget=can_chart: unbound_to_mousewheel(event, widget))
can_results.bind('<Enter>', lambda event, widget=can_results: bound_to_mousewheel(event, widget))
can_results.bind('<Leave>', lambda event, widget=can_results: unbound_to_mousewheel(event, widget))
# Used to identify what type was selected for highlighting, separated based on offense and defense as those are independent.
selected_defense = []
selected_offense = []
root.mainloop()
