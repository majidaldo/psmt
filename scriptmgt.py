#coded by Majid al-Dosari
"""
creates an array of tasks using some script.
a 'task' is defined by a variable set with its associated values,
one value for each variable
related runs chared by same functionality but different valued parameters

each task is associated with a number. this is simply to facilite use across
systems. a list of numbers is easy to pass around
assumping all input and output w/in same folder. there are work arounds such 
as outputing some sort of link

notes:
-didnt' want to manage processes. not much efficiency to gain plus
other tools more suitable
-on purpose did not include ability to renumber tasks
 any 'renaming' must be via a deletion and creating a new 'task' w/
 the same parameters and deleted.

components:
    #-script substitution. a 'script' can even be one line as a component
    # whole script. 
    #-run of script (demoted)
    #-batching
    
motivator: add context to data located as strings in a file system. this 
script is for related but independed parameter studies
why python: already using it in my scientific work.

bash way:
physical parameters->string manipulation (bash)->input (scripts)
input->compute->output files
output files -> map string of file names to physical parameters

python way: (eliminting going thru strings)
physical parameters->compute
want to deal w/ structure, not strings
"""

# todo:
#files to del
#merge/import w/
#ability to use {var:list} in user_getallparamsw

#minor todo: chk for repeated input iterator

import fnmatch
import itertools
import string
import subprocess
import os
import shutil
import pickle
import stat

#import rpdb2; rpdb2.start_embedded_debugger("wtfiswrong",fAllowRemote = True)






from sgmllib import SGMLParser
class gettagstuff(SGMLParser): #rendered useless but what the heck
    def reset(self):
        SGMLParser.reset(self)
        self.insideatag=False #?
        self.tagtxt=[]
        self.tags=[]
        self.tagattribs=[]
        self.tagdata=[]
        self.tagstruct=\
            {'tags':self.tags,'tagattribs':self.tagattribs,'tagdata':self.tagdata}
        return
        
    def unknown_starttag(self,tag,tagattribs): #link tag
        self.insideatag=True
        self.tags.extend((tag,))
        self.tagattribs.extend((tagattribs,))
        self.tagtxt.extend([self.get_starttag_text()])
        return
    def unknown_endtag(self,tag):
        self.insideatag=False
        return
    
    def handle_data(self,data):
        if self.insideatag==True: self.tagdata.extend((data,))
        return
        
#testt=gettagstuff()
#testt.feed("<link>asdfsfsfsfjjl</link> lkj<link h='3'>aasdf</link>"+dumpall)


class scripts(object):
    """script obj"""
    def __init__(self,*args,**kwargs):
        self.kwargs={}
        self.kwargs=self.actionbeforejoining(*args,**kwargs)
        self.tagkeys={}
        
        def subs():
            for k,v in kwargs.iteritems():
                #COOL NOTE HERE:              _______any obj that has str rep.
                #for example matrix
                self.kwargs[k]=string.Template(str(v)).safe_substitute(self.kwargs)
                t=gettagstuff()
                t.reset()
                t.feed(str(v))
                self.tagkeys.update({k:t.tagstruct})
                del t
            noofdollarsigns=0
            for asc in self.kwargs.values():
                asc=str(asc)
                noofdollarsigns=noofdollarsigns+asc.count('$')
            return noofdollarsigns
        
        lastsubsds=subs()
        nl=0
        #for recursive substitutions, inf loop danger
        while lastsubsds!=subs() and nl<10:
            lastsubsds=subs()
            nl=nl+1
        if nl>=10:
            print 'warning encounted a ', nl, '- (inf?) substitution loop'
        
        kwargs=self.actionafterjoiningandsubing(*args,**self.kwargs)
        return
    
    def actionbeforejoining(self,*args,**kwargs):
        #if kwargs has pbs then 
        #totmem=n*mem
        #mem=40mb/uc
        return kwargs
        
    def actionafterjoiningandsubing(self,*args,**kwargs): return kwargs
    
    def gettagdata(self,tag,attrib):
        """fetch things matching args. attrib is list of tuples [,(attr,val),]"""
        ti=self.tagstruct['tags'].index(tag)
        ai=self.tagstruct['tagattribs'][ti:].index(attrib)
        return self.tagstruct['tagdata'][ai]
    
    def removetags(self):pass#stub
    def removetags_useless(self):#todo: make it remove from a single k
        #'tags' can be scripts. just save those out
        for k,v in self.kwargs.iteritems():#if k in listofscripts?
            t=gettagstuff()
            t.feed(str(v))
            tags=t.tagstruct['tags']#.copy()
            r=self.kwargs[k] #why?
            for tag in tags:
                r=r.replace("</"+tag+">",'')
            for tag in t.tagtxt:
                r=r.replace(tag,'')
            self.kwargs[k]=r #why?
        return

    def saveascript(self,pathincfname,scripttxt,**kwargs):
        """..to a run output folder"""
        self.removetags()
        f=open(pathincfname,'w')
        f.write(scripttxt)
        fd=f.fileno()
        os.fchmod(fd,stat.S_IRWXU)
        f.close()
        return

    def savescripts(self,dir,listofscriptvars):
        #take from kwargs
        for ascript in listofscriptvars:
            apath=os.path.join(dir,ascript)
            self.saveascript(apath,self.kwargs[ascript])
        return



