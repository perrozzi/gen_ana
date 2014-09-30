#!/usr/bin/env python
import ROOT
from tools.Ratio import getRatio
import tools.parse as parse
ROOT.gROOT.SetBatch(True)
from array import array
from optparse import OptionParser
import sys, os

argv = sys.argv
parser = OptionParser()
parser.add_option("-V", "--var", dest="var", default="all",
        help="Variable to plot, default:all")
parser.add_option("-C", "--conf", dest="conf", default="vars.cfg",
        help="plot variables config")

(opts, args) = parser.parse_args(argv)

path ='../data/'
#files = [ 'tree_ZH50', 'tree_ZH_inclusive', 'tree_ZH_MG_012j', 'tree_ZH_MG_0j','tree_ZH_powheg','tree_ZH_sherpa']
files = [ 'tree_ZH50', 'tree_ZH_inclusive', 'tree_ZH_MG_012j', 'tree_ZH_MG_0j','tree_ZH_powheg_PU','tree_ZH_sherpa']
names = [ 'aMC@NLO FxFx(0-2j) + Herwig', 'aMC@NLO + Herwig', 'Madgraph MLM(0-2j) + Pythia', 'Madgraph + Pythia', 'Powheg + Herwig','Sherpa (AMEGIC+OpenLoops)']
colors = [98,98,9,9,8,15]
styles = [1,2,1,2,1,1]

norm = [
        0.0478840946816,
        0.0497891290506,
        0.0140102168962,
        0.022549493317,
        19531.0,
        99414.0
        ]
# Powheg PU: 19531.0
# Powheg:    33292.0

outfile = ROOT.TFile('test.root')

vars = parse.samples(opts.conf)

def fix_pdf(filename):
    os.system('pdf2ps %s %sps'%(filename,filename.rstrip('pdf')))
    os.system('ps2pdf %sps %s'%(filename.rstrip('pdf'),filename))
    os.system('rm %sps'%filename.rstrip('pdf'))
    os.system('pdfcrop %s %s --margins "20 20 20 20"'%(filename,filename))

def make_legend():
        l = ROOT.TLegend(0.59, 0.67,0.92,0.88)
        l.SetLineWidth(2)
        l.SetBorderSize(0)
        l.SetFillColor(0)
        l.SetFillStyle(4000)
        l.SetTextFont(62)
        return l

def set_palette(name='palette', ncontours=999):
    """Set a color palette from a given RGB list
    stops, red, green and blue should all be lists of the same length
    see set_decent_colors for an example"""

    if name == "gray" or name == "grayscale":
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [1.00, 0.84, 0.61, 0.34, 0.00]
        green = [1.00, 0.84, 0.61, 0.34, 0.00]
        blue  = [1.00, 0.84, 0.61, 0.34, 0.00]
    # elif name == "whatever":
        # (define more palettes)
    else:
        # default palette, looks cool
        stops = [0.00, 0.34, 0.61, 0.84, 1.00]
        red   = [0.00, 0.00, 0.87, 1.00, 0.51]
        green = [0.00, 0.81, 1.00, 0.20, 0.00]
        blue  = [0.51, 1.00, 0.12, 0.00, 0.00]

    s = array('d', stops)
    r = array('d', red)
    g = array('d', green)
    b = array('d', blue)

    npoints = len(s)
    ROOT.TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
    ROOT.gStyle.SetNumberContours(ncontours)

for var in vars.samples:

    if not opts.var == 'all':
        if not var.id == opts.var:
            continue

    if hasattr(var, 'var2'):
        
        set_palette()
        cut = '1'
        opt = ''


        for i,file in enumerate(files):
            c1 = ROOT.TCanvas("c1", "c1", 800, 600)
            c1.SetFillStyle(4000)
            c1.SetFrameFillStyle(1000)
            c1.SetFrameFillColor(0)
            ROOT.gStyle.SetOptStat(0)
            name = file.lstrip('tree_')+var.id
            _file = ROOT.TFile(path+file+'.root')
            outfile.cd()
            _tree = _file.Get('mytree')
            _tree.Draw('%s:%s>>%s%s'%(var.var2,var.var,name,var.range),"weight*(%s)"%cut,opt)
            histo = ROOT.gDirectory.Get(name)
            histo.SetTitle('')
            histo.SetDirectory(0)
            _file.Close()
            histo.Draw('COLZ')
            histo.GetXaxis().SetTitle(var.XaxisTitle)
            histo.GetYaxis().SetTitle(var.YaxisTitle)
            filename = 'var_plots/%s_%s.pdf'%(var.id,file)
            c1.Print(filename)
            fix_pdf(filename)

    else:
        opt = 'e'
        cut = '1'
        cut = 'Z.Pt() > 100. && Z.M() > 76. && Z.M() < 106. &&  h_dau[0].Pt() > 20. &&  h_dau[1].Pt() > 20.  && z_dau[0].Pt() > 20. && z_dau[1].Pt() > 20. && dR[0] < 0.3 && dR[1] < 0.3 && abs(h_dau[0].Eta()) < 2.5 && abs(h_dau[1].Eta()) < 2.5 && abs(z_dau[0].Eta()) < 2.5 && abs(z_dau[1].Eta()) < 2.5'
        #cut = 'dR[0] < 0.2 && dR[1] < 0.3'
        #"abs(aJets[1].Eta())<2.5 && abs(aJets[2].Eta())<2.5 && abs(aJets[3].Eta())<2.5"

        c1 = ROOT.TCanvas("c1", "c1", 800, 600)
        c1.SetFillStyle(4000)
        c1.SetFrameFillStyle(1000)
        c1.SetFrameFillColor(0)

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

        l = make_legend()
        ROOT.gStyle.SetOptStat(0)

        histos = []


        for i,file in enumerate(files):
            name = file.lstrip('tree_')+var.id
            _file = ROOT.TFile(path+file+'.root')
            outfile.cd()
            _tree = _file.Get('mytree')
            _tree.Draw('%s>>%s%s'%(var.var,name,var.range),"weight*(%s)"%cut,opt)
            histos.append(ROOT.gDirectory.Get(name))
            histos[-1].Scale(1./norm[i])
            #print file, ' Integral: %s'%histos[-1].Integral()
            histos[-1].SetTitle('')
            histos[-1].SetDirectory(0)
            _file.Close()

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
            ratios.append(getRatio(histo,histos[0],histo.GetXaxis().GetXmin(),histo.GetXaxis().GetXmax(),"",0.03))
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

        filename = 'var_plots/%s.pdf'%var.id
        c1.Print(filename)
        fix_pdf(filename)
