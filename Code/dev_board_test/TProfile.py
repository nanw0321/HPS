import os
path = '/home/nanw/HPS_Data/Dev_board'

import ROOT
from ROOT import TFile, TCanvas, TTree, gROOT, TProfile, gStyle, TGraph

from array import array

import numpy as np

#Drawing option
gStyle.SetOptStat(0)

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

#create list of TProfiles
prof0 = [None] * len(fn); prof1 = [None] * len(fn);
prof2 = [None] * len(fn); prof3 = [None] * len(fn);
prof4 = [None] * len(fn); prof5 = [None] * len(fn); 

for i in range(len(fn)):
	prof0[i] = TProfile("hprof0_"+str(i),"sample0",640,0,640,3500,7000,"s")
	prof1[i] = TProfile("hprof1_"+str(i),"sample1",640,0,640,3500,7000,"s")
	prof2[i] = TProfile("hprof2_"+str(i),"sample2",640,0,640,3500,7000,"s")
	prof3[i] = TProfile("hprof3_"+str(i),"sample3",640,0,640,3500,7000,"s")
	prof4[i] = TProfile("hprof4_"+str(i),"sample4",640,0,640,3500,7000,"s")
	prof5[i] = TProfile("hprof5_"+str(i),"sample5",640,0,640,3500,7000,"s")

#create list of error histograms for normalization
hsig0 = [None] * len(fn); hsig1 = [None] * len(fn);
hsig2 = [None] * len(fn); hsig3 = [None] * len(fn);
hsig4 = [None] * len(fn); hsig5 = [None] * len(fn);

for i in range(len(fn)):
	hsig0[i] = ROOT.TH1F("hsig0_"+str(i),"hsig0_"+str(i),200,0,200)
	hsig1[i] = ROOT.TH1F("hsig1_"+str(i),"hsig1_"+str(i),200,0,200)
	hsig2[i] = ROOT.TH1F("hsig2_"+str(i),"hsig2_"+str(i),200,0,200)
	hsig3[i] = ROOT.TH1F("hsig3_"+str(i),"hsig3_"+str(i),200,0,200)
	hsig4[i] = ROOT.TH1F("hsig4_"+str(i),"hsig4_"+str(i),200,0,200)
	hsig5[i] = ROOT.TH1F("hsig5_"+str(i),"hsig5_"+str(i),200,0,200)

#create list of mean and sigma plots
mgr0 = [None] * len(fn); mgr1 = [None] * len(fn);
mgr2 = [None] * len(fn); mgr3 = [None] * len(fn);
mgr4 = [None] * len(fn); mgr5 = [None] * len(fn);

egr0 = [None] * len(fn); egr1 = [None] * len(fn);
egr2 = [None] * len(fn); egr3 = [None] * len(fn);
egr4 = [None] * len(fn); egr5 = [None] * len(fn);

#create bin, mean, and (normalized) sigma arrays
binX = np.zeros(640)
for i in range(640):
	binX[i] = i

mean0 = np.zeros(640); mean1 = np.zeros(640)
mean2 = np.zeros(640); mean3 = np.zeros(640)
mean4 = np.zeros(640); mean5 = np.zeros(640)

sig0 = np.zeros(640); sig1 = np.zeros(640)
sig2 = np.zeros(640); sig3 = np.zeros(640)
sig4 = np.zeros(640); sig5 = np.zeros(640)

#generate TProfiles and save to list
print "Generate plots from file:"
for i in range(len(fn)):
	print "generating plots for file: ", i
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

#generate mean plots and save to list
for i in range(len(fn)):
	for nbin in range(640):
		mean0[nbin] = prof0[i].GetBinContent(nbin)
		mean1[nbin] = prof1[i].GetBinContent(nbin)
		mean2[nbin] = prof2[i].GetBinContent(nbin)
		mean3[nbin] = prof3[i].GetBinContent(nbin)
		mean4[nbin] = prof4[i].GetBinContent(nbin)
		mean5[nbin] = prof5[i].GetBinContent(nbin)

	mgr0[i] = TGraph(640,binX,mean0)
	mgr1[i] = TGraph(640,binX,mean1)
	mgr2[i] = TGraph(640,binX,mean2)
	mgr3[i] = TGraph(640,binX,mean3)
	mgr4[i] = TGraph(640,binX,mean4)
	mgr5[i] = TGraph(640,binX,mean5)

#generate sigma histograms and save to list, calculate normalization constant
cons0 = np.zeros(len(fn)); cons1 = np.zeros(len(fn));
cons2 = np.zeros(len(fn)); cons3 = np.zeros(len(fn));
cons4 = np.zeros(len(fn)); cons5 = np.zeros(len(fn));


