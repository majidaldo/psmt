Simple Tutorial
=======


Workflow Setup
===

First, to make the best use of this code, you must parameterize/template and automate as much as possible your simulation script(s) (you can have a set of simulation scripts for a simulation run. A run is identified by parameter values for all parameters). This code is best for 'production' execution of simulations.

Now typically these parameters are the numerical physical parameters that you are trying to study the effects of. But in the context of this code, you can be creative about 'parameters'. A parameter could be a snippet of code representing an input more complicated than just a number such as an equation. They could even be provenance information such as some code version number, a list of 'tags' that describe the simulation, or information about the computing environment such as CPU or compiler information. It could be any object but it should have a string representation if it needs to show up in your scripts.


Simple Use Tutorial
===
1. Script Management
---
Let's say numbercruncher.exe takes in two arguments, a and b, as command line arguments. You would make a 'script' that's just

    runline=numbercruncher.exe $a $b

Name the script by putting it in a dictionary. This dictionary is a collection of all scripts used in your simulation. In our case it's just one script that is one line long.

    myscripts={'runline':runline}

The string of runline is accessible from other scripts in the collection as $runline. Keep this in mind when setting up more sophisticated and/or modular scripts. As a quick example, you could make an MPI version of the previous like

    myscripts={'runline':runline,'mpirun':'mpirun -n 4 $runline'}

For the sake of this tutorial I'm keeping it simple, but you can go wild with flexibility by modularizing your scripts so that, for example, you could execute in different environments.

After you have your scripts set up, you initiate what I call the batch folder manager. In our simple case, it takes as a positional argument the folder where you want to store your set of simulations. The set of scripts is specified as the keyword argument `scriptargs`. The script(s) that you want written on the filesystem is specified with the keyword argument `listofscriptstosave`.

    from scriptmgt import *
    
    mysims=batchfoldermgt('/path/to/sims'
    ,scriptargs=myscripts
    ,listofscriptstosave=['runline']
        )


After setting up this object, you can use it to generate scripts. First, make a dictionary that has the variables you want to explore

    initvarsweep={'a':[1,2,3]
                 ,'b':['func1','func2']}

Now you need to pass this dictionary into the command that generates all combinations of these variables

    In [3]: mysims.user_gentaskarray(initvarsweep)
    Out[3]: [0, 1, 2, 3, 4, 5]

Each combination is now in a folder. To check what combination was stored in what folder, look inside the dictionary

    In [8]: mysims.runsi
    Out[8]:
    {frozenset({('a', 3), ('b', 'func2')}): 0,
     frozenset({('a', 1), ('b', 'func1')}): 3,
     frozenset({('a', 1), ('b', 'func2')}): 4,
     frozenset({('a', 3), ('b', 'func1')}): 1,
     frozenset({('a', 2), ('b', 'func2')}): 2,
     frozenset({('a', 2), ('b', 'func1')}): 5}

When you use the command again for some new values, you shouldn't add new parameters. It's possible but it's not recommended. You can check the variable sets that you used with 

    In [7]: mysims.getmyvarsets()
    Out[7]: frozenset({frozenset({'a', 'b'})})


In this case we only have one parameter set: a and b.


to be continued..ok it  looks like i need to use some autodoc tool. even the simple tutorial is too long for a readme.

