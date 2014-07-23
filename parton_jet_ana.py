#!/usr/bin/env python
import ROOT
import sys
import itertools
import math
from tools.histo_dict import histo_dict
from tools.progbar import progbar
import warnings
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*TCompare*')
import tools.parse

# ExRoot Tree Container Class
ROOT.gSystem.Load('/shome/peller/Madgraph/MG5_aMC_v2_1_0/ExRootAnalysis/lib/libExRootAnalysis.so')

def deltaRpT(vec1,vec2):
    dEta = vec1.Eta() - vec2.Eta()
    dPhi = ROOT.TVector2.Phi_mpi_pi(vec1.Phi() - vec2.Phi())
    dPt = vec1.Pt() - vec2.Pt()
    return math.sqrt(dEta*dEta + dPhi*dPhi + dPt*dPt)

def deltaR(vec1,vec2):
    return vec1.DeltaR(vec2)

group = 'ZH50'
#group = 'ZH30'
#group = 'ZH_inclusive'
#group = 'ZH_MG_012j'
#group = 'ZH_MG_0j'

# Herwig True | Pythia False ?
weighted = False
# ickkw reweighted True
clone = False
# FxFx True
overlay = False
normalize = True

collection = parse.samples('../data/samples_highstat.cfg')
#collection = parse.samples('../data/samples.cfg')

samples = collection.group[group]
outfile = ROOT.TFile('../data/%s.root'%group,'RECREATE')

# book histos
histos = histo_dict()
histos.add('mbb',40,140)
histos.add('mbbj',40,140)
histos['mbbj'].SetLineColor(ROOT.kRed)
histos.add('mll',50,150)
histos.add('l0_pt',0,250,8)
histos.add('l1_pt',0,250,8)
histos.add('b0j_pt',0,250,8)
histos['b0j_pt'].SetLineColor(ROOT.kRed)
histos.add('b1j_pt',0,250,8)
histos['b1j_pt'].SetLineColor(ROOT.kRed)
histos.add('dR0',0,1,0.05)
histos.add('dR1',0,1,0.05)
histos['dR1'].SetLineColor(ROOT.kGreen)
histos.add('b0j_dPt',-0.1,0.9,0.01)
histos.add('b1j_dPt',-0.1,0.9,0.01)

# first b-parton
histos.add('b0_pt',0,250,8)
if overlay:
    histos.add('b0_pt0j',0,250,8)
    histos.add('b0_pt1j',0,250,8)
    histos.add('b0_pt2j',0,250,8)
    histos['b0_pt'].SetLineColor(ROOT.kBlack)
    histos['b0_pt0j'].SetLineColor(ROOT.kGreen)
    histos['b0_pt1j'].SetLineColor(ROOT.kRed)
    histos['b0_pt2j'].SetLineColor(ROOT.kBlue)
    histos['b0_pt0j'].SetLineStyle(4)
    histos['b0_pt1j'].SetLineStyle(4)
    histos['b0_pt2j'].SetLineStyle(4)

# second b-parton
histos.add('b1_pt',0,250,8)
if overlay:
    histos.add('b1_pt0j',0,250,8)
    histos.add('b1_pt1j',0,250,8)
    histos.add('b1_pt2j',0,250,8)
    histos['b1_pt'].SetLineColor(ROOT.kBlack)
    histos['b1_pt0j'].SetLineColor(ROOT.kGreen)
    histos['b1_pt1j'].SetLineColor(ROOT.kRed)
    histos['b1_pt2j'].SetLineColor(ROOT.kBlue)
    histos['b1_pt0j'].SetLineStyle(4)
    histos['b1_pt1j'].SetLineStyle(4)
    histos['b1_pt2j'].SetLineStyle(4)

# first aJet0
histos.add('aJ0_pt',0,250,8)
if overlay:
    histos.add('aJ0_pt0j',0,250,8)
    histos.add('aJ0_pt1j',0,250,8)
    histos.add('aJ0_pt2j',0,250,8)
    histos['aJ0_pt'].SetLineColor(ROOT.kBlack)
    histos['aJ0_pt0j'].SetLineColor(ROOT.kGreen)
    histos['aJ0_pt1j'].SetLineColor(ROOT.kRed)
    histos['aJ0_pt2j'].SetLineColor(ROOT.kBlue)
    histos['aJ0_pt0j'].SetLineStyle(4)
    histos['aJ0_pt1j'].SetLineStyle(4)
    histos['aJ0_pt2j'].SetLineStyle(4)

