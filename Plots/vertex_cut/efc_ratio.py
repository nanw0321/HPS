import os
from os.path import isfile, join
path_recon = '/nfs/slac/g/hps_data2/tuple/ap-WBT/tuple/'
path_truth = '/nfs/slac/g/hps_data2/tuple/ap-WBT/truth/tuple/'

import ROOT
from ROOT import TFile, TCanvas, TTree, gROOT, TProfile, gStyle, TGraph

from array import array

import numpy as np

#drawing option
gStyle.SetOptFit(1)
gStyle.SetOptStat(0)

#read path for subdirectories
pth_recon = []
for pathname in os.listdir(path_recon):
    if isfile(join(path_recon, pathname)):
        continue
    else:
        pth_recon.append(pathname)

pth_truth = []
for pathname in os.listdir(path_truth):
    if isfile(join(path_truth, pathname)):
        continue
    else:
        pth_truth.append(pathname)

#loop through directories contained in both truth and recon
pth = list(set(pth_recon).intersection(pth_truth)); pth.sort();

#create list of plots
rat1 = [None] * len(pth)
rat2 = [None] * len(pth)
rat3 = [None] * len(pth)

for numf in range(len(pth)):
    if 0 < numf <4 or numf > 9:
        continue

    element = pth[numf]; print "recon folder: ", numf

    #read file names for looping
    fn_recon = []

    for filename in os.listdir(path_recon+str(element)):
        if filename.endswith(".root"):
            if filename.endswith("MeV.root") or \
               filename.endswith("loose.root") or \
               filename.endswith("loose_extrap.root"):
                continue
            else:
                fn_recon.append(filename)
        else:
            continue
    
    #create branch addresses for reading data off of root files
    posP, eleP, uncM, uncVZ = (array('d',[0]),) * 4
    triPosP, triEle1P, triM, triEndZ = (array('d',[0]),) * 4
    truPosP, truEle1P, truM, truEndZ = (array('d',[0]),) * 4
    posP2, eleP2, uncM2, uncVZ2 = (array('d',[0]),) * 4
    triPosP2, triEle1P2, triM2, triEndZ2 = (array('d',[0]),) * 4

    #create list of plots (tr - rec for pos, ele, m, Vz; efficiency)
    Hpp = [None] * len(fn_recon);
    Hpe = [None] * len(fn_recon);
    Hm = [None] * len(fn_recon);
    Hvzdiff = [None] * len(fn_recon);
    Hvz1 = [None] * len(fn_recon);
    Hvz2 = [None] * len(fn_recon);
    Hrat = [None] * len(fn_recon);
    Hcut = [None] * len(fn_recon);

    meanp = []; meane = []; meanm = []; meanvz = [];
    sigp = []; sige = []; sigm = []; sigvz = [];

    for i in range(len(fn_recon)):
        Hpp[i] = ROOT.TH1F("posP_"+str(i),"posP_"+str(i),120,-0.6,0.6); Hpp[i].Sumw2();
        Hpe[i] = ROOT.TH1F("eleP_"+str(i),"eleP_"+str(i),120,-0.4,0.8); Hpe[i].Sumw2();
        Hm[i] = ROOT.TH1F("M_"+str(i),"M_"+str(i),120,-0.03,0.03); Hm[i].Sumw2();
        Hvzdiff[i] = ROOT.TH1F("VZd_"+str(i),"VZd_"+str(i),200,-100,100); Hvzdiff[i].Sumw2();
        Hvz1[i] = ROOT.TH1F("VZ1_"+str(i),"VZ1_"+str(i),36,0,180); Hvz1[i].Sumw2();

    #recon plots
    for i in range(len(fn_recon)):
        f1 = TFile(path_recon+element+'/'+fn_recon[i])
        events1 = f1.Get("ntuple")
        events1.Branch("triPosP",triPosP,"triPosP/D")
        events1.Branch("triEle1P",triEle1P,"triEle1P/D")
        events1.Branch("triM",triM,"triM/D")
        events1.Branch("triEndZ",triEndZ,"triEndZ/D")
        events1.Branch("posP",posP,"posP/D")
        events1.Branch("eleP",eleP,"eleP/D")
        events1.Branch("uncM",uncM,"uncM/D")
        events1.Branch("uncVZ",uncVZ,"uncVZ")
        nentries1 = events1.GetEntries()

        for ii in range(nentries1):
            events1.GetEntry(ii)
            Hpp[i].Fill((events1.posP)-(events1.triPosP))
            Hpe[i].Fill((events1.eleP)-(events1.triEle1P))
            Hm[i].Fill((events1.uncM)-(events1.triM))
            Hvzdiff[i].Fill((events1.uncVZ)-(events1.triEndZ))
            Hvz1[i].Fill((events1.triEndZ))
        f1 = 0; events1 = 0

    #truth plots
    Htvz = [None]; Htvz = ROOT.TH1F("tVZ_"+str(i),"tVZ_"+str(i),36,0,180);
    f2 = TFile(path_truth+element+'/ap-WBT_'+element+'MeV_truth.root')
    events2 = f2.Get("ntuple")
    events2.Branch("triEndZ",truEndZ,"triEndZ/D")
    nentries2 = events2.GetEntries()

    for ii in range(nentries2):
        if ii %((nentries2-nentries2%10)/10) == 0:
            print "event: ", ii,"/total events", nentries2
        events2.GetEntry(ii)
        Htvz.Fill(events2.triEndZ)
    f2 = 0; events2 = 0;
    #fit
    g1 = ROOT.TF1("g1","gaus",-0.2,0.2)
    g2 = ROOT.TF1("g2","gaus",-0.2,0.2)
    g3 = ROOT.TF1("g3","gaus",-0.01,0.01)
    g4 = ROOT.TF1("g4","gaus",-15,15)

    #canvas
    c1 = TCanvas("c1","posP_diff",800,600)
    c2 = TCanvas("c2","eleP_diff",800,600)
    c3 = TCanvas("c3","M_diff",800,600)
    c4 = TCanvas("c4","VZ_diff",800,600)

    #plot on canvas
    c1.Print(str(element)+'_posP.pdf[')
    c2.Print(str(element)+'_eleP.pdf[')
    c3.Print(str(element)+'_M.pdf[')
    c4.Print(str(element)+'_VZ.pdf[')

    for i in range(len(fn_recon)):
        c1.cd(); Hpp[i].Fit(g1,"R"); Hpp[i].Draw();
        c2.cd(); Hpe[i].Fit(g2,"R"); Hpe[i].Draw();
        c3.cd(); Hm[i].Fit(g3,"R"); Hm[i].Draw();
        c4.cd(); Hvzdiff[i].Fit(g4,"R"); Hvzdiff[i].Draw();
        c1.Print(str(element)+'_posP.pdf'); c1.Clear();
        c2.Print(str(element)+'_eleP.pdf'); c2.Clear();
        c3.Print(str(element)+'_M.pdf'); c3.Clear();
        c4.Print(str(element)+'_VZ.pdf'); c4.Clear();

    c1.Print(str(element)+'_posP.pdf]'); c1.Close();
    c2.Print(str(element)+'_eleP.pdf]'); c2.Close();
    c3.Print(str(element)+'_M.pdf]'); c3.Close();
    c4.Print(str(element)+'_VZ.pdf]'); c4.Close();

    for i in range(len(fn_recon)):
        Hvz2[i] = ROOT.TH1F("VZ2_"+str(i),"VZ2_"+str(i),36,0,180); Hvz2[i].Sumw2();
    #3-sigma cut
    for i in range(len(fn_recon)):
        nentries3 = Hpp[i].GetEntries()
        meanp.append(Hpp[i].GetFunction("g1").GetParameter(1))
        meane.append(Hpe[i].GetFunction("g2").GetParameter(1))
        meanm.append(Hm[i].GetFunction("g3").GetParameter(1))
        meanvz.append(Hvzdiff[i].GetFunction("g4").GetParameter(1))
        sigp.append(Hpp[i].GetFunction("g1").GetParameter(2))
        sige.append(Hpe[i].GetFunction("g2").GetParameter(2))
        sigm.append(Hm[i].GetFunction("g3").GetParameter(2))
        sigvz.append(Hvzdiff[i].GetFunction("g4").GetParameter(2))

        f3 = TFile(path_recon+element+'/'+fn_recon[i])
        events3 = f3.Get("ntuple")
        events3.Branch("triPosP",triPosP2,"triPosP/D")
        events3.Branch("triEle1P",triEle1P2,"triEle1P/D")
        events3.Branch("triM",triM2,"triM/D")
        events3.Branch("triEndZ",triEndZ2,"triEndZ/D")
        events3.Branch("posP",posP2,"posP/D")
        events3.Branch("eleP",eleP2,"eleP/D")
        events3.Branch("uncM",uncM2,"uncM/D")
        events3.Branch("uncVZ",uncVZ2,"uncVZ")
        nentries3 = events3.GetEntries()

        lbp = meanp[i]-3*sigp[i]; ubp = meanp[i]+3*sigp[i];
        lbe = meane[i]-3*sige[i]; ube = meane[i]+3*sige[i];
        lbm = meanm[i]-3*sigm[i]; ubm = meanm[i]+3*sigm[i];
        lbvz = meanvz[i]-3*sigvz[i]; ubvz = meanvz[i]+3*sigvz[i];

        for ii in range(nentries3):
            events3.GetEntry(ii)
            difp = (events3.posP)-(events3.triPosP)
            dife = (events3.eleP)-(events3.triEle1P)
            difm = (events3.uncM)-(events3.triM)
            difvz = (events3.uncVZ)-(events3.triEndZ)
            if (lbp <= difp <= ubp) and (lbe <= dife <= ube) and \
            (lbm <= difm <= ubm) and (lbvz <= difvz <= ubvz):
                Hvz2[i].Fill(events3.triEndZ)
        f3 = 0; events3 = 0;
    
    #take the ratio and configure plots
    for i in range(len(fn_recon)):
        Hrat[i] = Hvz1[i]; Hrat[i].Sumw2();
        Hcut[i] = Hvz2[i]; Hcut[i].Sumw2();
        Hrat[i].Divide(Htvz); Hcut[i].Divide(Htvz);
        runname = fn_recon[i].replace(".root","")
        Hrat[i].SetTitle(runname+'_efficiency')
        Hcut[i].SetTitle(runname+'_efficiency')
        Hrat[i].SetLineColor(1)
        Hcut[i].SetLineColor(2)

    #create canvas to plot
    c5 = TCanvas("c1","VZ_efficiency",800,600)

    #plot on canvas
    c5.Print(str(element)+'_VZ_efficiency.pdf[')

    for i in range(len(fn_recon)):
        c5.cd()
        Hrat[i].Draw()
        Hcut[i].Draw("SAME")
        c5.Print(str(element)+'_VZ_efficiency.pdf'); c5.Clear();
    c5.Print(str(element)+'_VZ_efficiency.pdf]'); c5.Close();

    rat1[numf] = Hcut[0]; rat1[numf].Divide(Hrat[0]); rat1[numf].SetTitle(str(element)+'MeV_L1L1'); rat1[numf].SetLineColor(numf*3+20);
    rat2[numf] = Hcut[1]; rat2[numf].Divide(Hrat[1]); rat2[numf].SetTitle(str(element)+'MeV_L1L2'); rat2[numf].SetLineColor(numf*3+20);
    rat3[numf] = Hcut[2]; rat3[numf].Divide(Hrat[2]); rat3[numf].SetTitle(str(element)+'MeV_L2L2'); rat3[numf].SetLineColor(numf*3+20);

    rat1[numf].SetMaximum(3); rat1[numf].SetMinimum(0); rat1[numf].SetMarkerStyle(33); rat1[numf].SetMarkerColor(numf*3+20)
    rat2[numf].SetMaximum(3); rat2[numf].SetMinimum(0); rat2[numf].SetMarkerStyle(33); rat2[numf].SetMarkerColor(numf*3+20)
    rat3[numf].SetMaximum(3); rat3[numf].SetMinimum(0); rat3[numf].SetMarkerStyle(33); rat3[numf].SetMarkerColor(numf*3+20)

