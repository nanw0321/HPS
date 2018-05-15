import os
path_recon = '/home/nanw/HPS_Data/Vertex/reconstructed'

import ROOT
from ROOT import TFile, TCanvas, TTree, gROOT, TProfile, gStyle, TGraph

from array import array

import numpy as np

#read file names for looping through root files
fn_recon = []

for filename in os.listdir(path_recon):
	if filename.endswith(".root"):
		fn_recon.append(filename)
	else:
		continue

#create branch addresses for reading data off of root files
triPosP, triEle1P, triM, triEndZ, posP, eleP, uncM, uncVZ = (array('d',[0]),) * 8

#create list of plots (tr - rec for pos, ele, m, Vz)
Hpp = [None] * len(fn_recon);
Hpe = [None] * len(fn_recon);
Hm = [None] * len(fn_recon);
Hvz = [None] * len(fn_recon);

#drawing option
gStyle.SetOptFit(1)

#create TH1F in list
for i in range(len(fn_recon)):
	Hpp[i] = ROOT.TH1F("posP_"+str(i),"posP_"+str(i),120,-0.6,0.6)
	Hpe[i] = ROOT.TH1F("eleP_"+str(i),"eleP_"+str(i),120,-0.4,0.8)
	Hm[i] = ROOT.TH1F("M_"+str(i),"M_"+str(i),120,-0.03,0.03)
	Hvz[i] = ROOT.TH1F("VZ_"+str(i),"VZ_"+str(i),200,-150,50)

#generate plots and save to list
for i in range(len(fn_recon)):
	print "truth file number: "+ str(i)
	f1 = TFile(path_recon+'/'+fn_recon[i])
	events = f1.Get("ntuple")
	events.Branch("triPosP",triPosP,"triEle1P/D")
	events.Branch("triM",triM,"triM/D")
	events.Branch("triEndZ",triEndZ,"triEndZ/D")
	events.Branch("posP",posP,"posP/D")
	events.Branch("eleP",eleP,"eleP/D")
	events.Branch("uncM",uncM,"uncM/D")
	events.Branch("uncVZ",uncVZ,"uncVZ")
	nentries1 = events.GetEntries()
	for ii in range(nentries1):
		events.GetEntry(ii)
		Hpp[i].Fill((events.posP)-(events.triPosP))
		Hpe[i].Fill((events.eleP)-(events.triEle1P))
		Hm[i].Fill((events.uncM)-(events.triM))
		Hvz[i].Fill((events.uncVZ)-(events.triEndZ))

#configure saved plots
print "Configure plots"
for i in range(len(fn_recon)):
	runname = fn_recon[i].replace(".root","")
	Hpp[i].SetTitle(runname+'_posP');
	Hpe[i].SetTitle(runname+'_eleP');
	Hm[i].SetTitle(runname+'_M');
	Hvz[i].SetTitle(runname+'VZ');

#create fit functions
g1 = ROOT.TF1("g1","gaus",-0.2,0.2)
g2 = ROOT.TF1("g2","gaus",-0.2,0.2)
g3 = ROOT.TF1("g3","gaus",-0.01,0.01)
g4 = ROOT.TF1("g4","gaus",-15,15)

#create canvas to plot
c1 = TCanvas("c1","posP_diff",800,600)
c2 = TCanvas("c2","eleP_diff",800,600)
c3 = TCanvas("c3","M_diff",800,600)
c4 = TCanvas("c4","VZ_diff",800,600)

#plot on canvas
print "Draw on canvas"
c1.Print('posP.pdf[')
c2.Print('eleP.pdf[')
c3.Print('M.pdf[')
c4.Print('VZ.pdf[')

for i in range(len(fn_recon)):
	c1.cd(); Hpp[i].Fit(g1,"R"); Hpp[i].Draw();
	c2.cd(); Hpe[i].Fit(g2,"R"); Hpe[i].Draw();
	c3.cd(); Hm[i].Fit(g3,"R"); Hm[i].Draw();
	c4.cd(); Hvz[i].Fit(g4,"R"); Hvz[i].Draw();
	c1.Print('posP.pdf'); c1.Clear();
	c2.Print('eleP.pdf'); c2.Clear();
	c3.Print('M.pdf'); c3.Clear();
	c4.Print('VZ.pdf'); c4.Clear();

c1.Print('posP.pdf]'); c1.Close();
c2.Print('eleP.pdf]'); c2.Close();
c3.Print('M.pdf]'); c3.Close();
c4.Print('VZ.pdf]'); c4.Close();
