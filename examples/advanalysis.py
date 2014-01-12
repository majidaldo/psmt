
from analysisbase import analysis
from scriptmgt import batchfoldermgt


import scipy as sp
import numpy as np
from scipy import *
from scipy import optimize
from scipy import stats
from matplotlib import mlab
import itertools

class gkanalysis(analysis):
    
    def gethc2(self,params,resetts=True,takeoutfirstone=True
        ,sumup='all'):
        fns=self.batchobj.user_getoutputvsinput(params,['*cumdE.avetime'])
        d={}
        for afp in fns['*cumdE.avetime']:
            try: #b/c it maybe blank
                ld=sp.loadtxt(afp
                ,unpack=True
                ,usecols=(0,1,2,3))
                for ats,ajal,ajo, ajy in zip(*ld):
                    d.update({int(ats):(ajal,ajo, ajy)})
            except: continue
        tss=sp.reshape(d.keys(),(len(d.keys()),1))
        sa=sp.hstack([tss,d.values()])
        detype=[('ts',int),('jal',float),('jo',float),('jy',float)]
        sa=sp.array(map(tuple,sa.tolist()),dtype=detype) #i just had to make it tuples?!
        #..instead of nested brackets. idk why
        sa.sort(order='ts') #probably unnecessary here
        #..so i don't need ts if i'm taking data every ts
        if takeoutfirstone==True:
            sa=sa[1:]
        if resetts==True:
            sa['ts']=sa['ts']-sa['ts'][0]
        #if sumup==True: return self.sumhc(sa,sumup=sumup)
        return self.sumhc(sa,sumup=sumup)[:1001000]
        #else: return sa
    def sumhc(self,hc,sumup='all'):
        if sumup=='all':
            return sp.sum([hc['jal'],hc['jo'],hc['jy']],axis=0)
        elif sumup==False: return hc #w/ components intact
        summed=sp.zeros(len(hc))
        for ahc in sumup: summed+=hc[ahc]
        return summed
            
    def gethc(self,*args,**kwargs):
        try:  return self.gethc2(*args,**kwargs)
        except :multipleparamsets=args[0]
        def returnhcs(multipleparamsets,**kwargs):
            for aparamset in multipleparamsets:
                yield self.gethc2(aparamset,**kwargs)
        return returnhcs(multipleparamsets,**kwargs)
        
    def shortcutac(self,hc,trimend=True):
        #ac= real(ifft(real(fft(hc))**2))
        ffthc=(sp.fft(hc))
        ac= sp.real(sp.ifft((ffthc)*sp.conjugate(ffthc)))# i believe this
        if trimend==True:
            first90pc=int(len(hc)*.9)
            return self.divac(ac[:first90pc])
        else: return self.divac(ac)
        #last 10% of the series is ALWAYS meaningless

        #..isn't the normalized def.
        #supposely im part should be small
        
        #avgac=sp.average(ac)
        #avgac=sp.average(ac)
        #return ac
        
    def divac(self,ac):
        n=len(ac) #or hc
        ##div=[((n-k)*avgac**2) for k in xrange(n)]
        #divby=[(n-k) for k in xrange(n)]
        ##div=n
        #return ac/divby #ac[:-100000]/divby[:-100000]#(ac[0])#divby
        #chk end of corr for extremes
        return array(ac)/n
        
    def hcacintseries(self,hcac):
        #todo cache
        try: return self.cache['hcint'][hcac[-10:]]
        except:
            self.cache.update({'hcint':{}})
            hcint=sp.cumsum( [sp.trapz(hcac[i:i+2]) \
            for i in xrange(len(hcac-1))] )
            self.cache['hcint'].update({ tuple(hcac[-10:]) : hcint })
            return hcint
            
    def convertconductivity(self,params,dt=.001e-12):
        """multiply the integral by this"""
        #dt in ps; xyz in Ao; T in K
        #"18592486.74*integral*dt/x/y/z/T^2"
        params=dict(params)
        a=(params['Tk']*9.67114349e-05)+12.3918 #lattice const
        convert=(1/1e-12)*18592486.74*\
        dt/params['dx']/params['ly']/params['lz']/params['Tk']**2/a**3
        return convert
        
    def getkseries(self,params,ac,dt=.001e-12):
        """hcac integral in W/mK"""
        #dt in ps; xyz in Ao; T in K
        #"18592486.74*integral*dt/x/y/z/T^2"
        params=dict(params)
        #hc=(self.sumhc(self.gethc(params)))
        #ac=self.shortcutac(hc)
        #schcac=self.divac(schcac) #just a div by N for "stochastic" process
        hcintegral=self.hcacintseries(ac)
        convert=self.convertconductivity(params)
        return convert*hcintegral
        
#    def findpeaks(self, spectra,win,peaktol=.025): #401 in my case
#        #need to input below nyquist
#        """input noisy spectra
#        1st filters it b/c too many "needles" on a spike
#        """
#        fs=(savitzky_golay(spectra,win,5)) #play w/ these params
#        pt=peaktol*max(fs)
#        return dict(peakdet(fs,pt)[0]) #dict it?



