# ptbc

## Types Matchups
Different Type Matchups are stored as json files in "types/".   
The default json file is based on the current Pokemon type matchup.

## Algorithms
Different algorithms to generate scores used to determine balance are stored in "algorithms/".
The algorithms are only found when in the root "algorithms/" directory, and won't be found in any directory higher.

### Dynamic
The matchup_generator.py file will send the algorithm a dictionary, that is populated with dictionaries.
The keys of the first level of dictionary are the types.
The keys of the second level are "resistances", "weaknesses", "immunities", "super", "reduced", and "none".
These reflect the type's defensive and offensive capabilities.
"resistances", "weaknesses", and "immunities" are the type's defence.
"super", "reduced", and "none" are the types's offense.
Each of those values lead to a list of the types that fall into those categories.

### To Implement
A way to track special attributes of a type. This includes Grass immunity to powder moves, Ghost immunity to Prankster, etc.
This would most likely be added into the Type JSON, but unsure about how to fully implement it.