class arun(scripts): #useless
    """...is just a script that knows how to run itself
    a good place to input *run* (not physical) params.
    instantiated when everything is ready.
    """
    
    def actionafterjoiningandsubing(self,*args,**kwargs):
        self.cmd=kwargs['execcmd']
        self.mydir=kwargs['outdir']
        self.removetags()
        return
    
    def run(self,stdoutt=subprocess.PIPE):
        """stdout=None for screen(?)"""#no use here
        #create dir
        #rm tags
        #save script
        r=subprocess.Popen(self.cmd,stdout=stdoutt)
        self.stdout=r.STDOUT #correct?
        return r.STDOUT
        
    def kill(self):pass #needed?
    def deldir(self):pass
    def __del__(self):pass #has kill and deldir


    
    def mydirfiles(self):#needed?
        self.myfiles=os.listdir(self.mydir)
        return self.myfiles
    
    def updatemyinfo(self):pass



#execcmdtemp = "${execdir}${executible} $execparams"
#mpiruntemp= "mpirun $execcmd" #"mpirun -np $n $execcmd"
#mpi inside pbs run
#pbssub="qsub > $uniquedir" 


#test=scripts(a="${${${abc}}} asf $asdf ")
#tagtst=scripts(t="<link>asdfsfsfsfjjl</link> lkj",t2="<link h='3' j=f>aasdf</link>"+dumpall)

