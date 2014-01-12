
from scriptmgt import *

#dont forget to change pbs name
#todo: get it from os.path somehow


pbs=\
"""

#!/bin/sh
# Beginning of PBS batch script.
#PBS -N gk-$taskid
#PBS -l nodes=${nn}:ppn=${ppn}:x86
# Nodes required (#nodes:#processors per node:CPU type)
#PBS -l mem=${totmem}mb
# Total job memory required (specify how many megabytes)
#PBS -l pmem=${ppmem}mb
# Memory required per processor (specify how many megabytes)
#PBS -l walltime=${hr}:0:0
# You must specify Wall Clock time (hh:mm:ss) [Maximum allowed 30 days = 720:00:00]
cd $taskdir
#PBS -o ${taskdir}/stdo
# Send job stdout to file "myjob.output"
#PBS -j oe
# Send (join) both stderr and stdout to "myjob.output"
./run.sh
#exclude from being picked up in pbs b/c it finished
mv pbs pbsX
# Replace the above echo command with your executable program
# End of PBS batch script.

"""



run=\
"""

##!/bin/sh
cd $taskdir
if [ -e r.restart ]; then
mpirun -np $np ~/progs/lammps/lmp_openmpi < actions.lmpin
else
mpirun -np 1 ~/progs/lammps/lmp_openmpi < setup.lmpin
mpirun -np $np ~/progs/lammps/lmp_openmpi < actions.lmpin

fi
#cmd to exclude from being picked up IS IN the pbs file

"""


