#! /usr/bin/env python
import json
import sys
sys.path.append("../algorithms")
sys.path.append("../")
import type_matchup
import matchup_generator
import io

import alg_a
import alg_b
import alg_e

print("Errors above are on import")

# Test 1a
print("Testing 1")
results = matchup_generator.find_valid_matchups('e_types')

assert len(results) == 0, str(len(results))
print("Success!")

# Test 2a - 2b
print("Testing 2")
save_err = sys.stderr
sys.stderr = io.StringIO()
results = matchup_generator.find_valid_matchups('types_invalid')
t2_err = sys.stderr
sys.stderr = save_err
t2_err.seek(0)
err_list = t2_err.readlines()
 
assert len(results) == 0, str(len(results))
assert err_list[0] == "Error Found in Type_Matchup-Bad_Syntax.json:\n", err_list[0]
assert err_list[1] == "Expecting ',' delimiter: line 3 column 10 (char 26)\n", err_list[1]
assert err_list[3] == "Error Found in Type_Matchup-No_Matchup.json\n", err_list[3]
assert err_list[4] == "Missing 'matchups' Value.\n", err_list[4]
print("Success!")

t2_err.close()

print("Testing find_valid_matchups")
save_err = sys.stderr
sys.stderr = io.StringIO()
results = matchup_generator.find_valid_matchups('types_test')
sys.stderr = save_err

assert len(results) == 1, str(len(results))
assert results[0]['name'] == "Type_Matchup_Simple.json", results[0]['name']
print("Success!")

print("Testing Matchup Files")
# Test 2c
print("Testing Not_List")
f_test = open("types_test/Type_Matchup-Not_List.json", "r")

data_in = json.load(f_test)['matchups']

valid, errs = type_matchup.validate_input(data_in)

assert valid == False
assert errs[0] == "The input is not a list."

f_test.close()
print("Success!")

# Test 2d
print("Testing Missing_Entries")
f_test = open("types_test/Type_Matchup-Missing_Entries.json", "r")

data_in = json.load(f_test)['matchups']

valid, errs = type_matchup.validate_input(data_in)

assert valid == False, "Failure on Missing_Entries"
assert errs[0] == "Missing entry 'weaknesses' in type Fire."
assert errs[1] == "Missing entry 'resistances' in type Grass."
assert errs[2] == "Missing entry 'immunities' in type Normal."

f_test.close()
print("Success!")

# Test 2e
print("Testing Entry_Case")
f_test = open("types_test/Type_Matchup-Entry_Case.json")

data_in = json.load(f_test)['matchups']

valid, errs = type_matchup.validate_input(data_in)

assert valid == False, "Failure on Entry_Case"
assert errs[0] == "Wrong casing for 'weaknesses' in type Fire."
assert errs[1] == "Wrong casing for 'resistances' in type Normal."
assert errs[2] == "Wrong casing for 'immunities' in type Water."

f_test.close()
print("Success!")

# Test 2f
print("Testing Invalid_Type")
f_test = open("types_test/Type_Matchup-Invalid_Type.json")

data_in = json.load(f_test)['matchups']

valid, errs = type_matchup.validate_input(data_in)

assert valid == False, "Failure on Invalid_Type"
assert errs[0] == "Flying in weakness of Grass does not exist in the list of types."
assert errs[1] == "Ghost in immunities of Normal does not exist in the list of types."
assert errs[2] == "Ice in resistance of Water does not exist in the list of types."

f_test.close()
print("Success!")

# Test 2g
print("Testing Internal_Dup")
f_test = open("types_test/Type_Matchup-Internal_Dup.json")

data_in = json.load(f_test)['matchups']

valid, errs = type_matchup.validate_input(data_in)

assert valid == False, "Failure on Internal_Dup"
assert errs[0] == "Duplicate Entry Water in Weaknesses in entry Fire."
assert errs[1] == "Duplicate Entry Grass in Resistances in entry Grass."
assert errs[2] == "Duplicate Entry Water in Immunities in entry Water."

f_test.close()
print("Success!")