class batchfoldermgt(object): #input vars & varvals dict(var=val(s)) have order of list repr dir struct
    """primary purpose: programatic *file* creation, mgt,
    and and mapping of output(files) vs input parameters """
    def __init__(self,mydir,**kwargs):
        """takes in an (ordered?) list of run/script obj"""
        kwargs.setdefault('scriptargs',{})
        kwargs.setdefault('listofscriptstosave',[])
        self.kwargs={}
        self.kwargs.update(kwargs)
        outputmapping=kwargs.setdefault('outputmapping',[])
        self.scriptsclass=kwargs.setdefault('scriptsclass',scripts)
        generate=kwargs.setdefault('generate',None)
        
        self.runsi={}
        self.outputmapping=[] #list of wildcards to match in fnames, see getoutvsinput()
        #self.runobj=runscript #a prototype for all runs in the batch
        self.name=''#os.path.split(mydir)[1]
        self.mydir=mydir
        #try: os.mkdir(self.mydir)
        #except: print "warning: directory exists" #b/c gets error 
        if os.path.lexists(mydir)==False:
            raise NameError, "directory doesn't exist. create directory first."
        potentialfile=os.path.join(mydir,self.name+'runtypedata')
        if os.path.lexists(potentialfile)==True:
            self.load(mydir)
            #but if i gave you output mapping, don't load from file
            if outputmapping!=[]:self.outputmapping=outputmapping
        #save scripts
        if generate!=None:print "created tasks ids: ",self.user_gentaskarray(*generate)
        return

    def update(self):pass #update everything that needs to be
    
    def _manualparamchange(self,dolditem,dnewitem):
        """dangerous! input dic. you can change taskids directly 
        batch[params]=value"""
        oldparamset=frozenset(dolditem.iteritems())
        #oldtaskid=(dolditem.values()[0])
        newparamset=frozenset(dnewitem.iteritems())
        #newtaskid=(dnewitem.values()[0])
        tid=self.runsi.pop(oldparamset)
        self.runsi.update({newparamset:tid})
        self.savemyself()
        return

    def _addparams(self,dictofiters):
        #variable set of added iter /should/ match existing
        if len(dictofiters.keys())==0:
            print "no iterators input"
            return []
        taskidsadded=[]
        wanttoadd=self.genparamlist(dictofiters)
        willaddparams=frozenset.difference(frozenset(wanttoadd),frozenset(self.runsi.keys()))
        uatf=self.unacctedtaskfolders()
        unavailnos=frozenset.union(*uatf.values()).union(self.runsi.values())
        def getnextavailno(uavnos,startno):
            while startno in uavnos: startno=startno+1
            else: return startno
        startw=0
        for i in willaddparams:
            nextavailno=getnextavailno(unavailnos,startw)
            self.runsi.update({i:nextavailno})
            taskidsadded.extend([nextavailno])
            unavailnos=unavailnos.union(taskidsadded)
        return taskidsadded

    def user_addconststoexistingtable(self,dictofconsts):
        """to retro add params that don't change existing run
        effectively updates a const though"""
        dc=self.runsi.copy() #b/c can't iter a changing dict
        for dicset,taskid in dc.iteritems():
            self.runsi.pop(dicset)
            dictofset=dict(dicset)
            for avar in dictofconsts.keys():
                if avar in dictofset.keys(): print 'const not added b/c var \"', avar, '\" exists'
                else:(dictofset.update(dictofconsts))
            newdicset=frozenset(dictofset.iteritems())
            self.runsi.update({newdicset:taskid})
        self.savemyself()
        return
    #
    def _gentaskfolder(self,scriptargs,taskid,listofscriptstosave):
        """dont use b/c it doesn't chk against table"""
        #info: taskid arg passed to script
        #my context info
        scriptargs.update({'taskid':taskid})
        taskdir=os.path.join(self.mydir,str(taskid))
        scriptargs.update({'taskdir':taskdir})
        #take scripts from kwargs
        #scriptobj=scripts(**scriptargs) #can i attrib a class? so that self.scriptclass?
        scriptobj=self.scriptsclass(**scriptargs)
        try: os.mkdir(taskdir)
        except: print "warning:", taskdir, " exists"
        scriptobj.savescripts(taskdir,listofscriptstosave)
        return
    def _gentaskfolderarray(self,scriptargs,listoftaskids,listofscriptstosave):
        """dont use b/c it doesn't chk against table"""
        for ataskid in listoftaskids:
            self._gentaskfolder(scriptargs,ataskid,listofscriptstosave)
        return
    def user_gentaskarray(self,dictofiters,**kwargs):
        """if you need to delete a folder's contents, use user_deleteby... 
        w/ folder del option, then generate. this will force you to think
        about what you're doing
        special vars are taskid and taskdir
        """
        self.kwargs.update(kwargs)
        scriptargs=self.kwargs['scriptargs']
        listofscriptstosave=self.kwargs['listofscriptstosave']
        overwrite=kwargs.setdefault('overwrite',False)
        
        inputvarset=frozenset(dictofiters.keys())
        mvs=self.getmyvarsets()
        if inputvarset not in mvs and len(mvs)>0:
            print "warning: input variable set different from any existing"
        taskids=self._addparams(dictofiters)#does not overwrite
        #{generated params}-{taskids (newly added)}
        if overwrite==True:
            existingparams=frozenset(self.genparamlist(dictofiters))-frozenset(self.lookupbytaskids(taskids))
            existingtaskids=[self.runsi[aparam] for aparam in existingparams]
            taskids.extend(existingtaskids)
        
        runsirev=dict((v,k) for k, v in self.runsi.iteritems())
        for ataskid in taskids:
            taskidparams=dict(runsirev[ataskid]) #physical ones
            taskidparams.update(scriptargs)
            self._gentaskfolder(taskidparams,ataskid,listofscriptstosave)
        self.savemyself()
        return taskids
    def user_regenbytaskid(self,taskids,**kwargs):
        """by def. overwrites
        if you need to delete a folder's contents, use user_deleteby... 
        w/ folder del option, then generate. this will force you to think about
        what you're doing
        """
        self.kwargs.update(kwargs)
        scriptargs=self.kwargs['scriptargs']
        listofscriptstosave=self.kwargs['listofscriptstosave']
        
        paramsl=self.lookupbytaskids(taskids)
        for aparam in paramsl:
            aparam=dict(aparam)
            for k,v in aparam.iteritems(): aparam.update({k:[v]})
            self.user_gentaskarray(aparam,scriptargs,listofscriptstosave,overwrite=True)
        return paramsl
        
    def _remparams(self,dictofiters):
        wanttorem=self.genparamlist(dictofiters)
        willrem=frozenset.intersection(frozenset(self.runsi.keys()),frozenset(wanttorem))
        taskidsrem=[]
        for i in willrem:
            taskidsrem.extend([self.runsi.pop(i)])
        return taskidsrem#taskids removed
    def user_remconstfromtbl(self,dictof_a_const,as_inclset=False):
        if len(dictof_a_const)>1 or len(dictof_a_const)==0:
            print "nothing input or more than one variable input"
        paramswconst=frozenset(self.getallparamswith(dictof_a_const).values()[0])
        taskidswconst=[self.runsi[aparamset] for aparamset in paramswconst]
        if len(taskidswconst)==len(self.runsi.values()):#ie a constant across all 
            originalparams=self.lookupbytaskids(list(taskidswconst))
            for aparamset in originalparams:
                newset=aparamset-frozenset(dictof_a_const.iteritems())
                ti=self.runsi.pop(aparamset)
                self.runsi.update({newset:ti})
            self.savemyself()
            return originalparams
        else:
            print 'variable is not a constant across all parameter sets'
            return None
        
    def _deletetaskfolder(self,taskid):
        taskdir=os.path.join(self.mydir,str(taskid))
        shutil.rmtree(taskdir)
        return
    def user_deletebyvariters(self,dictofiters,deletefolders=False):
        """make sure you kill associated processes! del folders
        not recommended"""
        #del key
        deletedtasks=self._remparams(dictofiters)
        #del dir
        if deletefolders==True:
            for tasktodel in deletedtasks: self._deletetaskfolder(tasktodel)
        #todo: stop process?
        self.savemyself()
        #print "deleted task ids: ", deletedtasks
        return deletedtasks
    def user_deletebytaskids(self,taskids,deletefolders=False):
        """make sure you kill associated processes!"""
        runsirev=dict((v,k) for k, v in self.runsi.iteritems())
        taskidparams=[]
        for ataskid in taskids:
            takeout=runsirev[ataskid]
            taskidparams.extend(takeout) #physical ones
            self.runsi.pop(takeout)
            if deletefolders==True: self._deletetaskfolder(ataskid)
        self.savemyself()
        return taskidparams
    
    def user_import(self,dirr,paramsi={},overwritemyself=False):
        """todo:
        for merging data from one env/sys to another
        file move op
        """
        mergewith=batchfoldermgt(dirr)
        if paramsi!={}:
            params2import=self.genparamlist(paramsi)
        else: params2import=mergewith.runsi
        for aparamset in params2import:
            pass
        #link or move or copy?
        #todo
        #otherbatch=batchfoldermgt("dirr")
        pass
        #will have to regen
        
        #be careful not to exec stuff from dirr
        #regen existing?
        #move folder
        #create symb link folders to dirr?
        #savemyself
        #return new [(params,taskid)]
            
    def savemyself(self):#to do put after every
        mydata={'runsi':self.runsi,'outputmapping':self.outputmapping}
        myfilename=os.path.join(self.mydir,self.name+'runtypedata')
        f=open(myfilename,'w')
        pickle.dump(mydata,f)
        return
    
    def load(self,dirr):
        fname=os.path.join((dirr),self.name+'runtypedata')
        f=open(fname)
        mydata=pickle.load(f)
        self.runsi.update(mydata['runsi'])
        f.close()
        return
        
    #lower level fncs and utils
    def genparamlist(self,dictofiters):
        return [frozenset(zip(dictofiters.keys(),v)) \
            for v in itertools.product(*dictofiters.values())]
    def createindexeddict(self,starti,dictofiters):
        endic= dict(enumerate(self.genparamlist(dictofiters),start=starti))
        return dict(zip(endic.values(),endic.keys()))
    def lookupbytaskids(self,taskids):
        runsirev=dict((v,k) for k, v in self.runsi.iteritems())
        return [(runsirev[ataskid]) for ataskid in taskids]
    def getallparamswith(self,dictofconsts):#use previous
        """constant means more than just a no. could be any 'constant' obj"""
        dictofmatches={} #for each input dict item
        for varvalpair in dictofconsts.iteritems():
            varvalmatch=frozenset([])#[]
            for aparamset in self.runsi.keys():
                if varvalpair in aparamset:
                    #varvalmatch=varvalmatch.union([self.runsi[aparamset]])
                    varvalmatch=varvalmatch.union([aparamset])
            dictofmatches.update({varvalpair:varvalmatch})
        return dictofmatches
    def user_getallparamswith(self,dictofiters):#,combine=True):#todo should be list 4 each var
        """think of each input var as a discriminator"""        
        #make a dict of iters
        paramslist=self.genparamlist(dictofiters)
        combine=[]
        for adictofconsts in paramslist:
            r=self.getallparamswith( dict(adictofconsts) )
            combine.extend(frozenset.intersection(*r.values()))
        return combine
        