setup=\
"""
label inits
dimension 3
units metal
boundary p p p
newton on
atom_style charge


variable a equal (${Tk}*9.67114349e-05)+12.3918
#geometry
#primitive vecs  a1 -.5 .5 .5 a2 .5 -.5 .5 a3 .5 .5 -.5 &
#conventional a1 1 0 0 a2 0 1 0 a3 0 0 1 &
#basis vecs below ,A1(16),A2(24),O(96),Y(24) in order, for conventional
#half of that for primitive
#ERROR Input line too long!! changed input.cpp MAXLINES
#using $a as initial
lattice custom $a &
basis	0.0	0.0	0.0	     &          
basis	0.5	0	0.5	&
basis	0	0.5	0.5	&
basis	0.5	0.5	0	&
basis	0.75	0.25	0.25	&
basis	0.75	0.75	0.75	&
basis	0.25	0.25	0.75	&
basis	0.25	0.75	0.25	&
basis	0.25	0.75	0.75	&
basis	0.25	0.25	0.25	&
basis	0.75	0.75	0.25	&
basis	0.75	0.25	0.75	&
basis	0.5	0.5	0.5	&
basis	0	0.5	0	&
basis	0.5	0	0	&
basis	0	0	0.5	&
basis	0.375	0	0.25	& 
basis	0.125	0	0.75	&
basis	0.625	0.5	0.25	&
basis	0.875	0.5	0.75	&
basis	0.25	0.375	0	&
basis	0.75	0.125	0	&
basis	0.25	0.625	0.5	&
basis	0.75	0.875	0.5	&
basis	0	0.25	0.375	&
basis	0	0.75	0.125	&
basis	0.5	0.25	0.625	&
basis	0.5	0.75	0.875	&
basis	0.75	0.625	0	&
basis	0.75	0.375	0.5	&
basis	0.25	0.875	0	&
basis	0.25	0.125	0.5	&
basis	0.125	0.5	0.25	&
basis	0.875	0	0.25	&
basis	0.375	0.5	0.75	&
basis	0.625	0	0.75	&
basis	0	0.25	0.875	&
basis	0.5	0.25	0.125	&
basis	0	0.75	0.625	&
basis	0.5	0.75	0.375	&
basis	0.28023	0.1011	0.19922	& 
basis	0.21977	0.8989	0.69922	&
basis	0.71977	0.6011	0.30078	&
basis	0.78023	0.3989	0.80078	&
basis	0.19922	0.28023	0.1011	&
basis	0.69922	0.21977	0.8989	&
basis	0.30078	0.71977	0.6011	&
basis	0.80078	0.78023	0.3989	&
basis	0.1011	0.19922	0.28023	&
basis	0.8989	0.69922	0.21977	&
basis	0.6011	0.30078	0.71977	&
basis	0.3989	0.80078	0.78023	&
basis	0.8511	0.53023	0.05078	&
basis	0.6489	0.46977	0.55078	&
basis	0.3511	0.96977	0.94922	&
basis	0.1489	0.03023	0.44922	&
basis	0.03023	0.44922	0.1489	&
basis	0.96977	0.94922	0.3511	&
basis	0.46977	0.55078	0.6489	&
basis	0.53023	0.05078	0.8511	&
basis	0.94922	0.3511	0.96977	&
basis	0.44922	0.1489	0.03023	&
basis	0.05078	0.8511	0.53023	&
basis	0.55078	0.6489	0.46977	&
basis	0.71977	0.8989	0.80078	&
basis	0.78023	0.1011	0.30078	&
basis	0.28023	0.3989	0.69922	&
basis	0.21977	0.6011	0.19922	&
basis	0.80078	0.71977	0.8989	&
basis	0.30078	0.78023	0.1011	&
basis	0.69922	0.28023	0.3989	&
basis	0.19922	0.21977	0.6011	&
basis	0.8989	0.80078	0.71977	&
basis	0.1011	0.30078	0.78023	&
basis	0.3989	0.69922	0.28023	&
basis	0.6011	0.19922	0.21977	&
basis	0.1489	0.46977	0.94922	&
basis	0.3511	0.53023	0.44922	&
basis	0.6489	0.03023	0.05078	&
basis	0.8511	0.96977	0.55078	&
basis	0.96977	0.55078	0.8511	&
basis	0.03023	0.05078	0.6489	&
basis	0.53023	0.44922	0.3511	&
basis	0.46977	0.94922	0.1489	&
basis	0.05078	0.6489	0.03023	&
basis	0.55078	0.8511	0.96977	&
basis	0.94922	0.1489	0.46977	&
basis	0.44922	0.3511	0.53023	&
basis	0.78023	0.6011	0.69922	&
basis	0.71977	0.3989	0.19922	&
basis	0.21977	0.1011	0.80078	&
basis	0.28023	0.8989	0.30078	&
basis	0.69922	0.78023	0.6011	&
basis	0.19922	0.71977	0.3989	&
basis	0.80078	0.21977	0.1011	&
basis	0.30078	0.28023	0.8989	&
basis	0.6011	0.69922	0.78023	&
basis	0.3989	0.19922	0.71977	&
basis	0.1011	0.80078	0.21977	&
basis	0.8989	0.30078	0.28023	&
basis	0.3511	0.03023	0.55078	&
basis	0.1489	0.96977	0.05078	&
basis	0.8511	0.46977	0.44922	&
basis	0.6489	0.53023	0.94922	&
basis	0.53023	0.94922	0.6489	&
basis	0.46977	0.44922	0.8511	&
basis	0.96977	0.05078	0.1489	&
basis	0.03023	0.55078	0.3511	&
basis	0.44922	0.8511	0.46977	&
basis	0.94922	0.6489	0.53023	&
basis	0.55078	0.3511	0.03023	&
basis	0.05078	0.1489	0.96977	&
basis	0.21977	0.3989	0.30078	&
basis	0.28023	0.6011	0.80078	&
basis	0.78023	0.8989	0.19922	&
basis	0.71977	0.1011	0.69922	&
basis	0.30078	0.21977	0.3989	&
basis	0.80078	0.28023	0.6011	&
basis	0.19922	0.78023	0.8989	&
basis	0.69922	0.71977	0.1011	&
basis	0.3989	0.30078	0.21977	&
basis	0.6011	0.80078	0.28023	&
basis	0.8989	0.19922	0.78023	&
basis	0.1011	0.69922	0.71977	&
basis	0.6489	0.96977	0.44922	&
basis	0.8511	0.03023	0.94922	&
basis	0.1489	0.53023	0.55078	&
basis	0.3511	0.46977	0.05078	&
basis	0.46977	0.05078	0.3511	&
basis	0.53023	0.55078	0.1489	&
basis	0.03023	0.94922	0.8511	&
basis	0.96977	0.44922	0.6489	&
basis	0.55078	0.1489	0.53023	&
basis	0.05078	0.3511	0.46977	&
basis	0.44922	0.6489	0.96977	&
basis	0.94922	0.8511	0.03023 &
basis	0.125	0	0.25	& 
basis	0.375	0	0.75	&
basis	0.875	0.5	0.25	&
basis	0.625	0.5	0.75	&
basis	0.25	0.125	0	&
basis	0.75	0.375	0	&
basis	0.25	0.875	0.5	&
basis	0.75	0.625	0.5	&
basis	0	0.25	0.125	&
basis	0	0.75	0.375	&
basis	0.5	0.25	0.875	&
basis	0.5	0.75	0.625	&
basis	0.875	0	0.75	&
basis	0.625	0	0.25	&
basis	0.125	0.5	0.75	&
basis	0.375	0.5	0.25	&
basis	0.75	0.875	0	&
basis	0.25	0.625	0	&
basis	0.75	0.125	0.5	&
basis	0.25	0.375	0.5	&
basis	0	0.75	0.875	&
basis	0	0.25	0.625	&
basis	0.5	0.75	0.125	&
basis	0.5	0.25	0.375	&

region wholething block 0 1 0 1 0 1 units lattice
create_box 4 wholething #no. is ntypes  ***

#after basis kw 1st no. is basis atm, 2nd is type
create_atoms	1	box	basis	1	1 #creates 160 atoms at once
#...will need to spec types
group Al1 id <> 1 16
group Al2 id <> 17 40
group Al union Al1 Al2
group O id <> 41 136
group Y id <> 137 160
set group Al type 1
set group O type 2
set group Y type 3


#Atom properties
mass 1 26.98 #Al
mass 2 15.999 #O
mass 3 88.906 #Y
mass 4 69.7 #Dopant Ga for Al

#can add a dopant as mass 4
set group O charge -2.0 #O (-2)
set group Al charge 3.0 #Al (+3) ...the doped-for atom
set group Y charge 3.0 #Y (+3)

include runreqs.lmpin

#looking at one side of sim box
variable dx equal $dx
variable ly equal $ly
variable lz equal $lz
#create slab to be extruded
replicate 1 $ly $lz
replicate ${dx} 1 1

#random substitution
set group Al type/fraction 4 $dp $dseed  # ***
group Ga type 4
set group Ga charge 3.0 #Ga

variable T equal $Tk
velocity all create ${Tk} $vseed dist gaussian

reset_timestep 0
write_restart r.restart


"""




