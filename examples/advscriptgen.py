

import scriptmgt

pbs=\
"""

#!/bin/sh
# Beginning of PBS batch script.
#PBS -N melt-$taskid
#PBS -l nodes=${np}:ppn=1:x86
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

pbs2=\
"""

#!/bin/sh
# Beginning of PBS batch script.
#PBS -N mina-$taskid
#PBS -l nodes=1:ppn=1:x86
# Nodes required (#nodes:#processors per node:CPU type)
#PBS -l mem=100mb
# Total job memory required (specify how many megabytes)
#PBS -l pmem=100mb
# Memory required per processor (specify how many megabytes)
#PBS -l walltime=12:0:0
# You must specify Wall Clock time (hh:mm:ss) [Maximum allowed 30 days = 720:00:00]
cd $taskdir
#PBS -o ${taskdir}/stdo
# Send job stdout to file "myjob.output"
#PBS -j oe
# Send (join) both stderr and stdout to "myjob.output"
sage -python ~/progs/lammpstools/dumps2hdf5.py --deldumpfiles
#exclude from being picked up in pbs b/c it finished
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
#exclude from being picked up in pbs file

"""


setup=\
"""
label inits
dimension 3
units metal
boundary p p p
newton on
atom_style charge

#geometry
#primitive vecs  a1 -.5 .5 .5 a2 .5 -.5 .5 a3 .5 .5 -.5 &
#conventional a1 1 0 0 a2 0 1 0 a3 0 0 1 &
#basis vecs below ,A1(16),A2(24),O(96),Y(24) in order, for conventional
#half of that for primitive
#ERROR Input line too long!! changed input.cpp MAXLINES
#using 12.0 as initial
lattice custom 12.0 &
basis	0.0	0.0	0.0         &          
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
set group Al charge 3.0 #Al (+3) ...the doped for atom
set group Y charge 3.0 #Y (+3)

include runreqs.lmpin

fix relaxboxfix all box/relax iso $p
minimize 0 0 1000 1000

replicate $ud $ud $ud

#random doping
set group Al type/fraction 4 $dp $dseed  # ***
group Ga type 4
set group Ga charge 3.0 #Ga

#delete atoms
delete_atoms porosity wholething $vp 1234 compress yes

variable T0 equal 1500 #i've got another T0
velocity all create ${T0} $vseed dist gaussian

reset_timestep 0
write_restart r.restart



"""


runreqs=\
"""
timestep .002
kspace_style pppm .0001

$pot

#recovery from a binary w/ diffent no of procs
neigh_modify delay 0 every 1 check yes

"""




actions=\
"""
##input
read_restart r.restart
#stuff not in restart file
include runreqs.lmpin

#1. input min struct 2. set T0 3. npt for a long time
#4. increase by 100 K or so until TF

variable udXts equal 100000 #10000*($ud)^3 #cook time
variable U equal etotal
variable T equal temp
variable P equal press
variable a equal (vol^(1.0/3.0))/$ud
variable T0 equal 1500 #i've got another T0
variable ts equal step

group randa id 711 16 559 169 66 853 582 1126 844 871 &
143 607 894 621 825 289 178 76 233 1127

variable initloopno equal floor((${ts}/${udXts}))+1
variable todo equal 1500-floor((${ts}/${udXts})) #currloop is floor+1
if ${todo}==0 then "jump actions.lmpin bypass"

variable loopvar loop ${todo} #if set to 0 then will get an error 
#that i don't care about

#want sim to go to right loop initially from read ts
#assign Ttgt, then continue to loop
label loop
variable currloopno equal ${loopvar}+${initloopno}-1 #a workaround for loopvar b/c starts w/ 1

variable Ttgt equal ${T0}+(${currloopno}-1)*10 #dT=10

velocity all scale ${Ttgt}
#use rescale for a step
#on 2nd thought i don't want abrupt v deltas

fix nptfix all npt temp ${Ttgt} ${Ttgt} 1 iso $p $p 10 drag 1
fix avgfix all ave/time 10 100 1000 v_U v_T v_P v_a file ${Ttgt}.${ts}.thermoavgs.avetime

if "1500<=${Ttgt} && ${Ttgt}<=3500" then &
"dump rijdump randa custom 5 ${ts}.${Ttgt}.dump id type xu yu zu"