#create canvas for total ratio plot
c11 = TCanvas("c11","L1L1",800,600)
c12 = TCanvas("c12","L1L2",800,600)
c22 = TCanvas("c22","L2L2",800,600)

c11l = TCanvas("c11l","L1L1",800,600)
c12l = TCanvas("c12l","L1L2",800,600)
c22l = TCanvas("c22l","L2L2",800,600)

for numf in range(len(pth)):
    if 0 < numf <4 or numf > 9:
        continue
    if numf == 0:
        c11.cd(); rat1[numf].Draw("E1"); rat1[numf].Draw("SAME Lhist")
        c12.cd(); rat2[numf].Draw("E1"); rat2[numf].Draw("SAME Lhist")
        c22.cd(); rat3[numf].Draw("E1"); rat3[numf].Draw("SAME Lhist")
        c11l.cd(); rat1[numf].Draw("Lhist")
        c12l.cd(); rat2[numf].Draw("Lhist")
        c22l.cd(); rat3[numf].Draw("Lhist")
    else:
        c11.cd(); rat1[numf].Draw("SAME E1"); rat1[numf].Draw("SAME Lhist")
        c12.cd(); rat2[numf].Draw("SAME E1"); rat2[numf].Draw("SAME Lhist")
        c22.cd(); rat3[numf].Draw("SAME E1"); rat3[numf].Draw("SAME Lhist")
        c11l.cd(); rat1[numf].Draw("SAME Lhist")
        c12l.cd(); rat2[numf].Draw("SAME Lhist")
        c22l.cd(); rat3[numf].Draw("SAME Lhist")