# h-candidate pt
histos.add('hc_pt',0,250,8)
if overlay:
    histos.add('hc_pt0j',0,250,8)
    histos.add('hc_pt1j',0,250,8)
    histos.add('hc_pt2j',0,250,8)
    histos['hc_pt'].SetLineColor(ROOT.kBlack)
    histos['hc_pt0j'].SetLineColor(ROOT.kGreen)
    histos['hc_pt1j'].SetLineColor(ROOT.kRed)
    histos['hc_pt2j'].SetLineColor(ROOT.kBlue)
    histos['hc_pt0j'].SetLineStyle(4)
    histos['hc_pt1j'].SetLineStyle(4)
    histos['hc_pt2j'].SetLineStyle(4)

# h-candidate pt
histos.add('hl_pt',0,250,8)
if overlay:
    histos.add('hl_pt0j',0,250,8)
    histos.add('hl_pt1j',0,250,8)
    histos.add('hl_pt2j',0,250,8)
    histos['hl_pt'].SetLineColor(ROOT.kBlack)
    histos['hl_pt0j'].SetLineColor(ROOT.kGreen)
    histos['hl_pt1j'].SetLineColor(ROOT.kRed)
    histos['hl_pt2j'].SetLineColor(ROOT.kBlue)
    histos['hl_pt0j'].SetLineStyle(4)
    histos['hl_pt1j'].SetLineStyle(4)
    histos['hl_pt2j'].SetLineStyle(4)

# n-jets
histos.add('njets',10)
if overlay:
    histos.add('njets0j',10)
    histos.add('njets1j',10)
    histos.add('njets2j',10)
    histos['njets'].SetLineColor(ROOT.kBlack)
    histos['njets0j'].SetLineColor(ROOT.kGreen)
    histos['njets1j'].SetLineColor(ROOT.kRed)
    histos['njets2j'].SetLineColor(ROOT.kBlue)
    histos['njets0j'].SetLineStyle(4)
    histos['njets1j'].SetLineStyle(4)
    histos['njets2j'].SetLineStyle(4)

