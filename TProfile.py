import os
path = '/home/nanw/HPS/dev_board_test'

import ROOT
from ROOT import TFile, TCanvas, TTree, gROOT, TProfile, gStyle, TGraph

from array import array

import numpy as np

#read filenames for looping through root files
fn = []

for filename in os.listdir(path):
	if filename.endswith(".root"):
		fn.append(filename)
	else:
		continue

#create branch addresses for reading data off of root files
pchannel,sample0, sample1, sample2, sample3, sample4, sample5 = (array('d',[0]),) * 7
nbytes = 0

#create list of plots (profile and error graph)
prof0 = [None] * len(fn); prof1 = [None] * len(fn);
prof2 = [None] * len(fn); prof3 = [None] * len(fn);
prof4 = [None] * len(fn); prof5 = [None] * len(fn); 

egr0 = [None] * len(fn); egr1 = [None] * len(fn);
egr2 = [None] * len(fn); egr3 = [None] * len(fn);
egr4 = [None] * len(fn); egr5 = [None] * len(fn); 

#Drawing option
gStyle.SetOptStat(0)

#create TProfile
for i in range(len(fn)):
	prof0[i] = TProfile("hprof0_"+str(i),"sample0",640,0,640,3500,7000,"s")
	prof1[i] = TProfile("hprof1_"+str(i),"sample1",640,0,640,3500,7000,"s")
	prof2[i] = TProfile("hprof2_"+str(i),"sample2",640,0,640,3500,7000,"s")
	prof3[i] = TProfile("hprof3_"+str(i),"sample3",640,0,640,3500,7000,"s")
	prof4[i] = TProfile("hprof4_"+str(i),"sample4",640,0,640,3500,7000,"s")
	prof5[i] = TProfile("hprof5_"+str(i),"sample5",640,0,640,3500,7000,"s")

#create bin and sigma arrays
binX = np.zeros(640)
sig0 = np.zeros(640); sig1 = np.zeros(640)
sig2 = np.zeros(640); sig3 = np.zeros(640)
sig4 = np.zeros(640); sig5 = np.zeros(640)

#generate plots and save to list
print "Generate plots from file:"
for i in range(len(fn)):
	print i
	runname = fn[i].replace(".root","")
	f = TFile(path+'/'+fn[i])
	events = f.Get("results")
	events.Branch("pchannel",pchannel,"pchannel/D")
	events.Branch("sample0",sample0,"sample0/D")
	events.Branch("sample1",sample1,"sample1/D")
	events.Branch("sample2",sample2,"sample2/D")
	events.Branch("sample3",sample3,"sample3/D")
	events.Branch("sample4",sample4,"sample4/D")
	events.Branch("sample5",sample5,"sample5/D")
	nentries = events.GetEntries()
	for ii in range(nentries):
		nbytes += events.GetEntry(ii)
		prof0[i].Fill(events.pchannel,events.sample0,1)
		prof1[i].Fill(events.pchannel,events.sample1,1)
		prof2[i].Fill(events.pchannel,events.sample2,1)
		prof3[i].Fill(events.pchannel,events.sample3,1)
		prof4[i].Fill(events.pchannel,events.sample4,1)
		prof5[i].Fill(events.pchannel,events.sample5,1)

	for nbin in range(640):
		binX[nbin] = nbin
		sig0[nbin] = prof0[i].GetBinError(nbin)
		sig1[nbin] = prof1[i].GetBinError(nbin)
		sig2[nbin] = prof2[i].GetBinError(nbin)
		sig3[nbin] = prof3[i].GetBinError(nbin)
		sig4[nbin] = prof4[i].GetBinError(nbin)
		sig5[nbin] = prof5[i].GetBinError(nbin)
	
	egr0[i] = TGraph(640,binX,sig0)
	egr1[i] = TGraph(640,binX,sig1)
	egr2[i] = TGraph(640,binX,sig2)
	egr3[i] = TGraph(640,binX,sig3)
	egr4[i] = TGraph(640,binX,sig4)
	egr5[i] = TGraph(640,binX,sig5)

#create canvas to separate all data by sample number:
c1 = TCanvas("c1","profile histogram_mean",800,600);
c2 = TCanvas("c2","profile histogram_mean",800,600);
c3 = TCanvas("c3","profile histogram_mean",800,600);
c4 = TCanvas("c4","profile histogram_mean",800,600);
c5 = TCanvas("c5","profile histogram_mean",800,600);
c6 = TCanvas("c6","profile histogram_mean",800,600);

c1e = TCanvas("c1e","profile histogram_error",800,600);
c2e = TCanvas("c2e","profile histogram_error",800,600);
c3e = TCanvas("c3e","profile histogram_error",800,600);
c4e = TCanvas("c4e","profile histogram_error",800,600);
c5e = TCanvas("c5e","profile histogram_error",800,600);
c6e = TCanvas("c6e","profile histogram_error",800,600);


