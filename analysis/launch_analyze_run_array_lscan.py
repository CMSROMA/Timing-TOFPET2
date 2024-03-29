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

from ROOT import *

gROOT.SetBatch(True)

usage = "usage: python analysis/launch_analyze_run_array_lscan.py --firstRun 1 -i /home/cmsdaq/Workspace/TOFPET/Timing-TOFPET/output/TestArray -o /home/cmsdaq/Workspace/TOFPET/Timing-TOFPET/output/TestArray/RESULTS --arrayCode 0"

parser = optparse.OptionParser(usage)

parser.add_option("-r", "--firstRun", dest="firstRun",
                  help="first run number of the position scan")

parser.add_option("-n", "--nruns", dest="nruns", default=15,
                  help="number of runs in the scan")

parser.add_option("-p", "--positions", dest="positions", default='0,1,2,3,4,5,6,7,-2,-7,-6,-5,-4,-3,-1',
                  help="number of runs in the scan")

parser.add_option("-i", "--input", dest="inputDir",default="/data/TOFPET/LYSOARRAYS",
                  help="input directory")

parser.add_option("-o", "--output", dest="outputDir",default="/data/TOFPET/LYSOARRAYS/RESULTS",
                  help="output directory")

parser.add_option("-b", "--arrayCode", dest="arrayCode", default=-99,
                  help="code of the crystal array")

(opt, args) = parser.parse_args()

if not opt.firstRun:   
    parser.error('first run number not provided')

if not opt.inputDir:   
    parser.error('input directory not provided')

if not opt.outputDir:   
    parser.error('output directory not provided')

#------------------------------------------------

nFilesInScan = opt.nruns

#maybe this can be passed from command line 
#pos = [ 0, 1, 2, 3, 4, 5, 6, 7, -2, -7, -6, -5, -4, -3,-1 ]
pos = [ int(i) for i in opt.positions.split(',') ]
print("positions: "+str(sorted({ int(opt.firstRun)+i*3:pos[i] for i in range(len(pos))}.items())))

summaryFile = str(opt.outputDir)+"/"+"summary_"+"FirstRun" + str(opt.firstRun.zfill(6)) + "_LastRun" + str((int(opt.firstRun)+(nFilesInScan-1)*3)).zfill(6) + "_ARRAY" + str(opt.arrayCode.zfill(6))+".root"

#### Analysis Summary #####
histos={}

for v in [ 'Norm', 'LY', 'LY_sipm1','LY_sipm2','sigmaT','CTR','XT']:
    histos['%s_vs_pos'%v]=TGraphErrors()
    histos['%s_vs_pos'%v].SetName('%s_vs_bar'%v)

tfileResults={}
treeResults={}

lscan_step=4 #4mm step 

peak1_posref=-999.
peak1_norm_posref=-999.
peak1_sipm1_posref=-999.
peak1_sipm2_posref=-999.

for step in range(0,nFilesInScan):
    tfileResults[pos[step]] = TFile.Open(opt.inputDir+"/tree_Run%s_ARRAY%s.root"%(str(int(opt.firstRun)+step*3).zfill(6),opt.arrayCode.zfill(6)))
    print opt.inputDir+"/tree_Run%s_ARRAY%s.root" % (str(int(opt.firstRun)+step*3).zfill(6),opt.arrayCode.zfill(6))
    treeResults[pos[step]] = tfileResults[pos[step]].Get("results")

    treeResults[pos[step]].GetEntry(0)

    if (pos[step]==0):
        peak1_norm_posref=TMath.Mean(16,treeResults[pos[step]].peak1_norm_barCoinc)
        peak1_posref=TMath.Mean(16,treeResults[pos[step]].peak1_mean_barCoinc)
        peak1_sipm1_posref=TMath.Mean(16,treeResults[pos[step]].peak1_sipm1_mean_barCoinc)
        peak1_sipm2_posref=TMath.Mean(16,treeResults[pos[step]].peak1_sipm2_mean_barCoinc)

    if(peak1_posref<0):
        continue

    sipm1=TMath.Mean(16,treeResults[pos[step]].peak1_sipm1_mean_barCoinc)
    sipm2=TMath.Mean(16,treeResults[pos[step]].peak1_sipm2_mean_barCoinc)
    print(TMath.Mean(16,treeResults[pos[step]].peak1_mean_barCoinc))
    print((sipm1/peak1_sipm1_posref+sipm2/peak1_sipm2_posref)*0.5)
    print(TMath.Mean(16,treeResults[pos[step]].deltaT12_sigma_barCoinc)/2.)
    print(TMath.Mean(16,treeResults[pos[step]].Xtalk_median_barCoinc))

    histos['Norm_vs_pos'].SetPoint(step,pos[step]*lscan_step,TMath.Mean(16,treeResults[pos[step]].peak1_norm_barCoinc)/peak1_norm_posref)
    histos['Norm_vs_pos'].SetPointError(step,0.5,TMath.RMS(16,treeResults[pos[step]].peak1_norm_barCoinc)/peak1_norm_posref)
    histos['LY_vs_pos'].SetPoint(step,pos[step]*lscan_step,(sipm1/peak1_sipm1_posref+sipm2/peak1_sipm2_posref)*0.5)
    histos['LY_vs_pos'].SetPointError(step,0.5,TMath.RMS(16,treeResults[pos[step]].peak1_mean_barCoinc)/peak1_posref)
    histos['LY_sipm1_vs_pos'].SetPoint(step,pos[step]*lscan_step+0.5,(sipm1/peak1_sipm1_posref))
    histos['LY_sipm1_vs_pos'].SetPointError(step,0.5,TMath.RMS(16,treeResults[pos[step]].peak1_sipm1_mean_barCoinc)/peak1_sipm1_posref/16.)
    histos['LY_sipm2_vs_pos'].SetPoint(step,pos[step]*lscan_step-0.5,(sipm2/peak1_sipm2_posref))
    histos['LY_sipm2_vs_pos'].SetPointError(step,0.5,TMath.RMS(16,treeResults[pos[step]].peak1_sipm2_mean_barCoinc)/peak1_sipm2_posref/16.)