#create legend
legend1 = 0; legend1 = ROOT.TLegend(0.7, 0.6, 0.9, 0.9)
legend2 = 0; legend2 = ROOT.TLegend(0.7, 0.6, 0.9, 0.9)
legend3 = 0; legend3 = ROOT.TLegend(0.7, 0.6, 0.9, 0.9)

for numf in range(len(pth)):
    if 0 < numf < 4 or numf > 9:
        continue
    element = pth[numf]
    legend1.AddEntry(rat1[numf],str(element)+'MeV',"lep")
    legend2.AddEntry(rat2[numf],str(element)+'MeV',"lep")
    legend3.AddEntry(rat3[numf],str(element)+'MeV',"lep")

c11.cd(); legend1.Draw(); c11l.cd(); legend1.Draw()
c12.cd(); legend2.Draw(); c12l.cd(); legend2.Draw()
c22.cd(); legend3.Draw(); c22l.cd(); legend3.Draw()

c11.Print("L1L1.pdf"); c11l.Print("L1L1_line.pdf")
c12.Print("L1L2.pdf"); c12l.Print("L1L2_line.pdf")
c22.Print("L2L2.pdf"); c22l.Print("L2L2_line.pdf")


'''
for numf in range(len(pth)):
    if 0 < numf <4 or numf > 9:
        continue
    rat1[numf].SetLineColor(numf*3+20); rat1[numf].SetMinimum(0); rat1[numf].SetMarkerStyle(33); rat1[numf].SetMarkerColor(numf*3+20)
    rat2[numf].SetLineColor(numf*3+20); rat2[numf].SetMinimum(0); rat2[numf].SetMarkerStyle(33); rat2[numf].SetMarkerColor(numf*3+20)
    rat3[numf].SetLineColor(numf*3+20); rat3[numf].SetMinimum(0); rat3[numf].SetMarkerStyle(33); rat3[numf].SetMarkerColor(numf*3+20)

c11.Clear(); c12.Clear(); c22.Clear()

'''
