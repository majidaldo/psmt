
##Author: Majid al-Dosari
#Copyright (c) 2010, Majid al-Dosari
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the <organization> nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
#DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


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
from fsdict import fsdb


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
        #todo: cache should be some transparent way to store last few fnc
        #calls of some fnc
        self.batchobj=batchfolderobj
        self.params=one2one({})
        self.kwargs=kwargs
        
        #include all param sets?
        self.kwargs.setdefault('includeallparamsets',True)
        if self.kwargs['includeallparamsets']==True: self.addparamsets(self.batchobj.runsi.keys())
        
        analysisdir=os.path.join(self.batchobj.mydir,'analysis')
        self.kwargs.setdefault('dir',analysisdir)
        self.kwargs.setdefault('proto',-1)
        self.data=fsdb(self.kwargs['dir'])
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
    
    #todo put the following the following in fsdict? w/o the params thing
    #then just tack on params for the analysisbase method
    def savedata(self,paramsortaskid,strkeyseq,data
        ,dictkeys2folders=True): #todo list-ize
        #try len(param) to chk if data
        #perhaps flip this so that on the fs strkeyseq/taskid
        """for cases when you don't know the data "foldering"(organization)
        beforehand"""
        if type(strkeyseq)==str: strkeyseq=[strkeyseq]
        ti=self.batchobj.alwaysreturntaskid1(paramsortaskid)
        k=list(strkeyseq)+[ti]
        self.data.savedata(k,data,dictkeys2folders=dictkeys2folders)
        #.. while being dynamic
        return
        #list version
#    def savedata(self,*args,**kwargs):
#        try:
#            self.savedata(*args,**kwargs)
#        except:
#            for 
        
        #needed?
    def loaddata(self,paramsortaskid,strkeyseq):
        """for cases when you don't know the data "foldering"(organization)
        beforehand"""
        if type(strkeyseq)==str: strkeyseq=[strkeyseq]
        ti=self.batchobj.alwaysreturntaskid1(paramsortaskid)
        k=list(strkeyseq)+[ti]
        return self.data.loaddata(k,data)