#max freq  N/(2T) T is sampling time
#T=N*dt
#=>maxfreq= 1/(2*dt) = 1/(2*.001*1e-12) . /1e12 for THz todo: is there a 2pi factor here?
#around 500THz. vibes are around 4thz factor of 2

    #note psd chokes at nfft lower than n/2
    #works faster for even but few times the even no. takes a while. idkw
    #eg. 18000 vs 18002 for a len(tsd)=1e6
    def psd(self,tsd,seg=1024*16,dt=.001e-12,sides='onesided',scalebyfreq=True
    ,divby2=True
    ,takeeven=True,nsigfigs=3 #performance params
    ,chopoff=True): 
        if takeeven==True: seg=seg- ( seg % 2) #make even
        if nsigfigs!=None:
            bigno=seg
            numofdigits=int(math.log(bigno,10))+1
            divby=10**(numofdigits-nsigfigs)
            sigfigs=bigno/divby
            seg=int(sigfigs*divby)
            #return seg
        #when nfft is big, the psd calc becomes slow so it's good enough just to
        #take the nearest (lower?) even
        #if seg is odd, it will go down by 1 to make it even
        
        """a shortcut to get psd at expense of freq fidelity"""
        #seg default good for length ts ~1e6
        ps= mlab.psd(tsd,NFFT=seg
        ,Fs=1.0/(dt)#/2 #i guess this Fs is what i want
        ,scale_by_freq=scalebyfreq
        ,sides=sides#'twosided'
        #,detrend=mlab.detrend_mean
        #,noverlap=0
        #,pad_to=None
        ) 
        #return ps[1]*((2*ts)**-1) \
        #, ps[0] #freq vs power
        #return ps[1], ps[0]#/(pi)**.5 #freq in hz vs power
        ps=list(ps)
        if divby2==True:ps[0]=ps[0]/2
        if chopoff==True: return chopoffspectra([ps[1], ps[0]])
        else: return [ps[1], ps[0]]
        
    def smoothspectra(self,spectra,winfrac=.001):#useless
        #todo winfrac per f
        #useless?
        """Input spectra w/o mirror image""" #it has to do w/ width of peak
                                            #that is rel to size of features
        win=int(winfrac*len(spectra))
        if win%2==0: win+=1
        return (savitzky_golay(spectra,11,0)) #201 gets the peaks
    def findpeaks(self,spectra,peaktol=.025):
        """peaktol: fraction of highest spike
        returns {freq:amp}. spectra should be smoothed
        spectra has x index
        """
        #spectra can be a bit noisy but not so much
        # that you have 'needles' on the order of the spike
        pt=max(spectra[1])*peaktol
        return dict(  peakdet(spectra[1],pt,x=spectra[0])[0]  ) #zero idexes peaks
    def returnpeaklocs(self,*args,**kwargs):#just need to put in .psd args
        pt=kwargs.pop('peaktol')     
        sg=self.psd(*args,**kwargs)
        peaks=self.findpeaks(sg,peaktol=pt) #cool prog'ing!
        return sorted(peaks.keys())
        
    def findbestnfft(self,tsd,dt=.001e-12
    ,peaktol=.03,minpeakfreqdiff=.5e12 #physics params reject anything w/ dfreq smaller than ftol
    #..so smaller values of these give more peaks..but too low and you get "false" peaks    
    #,guessdf=None,cutfreq=None
    ,atatime=2,ntol=.98,minn=1024 #optimization params
    ,returnpeaks=False
    ,statmsgs=True):        
        #maxfreq=1.0/(dt*2)
        maxn=len(tsd)    
        #mindf=maxfreq/(maxn/2.0) #eqn. (maxfreq is const)
        """
        physical params
            peaktol: fraction of max peak to be id.ed as a peak
            ftol: min freq b/w peaks. used to eliminate noise adjacent to peaks
        optimization params
            ntol: frac of possible optimal numbers
            atatime: random no.s to assess at a time (not important. keep it 2)
        """
        
#        #a guess
#        if guessdf==None: guessdf=mindf*2 #ohh let's start somewhere in the middle
#        #but if you gave a startdf it has to be bigger than min df
#        if guessdf<mindf:
#            raise ValueError, 'given start freq rez is smaller than the smallest\
#            possible:'#, mindf
        
        #n=int(round( 2*maxfreq/guessdf )) #is there a 2 factor?

        #loop trytofind until not none.
        wadv=winadvisor(minpeakfreqdiff,maxn/2-2)        
#        wadvid=(tuple(tsd[:10]),peaktol,ftolmin) #using 1st 10 no.s as an id
#        try:
#            wadv=self.cache['wadvs'][wadvid]
#            print 'got from cache'
#        except:
#            print 'didn\'t get from cache'
#            wadv=winadvisor(ftolmin,maxn/2-2)
#            self.cache.update({'wadvs':{wadvid:wadv}})
#            wadv=self.cache['wadvs'][wadvid] #necessary?
#             #-2 is just a safety buffer
        
#        wintry=[n-2,n-1] #funcs as a 1st try (guess)
#        print wintry
#        pl1=self.returnpeaklocs(tsd,dt=dt,peaktol=peaktol,seg=wintry[0])
#        pl2=self.returnpeaklocs(tsd,dt=dt,peaktol=peaktol,seg=wintry[1])
#        result=wadv.trytofindhifi( wintry, [pl1,pl2] )
#        del pl1; del pl2
#        print result,wadv.stop
#        return wadv

        #to accel. finding optimum n, get for pwrs of two upto n
        highestpwrof2=int(math.log(wadv.n,2))
        lowestpwrof2=int(math.log(minn,2)); del minn
        twotothes=[]
        for apower in xrange(lowestpwrof2,highestpwrof2+1):
            #assert type(apower)==int
            twotothes.append(2**apower)
        datas=[]
        if statmsgs==True: print '**initial scan (powers of 2)'
        for apo in twotothes:
