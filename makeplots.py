import ROOT
from tools.Ratio import getRatio

filenames = ['/shome/peller/Madgraph/MG5_aMC_v2_1_0_cutsMod/ZH_inclusive/Events/run_05/Rivet.root',
             '/shome/peller/Madgraph/MG5_aMC_v2_1_0_cutsMod/ZH/Events/run_03/Rivet.root',
             '/shome/peller/Madgraph/MG5_aMC_v2_1_0_cutsMod/ZHj/Events/run_02/Rivet.root',
             '/shome/peller/Madgraph/MG5_aMC_v2_1_0_cutsMod/ZHjj/Events/run_03/Rivet.root']
names = ['ZH 0j inc.','ZH 0j','ZH 1j','ZH 2j','ZH 0,1,2j merged']
vars = ['log10_d_01',
        'log10_d_12',
        'log10_d_23',
        'log10_d_34',
        'log10_R_0',
        'log10_R_1',
        'log10_R_2',
        'log10_R_3',
        'log10_R_4']
var_names = ['log_{10}(d_{01})',
             'log_{10}(d_{12})',
             'log_{10}(d_{23})',
             'log_{10}(d_{34})',
             'log_{10}(R_{0})',
             'log_{10}(R_{1})',
             'log_{10}(R_{2})',
             'log_{10}(R_{3})',
             'log_{10}(R_{4})']


colors = [6,2,3,4]
styles = [7,2,3,4]
linewidth = 1

for var,var_name in zip(vars,var_names):

    histos = []

    c1 = ROOT.TCanvas("c1", "c1", 300, 250)
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

    ROOT.gPad.SetLogy()
    ROOT.gPad.SetTicks(1,1)
    ROOT.gStyle.SetOptStat(0)

    tot = None
    def make_legend():
            l = ROOT.TLegend(0.59, 0.67,0.95,0.85)
            l.SetLineWidth(1)
            l.SetBorderSize(0)
            l.SetFillColor(0)
            l.SetFillStyle(4000)
            l.SetTextFont(62)
            return l

    l = make_legend()

    for i,filename in enumerate(filenames):
        file = ROOT.TFile(filename)
        histos.append(file.Get(var))
        histos[-1].SetDirectory(0)
        l.AddEntry(histos[-1],names[i],'l')
        histos[-1].SetLineStyle(styles[i])
        if i == 1:
           tot = histos[-1].Clone('tot')
           tot.SetDirectory(0)
        if i > 1:
            tot.Add(histos[-1])
        histos[-1].SetLineColor(colors[i])
        histos[-1].SetLineWidth(linewidth)
        histos[-1].GetXaxis().SetTitle(var_name)
        opt = 'hist'
        if i > 0:
            opt += 'same'
        histos[-1].Draw(opt)
    tot.SetLineColor(1)
    tot.SetLineWidth(linewidth)
    tot.SetLineStyle(1)
    l.AddEntry(tot,names[4],'l')
    tot.Draw('hist,same')
    l.Draw()

    ratios = []

    for histo in histos:
        ratios.append(getRatio(histo,tot,histo.GetXaxis().GetXmin(),histo.GetXaxis().GetXmax(),"",0.03))

    unten.cd()

    for j,ra in enumerate(ratios):
        ratio, error = ra
        ratio.SetStats(0)
        ratio.SetLineColor(colors[j])
        ratio.SetLineStyle(styles[j])
        ratio.SetLineWidth(linewidth)
        ratio.GetXaxis().SetTitle(var_name)
        if j == 0:
            ratio.Draw("hist")
        else:
            ratio.Draw("hist,same")


    c1.Update()
    c1.Print(var+'.pdf')
