import os
path = '/home/nanw/HPS/dev_board_test'

import ROOT
from ROOT import TFile, TCanvas, TTree, gROOT

#create arrays
fn = []
histarray = []

#define canvas
c1 = TCanvas("c1","sample vs channel",800,600);

for filename in os.listdir(path):
	if filename.endswith(".root"):
		fn.append(filename)
	else:
		continue

for i in range(len(fn)):
	runname = fn[i].replace(".root","")
	#c1.Print(runname+".pdf[")
	f = TFile(path+'/'+fn[i])
	events = f.Get("results")
	for ii in range(6):
		histname = 'hist'+str(ii)
		str1 = 'sample'+str(ii)+':pchannel>>'+histname+'(700,0,700,2500,4500,7000)'
		events.Draw(str1)
		histo = gROOT.FindObject(histname)
		histarray.append(histo)
		print histname
		print histarray[0]
		print histarray[i*6+ii]
		#c1.Print(runname+".pdf")
	#c1.Print(runname+".pdf]")
	del f, events