#            if statmsgs==True:
#                print 'finding peaks for n=', apo
            plfid=(tuple(tsd[-10:]),dt,peaktol,apo) #id'ed w/ these
            try: pl=self.cache['plf'][plfid]#;print 'from cache'
            except:#not in cache
                pl=self.returnpeaklocs(tsd,dt=dt,peaktol=peaktol,seg=apo)
                self.cache.setdefault('plf',{})
                self.cache['plf'].update({plfid:pl})
                if statmsgs==True:
                    aorr=wadv.acceptorreject(pl)#wadv.evaled[apo]
                    if aorr==True: aorr='accepted'
                    else: aorr='rejected'
                    print 'found', len(pl), 'peaks for nfft=', apo,'.',aorr
            datas.append(pl)
        result=wadv.trytofindhifi( twotothes, datas )        
        if statmsgs==True: print '**initial scan complete'
        
        
        #import time
        #print wadv.n
        #todo: persist wadv cache wadv
        result=None
        while len(wadv.evaled.keys())/float(wadv.n)<ntol or result==None:
            #print result,len(wadv.evaled.keys())/float(wadv.n)
            try:
                #time.sleep(1)
                rns=wadv.getrandints(atatime,minn=1)
                datas=[]
                for arn in rns:
                    #if statmsgs==True: print 'finding peaks for n=', arn
                    pl=self.returnpeaklocs(tsd,dt=dt,peaktol=peaktol,seg=arn)
                    if statmsgs==True:
                        aorr=wadv.acceptorreject(pl)#wadv.evaled[apo]
                        if aorr==True: aorr='accepted'
                        else: aorr='rejected'
                        print 'found', len(pl), 'peaks for nfft=', arn,'.',aorr                   
                    datas.append(pl)
                result=wadv.trytofindhifi( rns, datas )
                #return wadv
                if statmsgs==True:
                    print 'stop?', wadv.stop #when the nfft diff =1
                    print 'accepted nfft\'s', result
                    print 'eval\'ed no.s fraction', len(wadv.evaled.keys())/float(wadv.n)
                #but if..
                if wadv.stop==True or 1==len(wadv.evaled.keys())/float(wadv.n): break
                    #return result #lo pri todo: does this work?
            except:# if the result is unexpected just try again
                result=None
        if returnpeaks==False:return result
        else: return result, self.findpeaks(self.psd(tsd,dt=dt,seg=result),peaktol=peaktol)
        

    def solveforpeaksparams(self,spectra,peaks=None,maxfreq=1,tauguess=None):#10e-12 
        """input smooth spectra
        notes:
            - only sure if spectra w/o index
            - 
        """
        if len(sp.shape(spectra))==1:# if no freq index take list index as freqs
            fi=sp.linspace(0,maxfreq,len(spectra))
            spectra=[fi,spectra]
        else: maxfreq= spectra[0][-1]
        #possibly use the shortcut psd
        #ss=self.smoothspectra(spectra[1])
        ss=spectra[1]
        if peaks==None:peaks=self.findpeaks([spectra[0],ss])
        peaksfunc=returnsumofpeaksfx(sp.array(peaks.keys())
        ,len(spectra[0]),maxfreq=maxfreq)
        
        if tauguess==None:#tau based on weighted avg of freqs
            tauguess=sp.average(spectra[0],weights=spectra[1])**-1*1000
            #assume the freq lasts 100-1000 times its cycle time?
        
        print 'no. of peaks detected:' , len(peaks)
        #guess as a vec
        
        #the peak val is actually something like a*tau so i put that in as a guess
        guess=sp.array(  list( sp.array(peaks.values())/tauguess)+([tauguess]*len(peaks))   )
        #guess=sp.array(([1]*len(peaks))+([tauguess]*len(peaks)))
        #.01 assumes typical spectra. just input the 'busy' part of the spectra
        #for some reason the guess needs to be close or else the solver wont find it
        
        #input one vec the abs is b/c i don't want the peaks func to see negs
        minfunc= lambda X: (peaksfunc( *sp.hsplit(sp.absolute(X),2) )  - spectra[1])
        #minscalar= lambda X: sum( minfunc(X)**2 )*tauguess**-1*10e6 #to make it a big no.

        #posbounds=[] #keep it +.
        #for avar in guess: posbounds.append((0,inf)) #Inf for other than bfgs
        s=sp.optimize.leastsq( minfunc, guess
        #couldn't get the below to work        
        #s=sp.optimize.fmin_l_bfgs_b( minscalar, guess,bounds=posbounds
            #,approx_grad=True,factr=10#?
            #,disp=2
        #s=sp.optimize.fmin_slsqp( minscalar, guess,bounds=posbounds,iprint=2
        #s=sp.optimize.fmin_tnc( minscalar, guess,bounds=posbounds,approx_grad=True

        #, xtol=1e-15 ,ftol=1e-15
        #,maxfev=0
        )
        heights,hwhms=sp.absolute(sp.hsplit(s[0],2)) #sp.absolute
        fit=[spectra[0],peaksfunc( heights, hwhms ) ]
        peakparams=dict(zip(peaks.keys(),zip(heights,hwhms)))
        #print peakparams#,max(fit[1]),trapz(fit[1]) #,'solver.o':s
        
        return {'peaksparams':peakparams,'fit':fit}#,'spectra':spectra} #,'solver.o':s
    
#    def solveforanexpdecayparams(self,*args,**kwargs): #not used
#        #1. from spectra, get tau guesses and az
#        #2. normalize az
#        #3. give it to func fitter
#        bestn=self.findbestwinsize(*args,**kwargs) #todo..fill
#        return az,tauz

    def solveforgkintparams(self,params,**kwargs):#,maxfreq=40e12):
        hc=kwargs.setdefault('hc',self.gethc(params,sumup='all'))
        kwargs.pop('hc')
        """maxfreq to analyze"""
#        try:
#            nfft=kwargs['nfft']# confusing! and doesn't make sense
#            #w/ just a peaktol constraint
#            self.findpeaks(self.psd(tsd,dt=dt,seg=result),peaktol=peaktol)
#            peaks=self.findpeaks([freqs,spectra],**kwargs)
#        except:
#            kwargs.update({'returnpeaks':True})            
#            nfft,peaks=self.findbestwinsize(hc,**kwargs)
        kwargs.update({'returnpeaks':True})            
        nfft,hzpeaks=self.findbestnfft(hc,**kwargs)
        #i found no need to include beyond 40(20?!) thz
        freqs,spectra=self.psd(hc,scalebyfreq=True,seg=nfft,chopoff=True) #spectra should be 1 sided
#        #somehow the scalebyfreq makes the psd comparable to closed form soln
#        #find index of maxfreq
#        for afreq in freqs:
#            if afreq>maxfreq:
#                fl=list(freqs)
#                imf=fl.index(afreq)
#                break
        #div spectra to a more manageable no. ..
        #magscale=(max(spectra)) #..to help the solver
        #already div by 2 in the psd
        #spectra=spectra/2 #!??!?! #b/c this is what the peakfit expects
        #*2.566972197*10**(-34)#/magscale #later x by magscale
        #can't do this..messes up time scale
