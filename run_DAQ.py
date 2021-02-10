#! /usr/bin/env python

import os
import sys
import optparse
import datetime
import subprocess
from glob import glob
from collections import defaultdict
from collections import OrderedDict
from array import array
import time
import re

#sys.path.insert(1, os.path.join(sys.path[0], './arduino/tablexy'))
#from xyMover import XYMover

usage = "usage: run from Timing-TOFPET: \n python run_DAQ.py -c config_main_bar.txt -o /data/TOFPET/LYSOBARS -n BAR000028_WS1_NW_NC" 
parser = optparse.OptionParser(usage)
parser.add_option("-c", "--config", dest="configFile",
                  help="config file")
parser.add_option("-o", "--outFolder", dest="outputFolder",
                  help="output directory")
parser.add_option("--pedAllChannels", dest="pedAllChannels", default=0, 
                  help="Set to 1 to collect pedestals for all channels (default is 0)")
parser.add_option("-n", "--name", dest="nameLabel",
                  help="label for output files")
(opt, args) = parser.parse_args()
if not opt.configFile:   
    parser.error('config file not provided')
if not opt.outputFolder:   
    parser.error('output folder not provided')
if not opt.nameLabel:   
    parser.error('label for output files not provided')

#############################

commandOutputDir = "mkdir -p "+opt.outputFolder
print commandOutputDir
os.system(commandOutputDir)

#############################
## Daq setup
#############################
#def RUN(runtype,time,ov,ovref,gate,label,enabledCh="",thresholds="",thresholdsT1="",nloops,sleep):
def RUN(runtype,time,ov,ovref,gate,label,enabledCh,thresholds,thresholdsT1,nloops,sleep,timePed):

    ###############
    ## Current time
    ###############
    current_time = datetime.datetime.now()
    simpletimeMarker = "%04d-%02d-%02d-%02d-%02d-%02d" % (current_time.year,current_time.month,current_time.day,current_time.hour,current_time.minute,current_time.second)
    print simpletimeMarker

    ####################
    ## Update run number
    ####################
    currentRun = 0
    #outputFileName = opt.outputFolder+"/RunNumbers.txt"
    ##outputFileName = "/media/cmsdaq/ext/data/RunNumbers.txt" 
    outputFileName = "/home/cmsdaq/Workspace/TOFPET/Timing-TOFPET2/data/RunNumbers.txt"

    file_runs = open(outputFileName, 'a+')
    
    lastRun = subprocess.check_output(['tail', '-1', outputFileName])
    lastRun = lastRun.rstrip('\n')
    
    if not lastRun:
        currentRun = 1
    else:
        currentRun = int(lastRun) + 1
    file_runs.write(str(currentRun)+'\n')    
    file_runs.close()

    #################
    ## Write commands
    #################
    newlabel = "Run"+str(currentRun).zfill(6)+"_"+simpletimeMarker+"_"+label

    
    if(runtype == "PED"):
        commandRun = "python run_TOFPET.py -c "+ opt.configFile+" --runType PED -d acquire_pedestal_data " + "-t "+ str(time)+" -v "+str(ov)+" --ovref "+str(ovref)+" -l "+str(newlabel)+" -g "+str(gate)+" -o "+opt.outputFolder+" --pedAllChannels " + str(opt.pedAllChannels) + " --nloops " + str(nloops) + " --sleep " + str(sleep)  
        if (enabledCh!=""):
            commandRun = commandRun +" --enabledChannels " + str(enabledCh) 
    if(runtype == "PHYS"):
        commandRun = "python run_TOFPET.py -c "+ opt.configFile+" --runType PHYS -d my_acquire_sipm_data " + "-t "+ str(time)+" -v "+str(ov)+" --ovref "+str(ovref)+" -l "+str(newlabel)+" -g "+str(gate)+" -o "+opt.outputFolder + " --nloops " + str(nloops) + " --sleep " + str(sleep) + " --timePed " + str(timePed)
        if (enabledCh!=""):
            commandRun = commandRun +" --enabledChannels " + str(enabledCh) 
            if (thresholds!=""):
                commandRun = commandRun + " --energyThr " + str(thresholds)
            if (thresholdsT1!=""):
                commandRun = commandRun + " --energyThrT1 " + str(thresholdsT1)

    print commandRun

## without Airtable
    os.system(commandRun)
    return;

