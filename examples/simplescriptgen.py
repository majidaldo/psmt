from scriptmgt import * 

runline='numbercruncher.exe $a $b'
myscripts={'runline':runline}

from scriptmgt import *

mysims=batchfoldermgt('.'
,scriptargs=myscripts
,listofscriptstosave=['runline']
	)

#the parameters specified in this dict are the
#params that are going to define a simulation run
initvarsweep={'a':[1,2,3]
             ,'b':['func1','func2']}

#the following generates your scripts
#In [3]: mysims.user_gentaskarray(initvarsweep)
#Out[3]: [0, 1, 2, 3, 4, 5]