#        maxfreq = freqs[imf] #Hz
        
        #pps=self.solveforpeaksparams(spectra[:imf],maxfreq=maxfreq*2*pi) #rads     
                
        #convvert peaks
        radpeaks={}        
        for ahzpeakloc,itspeakval in hzpeaks.iteritems():
            radpeaks.update({ahzpeakloc*2*sp.pi:itspeakval})
        del hzpeaks
        pps=self.solveforpeaksparams(spectra,peaks=radpeaks,maxfreq=freqs[-1]*2*pi) #rads
        #return pps
        #dfreq=maxfreq/(imf+1) #how imf cancels?
        #dfreq=freqs[-1]/(len(spectra)-1)
        T=dict(params)['Tk']
        a=(T*9.67114349e-05)+12.3918
        V=dict(params)['dx']*dict(params)['ly']*dict(params)['lz']*(a**3)
        kinfo={}
        for apeakloc,pparams in pps['peaksparams'].iteritems():
            #, i0 is height, i1 is halfwidh at half max
            peakfreq=apeakloc#rads  #*maxfreq
            tau=(pparams[1]) #idk why
            a=pparams[0]#todo magscale factor here prob has dt or ttime
            #print tau, a, apeakloc/2/pi/1e12
            pps['peaksparams'].update({apeakloc: (a
                ,pparams[1]#*magscale why did i do this?
                #, (maxfreq*pparams[1])**-1
                )}) #use pparams[1] to draw
            #conductivity="h*.9296243367e43/V/T^2/(1e24+tau^2*wo^2)"
            #conductivity=a*9.296243367e18/V/(T**2)/(1+(tau**2)*((peakfreq*2*pi)**2))\
            #conductivity=a*9.296243367e18/V/(T**2)/(1+(tau**2)*((peakfreq*2*pi)**2))
            #conductivity=(7.242963817e52/V/(T**2))    *(2.566972197e-34)*a/(1+(tau**2)*peakfreq**2) \
            #/(peakfreq/2/pi)
            #factor has conversions and 
            conductivity=2*pi*(1.859248674*10**19)*a*tau/V/T**2/(1+(tau**2)*peakfreq**2)
            if conductivity<0: print 'WARNING: negative conductivity component calculated.'
            kinfo.update({apeakloc:{'k':conductivity,'tau':tau,'f':peakfreq/2/pi}})
        pps.update({'kinfo':kinfo})
        fit=pps['fit']
        pps['fit']=[fit[0]/2.0/pi,fit[1]] #backto hz
        return pps
    

    def solveforavggkintparams2(self,*args,**kwargs):
        """a fx to reduce variability in the conductivity calc due to nfft
        sensitivity"""
        #only do if nfft not spec
        ncalcs=kwargs.setdefault('ncalcs',5) #no. of procedures
        ncalcs=kwargs.pop('ncalcs')
        calcs={}
        #gather the data
        for procn in xrange(ncalcs):
            acalc=self.solveforgkintparams(*args,**kwargs)
            calcs.update({procn:acalc})
        #group same freqs by least diff
        #use the one w/ the max no. of peaks
        #stats
        #eh not gonna worrk. just sum and put a std dev        
        ks=[]
        for acalc in calcs.iteritems():
            ks.append(sumks(acalc[1]['kinfo']))
        calcs.update( {'k': ( average(ks),sp.std(ks) )} )
        return calcs
    def solveforavggkintparams(self,*args,**kwargs):
        """this func is for processing lists of inputs"""
        params=args[0]
        #hc=args[1]
        #"scalar" case: one HC. one paramset
        try: params[0] #if just one paramset (not in a list) input this should fail
        except:
           # if len(shape(hc))==1:
               return self.solveforavggkintparams2(*args,**kwargs)
        #else expect a set of set of params
        paramslist=params; del params #name change
        #hclist=hc; del hc
        #a hc list for one paramset makes sense
        #..but not the other way around
        #assert len(paramslist)==len(hclist)
        #todo=dict(zip(paramslist,hclist))
        
        def returncalcgen(*args,**kwargs):
            for aparams in paramslist:
                acalc=self.solveforavggkintparams2(aparams,**kwargs)
                yield acalc
#        calcs={}
#        def returncalcgen(*args,**kwargs):
#            solverlooper=itertools.izip(paramslist),hclist)
#            for aparams,ahc in solverlooper:
#                #hcs=todo[aparams]
#                if len( shape(ahc) )==1: #ie just a vector
#                    acalc=self.solveforavggkintparams2(aparams,**kwargs)
#                    yield acalc
#                else: raise Exception, 'input HC not a vector'
                    #calcs.update({aparams:acalc})
#            else: #list of HCs
                #subcalcs=[]
#                    for ahc in hcs:
#                        acalc=self.solveforavggkintparams2(ahc,**kwargs)
#                        subcalcs.append(acalc)
                #calcs.update({aparams:subcalcs})
        return returncalcgen(*args,**kwargs)#calcs
        
    def savegkcalcs(self,paramslist,gkcalcs,solntype):
        #solnlooper=itertools.izip(paramslist,gkcalcs)
        savedataconstsolntype=lambda params,data: self.savedata(params,solntype,data)
        map(savedataconstsolntype,paramslist,gkcalcs)
        return
#        for aparams,acalc in solnlooper:
#            i=self.batchobj.runsi[aparams]
#            self.data[solntype][i]=acalc;del i
#        return
        
    def solvegktimeint2(self,params,hc=None,sumhcparts='all'
        ,zerotol=.05,stablepart=.02,taumultiplecutoff=30#or 15 #hc
        ,dt=.001e-12,minfreq=.01e12#,win=None #100k win (.01thz) seems best
        #detrending is futile
        ,nbins=100):
        if hc==None:hc=self.gethc(params,sumup=sumhcparts)
        #1#nstable=int(stablepart*len(hc))#it was found that 1st 2% of ts is stable
        #by 5%        
        #hc=detrendhc(hc,dt=dt,minfreq=minfreq)#win=nstable)#linear detrend
        #1#ac=self.shortcutac(hc,trimend=False)[:nstable]
        ac=self.shortcutac(hc,trimend=True)
        #cutac=chopoffactail(ac,zerotol=zerotol)
        #if len(cutac)/float(len(hc)) < stablepart: #if it's too short
        #    nstable=int(stablepart*len(hc))
        #    ac=self.shortcutac(hc,trimend=False)[:nstable]
        #else: ac=cutac;del cutac
        pxx,pys=returnpeaksofabsac(ac,peaktol=zerotol)
        a,tau=fitexpdecay(pxx,pys)
        #now cutoff at (5 to 10)tau
        itau=int(tau/dt)#;print itau
        ac=ac[:taumultiplecutoff*itau] #need 30 for the ones w/ doping, less for others
        ks=self.getkseries(params,ac,dt=dt)
        #plot(ks)
        h,lowest,binsize,useless=sp.stats.histogram(ks#[4*tau:]#doesn't matter
        #..for my procedure
            ,numbins=nbins,defaultlimits=(0,max(ks)),printextras=False)
        del useless;del lowest #b/c i set lowest to 0
        h=list(h)
        maxbini=h.index(max(h))
        lowerbound=maxbini*binsize;upperbound=lowerbound+binsize
        return {'ks':ks,'k':(average([lowerbound,upperbound]),binsize/2.0)\
            ,'tau':tau,'a':a}
    def solvegktimeint(self,*args,**kwargs):
        paramsorlistofthem=args[0]
        try: return self.solvegktimeint2(paramsorlistofthem,**kwargs)
        except:#list of params
            def returncalcgen(*args,**kwargs):
                for aparams in paramsorlistofthem:
                    print 'processing ', self.params[aparams]
                    acalc=self.solvegktimeint2(aparams,**kwargs)
                    yield acalc
            return returncalcgen(*args,**kwargs)

def gkproctest1(gkao,params,hc):
    tauxs=range(5,60);ks=[]
    for ataux in tauxs:
        print 'processing tau x', ataux
        k=gkao.solvegktimeint(params,hc=hc,taumultiplecutoff=ataux)['k'][0]
        ks.append(k)
    return tauxs, ks
def gkproctest(gkao,paramslist,hcs=None):
    if hcs==None: hcs=gkao.gethc(paramslist)
    results={}
    for aparams in paramslist:
        ahc=hcs.next()
        r=gkproctest1(gkao,aparams,ahc)
        results.update({aparams:r})
    return results

def plotgkproctest(gkao):
    results=gkao.data['gkproctest']
    ys=[]
    for aparams,xy in results.iteritems():
        ys.append(xy[1])
        xs=xy[0]
        #xl=random.choice(xs);yl=dict(zip(*xy))[xl]
        #print xl,yl
        #matplotlib.pyplot.text( xl,yl,yl)
        plot(*xy,label=str(gkao.params[aparams]))
    plot(xs,np.sum(ys,axis=0))
    return