### with Airtable
#    tags=newlabel.split('_')
#    print(tags)
#    posX=float(tags[4].replace('X',''))
#    posY=float(tags[5].replace('Y',''))
#    dbCommand = ". ~/AutoProcess/setup.sh; python3 ~/AutoProcess/insertRun.py --id=%s --type=%s --tag=%s --ov=%1.f --posx=%.1f --posy=%.1f "%(tags[0],runtype,newlabel,ov,posX,posY)
#    if (runtype == 'PHYS'):
#        dbCommand += ' --xtal=%s'%tags[2]
#    print(dbCommand)
#    insertDBStatus=os.WEXITSTATUS(os.system(dbCommand))
#    if (not insertDBStatus==0):
#        print('Error writing %s to runDB. Giving up'%tags[0])
#        return
#
##    commandRun='sleep 5'
#    exitStatus=os.WEXITSTATUS(os.system(commandRun))
#
#    if (exitStatus==0):
#        dbCommandCompleted = ". ~/AutoProcess/setup.sh; python3 ~/AutoProcess/updateRun.py --id=%s --status='%s'"%(tags[0],'DAQ COMPLETED')
#        print(dbCommandCompleted)
#        os.system(dbCommandCompleted)
#        if (not insertDBStatus==0):
#            print('Error writing %s to runDB. Giving up'%tags[0])
#            return
#        else:
#            print('%s successfully inserted into RunDB'%tags[0])
#    return;
###

###################
## Run daq sequence
###################


#Main sequence (test bar)
n_ch = 4 #number of channels in config file (2 for 2 pixels, 3 for 1 pixel and 1 bar, 4 for 2 bars, ...)
n_chip = 2 #number of active TOFPET2 chips
t_ped = 0.3 #s
t_phys = 10 #s
#ov_values = [-1] #V
ov_values = [7] #V
ovref_values = [7] #V
gate_values = [34] # # MIN_INTG_TIME/MAX_INTG_TIME 34 = (34 x 4 - 78) x 5 ns = 290ns (for values in range 32...127). Check TOFPET2C ASIC guide.
name = opt.nameLabel
nloops = 10# 10
t_ped_in_phys = 0.15 #s
sleep = 0


'''
#Main sequence (test array)
n_ch = 18 #number of channels in config file (2 for 2 pixels, 3 for 1 pixel and 1 bar, ..)
n_chip = 2 #number of active TOFPET2 chips
t_ped = 0.3 #s
t_phys = 300 #s
#ov_values = [-1] #V
ov_values = [7] #V
ovref_values = [7] #V
gate_values = [34] # # MIN_INTG_TIME/MAX_INTG_TIME 34 = (34 x 4 - 78) x 5 ns = 290ns (for values in range 32...127). Check TOFPET2C ASIC guide.
name = opt.nameLabel
nloops = 10
t_ped_in_phys = 0.15 #s
sleep = 0
'''

#--------------------------------------------------------------------

if int(opt.pedAllChannels)==1:
    n_ch = n_chip*64

nseq = 1
#nseq = int( t_tot / ( (2*t_ped*n_ch+t_phys)*len(ov_values)*len(gate_values) ) )
#print "Number of sequences in "+str(t_tot)+" seconds = "+ str(nseq)
#if nseq==0:
#    print "==> Please increase total time of the run (t_tot)"

#--------------------------------------------------------------------

########################
#Scan for test bar
########################

posFirstBarX = -1
posFirstBarY = -1

dict_Scan = {

    #DEFAULT
#    0: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","5_5_5_5",nloops,sleep),
#    1: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","10_10_10_10",nloops,sleep),
#    2: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","15_15_15_15",nloops,sleep),
#    3: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","20_20_20_20",nloops,sleep),
#    4: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","25_25_25_25",nloops,sleep),
#    5: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","30_30_30_30",nloops,sleep),
#    6: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","35_35_35_35",nloops,sleep),
#    7: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","40_40_40_40",nloops,sleep),
#    8: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","45_45_45_45",nloops,sleep),
#    9: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","50_50_50_50",nloops,sleep),
#    10: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","55_55_55_55",nloops,sleep),
#    11: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","60_60_60_60",nloops,sleep)

    0: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","35_35_35_35",nloops,sleep),
#    1: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","35_35_35_35",nloops,sleep),
#    2: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","35_35_35_35",nloops,sleep),
#    3: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","35_35_35_35",nloops,sleep),
#    4: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","35_35_35_35",nloops,sleep),
#    5: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","35_35_35_35",nloops,sleep),
#    6: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","35_35_35_35",nloops,sleep),
#    7: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","35_35_35_35",nloops,sleep),
#    8: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","35_35_35_35",nloops,sleep),
#    9: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3","20_20_20_20","35_35_35_35",nloops,sleep)

}
print "Scan" , dict_Scan


