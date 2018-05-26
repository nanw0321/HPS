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

#loop only through subdirectories that exist for both recon and truth
pth = list(set(pth_recon).intersection(pth_truth)); pth.sort();

for numf in range(len(pth)):
	f1 = 0
	f2 = 0
	events1 = 0
	events2 = 0
	element = pth[numf]
	print "recon folder:" + str(numf)

	#read file names for looping through root files
	fn_recon = []

	for filename in os.listdir(path_recon+str(element)):
		if filename.endswith(".root"):
			if filename.endswith("MeV.root"):
				continue
			else:
				fn_recon.append(filename)
		else:
			continue

	#create branch addresses for reading data off of root files
	triEndZ, truEndZ = (array('d',[0]),) * 2

	#create list of plots (recon Vz)
	Hvz = [None] * len(fn_recon); Hrat = [None] * len(fn_recon);

	for i in range(len(fn_recon)):
		Hvz[i] = ROOT.TH1F("VZ_"+str(i),"VZ_"+str(i),400,0,400)
	
	#generate plots and save to list
	for i in range(len(fn_recon)):
		print "    file: "+ str(i)
		f1 = TFile(path_recon+element+'/'+fn_recon[i])
		events1 = f1.Get("ntuple")
		events1.Branch("triEndZ",triEndZ,"triEndZ/D")
		nentries1 = events1.GetEntries()
		
		for ii in range(nentries1):
			events1.GetEntry(ii)
			Hvz[i].Fill((events1.triEndZ))

	#truth plots
	print "Truth: " + str(numf)
	Htvz = [None]; Htvz = ROOT.TH1F("tVZ_"+str(i),"tVZ_"+str(i),400,0,400)
	f2 = TFile(path_truth+element+'/ap-WBT_'+element+'MeV_truth.root')
	events2 = f2.Get("ntuple")
	events2.Branch("triEndZ",truEndZ,"triEndZ/D")
	nentries2 = events2.GetEntries()
	print "number of truth events: ", nentries2

	for ii in range(nentries2):
		if ii % ((nentries2-nentries2%10)/10) == 0:
			print "    event number: ",ii
		events2.GetEntry(ii)
		Htvz.Fill((events2.triEndZ))

	#take the ratio and configure plots
	print "Ratio folder: " + str(numf)
	for i in range(len(fn_recon)):
		print "    file: "+ str(i)
		Hrat[i] = Hvz[i]
		Hrat[i].Divide(Htvz)
		runname = fn_recon[i].replace(".root","")
		Hrat[i].SetTitle(runname+'efficiency');

	#create canvas to plot
	c1 = TCanvas("c1","VZ_efficiency",800,600)

	#plot on canvas
	c1.Print(str(element)+'_VZ_efficiency.pdf[')

	for i in range(len(fn_recon)):
		c1.cd(); Hrat[i].Draw();
		c1.Print(str(element)+'_VZ_efficiency.pdf'); c1.Clear();

	c1.Print(str(element)+'_VZ_efficiency.pdf]'); c1.Close();