def plotcondtrends(gkao,kcalctype,trends='all'
    ,subset={'ly':[2],'dx':[4,8,16,32,64],'Tk':[300]}): #or 'int'..egral
    if trends=='all': #else fronzenset(dict)
        r=gkao.batchobj.user_groupbyconsts(['dx','dseed','vseed']
            ,subsetdictofiters=subset)#,'ly','lz']#i1 is for the const throughout
        trends,consts=r[0],r[1];del r
#    trendsforseeds=gkao.batchobj.user_groupbyconsts(['dseed','vseed']
#            ,subsetdictofiters=subset)[0]
#    knoseeds={}
#    for ast, paramlist in trendsforseeds.iteritems():
#        ks=[]        
#        for aps in paramlist:
#            ti=gka.params[aps]
#            if ti in gkao.data[kcalctype].keys():
#                k=gkao.data[kcalctype][ti]['k']
#                ks.append(k)
#        knoseeds.update({ frozenset(ast):(average(ks),sp.std(ks)) })
        #keys have dx and dp
    for atrend, paramlist in trends.iteritems():
        kt={}#;xls=[];ks=[];kerrs=[]
        #atd=dict(atrend)
        for aparamset in paramlist:
            psd=dict(aparamset)
            taskid=gkao.batchobj.runsi[aparamset]
            T=psd['Tk']
            a=(T*9.67114349e-05)+12.3918
            xl=a*psd['dx']
            k=gkao.data[kcalctype][taskid]['k'];print taskid,k
            if k=={}: continue
            #else: k=k,0 for plotting tau
            kt.setdefault(xl,[])
            kt[xl].append(k[0])
            #xls.append(xl);ks.append(k[0]);kerrs.append(k[1])
        #print xls,ks,kerrs
        ktreduce={}
        for alength, ks in kt.iteritems():
            ktreduce[alength]=(average(kt[alength]),sp.std(kt[alength]))
        del kt
        xls,[ks,kerrs]=ktreduce.keys(), array(ktreduce.values()).transpose()       
        #^coool code!        
        kdata=array( zip( array(xls)**-1 ,  tuple(ks), tuple(kerrs)  )
            ,dtype=[('x^-1',float),('k',float),('kstdev',float)]   )
        kdata.sort(order='x^-1')
        #print consts
        lbl=frozenset.union(atrend,frozenset([(k,v[0]) for k,v in consts.iteritems()]))
        #print lbl        
        matplotlib.pyplot.errorbar(kdata['x^-1'],kdata['k'],yerr=kdata['kstdev']
           ,marker='o',label= str(dict(lbl)['dp']*100)  )
    legend(mode='expand',ncol=len(trends))
    plt.xlabel(r'$length^{-1}$ ($\AA^{-1}$)')
    plt.ylabel(r'Conductivity ($W\cdot m^{-1}K^{-1}$)')
    return
#def markcalcedhc(calcedk,tau):
#    atau=tau/.63
#    mpl.scatter(atau,calcedcond)
#    return

#should be given data
def plotkintandtau(gkao,params,hc,**kwargs):
    dt=kwargs.setdefault('dt',.001e-12)
    kwargs.pop('dt')
    gks=gkao.solveforavggkintparams(params,hc,**kwargs)
    calcedcond=gks['k']
    gks.pop('k')
    maxtaus=[]
    for acalck,info in gks.iteritems():
        taus=[]
        for afreq,infos in info['kinfo'].iteritems():
            taus.append((infos['tau']))
        maxtaus.append(max(taus))
    atau=average(maxtaus)*4 #the pt where conductivity is at the asymptotic value
     # a tuple
    hcacint=gkao.getkseries(params,hc,dt=dt)
    #todo: it's a waste to gen the xs. find units in the plot
    matplotlib.pyplot.plot(sp.linspace(0,len(hcacint)*dt,len(hcacint),endpoint=False),hcacint)
    matplotlib.pyplot.errorbar(atau,calcedcond[0],yerr=calcedcond[1]
        ,marker='o',c='r')
    return

import matplotlib
from matplotlib import rc
rc('text',usetex=False) # r'string'
matplotlib.rcParams['mathtext.default']='regular'
def plotniceac(gkao,hc,dt=.001e-12,endt=20e-12):
    dtps=dt/1e-12
    plt.xlabel(r'time (ps)');
    plt.ylabel(r'$\left\langle S_{x}(t)\cdot S_{x}(0) \right\rangle/\left\langle S_{x}(0)\cdot S_{x}(0) \right\rangle$')
    ac=gkao.shortcutac(hc)[:int(endt/dt)]
    xs=sp.linspace(0,len(ac)*dtps,len(ac),endpoint=False)
    p=plot(xs,array(ac)/ac[0])
    return (xs, ac),p
def plotniceabsac(gkao,hc,dt=.001e-12,endt=20e-12):
    dtps=dt/1e-12
    plt.xlabel(r'time (ps)');
    plt.ylabel(r'$|\left\langle S_{x}(t)\cdot S_{x}(0) \right\rangle/\left\langle S_{x}(0)\cdot S_{x}(0) \right\rangle|$')
    acr=gkao.shortcutac(hc)[:int(endt/dt)]
    ac=abs(array(acr))/acr[0]
    xs=sp.linspace(0,len(ac)*dtps,len(ac),endpoint=False)
    p=plot(xs,ac)
    return (xs, acr),p
def plotniceint(gkao,params,ac,dt=.001e-12,endt=20e-12):
    dtps=dt/1e-12
    plt.xlabel(r'time (ps)');
    plt.ylabel(r'Conductivity ($W\cdot m^{-1}K^{-1}$)')
    plt.ylim(0,15)
    ac=ac[:int(endt/dt)]
    ks=gkao.getkseries(params,ac,dt=dt)
    xs=sp.linspace(0,len(ac)*dtps,len(ac),endpoint=False)
    p=plot(xs,ks)
    return (xs,ks),p
def plotniceacproc(gkao,params,hc,dt=.001e-12):
    gks=gkao.solvegktimeint2(params,hc=hc)
    n=len(gks['ks']);tau=gks['tau'];a=gks['a']
    ac=plotniceabsac(gkao,hc,dt=dt,endt=30*tau)[0]
    ED=genexpdecay(a/ac[1][0],tau,0,dt=dt,n=n)
    pxx,pys=returnpeaksofabsac(ac[1]/ac[1][0],peaktol=.05,dt=dt)
    scatter(array(pxx)/1e-12,pys,color='red')
    plot(ED[0]/1e-12,ED[1],color='black')
    return
