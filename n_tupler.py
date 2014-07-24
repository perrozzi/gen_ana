#!/usr/bin/env python
import ROOT
import sys
import math
from tools.progbar import progbar
import warnings
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*TCompare*')
import tools.parse as parse
import array

# ExRoot Tree Container Class
ROOT.gSystem.Load('/shome/peller/Madgraph/MG5_aMC_v2_1_0/ExRootAnalysis/lib/libExRootAnalysis.so')
ROOT.gROOT.ProcessLine('.L VectorTLorentzVector_h.so')

def deltaRpT(vec1,vec2):
    dEta = vec1.Eta() - vec2.Eta()
    dPhi = ROOT.TVector2.Phi_mpi_pi(vec1.Phi() - vec2.Phi())
    dPt = vec1.Pt() - vec2.Pt()
    return math.sqrt(dEta*dEta + dPhi*dPhi + dPt*dPt)

def deltaR(vec1,vec2):
    return vec1.DeltaR(vec2)

#group = 'ZH50'
group = 'ZH'
#group = 'ZH_inclusive'
#group = 'ZH_MG_012j'
#group = 'ZH_MG_0j'

#collection = parse.samples('../data/samples_highstat.cfg')
collection = parse.samples('../data/samples.cfg')

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
# ickkw reweighted True
clone = False


samples = collection.group[group]


for sample in samples:
    print 'working on %s'%sample

    # parse filenames and open
    hep_f_name = '../data/input/' + sample.id + '.root'
    jet_f_name = '../data/output/' + sample.id + '.root'
    hep_file = ROOT.TFile(hep_f_name)
    jet_file = ROOT.TFile(jet_f_name)

    _stdhep = hep_file.Get('STDHEP')
    if clone:
        print 'cloning...'
        stdhep = _stdhep.CopyTree('GenParticle_size > 0')
    else:
        stdhep = _stdhep
    stdhepReader = ROOT.ExRootTreeReader(stdhep)
    particles = stdhepReader.UseBranch('GenParticle')
    events = stdhepReader.UseBranch('Event')
    numberOfEntries = stdhepReader.GetEntries()
    fastjet = jet_file.Get('AK5')

    # assert files have the same number of entries (ExRoot delets first and last (empty) events from STDHEP already)
    assert numberOfEntries  == fastjet.GetEntries()-2

    sample_weight = float(sample.xsec)/float(sample.n_gen) 

    # progress bar gimick
    print 'analyzing %s events'%numberOfEntries
    pb = progbar(30)
    step = numberOfEntries/pb.width

    for entry in xrange(numberOfEntries):

        if entry%step == 0:
            pb.move()

        stdhepReader.ReadEntry(entry)
        fastjet.GetEntry(entry+1)

        # EVENT gen_weight
        if weighted:
            gen_weight = events[0].Weight
        else:
            gen_weight = 1.
        weight[0] = gen_weight*sample_weight


        AK5_N = fastjet.AK5_N

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

        if len(ls) > 1 : 

            # born level leptons
            ls = sorted(ls, key=lambda x: x.Pt(), reverse=True)
            Z.clear()
            Z.push_back(ls[0]+ls[1])
            z_dau.clear()
            z_dau.push_back(ls[0])
            z_dau.push_back(ls[1])
    
        if len(bs) > 1 and len(jets) > 1:

            # born level bs from h decay
            bs = sorted(bs, key=lambda x: x.Pt(), reverse=True)
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


    hep_file.Close()
    jet_file.Close()
    
mytree.AutoSave()
outfile.Close()

