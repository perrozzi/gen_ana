#!/usr/bin/env python
import ROOT
from tools.Ratio import getRatio
import tools.parse as parse
ROOT.gROOT.SetBatch(True)

path ='../data/'
files = [ 'tree_ZH50', 'tree_ZH_inclusive', 'tree_ZH_MG_012j', 'tree_ZH_MG_0j','tree_ZH_powheg']
names = [ 'aMC@NLO 0-2j + Herwig', 'aMC@NLO + Herwig', 'Madgraph 0-2j + Pythia', 'Madgraph + Pythia', 'Powheg + Herwig']
colors = [2,46,4,9,8]
styles = [1,2,1,2,1]

outfile = ROOT.TFile('test.root')

vars = parse.samples('vars.cfg')

for var in vars.samples:

    opt = 'norm,e'

    c1 = ROOT.TCanvas("c1", "c1", 800, 600)

    oben = ROOT.TPad('oben','oben',0,0.3 ,1.0,1.0)
    oben.SetBottomMargin(0)
    oben.SetFillStyle(4000)
    oben.SetFrameFillStyle(1000)
    oben.SetFrameFillColor(0)
    unten = ROOT.TPad('unten','unten',0,0.0,1.0,0.3)
    unten.SetTopMargin(0.)
    unten.SetBottomMargin(0.35)
    unten.SetFillStyle(4000)
    unten.SetFrameFillStyle(1000)
    unten.SetFrameFillColor(0)

    oben.Draw()
    unten.Draw()

    oben.cd()

    if eval(var.log):
        ROOT.gPad.SetLogy()
    ROOT.gPad.SetTicks(1,1)

    l = ROOT.TLegend(0.59, 0.7,0.92,0.88)
    l.SetLineWidth(2)
    l.SetBorderSize(0)
    l.SetFillColor(0)
    l.SetFillStyle(4000)
    l.SetTextFont(62)
    ROOT.gStyle.SetOptStat(0)

    histos = []

    for i,file in enumerate(files):
        name = file.lstrip('tree_')+var.id
        _file = ROOT.TFile(path+file+'.root')
        outfile.cd()
        _tree = _file.Get('mytree')
        _tree.Draw('%s>>%s%s'%(var.var,name,var.range),"weight",opt)
        histos.append(ROOT.gDirectory.Get(name))
        histos[-1].SetTitle('')
        histos[-1].SetDirectory(0)

    for i,histo in enumerate(histos):
        histo.SetLineColor(colors[i])
        histo.SetLineStyle(styles[i])
        histo.SetLineWidth(2)
        l.AddEntry(histo,names[i],'l')

    scale = histos[0].GetMaximum()
    if eval(var.log):
        scale*=5.
    else:
        scale*=1.25
    histos[0].SetMaximum(scale)
    histos[0].Draw('hist')
    histos[0].GetXaxis().SetTitle(var.XaxisTitle)

    ratios = []

    for histo in histos:
        ratios.append(getRatio(histo,histos[0],histo.GetXaxis().GetXmin(),histo.GetXaxis().GetXmax(),"",0.05))
        histo.Draw('hist,same')
    l.Draw()

    unten.cd()

    for j,ra in enumerate(ratios):
        ratio, error = ra
        ratio.SetStats(0)
        ratio.SetLineColor(colors[j])
        ratio.SetLineStyle(styles[j])
        ratio.SetLineWidth(2)
        ratio.GetXaxis().SetTitle(var.XaxisTitle)
        if j == 0:
            ratio.Draw("hist")
        else:
            ratio.Draw("hist,same")

    c1.Print('var_plots/%s.pdf'%var.id)