def plotnicepsd(gkao,hc,**kwargs):
    plt.xlabel(r'frequency (THz)');
    plt.ylabel(r'a.u./frequency')
    psdd=gkao.psd(hc,**kwargs)
    plot(psdd[0]/1e12,psdd[1])
    return
def plotnicepsds(gkao,hcs,**kwargs):
    plt.yscale('log');plt.ylim(1e-9,None)
    plt.xlim(0,30)
    for ahc in hcs:
        plotnicepsd(gkao,ahc)
    plt.legend(['x=0%','x=50%'],ncol=2,loc=4)
    return

#moving avg not as general
#useless
def runningstd(ac,mu=0):
    sumsq=0
    ninvals=0
    stds=[]
    for anum in ac:
        if anum>0:
            ninvals+=1
            sumsq+=anum**2
            stds.append((sumsq*ninvals**-1)**.5)
        else: stds.append(stds[:-1])
    return stds #exactly as runningstd2
        
def runningstd2(ac):    return [sp.stats.tstd(ac[0:i+2],limits=(0,None))\
        for i in xrange(0,len(ac))]

#better than using avgs b/c dists are less sensitive to extremes

#useless?
def findstabilizedi(ac,conf=.95,xstd=.1,skip=0):#,noise=.05,chi2tol=8):nbins=30,
    sumsq=0
    ninvals=0
    ninstds=0
    stds=[]
    i=0
    for anum in ac:
        if anum>0:
            ninvals+=1
            sumsq+=anum**2
            curstd=xstd*(sumsq*ninvals**-1)**.5
            if anum<curstd: ninstds+=1
            stds.append(curstd)
        else: stds.append(stds[:-1])
        #if i+1<=skip:print i;pass#?#can be skip past early vals
        if float(ninstds)/ninvals > conf:return i
        #print i,float(ninstds)/ninvals
        i+=1
        

    #for i in xrange(ii+1,len(ac)-1):
        
#             #thisstd=sp.stats.tstd(ac[:i+2],
    #assert 0<conf and conf < 1
    #minac=min(ac);maxac=max(ac) #avg should be about 0
    #binranges=sp.linspace(minac,maxac,nbins+1)#last bin in hist2 is for
#    #>than last bin in array  #and i will ignore it

#95pc in the middle idea
#    def returnbinrange(binranges,binno):return binranges
#    def returnbinranges(binranges):
#        binsd=[]
#        for i in binranges[:-1:2]:
#nmostbins=
    #def myhist(*args,**kwargs): sp.stats.histogram2(ac,
    #bins=sp.zeros(  len(binranges)-1   ,dtype='int')
        #bins+=sp.stats.histogram2(ac[i],binranges)[0][:-1]#don't want the last bin
        #which is for vals from the last range to inf
        #chi2=sp.stats.normaltest(ac[i],binranges)[0] #i0 is chi2
        #if chi2<chi2tol: return ac[0:i]
        #how many in limits?


#        tstdd=nan
#        ii=2 #ewwww not pythonic
#        while tstdd==nan:#being really pedantic here
#            tstdd=sp.stats.tstd(ac[0:ii],limits=(0,None))
#        invals=[]
#        for i in ac[0:ii]: if i>0:invals.append(i)
#        ninvals=len(invals)
#        inavg=average(invals);del invals
#        
#        for i in xrange(ii+1,len(ac)-1):
#             #thisstd=sp.stats.tstd(ac[:i+2],
#            val=ac[i]
#            if val > 0:
#                inavg=(inavg)*ninvals/(ninvals+1)+val/(ninvals+1) #previous sum + new no.
#                ninvals+=1
#                tstdd=




from scipy import signal
def detrendhc(hc,dt=.001e-12,minfreq=.01e12,win=None):
    if win==None:win=int(minfreq**-1/dt)#
    bp= xrange(0,len(hc),win) #pts in b/w detrending
    dts=sp.signal.detrend(hc,type='linear',bp=bp) #or type 'constant'
    return dts


def genexpdecay(a,tau,w0hz,dt=.001e-12,n=1e6):
    ts=sp.linspace(0,dt*n,n,endpoint=False) #time series
    return [ts,a*cos(w0hz*2*pi*ts)*exp(-ts/tau)]
def fftofexpdecay(*args,**kwargs):
    kwargs.setdefault('ang','rads')
    args=list(args)
    args[0]=args[0]**.5 #to take it 'back' to x(t)
    expd=(   (genexpdecay(*args)[1])  )
    #expd=expd/range(1,len(expd)+1)
    ##return expd
    #p=gkad( expd ,    ts=.001e-12)
    
    #ifftexpd=(sp.fftpack.irfft(expd))
    #fftexpd=(sp.fftpack.rfft(expd))
    #return ifftexpd
    p=gka.psd( expd ,    ts=.001e-12  )
    if kwargs['ang']=='rads': return 2*sp.pi*p[0],p[1]#,(p[1]**.5)
    else: return p[0],p[1]

def genhc(a,tau,w0hz,dt=.001e-12,n=1e6,seed=None):
    """params correspond to a*exp(-1/tau)*cos(w) in the A.C."""
    #s/n up w/ n
    tau=float(tau)
    ts=sp.linspace(0,dt*n,n,endpoint=False) #time series
    aa=(sp.e**(1.0/(tau/dt)))**-1.0 #tau just from here
    sigma=(a-a*aa**2)**.5#a from here
    
    #an approx
    if w0hz==0: sinusoid=1
    else: sinusoid=cos(2*pi*w0hz*ts)*(2**.5)##by observation! i think it works
    #..for any fnc
    drunk=array(  ar(n,[aa],sigma=sigma,seed=seed)   )
    return sp.array([ts, drunk*sinusoid ])
    


def ar(n,alpha,sigma=1,seed=None): #magic 
#put no.s in even places in the input vec
#vector input is linear
#"cleaner" spectogram w/ longer vec
#neg no.s for oscilations
#peaks widths change w/ 
    if seed!=None:sp.random.seed(seed) #then it will assign a seed
    #sig=1
    mu=0
    errors = np.random.normal(mu, sigma, n)
    #sp.random.seed(123)
    #alpha = np.random.uniform(0,1,p) #sationary <1
    values = np.zeros(n)
    
    for i in xrange(len(values)): # i changed range to xrange
        value = 0
        n = len(alpha) if len(alpha)<=i else i
        for j in xrange(n):
            value = value + alpha[j] * values[i-j-1]
        values[i] = value + errors[i]
    return values
    
def rawpsd(d): return (abs(sp.fft(d))**2)/len(d)

def sumks(peaksparams):
    k=0
    for apeakloc,pparams in peaksparams.iteritems():
        k+=pparams['k']
    return k