#            r=self.getallparamswith(dictofconsts)
#        return list(frozenset.intersection(*r.values()))
        
#    def user_filterout(self,dictof):#use grpbycontst give it list of vars 
#        vd=self.getvarvalues()
#        xld=dict(zip(listofvars,varexclusionlist))
#            for avar,itsvals in xld.iteritems():
#                vd[avar].remove(itsvals)
#        pass
    #def gen selection w/ dict
    #1. gen iterator -> put each iteration into ugetallparamswith
    #then decide whether to filter for or filter out
    
    
    def getvarvalues(self):
        """returns all values of a variable"""
        vd={}
        for aps in self.runsi.keys():
            psd=dict(aps)
            for ap,itsval in psd.iteritems():
                if ap not in vd.keys():
                    vd.update({ap:[itsval]})
                elif itsval not in vd[ap]:
                    vd[ap].append(itsval)
        return vd
    def user_groupbyconsts(self,listofvars,varexclusionlist=None): #varexclusion useless?
        """input list of variables. output[0]: 'legend'. output[1] variables
        that were constant across all parameter sets.
        gets parametersets of a 'varying' set of variables
        paramlist returned. vars not in the arg will be returned w/ 
        respective consts.
        no. of sets always = no. avail?
        this is a high-level fn.
        usage scenario: multiple plots on the same plot. ie. plots w/ a legend
        
        note: don't know how it would work w/ multiple var sets.
        but you shouldn't have multiple var sets anyway
        """
        vd=self.getvarvalues()
        if listofvars==type(str):
            listofvars=[listofvars]# to correct a mistake i make a lot
            print 'put in a LIST (of strings) for listofvars arg, ok?'
        othervars=frozenset(vd.keys())-frozenset(listofvars)
        #todo: incl list?
        if varexclusionlist!=None:
            try:
                xld=dict(zip(listofvars,varexclusionlist))
                for avar,itsvals in xld.iteritems():
                    try: vd[avar].remove(itsvals)
                    except: pass
            except:
                raise ValueError, "exclusion list size must match var list size"
                
        othervaryingvars={};consts={}
        for aov in list(othervars):
            if len(vd[aov])>1:
                othervaryingvars.update({aov:vd[aov]})
                vd.pop(aov) #so by the end of looping, it's just the 
                #dict of list of vars (the fn arg w/ its values)
            else: consts.update({aov:vd[aov]})

        sd={}
        vi=itertools.product(*vd.values())
        for avi in vi:
            dc=dict(zip(vd.keys(),avi))
            dc=dict(  [ (k,[v]) for k,v in dc.iteritems() ] )
            #^^put it in iters
            paramlist=self.user_getallparamswith(dc) #list of sets
            if len(paramlist)>0:
                for aparamset in paramlist:
                    #values of othervars in the paramset
                    legend={}
                    psd=dict(aparamset)
                    #make 'legend'
                    for avar in othervaryingvars:
                        legend.update({avar:psd[avar]})
                    ls=frozenset(legend.iteritems())
                    if ls not in sd.keys():
                        sd.update({ls:[aparamset]})
                    else: sd[ls].extend([aparamset])
        return sd , consts
    def unacctedtaskfolders(self):
        dirl=os.listdir(self.mydir)
        numberedfolders=[]
        for adir in dirl:
            try: numberedfolders.extend([int(adir)])
            except:pass #non-int dirs (incl float dirs) are not 'tasks' so it's possible to
            #have some non-numerical folders in batch folder
        missingfromtable=frozenset(self.runsi.values())-frozenset(numberedfolders)
        extranumberedfolders=frozenset(numberedfolders)-frozenset(self.runsi.values())
        return {'missingfromtable':missingfromtable,'extranumberedfolders':extranumberedfolders}
    def foldercheck(self):
        uatf=self.unacctedtaskfolders()
        if len(uatf['missingfromtable'])>0:
            print "WARNING: can't find folders for tasks ", list(uatf['missingfromtable'])
        if  len(uatf['extranumberedfolders'])>0:
            print "WARNING: extraneous integer-numbered folders", list(uatf['extranumberedfolders'])
        return uatf
    def getmyvarsets(self):
        varsets=frozenset([])
        for aparamvarset in [(dict(i).keys()) for i in self.runsi.keys()]:
            varsets=varsets.union([frozenset(aparamvarset)])
        return varsets
    def getmyfoldercontents(self,taskids='all',followlinksv=False):
        """no ref to which params. use carefully"""
        if taskids=='all':taskids=self.runsi.values()
        listbytaskid=[]
        for ataskid in taskids:
            w=os.walk(  os.path.join(self.mydir,str(ataskid)) ,followlinks=followlinksv )
            fl=iter([os.path.join(aw[0],awfl) for aw in w for awfl in aw[2] ])
            listbytaskid.append(fl)
        return listbytaskid

    def user_getoutputvsinput(self,dictorsetofinparams,listofpatterns=None): #todo
        """
        keep in mind pattern is matched with full dir, so for a specific file
        you'll need to specify '*\specificfile.x' or '*\specdir\spf.x'
        """
        if listofpatterns==None: listofpatterns=self.outputmapping
        #chking mistake in input:
        if type(listofpatterns)==string:
            print 'input string in a list next time, ok?'
            listofpatterns=[listofpatterns]
        if type(dictorsetofinparams)==dict:
            paramset=frozenset(dictorsetofinparams.iteritems())
        else: paramset=frozenset(dictorsetofinparams)
        taskid=self.runsi[paramset]
        pfnames=list(self.getmyfoldercontents(taskids=[taskid])[0]) #0 just unwraps
        #doesnt work w/ iterator..WHY?!?!
        filematchresults=dict.fromkeys(listofpatterns)
        for astr in listofpatterns:
            astr=str(astr)#just to make sure numbers convert to str
            m= fnmatch.filter( pfnames, astr)
            filematchresults.update({astr:m})
        return filematchresults
        
    def user_getalloutputs(self,listofpatterns=None):
        inputs=self.runsi.keys()
        outsl=[]
        for ani in inputs:
            outsl.append(self.user_getoutputvsinput(ani,listofpatterns))
        z=zip(inputs,outsl)
        return dict(z)
        
    def user_getalloutputoffile(self,filename):
        #inputs=self.runsi.keys()
#        w=os.walk(self.mydir)
#        w.next()#passes root dir
#        fp=[]
#        for ani in inputs:
#            d,nd,fs=w.next()
#            for afile in fs:
#                if filename in fs:
#                    fp.append(os.path.join(d,fs[0]))
#                else: fp.append('')
        fp='*'+filename+'*'
        d=self.user_getalloutputs(listofpatterns=[fp])
        for k,v in d.iteritems():
            firstfind=v[fp][0] #first match
            if filename==os.path.split(firstfind)[1]:d[k]= firstfind
            else: d[k]=None
        #z=zip(inputs,fp)
        return d#z
        
