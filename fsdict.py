
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


#todo: add a special fnc that saves a certain depth of an input dict
#    for every item to save, see if nested

import cPickle
import os
import shutil

class av(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, k):
        try:
            return dict.__getitem__(self, k)
        except KeyError:
            value = self[k] = type(self)() #puts a nothing of self
            #eg type('asfs')() gives ''...very cool!
            return value



#recourse until 'edge' of fsdb
            
#a = AutoVivification()
#a[1][2][3] = 4
#a[1][3][3] = 5
#a[1][2]['test'] = 6
#create fs heirarchy of 'keys'?
#or fn as key?
#each 'node' has dict folder->key
#__delitem___ del file

#use av fncality for item entry?
#import shelve
import collections
class fsdictseq(collections.MutableMapping): #useless
    """emulates dict on filesystem in files.
    input key as fs-legal sequence of strings
    each string makes a folder on the fs
    to get around data access concurrency issues
    """
    def __init__(self,*args,**kwargs):
        self.folder=args[0]
        if not os.path.exists(self.folder):
            raise Exception , 'folder does not exist'
        if len(args)>1: self.update(args[1])
        self.kwargs={}
        #self.kwargs['writeback']=kwargs.setdefault('writeback',True)
        #kwargs.pop('writeback')#rem non kw kwargs first :S 
        self.update(kwargs)
        return
    
    def supposedpath(self,k,datafilename='po',root=False):
        fd=[self.folder]
        if type(k)==str: k=(k,) #to fix dumb mistake
        else:
            try: len(k)
            except TypeError: k=(k,) #else, probably some num
        if len(k)==0 and root==False:
            raise KeyError, 'no \"root\" accessible'
        for i in k:
            fd.append(str(i)) #to forgive if numbers entered
        fd=os.path.join(*fd)
        fp=os.path.join(fd,datafilename)
        return fd, fp #file directory, file path(dir+filename)
    def pathinfo(self,k,datafilename='po'):
        fd,fp=self.supposedpath(k,datafilename=datafilename)
        return {'dir':(fd,os.path.exists(fd)) , 'datafile':(fp,os.path.exists(fp))}
    
    def __setitem__(self,k,v): return self.setitem(k,v)
    def setitem(self,k,v,**kwargs):
        #depth determined by len of k
        #should only legal fs strings
        #1st write a map fp->k??
        ex=self.pathinfo(k)
        if not ex['dir'][1]:
            os.makedirs(ex['dir'][0])
        if v!=None:
            f=open(ex['datafile'][0],'w')
            cPickle.dump(v,f)
            f.close()
        #s=shelve.open(ex['datafile'][0])
        #s['val']=v
        #s.close()
        return
    
    def __getitem__(self,key): return self.getitem(key)
    def getitem(self,k,**kwargs):
        #self.kwargs.update(kwargs)
        #writeback=self.kwargs['writeback']
        ex=self.pathinfo(k)
        if ex['dir'][1]==False:
            raise KeyError , 'dir does not exist'
        elif False==ex['datafile'][1]: #todo is this good behaviour?
            return None
        else:
            f=open(ex['datafile'][0],'r')
            obj=cPickle.load(f)
            f.close()
            #s=shelve.open(ex['datafile'][0],writeback=writeback)
            #obj=s['val']
            #s.close()
            return obj
#    def get(self,k,default=None):
#        try:
#            return self.__getitem__(k)
#        except KeyError: return default
        
    def __delitem__(self,k):self.delitem(k)
    def delitem(self,k):
        #i don't want to immitate dict and return the whole data
        #val = self.getitem(k)
        ex=self.pathinfo(k)
        if False==ex['dir'][1]:# or False==ex['datafile'][1]:
            raise KeyError , 'dir does not exist'
        if False==ex['datafile'][1]:
            raise KeyError , 'file does not exist'
        else:
            os.remove(ex['datafile'][0])
            #olu=os.path.split(fd)[0] #one level up
            #kn=-1
            #ex=self.pathinfo(k[0:kn])
            #ex=self.pathinfo(k) #reinit
            #or len(k[0:kn-1])!=0 \
            kn=0
            while ex['dir'][0]!=self.folder \
            and os.walk(ex['dir'][0]).next()[1:3]==([],[]):
            #and len(os.walk(ex['dir'][0]).next()[1])==0 \
            #and len(os.walk(ex['dir'][0]).next()[2])==0:
            #and ex['datafile'][1]==False :
                #print 'will rem' , ex['dir'][0]
                shutil.rmtree(ex['dir'][0])
                kn=kn-1
                ex=self.pathinfo(k[0:kn])
        #go up one level and del if no 'po'
        return
    

    def __iter__(self):
        return iter(self.iter())
    def iter(self):
        w=os.walk(self.folder)
        while True:
            try:
                p,d,po=w.next()
                if po==['po']:
                    k=[];r=''
                    while r!=self.folder:
                        r,x=os.path.split(p)
                        k.append(x)
                        p=r
                    k.reverse()
                    yield tuple(k)
            except:
                raise StopIteration
                break
        
                
    def __len__(self):
        count=0
        for i in self.iter(): count+=1
        return count

