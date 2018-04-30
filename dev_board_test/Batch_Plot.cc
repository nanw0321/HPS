 //define string variables
TString runname = "l6b_axial_hole_f7_h_b180v_nominal";
TString dataname = "sample";
TString str1;
TString str2;

//load file
f = new TFile("20170830_"+runname+"_tuple.root");

//create canvas
TCanvas *c1 = new TCanvas("c1","sample vs pchannel",800,600);
c1->Print(runname+".pdf[")

//plot 2D histo
for (Int_t i=0;i<6;i++) {
str1.Form(dataname+"%d:pchannel>>hist1(700,0,700,2500,4500,7000)",i);
str2.Form(runname+"_sample%d",i);
results->Draw(str1,"","COLZ");
c1->Update();
Printf("i=%d",i);
c1->Update();
c1->Print(runname+".pdf");
}

c1->Print(runname+".pdf]");
