#!/usr/bin/env python
import ROOT
import sys
import math
from tools.progbar import progbar
import warnings
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*TCompare*')
import tools.parse as parse
import array
import itertools

ROOT.gROOT.ProcessLine('.L VectorTLorentzVector_h.so')

def deltaRpT(vec1,vec2):
    dEta = vec1.Eta() - vec2.Eta()
    dPhi = ROOT.TVector2.Phi_mpi_pi(vec1.Phi() - vec2.Phi())
    dPt = vec1.Pt() - vec2.Pt()
    return math.sqrt(dEta*dEta + dPhi*dPhi + dPt*dPt)

def deltaR(vec1,vec2):
    return vec1.DeltaR(vec2)

group = 'ZH_powheg'

outfile = ROOT.TFile('../data/tree_%s.root'%group,'RECREATE')
outfile.cd()

mytree = ROOT.TTree('mytree','mytree')

# Higgs branches
H = ROOT.std.vector(ROOT.TLorentzVector)()
mytree.Branch( "H", "vector<TLorentzVector>", H)
h_dau =ROOT.std.vector(ROOT.TLorentzVector)()
mytree.Branch( "h_dau", "vector<TLorentzVector>", h_dau)

# Z branches
Z = ROOT.std.vector(ROOT.TLorentzVector)()
mytree.Branch( "Z", "vector<TLorentzVector>", Z)
z_dau = ROOT.std.vector(ROOT.TLorentzVector)()
mytree.Branch( "z_dau", "vector<TLorentzVector>", z_dau)

# Jet branches
aJets = ROOT.std.vector(ROOT.TLorentzVector)()
mytree.Branch( "aJets", "vector<TLorentzVector>",aJets)
n_aJets = array.array('i',[0])
mytree.Branch('n_aJets',n_aJets,'n_aJets/I')

# weight branch
weight = array.array('f',[0])
mytree.Branch('weight',weight,'weight/F')

weighted = False

# parse filenames and open
infilename = '../data/input/ZllHbb_Powheg.root'
infile = ROOT.TFile(infilename)

particles= infile.Get('Particles')
ak5 = infile.Get('AK5')

numberOfEntries = 3000
#numberOfEntries = particles.GetEntries()

# progress bar gimick
print 'analyzing %s events'%numberOfEntries
pb = progbar(30)
step = numberOfEntries/pb.width

for entry in xrange(numberOfEntries):

    if entry%step == 0:
        pb.move()

    particles.GetEntry(entry+1)
    ak5.GetEntry(entry+1)

    weight[0] = 1.

    bs = [] # b quarks
    ls = [] # leptons
    jets = [] # jets

    # make jet 4-vectors
    for jet in xrange(ak5.ak5_size):
        if ak5.pt[jet] > 20:
            jets.append(ROOT.TLorentzVector())
            jets[-1].SetPtEtaPhiM(
                    ak5.pt[jet],
                    ak5.eta[jet],
                    ak5.phi[jet],
                    ak5.mass[jet])
    jets = sorted(jets, key=lambda x: x.Pt(), reverse=True)

    hs = []
    zs = []
    all_bs = []
    all_ls = []

    for p in xrange(particles.particles_size):
        # from hard interaction
        status = particles.status[p]
        pdgId = particles.pdgId[p]
        if (status == 3 and (pdgId == 23 or pdgId == 25)) or (status == 2 and abs(pdgId) == 5) or (status == 1 and (abs(pdgId) == 11 or abs(pdgId) ==13)):

            particle = ROOT.TLorentzVector()
            particle.SetPtEtaPhiM(
                    particles.pt[p],
                    particles.eta[p],
                    particles.phi[p],
                    particles.mass[p])

            if status == 3:
                if pdgId == 23:
                    zs.append(particle)
                else:
                    hs.append(particle)
            elif abs(pdgId) == 5:
                if particle.Pt() > 10:
                    all_bs.append(particle)

            else:
                if particle.Pt() > 10:
                    all_ls.append(particle)


    hs = sorted(hs, key=lambda x: x.Pt(), reverse=True)
    zs = sorted(zs, key=lambda x: x.Pt(), reverse=True)
    all_bs = sorted(all_bs, key=lambda x: x.Pt(), reverse=True)
    all_ls = sorted(all_ls, key=lambda x: x.Pt(), reverse=True)


    if len(hs) > 0 and len(zs) > 0:
        #H.clear()
        #H.push_back(hs[0])
        Z.clear()
        Z.push_back(zs[0])
        #mytree.Fill()

    bs = []
    if len(all_bs) > 1:
        dR = 999999
        for x,y in itertools.combinations(all_bs,2):
            delta = deltaRpT(x + y,hs[0])
            if delta < dR:
                dR = delta
                b0 = x
                b1 = y
        bs.append(b0)
        bs.append(b1)

    ls = []
    if len(all_ls) > 1:
        dR = 999999
        for x,y in itertools.combinations(all_ls,2):
            delta = deltaRpT(x+y,zs[0])
            if delta < dR:
                dR = delta
                l0 = x
                l1 = y
        ls.append(l0)
        ls.append(l1)

    #if len(ls) > 1 : 

        # born level leptons
        #Z.clear()
        #Z.push_back(ls[0]+ls[1])
        #z_dau.clear()
        #z_dau.push_back(ls[0])
        #z_dau.push_back(ls[1])

    if len(bs) > 1 and len(jets) > 1:

        # born level bs from h decay
        h = bs[0]+bs[1]

        #match bs to jets:
        #leading jet
        dRs = [deltaR(bs[0],jet) for jet in jets]
        dR0 = min(dRs)
        b0_jet = jets.pop(dRs.index(dR0))
        #second jet
        dRs = [deltaR(bs[1],jet) for jet in jets]
        dR1 = min(dRs)
        b1_jet = jets.pop(dRs.index(dR1))
            
        # higgs candidate
        H.clear()
        H.push_back(b0_jet + b1_jet)
        h_dau.clear()
        h_dau.push_back(b0_jet)
        h_dau.push_back(b1_jet)

        aJets.clear()
        n_aJets[0] = len(jets)
        if n_aJets[0] > 0:
            for jet in jets:
                aJets.push_back(jet)

        #mytree.Print()
        mytree.Fill()
    else:
        continue


infile.Close()
    
mytree.AutoSave()
outfile.Close()