#    histos['LY_vs_pos'].SetPoint(step,pos[step]*lscan_step,TMath.Mean(16,treeResults[pos[step]].peak1_mean_barCoinc))
#    histos['LY_vs_pos'].SetPointError(step,0.5,TMath.RMS(16,treeResults[pos[step]].peak1_mean_barCoinc))
    histos['sigmaT_vs_pos'].SetPoint(step,pos[step]*lscan_step,TMath.Mean(16,treeResults[pos[step]].deltaT12_sigma_barCoinc)/2.)
    histos['sigmaT_vs_pos'].SetPointError(step,0.5,TMath.RMS(16,treeResults[pos[step]].deltaT12_sigma_barCoinc)/2.)
    histos['CTR_vs_pos'].SetPoint(step,pos[step]*lscan_step,TMath.Mean(16,treeResults[pos[step]].CTR_sigma_barCoinc))
    histos['CTR_vs_pos'].SetPointError(step,0.5,TMath.RMS(16,treeResults[pos[step]].CTR_sigma_barCoinc))
    histos['XT_vs_pos'].SetPoint(step,pos[step]*lscan_step,TMath.Mean(16,treeResults[pos[step]].Xtalk_median_barCoinc))
    histos['XT_vs_pos'].SetPointError(step,0.5,TMath.RMS(16,treeResults[pos[step]].Xtalk_median_barCoinc))

##########################################

mergedLabel = str(opt.outputDir)+"/"+"tree_"+"FirstRun" + str(opt.firstRun.zfill(6)) + "_LastRun" + str((int(opt.firstRun)+(nFilesInScan-1)*3)).zfill(6) + "_ARRAY" + str(opt.arrayCode.zfill(6))

c1_LY = TCanvas("phe_peak", "phe_peak", 900, 700)     

c1_LY.cd()  
gStyle.SetOptStat(1111);
c1_LY.SetGrid();

t=TLatex()
t.SetTextSize(0.035)
for hh in ['Norm','LY','sigmaT','CTR','XT']:
    histos['%s_vs_pos'%hh].GetXaxis().SetTitle("Y (mm)")
    if (hh=='Norm'):
        histos['%s_vs_pos'%hh].GetYaxis().SetTitle("Rel. Norm")
    if (hh=='LY'):
        histos['%s_vs_pos'%hh].GetYaxis().SetTitle("Rel. Energy")
    elif (hh=='sigmaT'):
        histos['%s_vs_pos'%hh].GetYaxis().SetTitle("#sigma_{t} (ps)")
    elif (hh=='CTR'):
        histos['%s_vs_pos'%hh].GetYaxis().SetTitle("CTR (ps)")
    elif (hh=='XT'):
        histos['%s_vs_pos'%hh].GetYaxis().SetTitle("XT")
    histos['%s_vs_pos'%hh].SetLineColor( 2 )
    histos['%s_vs_pos'%hh].SetMarkerColor( 1 )
    histos['%s_vs_pos'%hh].SetMarkerStyle( 21 )
    histos['%s_vs_pos'%hh].Draw("APE")
    if (hh=='LY'):
        l=TLegend(0.6,0.78,0.9,0.88)
        l.SetTextSize(0.035)
        l.SetFillColor(0)
        l.SetBorderSize(0)
        histos['%s_vs_pos'%hh].GetYaxis().SetLimits(0.94,1.1)
        histos['%s_vs_pos'%hh].GetYaxis().SetRangeUser(0.94,1.1)
        l.AddEntry(histos['%s_vs_pos'%hh],'Energy Tot','PL')
        for sipm in [1,2]:
            histos['%s_sipm%d_vs_pos'%(hh,sipm)].SetMarkerStyle(23+sipm)
            histos['%s_sipm%d_vs_pos'%(hh,sipm)].SetMarkerColor(1+sipm)
            histos['%s_sipm%d_vs_pos'%(hh,sipm)].SetLineColor(1+sipm)
            histos['%s_sipm%d_vs_pos'%(hh,sipm)].Draw("PSAME")
            l.AddEntry(histos['%s_sipm%d_vs_pos'%(hh,sipm)],'SiPM %d'%sipm,'PL')
        l.Draw()
    elif (hh=='sigmaT'):
        histos['%s_vs_pos'%hh].GetYaxis().SetLimits(105,145)
        histos['%s_vs_pos'%hh].GetYaxis().SetRangeUser(105,145)
    elif (hh=='CTR'):
        histos['%s_vs_pos'%hh].GetYaxis().SetLimits(140,220)
        histos['%s_vs_pos'%hh].GetYaxis().SetRangeUser(140,220)
    elif (hh=='XT'):
        histos['%s_vs_pos'%hh].GetYaxis().SetLimits(0.,0.5)
        histos['%s_vs_pos'%hh].GetYaxis().SetRangeUser(0.,0.5)

    t.DrawLatexNDC(0.12,0.91,"FirstRun" + str(opt.firstRun.zfill(6)) + "_LastRun" + str((int(opt.firstRun)+(nFilesInScan-1)*3)).zfill(6) + "_ARRAY" + str(opt.arrayCode.zfill(6)))
    c1_LY.SaveAs(mergedLabel+"_"+"LSCAN_SUMMARY_%s.png"%hh)