# Test 2h
print("Testing External_Dup")
f_test = open("types_test/Type_Matchup-External_Dup.json")

data_in = json.load(f_test)['matchups']

valid, errs = type_matchup.validate_input(data_in)

assert valid == False
assert errs[0] == "Duplicate Entry Fire in Resistances and Immunities in entry Fire."
assert errs[1] == "Duplicate Entry Water in Resistances and Weaknesses in entry Grass."
assert errs[2] == "Duplicate Entry Grass in Weaknesses and Immunities in entry Water."

f_test.close()
print("Success!")

# Test 2i
print("Testing Duplicate_Type")
f_test = open("types_test/Type_Matchup-Duplicate_Type.json")

data_in = json.load(f_test)['matchups']

valid, errs = type_matchup.validate_input(data_in)

assert valid == False
assert errs[0] == "Duplicate Types Given in List\nFire,fIrE"

f_test.close()
print("Success!")

# Test 3a
print("Testing find_valid_plugins")
results = matchup_generator.find_valid_plugins(alg_e)

assert len(results) == 0, str(len(results))
print("Success!")

# Test 4
print("Testing find_valid_plugins 4")
results = matchup_generator.find_valid_plugins(alg_a)

assert len(results) == 1, str(len(results))
assert results[0]['name'] == 'Raw_Calc', str(results[0]['name'])
print("Success!")

# Test 5
print ("Testing 5 a-b")
test_string = ["Option 1"]
results = matchup_generator.pick_option(test_string, "An Option")
assert results == 0, results
print("Success")

print ("Testing 5 d - i")
test_string = ["Option 1", "Option 2", "Option 3"]
save_in = sys.stdin
sys.stdin = io.StringIO("exit")
save_out = sys.stdout
sys.stdout = io.StringIO()
results = matchup_generator.pick_option(test_string, "an Option")
sys.stdin = save_in
t5_out = sys.stdout
sys.stdout = save_out
t5_out.seek(0)
out_lines = t5_out.readlines()

# Testing pick_option print statements, and exit handling
assert results == None, results
assert out_lines[0] == "0: " + test_string[0] + "\n", out_lines[0]
assert out_lines[1] == "1: " + test_string[1] + "\n", out_lines[1]
assert out_lines[2] == "2: " + test_string[2] + "\n", out_lines[2]
assert out_lines[3] == "Enter a number to select an Option\n", out_lines[3]
assert out_lines[4] == "Type 'exit' to quit.\n", out_lines[4]

# Testing invalid inputs and upper range
save_in = sys.stdin
sys.stdin = io.StringIO("a\n10\n-1\n2")
save_out = sys.stdout
sys.stdout = io.StringIO()
results = matchup_generator.pick_option(test_string, "an Option")
sys.stdin = save_in
t5_out = sys.stdout
sys.stdout = save_out
t5_out.seek(0)
out_lines = t5_out.readlines()
assert results == 2, results
assert out_lines[5] == "--> a is not a valid value!\n", out_lines[5]
assert out_lines[6] == "--> 10 is not a valid value!\n", out_lines[6]
assert out_lines[7] == "--> -1 is not a valid value!\n", out_lines[7]

# Testing invalid inputs and lower range
save_in = sys.stdin
sys.stdin = io.StringIO("-0\n0")
save_out = sys.stdout
sys.stdout = io.StringIO()
results = matchup_generator.pick_option(test_string, "an Option")
sys.stdin = save_in
t5_out = sys.stdout
sys.stdout = save_out
t5_out.seek(0)
out_lines = t5_out.readlines()
assert results == 0, results
assert out_lines[5] == "--> -0 is not a valid value!\n", out_lines[5]

# Testing in range
save_in = sys.stdin
sys.stdin = io.StringIO("1\n")
save_out = sys.stdout
sys.stdout = io.StringIO()
results = matchup_generator.pick_option(test_string, "an Option")
sys.stdin = save_in
t5_out = sys.stdout
sys.stdout = save_out
t5_out.seek(0)
out_lines = t5_out.readlines()
assert results == 1, results
assert len(out_lines) == 6, len(out_lines)
print("Success")

