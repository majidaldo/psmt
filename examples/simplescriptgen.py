from scriptmgt import * 

runline='numbercruncher.exe $a $b'
myscripts={'runline':runline}

from scriptmgt import *

mysims=batchfoldermgt('.'
,scriptargs=myscripts
,listofscriptstosave=['runline']
	)

	