for i in range(len(fn)):
	for nbin in range(640):
		hsig0[i].Fill(prof0[i].GetBinError(nbin))
		hsig1[i].Fill(prof1[i].GetBinError(nbin))
		hsig2[i].Fill(prof2[i].GetBinError(nbin))
		hsig3[i].Fill(prof3[i].GetBinError(nbin))
		hsig4[i].Fill(prof4[i].GetBinError(nbin))
		hsig5[i].Fill(prof5[i].GetBinError(nbin))
	hsig0[i].Fit("gaus","Q","",hsig0[i].GetMean()*0.7,hsig0[i].GetMean()*1.3); cons0[i] = hsig0[i].GetFunction("gaus").GetParameter(1);
	hsig1[i].Fit("gaus","Q","",hsig1[i].GetMean()*0.7,hsig1[i].GetMean()*1.3); cons1[i] = hsig1[i].GetFunction("gaus").GetParameter(1);
	hsig2[i].Fit("gaus","Q","",hsig2[i].GetMean()*0.7,hsig2[i].GetMean()*1.3); cons2[i] = hsig2[i].GetFunction("gaus").GetParameter(1);
	hsig3[i].Fit("gaus","Q","",hsig3[i].GetMean()*0.7,hsig3[i].GetMean()*1.3); cons3[i] = hsig3[i].GetFunction("gaus").GetParameter(1);
	hsig4[i].Fit("gaus","Q","",hsig4[i].GetMean()*0.7,hsig4[i].GetMean()*1.3); cons4[i] = hsig4[i].GetFunction("gaus").GetParameter(1);
	hsig5[i].Fit("gaus","Q","",hsig5[i].GetMean()*0.7,hsig5[i].GetMean()*1.3); cons5[i] = hsig5[i].GetFunction("gaus").GetParameter(1);

#generate sigma plots and save to list
for i in range(len(fn)):
	for nbin in range(640):
		sig0[nbin] = (prof0[i].GetBinError(nbin))/cons0[i]
		sig1[nbin] = (prof1[i].GetBinError(nbin))/cons1[i]
		sig2[nbin] = (prof2[i].GetBinError(nbin))/cons2[i]
		sig3[nbin] = (prof3[i].GetBinError(nbin))/cons3[i]
		sig4[nbin] = (prof4[i].GetBinError(nbin))/cons4[i]
		sig5[nbin] = (prof5[i].GetBinError(nbin))/cons5[i]
	egr0[i] = TGraph(640,binX,sig0)
	egr1[i] = TGraph(640,binX,sig1)
	egr2[i] = TGraph(640,binX,sig2)
	egr3[i] = TGraph(640,binX,sig3)
	egr4[i] = TGraph(640,binX,sig4)
	egr5[i] = TGraph(640,binX,sig5)

#configure list of plots
print "Configure plots"
for i in range(len(fn)):
	mgr0[i].SetMinimum(3500); mgr0[i].SetMaximum(7000);
	mgr1[i].SetMinimum(3500); mgr1[i].SetMaximum(7000);
	mgr2[i].SetMinimum(3500); mgr2[i].SetMaximum(7000);
	mgr3[i].SetMinimum(3500); mgr3[i].SetMaximum(7000);
	mgr4[i].SetMinimum(3500); mgr4[i].SetMaximum(7000);
	mgr5[i].SetMinimum(3500); mgr5[i].SetMaximum(7000);
	mgr0[i].SetTitle(runname+'_sample0'); mgr0[i].SetLineColor(i+1);
	mgr1[i].SetTitle(runname+'_sample1'); mgr1[i].SetLineColor(i+1);
	mgr2[i].SetTitle(runname+'_sample2'); mgr2[i].SetLineColor(i+1);
	mgr3[i].SetTitle(runname+'_sample3'); mgr3[i].SetLineColor(i+1);
	mgr4[i].SetTitle(runname+'_sample4'); mgr4[i].SetLineColor(i+1);
	mgr5[i].SetTitle(runname+'_sample5'); mgr5[i].SetLineColor(i+1);
	egr0[i].SetLineColor(i+1);
	egr1[i].SetLineColor(i+1);
	egr2[i].SetLineColor(i+1);
	egr3[i].SetLineColor(i+1);
	egr4[i].SetLineColor(i+1);
	egr5[i].SetLineColor(i+1);
	egr0[i].SetMaximum(2);
	egr1[i].SetMaximum(2);
	egr2[i].SetMaximum(2);
	egr3[i].SetMaximum(2);
	egr4[i].SetMaximum(2);
	egr5[i].SetMaximum(2);