#configure saved plots
print "Configure plots"
for i in range(len(fn)):
	prof0[i].SetMinimum(3500); prof0[i].SetMaximum(7000);
	prof1[i].SetMinimum(3500); prof1[i].SetMaximum(7000);
	prof2[i].SetMinimum(3500); prof2[i].SetMaximum(7000);
	prof3[i].SetMinimum(3500); prof3[i].SetMaximum(7000);
	prof4[i].SetMinimum(3500); prof4[i].SetMaximum(7000);
	prof5[i].SetMinimum(3500); prof5[i].SetMaximum(7000);
	
	prof0[i].SetTitle(runname+'_sample0'); prof0[i].SetLineColor(i+1);
	prof1[i].SetTitle(runname+'_sample1'); prof1[i].SetLineColor(i+1);
	prof2[i].SetTitle(runname+'_sample2'); prof2[i].SetLineColor(i+1);
	prof3[i].SetTitle(runname+'_sample3'); prof3[i].SetLineColor(i+1);
	prof4[i].SetTitle(runname+'_sample4'); prof4[i].SetLineColor(i+1);
	prof5[i].SetTitle(runname+'_sample5'); prof5[i].SetLineColor(i+1);
	
	egr0[i].SetLineColor(i+1); egr0[i].SetMaximum(200);
	egr1[i].SetLineColor(i+1); egr1[i].SetMaximum(200);
	egr2[i].SetLineColor(i+1); egr2[i].SetMaximum(200);
	egr3[i].SetLineColor(i+1); egr3[i].SetMaximum(200);
	egr4[i].SetLineColor(i+1); egr4[i].SetMaximum(200);
	egr5[i].SetLineColor(i+1); egr5[i].SetMaximum(200);

#plot saved plots on canvas
print "Draw plots on canvas"
for i in range(len(fn)):
	if i == 0:
		c1.cd(); prof0[i].Draw("HIST")
		c2.cd(); prof1[i].Draw("HIST")
		c3.cd(); prof2[i].Draw("HIST")
		c4.cd(); prof3[i].Draw("HIST")
		c5.cd(); prof4[i].Draw("HIST")
		c6.cd(); prof5[i].Draw("HIST")
	else:
		c1.cd(); prof0[i].Draw("SAME")
		c2.cd(); prof1[i].Draw("SAME")
		c3.cd(); prof2[i].Draw("SAME")
		c4.cd(); prof3[i].Draw("SAME")
		c5.cd(); prof4[i].Draw("SAME")
		c6.cd(); prof5[i].Draw("SAME")


	if i == 0:
		c1e.cd(); egr0[i].Draw()
		c2e.cd(); egr1[i].Draw()
		c3e.cd(); egr2[i].Draw()
		c4e.cd(); egr3[i].Draw()
		c5e.cd(); egr4[i].Draw()
		c6e.cd(); egr5[i].Draw()
	else:
		c1e.cd(); egr0[i].Draw("SAME")
		c2e.cd(); egr1[i].Draw("SAME")
		c3e.cd(); egr2[i].Draw("SAME")
		c4e.cd(); egr3[i].Draw("SAME")
		c5e.cd(); egr4[i].Draw("SAME")
		c6e.cd(); egr5[i].Draw("SAME")

#create and plot legend on canvas
legend1 = [None] * 6
legend2 = [None] * 6

for i in range(6):
	legend1[i] = ROOT.TLegend(0.48,0.1,0.9,0.4)
	legend2[i] = ROOT.TLegend(0.6,0.6,0.9,0.9)

for i in range(len(fn)):
	legend1[0].AddEntry(prof0[i],fn[i][9:-11],"lep")
	legend1[1].AddEntry(prof1[i],fn[i][9:-11],"lep")
	legend1[2].AddEntry(prof2[i],fn[i][9:-11],"lep")
	legend1[3].AddEntry(prof3[i],fn[i][9:-11],"lep")
	legend1[4].AddEntry(prof4[i],fn[i][9:-11],"lep")
	legend1[5].AddEntry(prof5[i],fn[i][9:-11],"lep")
	
	legend2[0].AddEntry(egr0[i],fn[i][9:-11],"l")
	legend2[1].AddEntry(egr1[i],fn[i][9:-11],"l")
	legend2[2].AddEntry(egr2[i],fn[i][9:-11],"l")
	legend2[3].AddEntry(egr3[i],fn[i][9:-11],"l")
	legend2[4].AddEntry(egr4[i],fn[i][9:-11],"l")
	legend2[5].AddEntry(egr5[i],fn[i][9:-11],"l")

print "Draw legend on canvas"
c1.cd(); legend1[0].Draw();
c2.cd(); legend1[1].Draw();
c3.cd(); legend1[2].Draw();
c4.cd(); legend1[3].Draw();
c5.cd(); legend1[4].Draw();
c6.cd(); legend1[5].Draw();

c1e.cd(); legend2[0].Draw();
c2e.cd(); legend2[1].Draw();
c3e.cd(); legend2[2].Draw();
c4e.cd(); legend2[3].Draw();
c5e.cd(); legend2[4].Draw();
c6e.cd(); legend2[5].Draw();

print "Print canvas to pdf"
c1.Print('Profile_Histogram_sample0_mean.pdf')
c2.Print('Profile_Histogram_sample1_mean.pdf')
c3.Print('Profile_Histogram_sample2_mean.pdf')
c4.Print('Profile_Histogram_sample3_mean.pdf')
c5.Print('Profile_Histogram_sample4_mean.pdf')
c6.Print('Profile_Histogram_sample5_mean.pdf')

c1e.Print('Profile_Histogram_sample0_error.pdf')
c2e.Print('Profile_Histogram_sample1_error.pdf')
c3e.Print('Profile_Histogram_sample2_error.pdf')
c4e.Print('Profile_Histogram_sample3_error.pdf')
c5e.Print('Profile_Histogram_sample4_error.pdf')
c6e.Print('Profile_Histogram_sample5_error.pdf')
