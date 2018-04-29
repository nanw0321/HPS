//Load file
f = new TFile("20170830_l6b_axial_hole_f7_h_b180v_nominal_tuple.root");

//Create variables in memory and link to leaves
Double_t event,hybrid,apv,pchannel,rchannel,sample0,sample1,sample2,sample3,sample4,sample5;

results->SetBranchAddress("event",&event);
results->SetBranchAddress("hybrid",&hybrid);
results->SetBranchAddress("apv",&apv);
results->SetBranchAddress("pchannel",&pchannel);
results->SetBranchAddress("rchannel",&rchannel);
results->SetBranchAddress("sample0",&sample0);
results->SetBranchAddress("sample1",&sample1);
results->SetBranchAddress("sample2",&sample2);
results->SetBranchAddress("sample3",&sample3);
results->SetBranchAddress("sample4",&sample4);
results->SetBranchAddress("sample5",&sample5);

//Number of entries for looping
Long64_t nentries = results->GetEntries();
Long64_t nbytes = 0;

//2D histogram
TCanvas *c1 = new TCanvas("c1","sample vs pchannel", 800,600);
results->Draw("sample0+sample1+sample2+sample3+sample4+sample5:pchannel>>hist1");
Int_t nbinx = hist1->GetNbinsX();
Int_t nbiny = hist1->GetNbinsY();
Int_t xmin = hist1->GetXaxis()->GetXmin();
Int_t xmax = hist1->GetXaxis()->GetXmax();
Int_t ymin = hist1->GetYaxis()->GetXmin();
Int_t ymax = hist1->GetYaxis()->GetXmax();
Int_t binwidthx = hist1->GetXaxis()->GetBinWidth(binwidthx);
Int_t binwidthy = hist1->GetXaxis()->GetBinWidth(binwidthy);

//Profile Histogram
TCanvas *c2 = new TCanvas("c2","profile histogram", 800,600);
hprof = new TProfile("hprof", "Profile of sample vs channel",nbinx,xmin,xmax,ymin,ymax);

for (Long64_t i=0; i<nentries; i++) {
	nbytes += results->GetEntry(i);
	hprof->Fill(pchannel,sample0+sample1+sample2+sample3+sample4+sample5,binwidthx);
}
hprof->SetMinimum(ymin)；
hprof->Draw();