#all this commented out stuff comes from ABC

#    def keys(self):
#        #ks=[i for i in self.iter()]
#        return [i for i in self.iter()]
#        #return frozenset(ks) #but dicts don't give back sets? PEP 3119
#        
#    def items(self):
#        return [(i,self[i]) for i in self.iter()]
#        
#    def values(self):
#        return [self[i] for i in self.iter()]
    
#    def pop(self,k):
#        v=self[k]
#        self.delitem(k)
#        return v
    
#    def popitem(self):
#        try:
#            k1=self.iter().next()
#            v=self.pop(k1)
#        except StopIteration: raise KeyError
#        return k1,v
    
    #def clear(self):
    #    [self.delitem(i) for i in self.iter()]
    #    return
        
#    def update(self,*d):
#        try:
#            for k,v in d[0].items():
#                self[k]=v
#        except:
#            for k,v in d[0]:
#                self[k]=v
#        finally:
#            if len(d)>1:
#                for k,v in d[1].items():
#                    self[k]=v
#        return
#        
    def __repr__(self): #todo {} for file if no po
        return str(dict([(k,'file') for k in self.iter()]))
    #def __str__(self):
    #    return str(self)
    
#why did i do directories?!?! can derive a flat version (no folders) of this
#just override pathinfo and supposedpath then slightly change iter
#todo str anything see what youi can do

#import rpdb2; rpdb2.start_embedded_debugger("wtfiswrong",fAllowRemote = True)

#description for another dictlike object (derived?) that can recurse
#see note in __getitem
#more dict-like but does not give KeyErrors so always check for a key
#    explicitly if you need to. todo how to give key error?

