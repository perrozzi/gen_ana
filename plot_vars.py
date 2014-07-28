import ROOT
from tools.Ratio import getRatio

path ='../data/'
files = [ 'tree_ZH50', 'tree_ZH_inclusive', 'tree_ZH_MG_012j', 'tree_ZH_MG_0j','tree_ZH_powheg']
names = [ 'aMC@NLO 0-2j + Herwig', 'aMC@NLO + Herwig', 'Madgraph 0-2j + Pythia', 'Madgraph + Pythia', 'Powheg + Herwig']
colors = [2,4,8,9,1]
styles = [1,2,3,4,5]

outfile = ROOT.TFile('test.root')

vars = ['Z.M()','Z.Pt()','Z.Eta()','n_aJets','aJets[0].Pt()','aJets[0].Eta()','aJets[1].Pt()','aJets[1].Eta()','H.Pt()','H.M()','H.Eta()','genH.Pt()','genH.M()','genH.Eta()']
ranges = ['(50,40,140)','(50,0,250)','(50,-5,5)','(10,0,10)','(50,0,250)','(50,-5,5)','(50,0,250)','(50,-5,5)','(50,0,250)','(50,75,175)','(50,-5,5)','(50,0,250)','(40,124.5,125.5)','(50,-5,5)']
var_names = ['mass(Z) (GeV)','p_{T}(Z) (GeV)','Eta(Z)','#(additional jets)','p_{T}(leading jet) (GeV)','Eta(leading jet)','p_{T}(second jet) (GeV)','Eta(second jet)','P_{T}(H(jj)) (GeV)','mass(H(jj)) (GeV)','Eta(H(jj))','P_{T}(H) (GeV)','mass(H) (GeV)','Eta(H)']

for var,range,var_name in zip(vars,ranges,var_names):

    opt = 'norm'

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
        name = file.lstrip('tree_')
        _file = ROOT.TFile(path+file+'.root')
        outfile.cd()
        _tree = _file.Get('mytree')
        _tree.Draw('%s>>%s%s'%(var,name,range),"weight",opt)
        histos.append(ROOT.gDirectory.Get(name))
        histos[-1].SetTitle('')
        histos[-1].SetDirectory(0)

    for i,histo in enumerate(histos):
        histo.SetLineColor(colors[i])
        histo.SetLineStyle(styles[i])
        histo.SetLineWidth(2)
        l.AddEntry(histo,names[i],'l')

    histos[0].Draw('')
    histos[0].GetXaxis().SetTitle(var_name)

    ratios = []

    for histo in histos:
        ratios.append(getRatio(histos[0],histo,histo.GetXaxis().GetXmin(),histo.GetXaxis().GetXmax(),"",10))
        histo.Draw('same')
    l.Draw()

    unten.cd()

    for j,ra in enumerate(ratios):
        ratio, error = ra
        ratio.SetStats(0)
        ratio.SetLineColor(colors[j])
        ratio.SetLineStyle(styles[j])
        ratio.SetLineWidth(2)
        ratio.GetXaxis().SetTitle(var_name)
        ratio.GetXaxis().SetTitle('Ratio')
        if j == 0:
            ratio.Draw("hist")
        else:
            ratio.Draw("hist,same")

    f_name = var
    for char in '()[].':
        f_name = f_name.replace(char,'')
    print f_name
    c1.Print('var_plots/%s.pdf'%f_name)