for sample in samples:
    print 'working on %s'%sample

    # parse filenames and open
    hep_f_name = '../data/input/' + sample.id + '.root'
    jet_f_name = '../data/output/' + sample.id + '.root'
    hep_file = ROOT.TFile(hep_f_name)
    jet_file = ROOT.TFile(jet_f_name)
    outfile.cd()

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


        event_weight = gen_weight*sample_weight

        AK5_N = fastjet.AK5_N
        histos['njets'].Fill(AK5_N,event_weight)

        if overlay:
            if sample.process == 'ZH':
                histos['njets0j'].Fill(AK5_N,event_weight)
            elif sample.process == 'ZHj':
                histos['njets1j'].Fill(AK5_N,event_weight)
            elif sample.process == 'ZHjj':
                histos['njets2j'].Fill(AK5_N,event_weight)

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
            z = ls[0]+ls[1]
    
            histos['l0_pt'].Fill(ls[0].Pt(),event_weight)
            histos['l1_pt'].Fill(ls[1].Pt(),event_weight)
            histos['mll'].Fill(z.M(),event_weight)
            '''
            if z.Pt() < 100:
                continue
            '''
        if len(bs) > 1 and len(jets) > 1:

            # born level bs from h decay
            bs = sorted(bs, key=lambda x: x.Pt(), reverse=True)
            h = bs[0]+bs[1]

            '''
            if h.Pt() < 50:
                continue
            if abs(bs[0].Eta()) > 2.5:
                continue
            if abs(bs[1].Eta()) > 2.5:
                continue
            if bs[1].Pt() < 20:
               continue
            '''


            #match bs to jets:
            #leading jet
            dRs = [deltaR(bs[0],jet) for jet in jets]
            dR0 = min(dRs)
            b0_jet = jets.pop(dRs.index(dR0))
            #second jet
            dRs = [deltaR(bs[1],jet) for jet in jets]
            dR1 = min(dRs)
            b1_jet = jets.pop(dRs.index(dR1))

            '''
            if dR0 > 0.3 or dR1 > 0.3:
                continue
            '''
            
            # higgs candidate
            hc = b0_jet + b1_jet

            # H + Z
            hl = hc + z

            #Fill Histos
            histos['dR0'].Fill(dR0,event_weight)
            histos['dR1'].Fill(dR1,event_weight)
            histos['b0j_pt'].Fill(b0_jet.Pt(),event_weight)
            histos['b0j_dPt'].Fill((bs[0].Pt()-b0_jet.Pt())/bs[0].Pt(),event_weight)
            histos['b1j_pt'].Fill(b1_jet.Pt(),event_weight)
            histos['b1j_dPt'].Fill((bs[1].Pt()-b1_jet.Pt())/bs[1].Pt(),event_weight)
            if len(jets) > 0:
                histos['aJ0_pt'].Fill(jets[0].Pt(),event_weight)

            histos['mbb'].Fill(h.M(),event_weight)

            histos['mbbj'].Fill(hc.M(),event_weight)
            histos['hc_pt'].Fill(hc.Pt(),event_weight)
            histos['hl_pt'].Fill(hl.Pt(),event_weight)
            histos['b0_pt'].Fill(bs[0].Pt(),event_weight)
            histos['b1_pt'].Fill(bs[1].Pt(),event_weight)

            if overlay:
                if sample.process == 'ZH':
                    histos['b0_pt0j'].Fill(bs[0].Pt(),event_weight)
                    histos['b1_pt0j'].Fill(bs[1].Pt(),event_weight)
                    histos['hc_pt0j'].Fill(hc.Pt(),event_weight)
                    histos['hl_pt0j'].Fill(hl.Pt(),event_weight)
                    if len(jets) > 0:
                        histos['aJ0_pt0j'].Fill(jets[0].Pt(),event_weight)
                elif sample.process == 'ZHj':
                    histos['b0_pt1j'].Fill(bs[0].Pt(),event_weight)
                    histos['b1_pt1j'].Fill(bs[1].Pt(),event_weight)
                    histos['hc_pt1j'].Fill(hc.Pt(),event_weight)
                    histos['hl_pt1j'].Fill(hl.Pt(),event_weight)
                    if len(jets) > 0:
                        histos['aJ0_pt1j'].Fill(jets[0].Pt(),event_weight)
                elif sample.process == 'ZHjj':
                    histos['b0_pt2j'].Fill(bs[0].Pt(),event_weight)
                    histos['b1_pt2j'].Fill(bs[1].Pt(),event_weight)
                    histos['hc_pt2j'].Fill(hc.Pt(),event_weight)
                    histos['hl_pt2j'].Fill(hl.Pt(),event_weight)
                    if len(jets) > 0:
                        histos['aJ0_pt2j'].Fill(jets[0].Pt(),event_weight)

        else:
            continue

    hep_file.Close()
    jet_file.Close()

if normalize:
    histos.normalize()

c1 = ROOT.TCanvas('c1','c1',1000,1000)
c1.Divide(2,2)

c1.cd(1)
#histos['mbb'].Draw()
#histos['mbbj'].Draw("same")

histos['njets'].Draw()
if overlay:
    histos['njets0j'].Draw("same")
    histos['njets1j'].Draw("same")
    histos['njets2j'].Draw("same")
c1.cd(2)
ROOT.gPad.SetLogy()
#histos['mll'].Draw()
#histos['dR0'].Draw()
#histos['dR1'].Draw("same")
histos['hc_pt'].Draw()
if overlay:
    histos['hc_pt0j'].Draw("same")
    histos['hc_pt1j'].Draw("same")
    histos['hc_pt2j'].Draw("same")
c1.cd(3)
ROOT.gPad.SetLogy()
#histos['l0_pt'].Draw()
#histos['l1_pt'].Draw("same")
#histos['b0_pt'].Draw()
#histos['b0_pt0j'].Draw("same")
#histos['b0_pt1j'].Draw("same")
#histos['b0_pt2j'].Draw("same")
histos['aJ0_pt'].Draw()
if overlay:
    histos['aJ0_pt0j'].Draw("same")
    histos['aJ0_pt1j'].Draw("same")
    histos['aJ0_pt2j'].Draw("same")
c1.cd(4)
ROOT.gPad.SetLogy()
histos['hl_pt'].Draw()
if overlay:
    histos['hl_pt0j'].Draw("same")
    histos['hl_pt1j'].Draw("same")
    histos['hl_pt2j'].Draw("same")

#histos['b1_pt'].Draw()
#histos['b1_pt0j'].Draw("same")
#histos['b1_pt1j'].Draw("same")
#histos['b1_pt2j'].Draw("same")

c1.Update()
c1.SaveAs('plots/%s.pdf'%group)

histos.write()
histos.dump(prefix='plots/%s_'%group)