#Major question: should the indexing follow the folders of the object?
#..line to add: if the obj retrieved is not type(self) fsdict
class fsdict(collections.MutableMapping):
    """dict behavior for stuff on the fs
    makes the (reasonable) assumption that if a folder name is a digit, it
    is given back as an integer
    caution: no keyerror is given if the object is not on the fs
    can init w/ a dict
    options: proto=pickle protocol no. if def. it's just passed to pickle
    """
    def __init__(self,*args,**kwargs):
        """
        1st arg needs to be a folder. the rest are dict args
        """
        self.folder=args[0]
        #if not os.path.exists(self.folder): #i would like to keep this but
        #i couldn't
        #    raise Exception , 'folder does not exist'
        if len(args)>1: self.update(args[1])
        self.kwargs={}
        #self.kwargs['writeback']=kwargs.setdefault('writeback',True)
        #kwargs.pop('writeback')#rem non kw kwargs first :S 
        try:
            self.kwargs['proto']=kwargs.pop('proto')#rem non kw kwargs first :S 
        except: pass
        self.update(kwargs)
        return
    
    def supposedpath(self,k,datafilename='po'):#,root=False):
        fd=self.folder
        try: k=str(k)
        except: KeyError
        fd=os.path.join(fd,k)
        fp=os.path.join(fd,datafilename)
        return fd, fp #file directory, file path(dir+filename)
    def pathinfo(self,k,datafilename='po'):
        fd,fp=self.supposedpath(k,datafilename=datafilename)
        return {'dir':(fd,os.path.exists(fd)) , 'datafile':(fp,os.path.exists(fp))}
    
    def __setitem__(self,k,v):
        ex=self.pathinfo(k)
        try:
            self.__delitem__(k)
            #you get windowserror if you're have win explorer
            #..on the file its deleting :S
            os.makedirs(ex['dir'][0])
        except KeyError:
            os.makedirs(ex['dir'][0])
        f=open(ex['datafile'][0],'w')
        try: pargs=(v,f,self.kwargs['proto'])
        except: pargs=(v,f)
        cPickle.dump(*pargs)
        f.close()
        #s=shelve.open(ex['datafile'][0])
        #s['val']=v
        #s.close()
        return
    
    
    def __contains__(self,k):
        if self.pathinfo(k)['dir'][1]==True: return True
        else: return False
    
    def __getitem__(self,k):
        #self.kwargs.update(kwargs)
        #writeback=self.kwargs['writeback']
        ex=self.pathinfo(k)
        if ex['dir'][1]==False:
            #raise KeyError ,'dir '+str(ex['dir'][0])+' does not exist' #the safer way
            ####os.makedirs(ex['dir'][0])# is this good behavior?
            #but i don't want it to make dirs just to access
            
            return fsdict((ex['dir'][0])) #these 2 lines# the cooler way
            #why did i do this instead of keyerror?!?!
            #a: b/c i depend on keyerror to go into the next nesting if the 
            #dir doesn't exist so that i can access it
        elif False==ex['datafile'][1]: #todo is this good behaviour?
            return fsdict((ex['dir'][0])) #raise an error of type NoFile
            #or none?
        else:
            f=open(ex['datafile'][0],'r')
            obj=cPickle.load(f)
            f.close()
            #s=shelve.open(ex['datafile'][0],writeback=writeback)
            #obj=s['val']
            #s.close()
            return obj
            
    def __delitem__(self,k):
        #i don't want to immitate dict and return the whole data
        #val = self.getitem(k)
        ex=self.pathinfo(k)
        if False==ex['dir'][1]:# or False==ex['datafile'][1]:
            raise KeyError , 'dir '+str(ex['dir'][0])+' does not exist'
        else:
            shutil.rmtree(ex['dir'][0])
        return
    
    def __iter__(self):
        w=os.walk(self.folder)
        pi=w.next()
        for i in pi[1]:
            if str.isdigit(i)==True: yield int(i)
            else: yield i
        return
        
    def __len__(self):
        count=0
        for i in self.iter(): count+=1
        return count
    
    #def setdefault(self):
        
    def __repr__(self): #todo {} for file if no po
        return str(dict([(k,self[k]) for k in self.__iter__()]))

#todo: wrap av around fsdict
#todo make a fnc savedata and savedataorder doesn't matter
class fsdb(fsdict):
    """allows more db-like access to stuff on the fs"""
    def keyseq2index(self,strkeyseq):
        if type(strkeyseq)==str: strkeyseq=[strkeyseq]
        stri=''
        for ak in strkeyseq:
            stri=stri+"["+"\'"+str(ak)+"\'"+']'
        return stri
    def savedata(self,strkeyseq,data):
        """for cases when you don't know the data "foldering"(organization)
        beforehand"""
        if type(strkeyseq)==str: strkeyseq=[strkeyseq]
        i=self.keyseq2index(strkeyseq)
        exec('self'+i+'=data') #is this pythonic? idk another way
        #while being dynamic        
        
#        #a loop to make folders in case they don't exist
#        foldering=[]
#        strkeyseqi=iter(strkeyseq)
#        while len(foldering)!=len(strkeyseq):
#            taildir=strkeyseqi.next()
#            foldering.append(taildir)
#            i=self.keyseq2index(foldering)
#            print i
#            try: exec('self'+i)
#            except KeyError:#make the folder
#                previousfoldering=self.keyseq2index(foldering[:-1])
#                #todo ..check ..__contains__(key)
#                exec('self'+previousfoldering+'.update({taildir:{}})' )
        return
    def savedataset(self,strkeyseqlist,dataset):
        """args should be same length"""
        for astrkeyseq in strkeyseqlist:
            for adata in dataset:
                self.savedata(astrkeyseq,adata)
        return
    
    def loaddata(self,strkeyseq):
        if type(strkeyseq)==str: strkeyseq=[strkeyseq]
        i=self.keyseq2index(strkeyseq)
        return eval('self'+i) #is this pythonic? idk another way
        #while being dynamic
        
        #nonsense
#    def tryloaddata(self,strkeyseq):
#        icombos=itertools.strkeyseq
#        try
#        yield
#import itertools
    

#
dbtf="C:\\Users\\Majid\\Documents\\Academics\\tests"
fsdbt=fsdb(dbtf)
fsdbrt=fsdict(dbtf)

#fsdbrt['asdf']=4
