#!/usr/bin/env python
import tkinter as tk
import algorithms.type_matchup as type_matchup
import matchup_generator

root = tk.Tk()
root.title("ptbc")
frm_selections = tk.Frame(root)
frm_selections.grid(row=0,column=0)

frm_chart = tk.Frame(root)
frm_chart.grid(row=0,column=1)

frm_controls = tk.Frame(root)
frm_controls.grid(row=0, column=0)

test_matchup = [
{
	"name" : "Fire",
	"resistances" : ["Grass", "Fire"],
	"weaknesses"  : ["Water"],
	"immunities"  : []
},
{
	"name" : "Grass",
	"resistances" : ["Water","Grass"],
	"weaknesses"  : ["Fire"],
	"immunities"  : []
},
{
	"name" : "Normal",
	"resistances" : [],
	"weaknesses"  : [],
	"immunities"  : []
},
{
	"name" : "Water",
	"resistances" : ["Fire","Water"],
	"weaknesses"  : ["Grass"],
	"immunities"  : []
}
]

matchup_list = matchup_generator.find_valid_matchups('types')

type_test = type_matchup.generate_data(test_matchup)
matchup_data = type_matchup.generate_matchups(type_test['data'])

def updateChart(matchup_data : dict):
	# should I create a system where it doesn't delete everything, instead it will delete everything it doesn't need
	# and update what's left. If it needs more it adds more.
	for i in frm_chart.grid_slaves():
		i.grid_forget()
	for i in range(len(matchup_data['header'])):
		e_top = tk.Label(frm_chart, text=matchup_data['header'][i], relief=tk.RAISED, bg="#CACACA", width=3)
		e_left = tk.Label(frm_chart, text=matchup_data['header'][i], relief=tk.RAISED, bg="#CACACA", width=3)
		e_top.grid (row=0, column=i+1)
		e_left.grid (row=i+1, column=0)
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
def xxx():
	idata = matchup_list[v.get()]['matchup']
	type_data = type_matchup.generate_data(idata)
	matchup_data = type_matchup.generate_matchups(type_data['data'])
	updateChart(matchup_data)

lbl_selection = tk.Label(frm_selections, textvariable=v)
lbl_selection.grid()
for num, value in enumerate(matchup_list):
    option_list.append(tk.Radiobutton(frm_selections, text=value['name'], variable=v, value=num, indicator=0))
    option_list[-1].grid()
update_button = tk.Button(frm_selections, text="Update", command=xxx)
update_button.grid()
quit_button = tk.Button(frm_selections, text='Quit', command=root.quit)
quit_button.grid()
xxx()
root.mainloop()