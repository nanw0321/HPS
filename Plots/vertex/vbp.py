import os
from os.path import isfile, join
path_recon = '/nfs/slac/g/hps_data2/tuple/ap-WBT/tuple/'
#path_truth = '/nfs/slac/g/hps_data2/tuple/ap-WBT/truth/tuple/'

import ROOT
from ROOT import TFile, TCanvas, TTree, gROOT, TProfile, gStyle, TGraph

from array import array

import numpy as np

#drawing option
gStyle.SetOptFit(1)

#read path for subdirectories
pth_recon = []
for pathname in os.listdir(path_recon):
	if isfile(join(path_recon, pathname)):
		continue
	else:
		pth_recon.append(pathname)

'''
pth_truth = []
for pathname in os.listdir(path_truth):
	if isfile(join(path_truth, pathname)):
		continue
	else:
		pth_truth.append(pathname)

#loop only through subdirectories that exist for both recon and truth
pth = list(set(pth_recon).intersection(pth_truth)); pth.sort();
'''

for numf in range(len(pth_recon)):
	element = pth_recon[numf]
	print "folder:" + str(numf)

	#read file names for looping through root files
	fn_recon = []
	fn_truth = []

	for filename in os.listdir(path_recon+str(element)):
		if filename.endswith(".root"):
			if filename.endswith("MeV.root"):
				continue
			else:
				fn_recon.append(filename)
		else:
			continue


	#create branch addresses for reading data off of root files
	triPosP, triEle1P, triM, triEndZ, posP, eleP, uncM, uncVZ = (array('d',[0]),) * 8
	truPosP, truEle1P, truM, truEndZ = (array('d',[0]),) * 4

	#create list of plots (tr - rec for pos, ele, m, Vz)
	Hpp = [None] * len(fn_recon);
	Hpe = [None] * len(fn_recon);
	Hm = [None] * len(fn_recon);
	Hvz = [None] * len(fn_recon);
	
	for i in range(len(fn_recon)):
		Hpp[i] = ROOT.TH1F("posP_"+str(i),"posP_"+str(i),120,-0.6,0.6)
		Hpe[i] = ROOT.TH1F("eleP_"+str(i),"eleP_"+str(i),120,-0.4,0.8)
		Hm[i] = ROOT.TH1F("M_"+str(i),"M_"+str(i),120,-0.03,0.03)
		Hvz[i] = ROOT.TH1F("VZ_"+str(i),"VZ_"+str(i),200,-100,100)
		print "A", Hpp[i]

	#generate plots and save to list
	for i in range(len(fn_recon)):
		print "B", Hpp[i]
		print "    file: "+ str(i)
		f1 = TFile(path_recon+element+'/'+fn_recon[i])
		print "C", Hpp[i]
		events = f1.Get("ntuple")
		print "D", Hpp[i]
		events.Branch("triPosP",triPosP,"triPosP/D")
		events.Branch("triM",triM,"triM/D")
		events.Branch("triEndZ",triEndZ,"triEndZ/D")
		events.Branch("posP",posP,"posP/D")
		events.Branch("eleP",eleP,"eleP/D")
		events.Branch("uncM",uncM,"uncM/D")
		events.Branch("uncVZ",uncVZ,"uncVZ")
		print "E", Hpp[i]
		nentries = events.GetEntries()
		print "F", Hpp[i]
		
		for ii in range(nentries):
			events.GetEntry(ii)
			Hpp[i].Fill((events.posP)-(events.triPosP))
			Hpe[i].Fill((events.eleP)-(events.triEle1P))
			Hm[i].Fill((events.uncM)-(events.triM))
			Hvz[i].Fill((events.uncVZ)-(events.triEndZ))

	#configure saved plots
	for i in range(len(fn_recon)):
		print "    file " + str(i)
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
	c1.Print(str(element)+'_posP.pdf[')
	c2.Print(str(element)+'_eleP.pdf[')
	c3.Print(str(element)+'_M.pdf[')
	c4.Print(str(element)+'_VZ.pdf[')

	for i in range(len(fn_recon)):
		c1.cd(); Hpp[i].Fit(g1,"R"); Hpp[i].Draw();
		c2.cd(); Hpe[i].Fit(g2,"R"); Hpe[i].Draw();
		c3.cd(); Hm[i].Fit(g3,"R"); Hm[i].Draw();
		c4.cd(); Hvz[i].Fit(g4,"R"); Hvz[i].Draw();
		c1.Print(str(element)+'_posP.pdf'); c1.Clear();
		c2.Print(str(element)+'_eleP.pdf'); c2.Clear();
		c3.Print(str(element)+'_M.pdf'); c3.Clear();
		c4.Print(str(element)+'_VZ.pdf'); c4.Clear();

	c1.Print(str(element)+'_posP.pdf]'); c1.Close();
	c2.Print(str(element)+'_eleP.pdf]'); c2.Close();
	c3.Print(str(element)+'_M.pdf]'); c3.Close();
	c4.Print(str(element)+'_VZ.pdf]'); c4.Close();

	f1 = 0;
	events = 0;
