import os
path = '/home/nanw/HPS/dev_board_test'

import ROOT
from ROOT import TFile, TCanvas, TTree, gROOT, TProfile

from array import array

#read filenames
fn = []

for filename in os.listdir(path):
	if filename.endswith(".root"):
		fn.append(filename)
	else:
		continue

#create branch addresses
pchannel,sample0, sample1, sample2, sample3, sample4, sample5 = (array('d',[0]),) * 7
nbytes = 0

#TProfile
hprof0 = TProfile("hprof0","sample0",700,0,700,4500,7000)
hprof1 = TProfile("hprof1","sample1",700,0,700,4500,7000)
hprof2 = TProfile("hprof2","sample2",700,0,700,4500,7000)
hprof3 = TProfile("hprof3","sample3",700,0,700,4500,7000)
hprof4 = TProfile("hprof4","sample4",700,0,700,4500,7000)
hprof5 = TProfile("hprof5","sample5",700,0,700,4500,7000)

##--if all data on the same plot:
c1 = TCanvas("c1","profile histogram",800,600);
c1.Print('Profile_Histogram_all.pdf[')

for i in range(len(fn)):
	print i
	if i > 0:
		print "i = 1"
		break
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
		hprof0.Fill(events.pchannel,events.sample0,1)
		hprof1.Fill(events.pchannel,events.sample1,1)
		hprof2.Fill(events.pchannel,events.sample2,1)
		hprof3.Fill(events.pchannel,events.sample3,1)
		hprof4.Fill(events.pchannel,events.sample4,1)
		hprof5.Fill(events.pchannel,events.sample5,1)

	hprof0.SetMinimum(4500)
	hprof0.SetTitle(runname+'_sample0')
	hprof1.SetMinimum(4500)
	hprof1.SetTitle(runname+'_sample1')
	hprof2.SetMinimum(4500)
	hprof2.SetTitle(runname+'_sample2')
	hprof3.SetMinimum(4500)
	hprof3.SetTitle(runname+'_sample3')
	hprof4.SetMinimum(4500)
	hprof4.SetTitle(runname+'_sample4')
	hprof5.SetMinimum(4500)
	hprof5.SetTitle(runname+'_sample5')

	if i == 0:
		hprof0.Draw()
	else:
		hprof0.Draw("SAME")

	hprof1.Draw("SAME")
	hprof2.Draw("SAME")
	hprof3.Draw("SAME")
	hprof4.Draw("SAME")
	hprof5.Draw("SAME")
c1.Print('Profile_Histogram_all.pdf')
c1.Print('Profile_Histogram_all.pdf]')