# Testing 6 is tested by Main.

# Testing 7
print("Testing 7a")
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
type_test = type_matchup.generate_data(test_matchup)
results, error = matchup_generator.validate_table(type_test, None)

assert results == False, results
assert error == "The algorithm must return a list of length 2, and each index being a dictionary of each type, and a numeric value.", error
print("Success")

print("Testing 7b")
results, error = matchup_generator.validate_table(type_test, 12)
assert results == False, results
assert error == "The algorithm must return a list of length 2, and each index being a dictionary of each type, and a numeric value.", error
print("Success")

print("Testing 7c")
results, error = matchup_generator.validate_table(type_test, [0])
assert results == False, results
assert error == "The algorithm must return a list of length 2, and each index being a dictionary of each type, and a numeric value.", error
print("Success")

print("Testing 7d")
results, error = matchup_generator.validate_table(type_test, [[0,1], [9,8]])
assert results == False, results
assert error == "The algorithm must return a list of length 2, and each index being a dictionary of each type, and a numeric value.", error
print("Success")

print("Testing 7e")
results, error = matchup_generator.validate_table(type_test, [{"Grass" : 5, "Water" : -1}, {"Fire": 0, "Normal" : -2}])
assert results == False, results
assert error == "The dictionaries must be the same length as the number of Types.", error
print("Success")

print("Testing 7f")
test_data = [{"Grass" : 5, "Water" : -1, "Fire" : 2, "Ghost" : 2}, {"Fire": 0, "Normal" : -2, "Grass" : 2, "Water" : -1}]
results, error = matchup_generator.validate_table(type_test, test_data)
assert results == False, results
assert error == "The dictionaries keys must be the Types.", error
print("Success")

print("Testing 7g")
test_data = [{"Grass" : "D:-9", "Water" : "D:-4", "Fire" : "D:2", "Normal" : "D:3"}, {"Fire": "O:-4", "Normal" : "O:5", "Grass" : "O:0", "Water" : "O:1"}]
results, error = matchup_generator.validate_table(type_test, test_data)
assert results == False, results
assert error == "Each entry must be a number.", error
print("Success")

print("Testing 7g set 2")
test_data = [{"Grass" : 0, "Water" : 0, "Fire" : 0, "Normal" : 0}, {"Fire": "O:-4", "Normal" : "O:5", "Grass" : "O:0", "Water" : "O:1"}]
results, error = matchup_generator.validate_table(type_test, test_data)
assert results == False, results
assert error == "Each entry must be a number.", error
print("Success")

print("Testing 7h")
test_data = [{"Grass" : 0, "Water" : 0, "Fire" : 0, "Normal" : 0, "hello" : 5}, {"Fire": 0, "Normal" : 0, "Grass" : 0, "Water" : 0, "Hello" : 0}]
results, error = matchup_generator.validate_table(type_test, test_data)
assert results == False, results
assert error == "The dictionaries must be the same length as the number of Types.", error
print("Success")

print("Testing 7h set 2")
test_data = [{"Grass" : 0, "Water" : 0, "Fire" : 0, "Normal" : 0}, {"Fire": 0, "Normal" : 0, "Grass" : 0, "Water" : 0, "Hello" : 0}]
results, error = matchup_generator.validate_table(type_test, test_data)
assert results == False, results
assert error == "The dictionaries must be the same length as the number of Types.", error
print("Success")

print("Testing 8")
save_err = sys.stderr
sys.stderr = io.StringIO()
results = matchup_generator.find_valid_plugins(alg_b)
t8_err = sys.stderr
sys.stderr = save_err
t8_err.seek(0)
err_lines = t8_err.readlines()
assert results == [], results
assert err_lines[0] == "The plugin alg_b.algorithm-import_exception had an exception when importing.\n", err_lines[0]
assert err_lines[1] == "  An error was made\n", err_lines[1]
print("Success")
# Test generate_table. Print needs to go to a file so that it can be verified.