########################
#Scan for test array
########################

'''
posFirstBarX = -1
posFirstBarY = -1

dict_Scan = {

    #DEFAULT TEST ARRAY
    0: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3_4_5_6_7_8_9_10_11_12_13_14_15_16_17","20_20_20_20_20_20_20_20_20_20_20_20_20_20_20_20_20_20","35_35_35_35_35_35_35_35_35_35_35_35_35_35_35_35_35_35",nloops,sleep),
    #1: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3_4_5_6_7_8_9_10_11_12_13_14_15_16_17","20_20_20_20_20_20_20_20_20_20_20_20_20_20_20_20_20_20","35_35_35_35_35_35_35_35_35_35_35_35_35_35_35_35_35_35",nloops,sleep),
    #2: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3_4_5_6_7_8_9_10_11_12_13_14_15_16_17","20_20_20_20_20_20_20_20_20_20_20_20_20_20_20_20_20_20","35_35_35_35_35_35_35_35_35_35_35_35_35_35_35_35_35_35",nloops,sleep),
 #   3: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3_4_5_6_7_8_9_10_11_12_13_14_15_16_17","20_20_20_20_20_20_20_20_20_20_20_20_20_20_20_20_20_20","35_35_35_35_35_35_35_35_35_35_35_35_35_35_35_35_35_35",nloops,sleep),
 #   4: (round(posFirstBarX,1),round(posFirstBarY,1),"0_1_2_3_4_5_6_7_8_9_10_11_12_13_14_15_16_17","20_20_20_20_20_20_20_20_20_20_20_20_20_20_20_20_20_20","35_35_35_35_35_35_35_35_35_35_35_35_35_35_35_35_35_35",nloops,sleep),

}
print "Scan" , dict_Scan
'''

###################################################################
########################### Run DAQ ############################### 
###################################################################

#
#aMover=XYMover(8820)
#print (aMover.estimatedPosition())

for seq in range(0,nseq):
    for ov in ov_values:
        for ovref in ovref_values:
            for gate in gate_values:
                for kStep, kInfo in dict_Scan.items():

#                    print "++++ Centering Bar: "+str(kStep)+": X="+str(kInfo[0])+" Y="+str(kInfo[1])+" Channels="+str(kInfo[2])+" +++++"
#                    print aMover.moveAbsoluteXY(kInfo[0],kInfo[1])
#                    if (aMover.moveAbsoluteXY(kInfo[0],kInfo[1]) is "error"):
#                        print "== Out of range: skipping this position =="
#                        continue
#                    print aMover.estimatedPosition()
#                    print "++++ Done +++++"                    
#
                    #===
                    #== full file name ==
                    #thisname = name+"_POS"+str(kStep)+"_X"+str(kInfo[0])+"_Y"+str(kInfo[1])+"_CH"+str(kInfo[2]).replace("_","-")+"_ETHR"+str(kInfo[3]).replace("_","-")+"_T1THR"+str(kInfo[4]).replace("_","-")
                    #print(thisname)
                    #===
                    #== short file name ==
                    thisname = name+"_POS"+str(kStep)+"_X"+str(kInfo[0])+"_Y"+str(kInfo[1])
                    print(thisname)

                    #============================================
                    #RUN("PED",t_ped,ov,ovref,gate,thisname,kInfo[2],"","",kInfo[5],kInfo[6],0.)
                    #RUN("PHYS",t_phys,ov,ovref,gate,thisname,kInfo[2],kInfo[3],kInfo[4],kInfo[5],kInfo[6],t_ped_in_phys) 
                    #RUN("PED",t_ped,ov,ovref,gate,thisname,kInfo[2],"","",kInfo[5],kInfo[6],0.)
                    #============================================

                    #same OV for all
                    #============================================
                    RUN("PED",t_ped,ov,ov,gate,thisname,kInfo[2],"","",kInfo[5],kInfo[6],0.)
                    RUN("PHYS",t_phys,ov,ov,gate,thisname,kInfo[2],kInfo[3],kInfo[4],kInfo[5],kInfo[6],t_ped_in_phys) 
                    RUN("PED",t_ped,ov,ov,gate,thisname,kInfo[2],"","",kInfo[5],kInfo[6],0.)
                    #============================================
