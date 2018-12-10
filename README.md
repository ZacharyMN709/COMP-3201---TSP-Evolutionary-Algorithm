# COMP 3201 - Evolutionary Algorithm Runner

In order to run the code, you will need numpy, pandas, matplotlib and seaborn. These
are common scientific computing libraries for Python.

There are two problems presently set up to be solved. The 8-Queens problem, as well
as the TSP problem, complete with datasets. Both of these problems use a JSON
object to initialize variables, so by changing the variables in the objects, the 
algorithm can be completely changed.


### JSON Structure
The basic JSON object looks like this:

    {
    "maximization": true,
    "methods": [0, 0, 1, 1, 2, 0, 0],
    "print_stats": true,
    "generation_limit": 10000,
    "report_rate": 100,
    "runs": 1,
    "data_type": 2
    }

Each variable controls a different aspect of the program. The JSON object has some other
variables, for future implementation of database to save the stats in a more cohesive
manner.

As for the variables in the JSON object, their purposes are:
 - `maximization`: Controls whether to find the max or min when selecting fitnesses
 - `methods`: Each integer in this list controls which method to use for the 7 steps in our EA
 - `print_stats`: Whether or not the stats should be printed to the console
 - `report_rate`: How often the stats are printed to the console or saved, if either.
 - `runs`: The number of times each combination of funtions is run. 
 Useful for automating testing or collecting statistics.
 - `data_type`: How the individuals are represented.
 
 Additionally, the TSP JSON object has the field `data_set`. This is the
 set of cities to load from the text file. They are as follows:
 
    0: Sahara
    1: Uruguay
    2: Canada


###EA Structure

The 7 steps of the EA each derive from a helper class which handles manging function
pointers, names, and keeping track of all the variables needed to run the EA. Below 
are valid integers for each of the classes. The order they are listed here is the
order which they are called in the EA, and also the order that the JSON object expects.
  
    Methods available in FitnessHelper:
      0:  Euclidean
    Methods available in PopulationInitializationHelper:
      0:  Random 
      1:  Cluster 
      2:  Euler
    Methods available in ParentSelectionHelper:
      0:  MPS 
      1:  Tourney 
      2:  Random
    Methods available in RecombinationHelper:
      0:  Order Crossover 
      1:  PMX Crossover
    Methods available in MutatorHelper:
      0:  Swap 
      1:  Insert 
      2:  Inversion 
      3:  Shift
    Methods available in SurvivorSelectionHelper:
      0:  Mu + Lambda 
      1:  Replace
    Methods available in PopulationManagementHelper:
      0:  None 
      1:  Annealing 
      2:  Entropy 
      3:  Oroborous 
      4:  Engineering
      
To clarify above, if the JSON object had this list: `"methods": [0, 0, 1, 1, 2, 0, 0]`
the methods used would be:

    FitnessHelper:
      0:  Euclidean
    PopulationInitializationHelper:
      0:  Random 
    ParentSelectionHelper:
      1:  Tourney 
    RecombinationHelper:
      1:  PMX Crossover
    MutatorHelper:
      2:  Inversion 
    SurvivorSelectionHelper:
      0:  Mu + Lambda 
    PopulationManagementHelper:
      0:  None 

Data Type Support
------
Our algorithm supports multiple representations for the individuals used in the EA.
This is what the integers `data_type` is for, and each integer represents the
following data type to be used:

    `0`: Python lists
    `1`: Numpy arrays
    `2`: C-Arrays
    

Finally, in order to run the program, simply give your Python3 interpreter the argument
 `8Q_Runner.py` or `TSP_Runner.py` in your shell or run the file through your 
 preferred IDE. Both files, when called as the main function, read the appropriate
 JSON file and automatically load the files and create the objects require for the
 EA to run. After that single call, as long as you have `print_stats` set as true
 in the JSON file, the program will start printing results to screen.