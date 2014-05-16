import ROOT
import sys
import itertools
import math
from histo_dict import histo_dict
from progbar import progbar
import warnings
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*TCompare*')

# ExRoot Tree Container Class
ROOT.gSystem.Load('/shome/peller/Madgraph/MG5_aMC_v2_1_0/ExRootAnalysis/lib/libExRootAnalysis.so')

def deltaRpT(vec1,vec2):
    dEta = vec1.Eta() - vec2.Eta()
    dPhi = ROOT.TVector2.Phi_mpi_pi(vec1.Phi() - vec2.Phi())
    dPt = vec1.Pt() - vec2.Pt()
    return math.sqrt(dEta*dEta + dPhi*dPhi + dPt*dPt)

def deltaR(vec1,vec2):
    return vec1.DeltaR(vec2)

# parse filenames and open
hep_f_name = sys.argv[1] #ExRoot input
jet_f_name = sys.argv[2] #Sparty input
hep_file = ROOT.TFile(hep_f_name)
jet_file = ROOT.TFile(jet_f_name)
outfile = ROOT.TFile('output.root','RECREATE')

stdhep = hep_file.Get('STDHEP')
stdhepReader = ROOT.ExRootTreeReader(stdhep)
particles = stdhepReader.UseBranch('GenParticle')
events = stdhepReader.UseBranch('Event')
numberOfEntries = stdhepReader.GetEntries()
fastjet = jet_file.Get('my_Tree')


# book histos
histos = histo_dict()
histos.add('mbb',40,140)
histos.add('mbbj',40,140)
histos['mbbj'].SetLineColor(ROOT.kRed)
histos.add('mll',50,150)
histos.add('njets',10)
histos.add('l0_pt',0,250,2)
histos.add('l1_pt',0,250,2)
histos.add('b0_pt',0,250,2)
histos.add('b0j_pt',0,250,2)
histos['b0j_pt'].SetLineColor(ROOT.kRed)
histos.add('b1_pt',0,250,2)
histos.add('b1j_pt',0,250,2)
histos['b1j_pt'].SetLineColor(ROOT.kRed)
histos.add('dR0',0,1,0.05)
histos.add('dR1',0,1,0.05)
histos['dR1'].SetLineColor(ROOT.kGreen)
histos.add('b0j_dPt',-0.1,0.9,0.01)
histos.add('b1j_dPt',-0.1,0.9,0.01)


# assert files have the same number of entries (ExRoot delets first and last (empty) events from STDHEP already)
assert numberOfEntries  == fastjet.GetEntries()-2

# progress bar gimick
print 'analyzing %s events'%numberOfEntries
pb = progbar(30)
step = numberOfEntries/pb.width

for entry in xrange(numberOfEntries):

    if entry%step == 0:
        pb.move()

    stdhepReader.ReadEntry(entry)
    fastjet.GetEntry(entry+1)

    # EVENT weight
    weight = events[0].Weight

    AK5_N = fastjet.AK5_N
    histos['njets'].Fill(AK5_N,weight)

    bs = [] # b quarks
    ls = [] # leptons
    jets = [] # jets

    # make jet 4-vectors
    for jet in xrange(AK5_N):
        jets.append(ROOT.TLorentzVector())
        jets[-1].SetPtEtaPhiE(
                fastjet.AK5_pt[jet],
                fastjet.AK5_eta[jet],
                fastjet.AK5_phi[jet],
                fastjet.AK5_e[jet])
    jets = sorted(jets, key=lambda x: x.Pt(), reverse=True)

    for particle in particles:
        #initial b quark from higgs decay
        if abs(particle.PID) == 5:
            M1_index = particle.M1
            pM1 = particles[M1_index]
            if pM1.PID == 25:
                bs.append(ROOT.TLorentzVector())
                bs[-1].SetPtEtaPhiE(
                        particle.PT,
                        particle.Eta,
                        particle.Phi,
                        particle.E)

        #e or mu or tau from z decay
        if abs(particle.PID) in [11,13,15]:
            M1_index = particle.M1
            pM1 = particles[M1_index]
            if pM1.PID == 23:
                ls.append(ROOT.TLorentzVector())
                ls[-1].SetPtEtaPhiE(
                        particle.PT,
                        particle.Eta,
                        particle.Phi,
                        particle.E)

    if len(ls) > 1 and len(bs) > 1 and len(jets) > 1: 

        # born level leptons
        ls = sorted(ls, key=lambda x: x.Pt(), reverse=True)
        z = ls[0]+ls[1]

        if z.Pt() < 100:
            continue

        # born level bs from h decay
        bs = sorted(bs, key=lambda x: x.Pt(), reverse=True)
        h = bs[0]+bs[1]

        if h.Pt() < 50:
            continue
        if abs(bs[0].Eta()) > 2.5:
            continue
        if abs(bs[1].Eta()) > 2.5:
            continue
        if bs[1].Pt() < 20:
            continue


        #match bs to jets:
        #leading jet
        dRs = [deltaR(bs[0],jet) for jet in jets]
        dR0 = min(dRs)
        b0_jet = jets.pop(dRs.index(dR0))
        #second jet
        dRs = [deltaR(bs[1],jet) for jet in jets]
        dR1 = min(dRs)
        b1_jet = jets.pop(dRs.index(dR1))

        if dR0 > 0.3 or dR1 > 0.3:
            continue
        
        # higgs candidate
        hc = b0_jet + b1_jet

        #Fill Histos
        histos['dR0'].Fill(dR0,weight)
        histos['dR1'].Fill(dR1,weight)
        histos['b0j_pt'].Fill(b0_jet.Pt(),weight)
        histos['b0j_dPt'].Fill((bs[0].Pt()-b0_jet.Pt())/bs[0].Pt(),weight)
        histos['b1j_pt'].Fill(b1_jet.Pt(),weight)
        histos['b1j_dPt'].Fill((bs[1].Pt()-b1_jet.Pt())/bs[1].Pt(),weight)

        histos['l0_pt'].Fill(ls[0].Pt(),weight)
        histos['l1_pt'].Fill(ls[1].Pt(),weight)
        histos['mll'].Fill(z.M(),weight)
        histos['mbb'].Fill(h.M(),weight)

        histos['mbbj'].Fill(hc.M(),weight)
        histos['b0_pt'].Fill(bs[0].Pt(),weight)
        histos['b1_pt'].Fill(bs[1].Pt(),weight)

    else:
        continue

c1 = ROOT.TCanvas('c1','c1',1000,1000)
c1.Divide(2,2)

c1.cd(1)
histos['mbb'].Draw()
histos['mbbj'].Draw("same")
c1.cd(2)
#histos['mll'].Draw()
histos['dR0'].Draw()
histos['dR1'].Draw("same")
c1.cd(3)
#histos['l0_pt'].Draw()
#histos['l1_pt'].Draw("same")
histos['b0_pt'].Draw()
histos['b0j_pt'].Draw("same")
c1.cd(4)
histos['b1_pt'].Draw()
histos['b1j_pt'].Draw("same")

c1.Update()
c1.SaveAs('test.pdf')

histos.dump()