runreqs=\
"""
timestep .001
kspace_style pppm .00001 #usually at .0001 but need some speed, .00001 conserves but slow

$pot

#recovery from a binary w/ diffent no of procs
neigh_modify delay 0 every 1 check yes

"""


actions=\
"""
label start
##input
read_restart r.restart
#stuff not in restart file
include runreqs.lmpin

set group Al type 1
set group O type 2
set group Y type 3
set group Ga type 4
group AlGa union Al Ga

variable a equal (${Tk}*9.67114349e-05)+12.3918
lattice sc 1 spacing $a $a $a

variable simsize equal ($dx)*$lz*$ly
variable sXts equal 1000*(${simsize}) #cook time
variable U equal etotal
variable ts equal step
variable tsminussXts equal step-${sXts}
#^stupid lammps syntax..no space around the minus sign!!!
variable dx equal $dx
variable ly equal $ly
variable lz equal $lz
variable Tk equal $Tk
compute kea all ke/atom

fix nvtf all nvt temp $Tk $Tk 1
fix_modify nvtf energy yes

#two stages: 1. thermalize 2. ss while recording
#what stage is the sim at?
if ${ts} < ${sXts} then "jump actions.lmpin transient" &
else "jump actions.lmpin ss" 

label transient
run ${sXts} upto every 1000 "write_restart r.restart"
#need to erase fix data b/c i don't want to record it
unfix nvtf
#reset_timestep 0
write_restart r.restart #so i don't save previous fix info

label ss
fix nvtf all nvt temp $Tk $Tk 1
fix_modify nvtf energy yes
run 0

compute   AlGaKE AlGa ke/atom
compute   AlGaPE AlGa pe/atom
compute   AlGaStress AlGa stress/atom virial #virial means KE contrib not included
compute   fluxAlGa AlGa heat/flux AlGaKE AlGaPE AlGaStress #all ignored? all same grp
variable  JxAlGa equal c_fluxAlGa[1]#/vol

compute   OKE O ke/atom
compute   OPE O pe/atom
compute   OStress O stress/atom virial
compute   fluxO O heat/flux OKE OPE OStress #all ignored? all same grp
variable  JxO equal c_fluxO[1]#/vol

compute   YKE Y ke/atom
compute   YPE Y pe/atom
compute   YStress Y stress/atom virial
compute   fluxY Y heat/flux YKE YPE YStress #all ignored? all same grp
variable  JxY equal c_fluxY[1]#/vol

#just so i can have file names w/ timesteps
fix qf all ave/time 1 1 1 v_JxAlGa v_JxO v_JxY file ${ts}.cumdE.avetime
if ${tsminussXts} > 1000000 then "jump actions.lmpin end"
label keepgoing
run 1000
write_restart r.restart
run 0 #idk why i need to include this
if ${tsminussXts} > 1000000 then "jump actions.lmpin end" else "jump actions.lmpin keepgoing"

label end

"""

