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

