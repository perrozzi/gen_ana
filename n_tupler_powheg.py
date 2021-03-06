#!/usr/bin/env python
import ROOT
import sys
import math
from tools.progbar import progbar
import warnings
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*TCompare*')
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*TTLorentzVector*')
import tools.parse as parse
import array
import itertools
from tools.delta import *

ROOT.gROOT.ProcessLine('.L VectorTLorentzVector_h.so')

group = 'ZH_powheg'

outfile = ROOT.TFile('../data/tree_%s_PU.root'%group,'RECREATE')
outfile.cd()

mytree = ROOT.TTree('mytree','mytree')

# Higgs branches
H = ROOT.std.vector(ROOT.TLorentzVector)()
mytree.Branch( "H", "vector<TLorentzVector>", H)
genH = ROOT.std.vector(ROOT.TLorentzVector)()
mytree.Branch( "genH", "vector<TLorentzVector>", genH)
h_dau =ROOT.std.vector(ROOT.TLorentzVector)()
mytree.Branch( "h_dau", "vector<TLorentzVector>", h_dau)
genh_dau =ROOT.std.vector(ROOT.TLorentzVector)()
mytree.Branch( "genh_dau", "vector<TLorentzVector>", genh_dau)
dR = array.array('f',[0]*2)
mytree.Branch('dR', dR, 'dR[2]/F')

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
infilename = '../data/input/ZllHbb_Powheg_PU.root'
ak5filename = '../data/output/Powheg_PU.root'
infile = ROOT.TFile(infilename)
ak5file = ROOT.TFile(ak5filename)

particles= infile.Get('Particles')
ak5 = ak5file.Get('AK5')

assert particles.GetEntries() ==  ak5.GetEntries()

numberOfEntries = particles.GetEntries()
#numberOfEntries = 1000

# progress bar gimick
print 'analyzing %s events'%numberOfEntries
pb = progbar(30)
step = numberOfEntries/pb.width

for entry in xrange(numberOfEntries):

    if entry%step == 0:
        pb.move()

    particles.GetEntry(entry+1)
    ak5.GetEntry(entry)

    weight[0] = 1.

    bs = [] # b quarks
    ls = [] # leptons
    jets = [] # jets

    # make jet 4-vectors
    for jet in xrange(ak5.AK5_N):
        #if ak5.AK5_pt[jet] > 20.:
        jets.append(ROOT.TLorentzVector())
        jets[-1].SetPtEtaPhiE(
                ak5.AK5_pt[jet],
                ak5.AK5_eta[jet],
                ak5.AK5_phi[jet],
                ak5.AK5_e[jet])
    jets = sorted(jets, key=lambda x: x.Pt(), reverse=True)

    hs = []
    zs = []

    for p in xrange(particles.particles_size):
        # from hard interaction
        status = particles.status[p]
        pdgId = particles.pdgId[p]
        mother = particles.particles_mother[p]
        if (status == 3 and (pdgId == 23 or pdgId == 25)) or (mother == 25 and abs(pdgId) == 5) or (mother == 23 and (abs(pdgId) == 11 or abs(pdgId) ==13)):

            particle = ROOT.TLorentzVector()
            particle.SetPtEtaPhiM(
                    particles.pt[p],
                    particles.eta[p],
                    particles.phi[p],
                    particles.mass[p])

            if status == 3:
                if pdgId == 23:
                    zs.append(particle)
                elif pdgId == 25:
                    hs.append(particle)
            elif abs(pdgId) == 5:
                bs.append(particle)

            else:
                ls.append(particle)


    hs = sorted(hs, key=lambda x: x.Pt(), reverse=True)
    zs = sorted(zs, key=lambda x: x.Pt(), reverse=True)
    bs = sorted(bs, key=lambda x: x.Pt(), reverse=True)
    ls = sorted(ls, key=lambda x: x.Pt(), reverse=True)

    if len(bs) > 1 and len(jets) > 1 and len(ls) > 1:

        # born level bs from h decay
        h = bs[0]+bs[1]
        genH.clear()
        genH.push_back(h)
        Z.clear()
        Z.push_back(zs[0])

        z_dau.clear()
        z_dau.push_back(ls[0])
        z_dau.push_back(ls[1])

        #match bs to jets:
        #leading jet
        dRs = [deltaR(bs[0],jet) for jet in jets]
        dR0 = min(dRs)
        b0_jet = jets.pop(dRs.index(dR0))
        #second jet
        dRs = [deltaR(bs[1],jet) for jet in jets]
        dR1 = min(dRs)
        b1_jet = jets.pop(dRs.index(dR1))

        dR[0] = dR0
        dR[1] = dR1

        #if dR0 > 0.05 or dR1 > 0.1:
        #    continue
            
        # higgs candidate
        H.clear()
        H.push_back(b0_jet + b1_jet)
        h_dau.clear()
        h_dau.push_back(b0_jet)
        h_dau.push_back(b1_jet)
        genh_dau.clear()
        genh_dau.push_back(bs[0])
        genh_dau.push_back(bs[1])

        aJets.clear()
        n_aJets[0] = len(jets)
        if n_aJets[0] > 0:
            for jet in jets:
                aJets.push_back(jet)

        #mytree.Print()
        mytree.Fill()
    else:
        #print 'event skipped'
        #print len(bs), len(ls), len(jets)
        continue


infile.Close()
    
mytree.AutoSave()
outfile.Close()