#compute myKE all ke/atom
#compute myPE all pe/atom


#compute   AlGaKE AlGa ke/atom
#compute   AlGaPE AlGa pe/atom
#compute   AlGaStress AlGa stress/atom virial
#compute   fluxAlGa AlGa heat/flux AlGaKE AlGaPE AlGaStress #all ignored? all same grp
#variable  JxAlGa equal c_fluxAlGa[1]/vol
#
#compute   OKE O ke/atom
#compute   OPE O pe/atom
#compute   OStress O stress/atom virial
#compute   fluxO O heat/flux OKE OPE OStress #all ignored? all same grp
#variable  JxO equal c_fluxO[1]/vol
#
#compute   YKE Y ke/atom
#compute   YPE Y pe/atom
#compute   YStress Y stress/atom virial
#compute   fluxY Y heat/flux YKE YPE YStress #all ignored? all same grp
#variable  JxY equal c_fluxY[1]/vol




#compute allKE all ke/atom
#compute allPE all pe/atom
#compute   allStress AlGa stress/atom virial
#
#compute   fluxAlGa AlGa heat/flux allKE allPE allStress #all ignored? all same grp
#variable  JxAlGa equal c_fluxAlGa[1]/vol
#compute   fluxO O heat/flux allKE allPE allStress #all ignored? all same grp
#variable  JxO equal c_fluxO[1]/vol
#compute   fluxY Y heat/flux allKE allPE allStress #all ignored? all same grp
#variable  JxY equal c_fluxY[1]/vol

pot0=\
"""

pair_style hybrid/overlay born/coul/long 4.0 7.0 mbmh mbmh2
##2body params
#w/o Ga
pair_coeff 2 2 born/coul/long 2449.44 0.2907 0 0 0
pair_coeff 1 2 born/coul/long 1740.31 0.2907 0 0 0
pair_coeff 2 3 born/coul/long 1250.85 0.3497 0 0 0
pair_coeff 1 1 born/coul/long 312.11 0.071124 0 0 0
pair_coeff 3 3 born/coul/long 245.14 0.071124 0 0 0
pair_coeff 1 3 born/coul/long 256.55 0.071124 0 0 0
#w Ga, replaced the 1s w 4s  (but smaller no. has to be 1st
pair_coeff 2 4 born/coul/long 1740.31 0.2907 0 0 0
pair_coeff 4 4 born/coul/long 312.11 0.071124 0 0 0
pair_coeff 1 4 born/coul/long 312.11 0.071124 0 0 0
pair_coeff 3 4 born/coul/long 256.55 0.071124 0 0 0
##3body params
pair_coeff * * mbmh /home/aldosams/research/yag/commoninput/potentials/0/yag.mbmh A O Y A #maps 4th type to A
pair_coeff * * mbmh2 /home/aldosams/research/yag/commoninput/potentials/0/yag.mbmh2 A O Y A

"""



#lattice constant function a=9.67114349e-05*T+12.3918
class gkyagscripts(scripts):
    def actionbeforejoining(self,*args,**kwargs):
        #if kwargs has pbs then 
        #totmem=n*mem
        #mem=40mb/ud
        scriptnames =(kwargs.keys())
        if 'lmpyag' in scriptnames:
            kwargs.setdefault('np',1)
            kwargs.setdefault('totmem',50) #size as sys size mb per atom
        if 'pbs' in scriptnames:
            kwargs.setdefault('hr',1)
            kwargs.setdefault('ppn',1)
            kwargs.setdefault('totmem',50)
            
            ncells=kwargs['lz']*kwargs['lz']*kwargs['dx']
            kwargs['np']=8#8 #int(ncells/2)
            #no. of procs divisible
            kwargs['np']=int(kwargs['np']/kwargs['ppn'])*kwargs['ppn'] #procs should be /sible by ppn
            kwargs['nn']=kwargs['np']/kwargs['ppn']
            #kwargs['totmem']=kwargs['np']*4+((kwargs['ud'])**3) #about 1mb/uc +4mb prog
            #why does previous not work?!#is it the avging?
            kwargs['totmem']=5*kwargs['np']+(30*ncells) #5 for exe other is for whatever 
            #4 for .001 kspace, 10/11/13? for .00001, 5 for .0001
            ppmem=int(float(kwargs['totmem'])/int(kwargs['np'])+1) #float() just to make sure it's an no.
            kwargs.update({'ppmem':ppmem})
        return kwargs