def plotpeaks(peaksparams,maxfreq=1,n=300):
    for apeakloc,pparams in peaksparams.iteritems():
        plot(sp.linspace(0,maxfreq,n)
        ,returnsumofpeaksfx([apeakloc],n,maxfreq=maxfreq)([pparams[0]],[pparams[1]]))
    return

#from scipy.stats import cauchy
def returnsumofpeaksfx(peaklocs,specsize,maxfreq=1):
    """returns a fnc that takes in dist. params (as an array)
    """
    #kwargs.setdefault('specrange',specsize)
    #input params[] as vec
#    def dist(xs,x0,g,h):
#        pdf= lambda x: h/(1+((x-x0)/g)**2)
#        return sp.array(map(pdf,xs))

    xs=sp.linspace(0
    ,maxfreq #?!?!?!
    ,specsize) #so this shouldn't be regened
    #w/ each soln iteration
    xs2=xs**2
    
    #for cauchy height=1/(pi*gamma)
    
    #def peakgen(h,f,freqscale):
#    def peakgen(h,f,hwhm):
#        #halfwidth at half max is frac relative to freq scale
#        return h/(  ((xs-f)/hwhm)**2  +  1 ) #graphical
        #return h*g**2/((xs-f)**2+g**2)
#        return cauchy.pdf(xs*freqscale
#            ,scale=((pi*h)**-1)
#            ,loc=f*freqscale)



    def peakgen(A,w0,tau): #radians
        #"2*A*tau*(1+w^2*tau^2+w0^2*tau^2)
        #/(1+w^2*tau^2+2*tau^2*w*w0+w0^2*tau^2)
        #/(1+w^2*tau^2-2*tau^2*w*w0+w0^2*tau^2)"
        #tau=abs(tau)#don't want any neg. taus
        #..or As
        #A=abs(A)
        w02=(w0)**2; tau2=(tau)**2
        return 2*A*tau*(1+xs2*tau2+w02*tau2) \
         /(1+xs2*tau2+2*tau2*xs*w0+w02*tau2) \
         /(1+xs2*tau2-2*tau2*xs*w0+w02*tau2)
        #return 2*A*tau/(1+((xs-w0)**2)*tau**2)

#    #goes w/ below
#    xs=xs*2*pi
#    xs2=xs**2
#    def peakgen(A,zeta,tau): #Hz
#        #"8*A*tau*Pi^2*(4*Pi^2+4*tau^2*w^2*Pi^2+tau^2*zeta^2)
#        #/(4*Pi^2+tau^2*zeta^2-4*tau^2*zeta*w*Pi+4*tau^2*w^2*Pi^2)
#        #/(4*Pi^2+4*tau^2*w^2*Pi^2+4*tau^2*zeta*w*Pi+tau^2*zeta^2)"
#        zeta2=(zeta)**2; tau2=(tau)**2; pi2=pi**2
#
#        return 8*A*tau*pi2*(4*pi2+4*tau2*xs2*pi2+tau2*zeta2) \
#        /(4*pi2+tau2*zeta2-4*tau2*zeta*xs*pi+4*tau2*xs2*pi2) \
#        /(4*pi2+tau2*zeta2+4*tau2*zeta*xs*pi+4*tau2*xs2*pi2)
        
    def peaksgen(hs,peaklocs,hwhms):
        #return sum(map(peakgen,hs,peaklocs,[freqscale]*len(hs)),axis=0)
        #return sum(map(peakgen,hs,peaklocs),axis=0)
        return sum(map(peakgen,hs,peaklocs,hwhms),axis=0)
    return lambda heights,hwhms: peaksgen(heights,peaklocs,hwhms)#vec
    #return lambda heights: peaksgen(heights)#vec
#(returnsumofpeaksfx([4k,5k,7k,15k,20k....],~1e6/2,~1e6/2)


def returnsumofexpdecays(w0hzs,n,dt=1):
    """returns a fnc that takes in AC params
    """
    xs=sp.linspace(0,dt*n,n,endpoint=False)
    
    def acgen(A,w0,tau):
        return A*sp.e**(-xs/tau)*cos(xs*2*pi*w0)
        
    def acsgen(aas,w0s,tawz):
        #return sum(map(peakgen,hs,peaklocs,[freqscale]*len(hs)),axis=0)
        #return sum(map(peakgen,hs,peaklocs),axis=0)
        return sum(map(acgen,aas,w0s,tawz),axis=0)
    return lambda az,taus: acsgen(az,w0hzs,taus)#vec
    #return lambda heights: peaksgen(heights)#vec
#(returnsumofpeaksfx([4k,5k,7k,15k,20k....],~1e6/2,~1e6/2)

    
def savitzky_golay(y, window_size, order, deriv=0):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techhniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv]
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m, y, mode='valid')


#
#def peaksinsegs(data, step): #breaks it into blocks. useless
#    data = data.ravel()
#    length = len(data)
#    if length % step == 0:
#        data.shape = (length/step, step)
#    else:
#        data.resize((length/step, step))
#    max_data = np.maximum.reduce(data,1)
#    min_data = np.minimum.reduce(data,1)
#    return np.concatenate((max_data[:,np.NewAxis], min_data[:,np.NewAxis]), 1)

#higher n should find more (false) peaks
import itertools
import random
class winadvisor(object):
    #store bins collection
    def __init__(self,delta,n,**kwargs):#,data=None):#,stufftobin=None):
        self.delta=delta
        self.stop=False
        self.n=n
        self.kwargs=kwargs
        self.kwargs.setdefault('sort',True)
        self.evaled={} #possibly derive to keep only last few
        #self.lastresult=self.acceptorreject(data)
        #bin
        return

#    def bin(self,*stufftobin):
#        for tobin in stufftobin:
            
    def acceptorreject(self,data,**kwargs):
        """better to input ordered data"""
        if len(data)==1:return True#assert len(data)>=2
        sort=kwargs.setdefault('sort',self.kwargs['sort']) #so the sort is just for this fnc call
        if sort==True: data=sorted(data)
        combogen=itertools.combinations(data,2)
        for acombo in combogen:
            if abs(acombo[0]-acombo[1])<self.delta:
                return False #for reject
        return True
    
    #can be used for a guess
    def upordownorend(self,twoindices,twodatas):
        #first data assumed lower index
        #can go up if lower index
        #i2-i1>=1
        twoindices=tuple(twoindices)
        assert len(twoindices) and len(twodatas)==2
        di=twoindices[1]-twoindices[0]
        loi=twoindices[0];hii=twoindices[1]
        assert di>0
        
