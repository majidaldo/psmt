#import os
#import sys
#pathname = os.path.dirname(sys.argv[0])
#pathname= os.path.join(pathname,'fsdict.py')
#__name__='notmain'
#execfile(pathname)
#del pathname
#__name__='__main__'

import os
import sys
from fsdict import fsdict


#base class for analysis

import numpy as np
import scipy as sp
import matplotlib as mpl
try:
    import matplotlib.pyplot as plt
    from pylab import *
    from sp import *
except: pass

class one2one(dict):
    """looks up values as well"""
    def __getitem__(self,k):#d=None):
        try:
            return dict.__getitem__(self,k) #cool!
        except KeyError:
            for ak,av in self.iteritems():
                if k==av: return ak
                else: continue
            raise KeyError#return d


class analysis(object):
    def __init__(self,batchfolderobj,**kwargs):
        self.cache={} # a db to chk for stuff so in a calc you can put
        #try: somecalc=self.cache[keytoacalc]
        self.batchobj=batchfolderobj
        self.params=one2one({})
        self.kwargs=kwargs
        
        #include all param sets?
        self.kwargs.setdefault('includeallparamsets',True)
        if self.kwargs['includeallparamsets']==True: self.addparamsets(self.batchobj.runsi.keys())
        
        analysisdir=os.path.join(self.batchobj.mydir,'analysis')
        self.kwargs.setdefault('dir',analysisdir)
        self.kwargs.setdefault('proto',-1)
        self.data=fsdict(self.kwargs['dir'])
        return

    def addparamsets(self,psl):
        d=dict((v,k) for k, v in self.batchobj.runsi.iteritems() if k in psl)
        self.params.update(d)
        return
    
    
    def keyseq2index(self,strkeyseq):
        if type(strkeyseq)==str: strkeyseq=[strkeyseq]
        stri=''
        for ak in strkeyseq:
            stri=stri+"["+"\'"+str(ak)+"\'"+']'
        return stri
    
    def savedata(self,params,strkeyseq,data): #todo list-ize
        #try len(param) to chk if data
        #perhaps flip this so that on the fs strkeyseq/taskid
        """for cases when you don't know the data "foldering"(organization)
        beforehand"""
        if type(strkeyseq)==str: strkeyseq=[strkeyseq]
        i=self.keyseq2index([self.params[params]]+strkeyseq)
        exec('self.data'+i+'=data') #is this pythonic? idk another way
        #.. while being dynamic
        return
    def loaddata(self,params,strkeyseq):
        """for cases when you don't know the data "foldering"(organization)
        beforehand"""
        if type(strkeyseq)==str: strkeyseq=[strkeyseq]
        i=self.keyseq2index([self.params[params]]+strkeyseq)
        return eval('self.data'+i) #is this pythonic? idk another way
        #.. and be dynamic