#scripts=gkyagscripts #to override original class name




#these override
gkscripts={'pbs':pbs,'run.sh':run,'setup.lmpin':setup,'actions.lmpin':actions
            ,'runreqs.lmpin':runreqs
            ,'pot0':pot0
            ,'hr':12
            ,'ppn':8 #8 1
            }
            

#run from local
gkb=batchfoldermgt('/home/aldosams/research/yag/runtypes/gk'
    ,scriptsclass=gkyagscripts #plural scriptS
    ,scriptargs=gkscripts
    ,listofscriptstosave=['pbs','run.sh'
        ,'runreqs.lmpin','setup.lmpin','actions.lmpin']
        )

#write down vars first. a is not a var.
#ly lz transverse width
#Tk
#gkparams={'dp':[0]#,.25,.50,.75] begin w/ 100
#            ,'pot':['$pot0']#,'$pot1']
#            ,'Tk':[300]
#            ,'vseed':[1234]
#            ,'dseed':[1234]
#            ,'dx':[4,8]#,8,16,32]
#            ,'lz':[1],'ly':[1]
#            }
#            

#the variables of the first parameter set used to generate
#the scripts define the parameter set.
initialsweep={'dp':[0,.25,.50,.75] #begin w/ 100
            ,'pot':['$pot0']#,'$pot1']
            ,'Tk':[300]
            ,'vseed':[1234]
            ,'dseed':[1234]
            ,'dx':[4,8,16,32]
            ,'lz':[1],'ly':[1]
            }
forgotpt1={'dp':[1]
            ,'pot':['$pot0']
            ,'Tk':[300]
            ,'vseed':[1234]
            ,'dseed':[1234]
            ,'dx':[4,8,16,32]
            ,'lz':[1],'ly':[1]
            }

lateraltest={'dp':[0]
            ,'pot':['$pot0']
            ,'Tk':[300]
            ,'vseed':[1234]
            ,'dseed':[1234]
            ,'dx':[16]
            ,'lz':[2],'ly':[2]
            }
            
vrandtest={'dp':[.50]
            ,'pot':['$pot0']
            ,'Tk':[300]
            ,'vseed':[4321]
            ,'dseed':[1234]
            ,'dx':[16]
            ,'lz':[1],'ly':[1]
            }

dprandtest={'dp':[.50]
            ,'pot':['$pot0']
            ,'Tk':[300]
            ,'vseed':[1234]
            ,'dseed':[4321]
            ,'dx':[16]
            ,'lz':[1],'ly':[1]
            }

biggersubs=dprandtest={'dp':[.50]
            ,'pot':['$pot0']
            ,'Tk':[300]
            ,'vseed':[1234]
            ,'dseed':[4321]
            ,'dx':[16]
            ,'lz':[2],'ly':[2]
            }

biggervrandtest={'dp':[.50]
            ,'pot':['$pot0']
            ,'Tk':[300]
            ,'vseed':[4321]
            ,'dseed':[1234]
            ,'dx':[16]
            ,'lz':[2],'ly':[2]
            }

fattersweep={'dp':[0,.50,1]
            ,'pot':['$pot0']
            ,'Tk':[300]
            ,'vseed':[1234,4321,9876,6789,111,222,333,444]
            ,'dseed':[1234]
            ,'dx':[4,8,16]#32 is too big for now
            ,'lz':[2],'ly':[2]
            }

longfattersweep={'dp':[0]
            ,'pot':['$pot0']
            ,'Tk':[300]
            ,'vseed':[1234,4321,9876]
            ,'dseed':[1234]
            ,'dx':[32,64]
            ,'lz':[2],'ly':[2]
            }

fatteryet={'dp':[0,.50,1] 
            ,'pot':['$pot0']#,'$pot1']
            ,'Tk':[300]
            ,'vseed':[1234,4321,9876,6789]
            ,'dseed':[1234]
            ,'dx':[8]
            ,'lz':[4],'ly':[4]
            }

#will this show increasing trend?
cold100ksweep={'dp':[0] 
            ,'pot':['$pot0']#,'$pot1']
            ,'Tk':[100]
            ,'vseed':[1234,4321,9876]
            ,'dseed':[1234]
            ,'dx':[4,8,16]
            ,'lz':[2],'ly':[2]
            }
#sample gen cmd
#gkb.user_gentaskarray(gkparams,overwrite=T/F)

