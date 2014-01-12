Computational Parameter Study Management Tool
====

http://msdresearch.blogspot.com/2012/01/parameter-study-management-with-python.html


Python tools for the mgt. of computational parameter studies.
Features:
* Management of arrays of scripts
* parameter mgt
* Python specific: 
   - A base class for analysis of the generated data 
   - python dictionary class that stores its data on the f/s

The modules in this repo in general address the following separately:

1. generating and keeping track of simulations

2. programmatic analysis of simulation outputs

3. (The management of program execution is separate but related. In my case I dealt with the PBS resource manager on a cluster computer and made the 'pbsmgr' repo. But since execution environments vary, I did not make an effort to integrate it in this repo as a design decision.)

In the most integrated workflow, 1, 2, and 3 work together. However, with this separation, you can just use 1, or 1 and 2, or 1, 2, and 3. #2 is useful if you use Python for your analysis.


Install with just
    python setup.py install


Workflow Setup
===

First, to make the best use of this code, you must parameterize/template and automate as much as possible your simulation script(s) (you can have a set of simulation scripts for a simulation run. a run is identified by parameter values for all parameters). This code is best for 'production' execution of simulations.

Now typically these parameters are the numerical physical parameters that you are trying to study the effects of. But in the context of this code, you can be creative about 'parameters'. A parameter could be a snippet of code representing an input more complicated than just a number such as an equation. They could even be provenance information such as some code version number, a list of 'tags' that describe the simulation, or information about the computing environment such as CPU or compiler information. It could be any object but it should have a string representation if it needs to show up in your scripts.


Simple Use Tutorial
===
Script Management
---



