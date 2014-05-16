import ROOT
import sys
import itertools

f_name = sys.argv[1]
infile = ROOT.TFile(f_name)
tree = infile.Get('my_Tree')

histo = ROOT.TH1F('histo','histo',250,0,250)

for i in range(tree.GetEntries()):
    tree.GetEntry(i)
    njets = tree.AK5_N
    vectors = []
    dijets = []
    for jet in range(njets):
        E   = tree.AK5_e[jet]
        Phi = tree.AK5_phi[jet] 
        Eta = tree.AK5_eta[jet]
        Pt  = tree.AK5_pt[jet]
        nc = tree.AK5_numC[jet]
        if Pt > 20. and abs(Eta)<2.5 and nc < 5:
            vectors.append(ROOT.TLorentzVector())
            vectors[-1].SetPtEtaPhiE(Pt,Eta,Phi,E)
    #pairwise
    dijet_pt = 0
    mass = 0
    for x,y in itertools.combinations(vectors,2):
        dijet = x + y
        if dijet.Pt() > dijet_pt:
            dijet_pt = dijet.Pt()
            mass = dijet.M()

    if dijet_pt > 50:
        histo.Fill(mass)

histo.Draw()