#create legend
legend1 = [None] * 6
legend2 = [None] * 6
legend3 = [None] * 6
legend4 = [None] * 6


for i in range(6):
	legend1[i] = ROOT.TLegend(0.48,0.1,0.9,0.4)
	legend2[i] = ROOT.TLegend(0.6,0.7,0.9,0.9)
	legend3[i] = ROOT.TLegend(0.48,0.1,0.9,0.4)
	legend4[i] = ROOT.TLegend(0.6,0.7,0.9,0.9)

for i in [0,1,2]:
	legend1[0].AddEntry(mgr0[i],fn[i][9:-11],"l")
	legend1[1].AddEntry(mgr1[i],fn[i][9:-11],"l")
	legend1[2].AddEntry(mgr2[i],fn[i][9:-11],"l")
	legend1[3].AddEntry(mgr3[i],fn[i][9:-11],"l")
	legend1[4].AddEntry(mgr4[i],fn[i][9:-11],"l")
	legend1[5].AddEntry(mgr5[i],fn[i][9:-11],"l")
	legend2[0].AddEntry(egr0[i],fn[i][9:-11],"l")
	legend2[1].AddEntry(egr1[i],fn[i][9:-11],"l")
	legend2[2].AddEntry(egr2[i],fn[i][9:-11],"l")
	legend2[3].AddEntry(egr3[i],fn[i][9:-11],"l")
	legend2[4].AddEntry(egr4[i],fn[i][9:-11],"l")
	legend2[5].AddEntry(egr5[i],fn[i][9:-11],"l")

for i in [3,4,5,6]:
	legend3[0].AddEntry(mgr0[i],fn[i][9:-11],"l")
	legend3[1].AddEntry(mgr1[i],fn[i][9:-11],"l")
	legend3[2].AddEntry(mgr2[i],fn[i][9:-11],"l")
	legend3[3].AddEntry(mgr3[i],fn[i][9:-11],"l")
	legend3[4].AddEntry(mgr4[i],fn[i][9:-11],"l")
	legend3[5].AddEntry(mgr5[i],fn[i][9:-11],"l")
	legend4[0].AddEntry(egr0[i],fn[i][9:-11],"l")
	legend4[1].AddEntry(egr1[i],fn[i][9:-11],"l")
	legend4[2].AddEntry(egr2[i],fn[i][9:-11],"l")
	legend4[3].AddEntry(egr3[i],fn[i][9:-11],"l")
	legend4[4].AddEntry(egr4[i],fn[i][9:-11],"l")
	legend4[5].AddEntry(egr5[i],fn[i][9:-11],"l")

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

#mean plots
c1.Print('Profile_Histogram_sample0_mean.pdf[')
c2.Print('Profile_Histogram_sample1_mean.pdf[')
c3.Print('Profile_Histogram_sample2_mean.pdf[')
c4.Print('Profile_Histogram_sample3_mean.pdf[')
c5.Print('Profile_Histogram_sample4_mean.pdf[')
c6.Print('Profile_Histogram_sample5_mean.pdf[')

for i in [0,1,2]:
	if i == 0:
		c1.cd(); mgr0[i].Draw()
		c2.cd(); mgr1[i].Draw()
		c3.cd(); mgr2[i].Draw()
		c4.cd(); mgr3[i].Draw()
		c5.cd(); mgr4[i].Draw()
		c6.cd(); mgr5[i].Draw()
	else:
		c1.cd(); mgr0[i].Draw("SAME")
		c2.cd(); mgr1[i].Draw("SAME")
		c3.cd(); mgr2[i].Draw("SAME")
		c4.cd(); mgr3[i].Draw("SAME")
		c5.cd(); mgr4[i].Draw("SAME")
		c6.cd(); mgr5[i].Draw("SAME")

c1.cd(); legend1[0].Draw();
c2.cd(); legend1[1].Draw();
c3.cd(); legend1[2].Draw();
c4.cd(); legend1[3].Draw();
c5.cd(); legend1[4].Draw();
c6.cd(); legend1[5].Draw();

c1.Print('Profile_Histogram_sample0_mean.pdf'); c1.Clear()
c2.Print('Profile_Histogram_sample1_mean.pdf'); c2.Clear()
c3.Print('Profile_Histogram_sample2_mean.pdf'); c3.Clear()
c4.Print('Profile_Histogram_sample3_mean.pdf'); c4.Clear()
c5.Print('Profile_Histogram_sample4_mean.pdf'); c5.Clear()
c6.Print('Profile_Histogram_sample5_mean.pdf'); c6.Clear()