variable runfor equal ${udXts}*(${currloopno}) #has to be bigger than 1000
run ${runfor} upto every 1000 "write_restart r.restart"
if "1500<=${Ttgt} && ${Ttgt}<=3500" then "jump actions.lmpin postproc" &
else "jump actions.lmpin dontpostproc"
label postproc
undump rijdump
shell /home/aldosams/progs/sage/sage -python ../dumps2lis.py
label dontpostproc

next loopvar
jump actions.lmpin loop

label bypass

"""

#todo add option for atoms.hdf5 fn bc i want $Temperature.atoms.hdf5
#also dumps2hdf5 in the bash script before actions.lmpin mpirun -np 1

#wish i used this
#pair_style hybrid/overlay born/coul/long 4.0 7.0 mbmh mbmh2
pot0=\
"""

pair_style hybrid/overlay born/coul/long 7.0 mbmh mbmh2
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
pair_coeff * * mbmh /gpfs20/home/aldosams/research/yag/commoninput/potentials/0/yag.mbmh A O Y A #maps 4th type to A
pair_coeff * * mbmh2 /gpfs20/home/aldosams/research/yag/commoninput/potentials/0/yag.mbmh2 A O Y A

"""


#these are crap
pot1=\
"""
pair_style hybrid/overlay born/coul/long 7.0 mbmh2
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
pair_coeff * * mbmh2 /gpfs20/home/aldosams/research/yag/commoninput/potentials/1/yag.mbmh2 A O Y A

"""

pot2b=\
"""

pair_style born/coul/long 7.0
##2body params
#w/o Ga
pair_coeff 2 2  2449.44 0.2907 0 0 0
pair_coeff 1 2  1740.31 0.2907 0 0 0
pair_coeff 2 3  1250.85 0.3497 0 0 0
pair_coeff 1 1  312.11 0.071124 0 0 0
pair_coeff 3 3  245.14 0.071124 0 0 0
pair_coeff 1 3  256.55 0.071124 0 0 0
#w Ga, replaced the 1s w 4s  (but smaller no. has to be 1st
pair_coeff 2 4  1740.31 0.2907 0 0 0
pair_coeff 4 4  312.11 0.071124 0 0 0
pair_coeff 1 4  312.11 0.071124 0 0 0
pair_coeff 3 4  256.55 0.071124 0 0 0

"""


class yagscripts(scripts):
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
            kwargs.setdefault('np',1)
            kwargs.setdefault('totmem',50)
            
            if kwargs['ud']>=2:
                kwargs['np']=(kwargs['ud']**3)
                #kwargs['totmem']=kwargs['np']*4+((kwargs['ud'])**3) #about 1mb/uc +4mb prog
                #why does previous not work?!#is it the avging?
                kwargs['totmem']=5*kwargs['np']+(10*(kwargs['ud'])**3) +200 
                #put in 200 for post processing
            
            ppmem=int(float(kwargs['totmem'])/int(kwargs['np'])+1) #float() just to make sure it's an no.
            kwargs.update({'ppmem':ppmem})
        return kwargs

#these override
minascripts={'pbs':pbs,'run.sh':run,'pbs2':pbs2
            ,'setup.lmpin':setup,'actions.lmpin':actions
            ,'runreqs.lmpin':runreqs
            ,'pot0':pot0,'pot1':pot1
            ,'hr':12}
#scripts=yagscripts #to override original class name

####run from local
meltb=batchfoldermgt('/home/aldosams/research/yag/runtypes/melt'
    ,scriptsclass=yagscripts
    ,scriptargs=minascripts
    ,listofscriptstosave=['pbs','run.sh'#,'pbs2'
        ,'runreqs.lmpin','setup.lmpin','actions.lmpin']
        )
#first parameter set defines the parameters for a set of simulations
minaparams={'ud':[2]
            ,'p':[10]
            ,'dp':[.01,.05]
            ,'vp':[.05,.01]#
            ,'pot':['$pot0']#,'$pot1']
            ,'vseed':[1234]
            ,'dseed':[1234]
            }
#second script set
justga={'ud':[2]
            ,'p':[10]
            ,'dp':[.05]
            ,'vp':[0]#
            ,'pot':['$pot0']#,'$pot1']
            ,'vseed':[1234]
            ,'dseed':[1234]
            }
#just pass the above two dicts into user_gentaskarray