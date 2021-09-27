import ROOT

# load data into dataframe
df = ROOT.RDataFrame("Events","Run2012BC_DoubleMuParked_Muons.root")

# filter out only events with two muons 
df_2mu = df.Filter("nMuon == 2", "Events with exactly two muons!")

# filter out only events with opposite charge muons
df_os = df_2mu.Filter("Muon_charge[0] != Muon_charge[1]", "Munos with opposite charge")

# c++ code to calculate invariant mass of the two muons
ROOT.gInterpreter.Declare('''
using Vec_t = const ROOT::RVec<float>&;
float ComputeInvariantMass(Vec_t pt, Vec_t eta, Vec_t phi, Vec_t mass) {
    const ROOT::Math::PtEtaPhiMVector p1(pt[0], eta[0], phi[0], mass[0]);
    const ROOT::Math::PtEtaPhiMVector p2(pt[1], eta[1], phi[1], mass[1]);
    return (p1 + p2).M();
}
''')

# adding the computed mass to the dataframe
df_mass = df_os.Define("Dimoun_mass", "ComputeInvariantMass(Muon_pt, Muon_eta, Muon_phi, Muon_mass)")

# put the dimuon mass from dataframe into hist 
h = df_mass.Histo1D(("Dimoun_mass", ";m_{#mu#mu} (GeV);N_{Events}", 30000, 0.25, 300), "Dimuon_mass")

report = df_mass.Report() # cut-flow report? gathers some stats..

# drawing the plot 

# Produce plot
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTextFont(42)
c = ROOT.TCanvas("c", "", 800, 700)
# The contents of one of the dataframe results are accessed for the first time here:
# accessing the dataframe calls the function ComputeInvariantMass and the calculation is made now
h.GetXaxis().SetTitleSize(0.04)
h.GetYaxis().SetTitleSize(0.04)
c.SetLogx(); c.SetLogy()
h.Draw()

label = ROOT.TLatex()
label.SetNDC(True)
label.SetTextSize(0.040)
label.DrawLatex(0.100, 0.920, "#bf{CMS Open Data}")
label.DrawLatex(0.550, 0.920, "#sqrt{s} = 8 TeV, L_{int} = 11.6 fb^{-1}")

# Save as png file
c.SaveAs("dimuon_spectrum.png")

# Print cut-flow report
report.Print()