for i in [3,4,5,6]:
	if i == 3:
		c1.cd(); mgr0[i].Draw()
		c2.cd(); mgr1[i].Draw()
		c3.cd(); mgr2[i].Draw()
		c4.cd(); mgr3[i].Draw()
		c5.cd(); mgr4[i].Draw()
		c6.cd(); mgr5[i].Draw()
	else:
		c1.cd(); mgr0[i].Draw("SAME")
		c2.cd(); mgr1[i].Draw("SAME")
		c3.cd(); mgr2[i].Draw("SAME")
		c4.cd(); mgr3[i].Draw("SAME")
		c5.cd(); mgr4[i].Draw("SAME")
		c6.cd(); mgr5[i].Draw("SAME")

c1.cd(); legend3[0].Draw();
c2.cd(); legend3[1].Draw();
c3.cd(); legend3[2].Draw();
c4.cd(); legend3[3].Draw();
c5.cd(); legend3[4].Draw();
c6.cd(); legend3[5].Draw();

c1.Print('Profile_Histogram_sample0_mean.pdf')
c2.Print('Profile_Histogram_sample1_mean.pdf')
c3.Print('Profile_Histogram_sample2_mean.pdf')
c4.Print('Profile_Histogram_sample3_mean.pdf')
c5.Print('Profile_Histogram_sample4_mean.pdf')
c6.Print('Profile_Histogram_sample5_mean.pdf')

c1.Print('Profile_Histogram_sample0_mean.pdf]')
c2.Print('Profile_Histogram_sample1_mean.pdf]')
c3.Print('Profile_Histogram_sample2_mean.pdf]')
c4.Print('Profile_Histogram_sample3_mean.pdf]')
c5.Print('Profile_Histogram_sample4_mean.pdf]')
c6.Print('Profile_Histogram_sample5_mean.pdf]')

#sigma plots
c1e.Print('Profile_Histogram_sample0_error.pdf[')
c2e.Print('Profile_Histogram_sample1_error.pdf[')
c3e.Print('Profile_Histogram_sample2_error.pdf[')
c4e.Print('Profile_Histogram_sample3_error.pdf[')
c5e.Print('Profile_Histogram_sample4_error.pdf[')
c6e.Print('Profile_Histogram_sample5_error.pdf[')

for i in [0,1,2]:
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

c1e.cd(); legend2[0].Draw();
c2e.cd(); legend2[1].Draw();
c3e.cd(); legend2[2].Draw();
c4e.cd(); legend2[3].Draw();
c5e.cd(); legend2[4].Draw();
c6e.cd(); legend2[5].Draw();

c1e.Print('Profile_Histogram_sample0_error.pdf'); c1e.Clear()
c2e.Print('Profile_Histogram_sample1_error.pdf'); c2e.Clear()
c3e.Print('Profile_Histogram_sample2_error.pdf'); c3e.Clear()
c4e.Print('Profile_Histogram_sample3_error.pdf'); c4e.Clear()
c5e.Print('Profile_Histogram_sample4_error.pdf'); c5e.Clear()
c6e.Print('Profile_Histogram_sample5_error.pdf'); c6e.Clear()

for i in [3,4,5,6]:
	if i == 3:
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

c1e.cd(); legend4[0].Draw();
c2e.cd(); legend4[1].Draw();
c3e.cd(); legend4[2].Draw();
c4e.cd(); legend4[3].Draw();
c5e.cd(); legend4[4].Draw();
c6e.cd(); legend4[5].Draw();

c1e.Print('Profile_Histogram_sample0_error.pdf')
c2e.Print('Profile_Histogram_sample1_error.pdf')
c3e.Print('Profile_Histogram_sample2_error.pdf')
c4e.Print('Profile_Histogram_sample3_error.pdf')
c5e.Print('Profile_Histogram_sample4_error.pdf')
c6e.Print('Profile_Histogram_sample5_error.pdf')

c1e.Print('Profile_Histogram_sample0_error.pdf]')
c2e.Print('Profile_Histogram_sample1_error.pdf]')
c3e.Print('Profile_Histogram_sample2_error.pdf]')
c4e.Print('Profile_Histogram_sample3_error.pdf]')
c5e.Print('Profile_Histogram_sample4_error.pdf]')
c6e.Print('Profile_Histogram_sample5_error.pdf]')


'''
c1.Clear()
c2.Clear()
c3.Clear()
c4.Clear()
c5.Clear()
c6.Clear()

c1e.Clear()
c2e.Clear()
c3e.Clear()
c4e.Clear()
c5e.Clear()
c6e.Clear()

c1.Close()
c2.Close()
c3.Close()
c4.Close()
c5.Close()
c6.Close()

c1e.Close()
c2e.Close()
c3e.Close()
c4e.Close()
c5e.Close()
c6e.Close()

'''