#        idd=dict( zip(indices,datas) )
#        if (twoindices[0]) in self.lastpaidevaled.keys() \
#        or (twoindices[1]) in self.lastpaidevaled.keys():
    
        #see if it was already evaluated and get val from there
        try: lo=self.evaled[twoindices[0]]
        except:
            lo=self.acceptorreject(twodatas[0])
            self.evaled.update({twoindices[0]:lo})
        try: hi=self.evaled[twoindices[1]]
        except:
            hi=self.acceptorreject(twodatas[1])
            self.evaled.update({twoindices[1]:hi})
            
        if lo == True and hi==True:
            #try going higher
            #True anything below i lo
            for i in xrange(1,hii+1): self.evaled.setdefault(i,True)
            return 1
        if lo == True and hi==False:
            if di>1:
                 #optimum could be b/w indices
                for i in xrange(1,loi+1): self.evaled.setdefault(i,True)
                for i in xrange(hii,self.n+1): self.evaled.setdefault(i,False)
                return None
            else:
                self.stop=True                
                return 0 # ie bingo
        if lo == False and hi==False:
            for i in xrange(loi,self.n+1): self.evaled.setdefault(i,False)
            return -1 #try going lower
        if lo == False and hi==True:
            #print loi, hii
            raise Exception, 'unexpected situation'
            
            
 
    def trytofindhifi(self,indices,datas):
        """..but w/o false peaks"""
        assert len(indices)>=2
        assert len(indices)==len(datas)
        assert sorted(indices)==indices
        
        indices=list(indices)        
        mini=indices[0]#min(indices)
        maxi=indices[-1]#max(indices)
        ii=iter(indices)
        idd=dict( zip(indices,datas) )
        i2nexti=1
        for curi in ii:
            nexti=indices[i2nexti]
            #print curi,nexti
            ude=self.upordownorend( [curi,nexti], [idd[curi],idd[nexti]] )
            #print ude            
            if ude==1:
                if nexti==maxi:
                    if maxi==self.n:self.stop=True
                    return maxi
                #else keep searching
                #
            if ude==None: return curi
            if ude==0: return curi
            if ude==-1 and curi==mini: return None #it's all crap
            i2nexti+=1
    
    def getrandints(self,no,minn=1):#no. can get big
#        maxn=self.n
#        got=[]
#        if len(self.evaled.keys())==(self.n-minn+1): return None
#        for i in xrange(no):
#            rn=random.randint(minn,maxn)
#            #this loop becomes slow when the no.s are close to being exhausted
#            while (rn in got) or (rn in self.evaled.keys()):#conditions to keep looking
#                rn=random.randint(minn,maxn)
#            got.append(rn)
#            if len(self.evaled.keys())==(self.n-minn+1): return got #if exhausted
#        return sorted(got)
        maxn=self.n
        got=[]
        if len(self.evaled.keys())==(self.n-minn+1): return None
        choices=xrange(minn,maxn+1)
        choices=list(frozenset(choices)-frozenset(self.evaled.keys()))
        #much faster!!
        for i in xrange(no):
            rn=random.choice(choices)
            got.append(rn)
            choices.remove(rn)
            if len(self.evaled.keys())==(self.n-minn+1): return got #if exhausted
        return sorted(got)

def returnpeaksofabsac(ac,dt=.001e-12,peaktol=.05):
    #not that sensitive to peaktol, peak tol .1 gives same ans
    #can input just 25% of full ac
    ac=sp.absolute(ac)
    n=len(ac)
    xs=sp.linspace(0,dt*n,n,endpoint=False)
    pt=max(ac)*peaktol
    pd= dict(  peakdet(ac,pt,x=xs)[0]  );del xs
    xf=pd.keys();yf=pd.values()
    return array(xf),array(yf)

def fitexpdecay(xs,ys):
    xs=array(xs);ys=array(ys);
    def expdecay(t,a,tau): return a*sp.exp(-t/float(abs(tau)))
    def mined(a_n_tau): return ( ys - expdecay(xs,a_n_tau[0],a_n_tau[1]) )**2
    #def minedjusttau(tau): return mined([max(ys),tau])
    #s=sp.optimize.leastsq(minedjusttau, (xs[1]-xs[0])*3000  )    
    s=sp.optimize.leastsq(mined, [max(ys),(xs[1]-xs[0])*3000]  ) #this way
    #just b/c i like the resulting tau better
    #print s
    return abs(s[0][0]),abs(s[0][1]) #a, tau
    

def chopoffspectra(spectra,zerotol=.001):
    """ if expecting nothing beyond a certain freq"""
    maxval=zerotol*max(spectra[1]) #is the vals i
    #start from highest side and go low
    maxi=len(spectra[1])-1
    for ani in xrange(len(spectra[1])):
        decreasingi=maxi-ani
        if spectra[1][decreasingi]<maxval:pass
        else: return spectra[0][:decreasingi],spectra[1][:decreasingi]

def chopoffactail(ac,zerotol=.03):#,noisefactor=10):#,zerotol=.03):#:
    """ takes out the converged part of the FULL input ac"""
    aac=abs(array(ac)) # i don't want to deal with up and down
#    noise=average(  aac[int(len(ac)/2.0):] )*noisefactor
#    print noise
    maxval=zerotol*max(aac) #is the vals i
    #start from highest side and go low
    maxi=len(aac)-1
    for ani in xrange(len(aac)):
        decreasingi=maxi-ani
        if aac[decreasingi]<maxval:pass
        else: return ac[:decreasingi]




def peakdet(v, delta, x = None): #looks for peak /shapes/
#tolerates noise in spectra
    """
Converted from MATLAB script at http://billauer.co.il/peakdet.html
Currently returns two lists of tuples, but maybe arrays would be better
function [maxtab, mintab]=peakdet(v, delta, x)
%PEAKDET Detect peaks in a vector
% [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
% maxima and minima ("peaks") in the vector V.
% MAXTAB and MINTAB consists of two columns. Column 1
% contains indices in V, and column 2 the found values.
%
% With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
% in MAXTAB and MINTAB are replaced with the corresponding
% X-values.
%
% A point is considered a maximum peak if it has the maximal
% value, and was preceded (to the left) by a value lower by
% DELTA.
% Eli Billauer, 3.4.05 (Explicitly not copyrighted).
% This function is released to the public domain; Any use is allowed.
"""
    maxtab = []
    mintab = []
       
    if x is None:
        x = arange(len(v))
    
    v = asarray(v)
    
    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')
    
    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')
    
    if delta <= 0:
        sys.exit('Input argument delta must be positive')
    
    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN
    
    lookformax = True
    
    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        
        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return maxtab, mintab



try:
    gkb=batchfoldermgt('\\\\129.59.197.166\\aldosams\\research\\yag\\runtypes\\gk')
except:
    gkb=batchfoldermgt('/home/aldosams/research/yag/runtypes/gk')
    
gka=gkanalysis(gkb)

