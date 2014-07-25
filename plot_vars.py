import ROOT

path ='../data/'
files = [ 'tree_ZH50', 'tree_ZH_inclusive', 'tree_ZH_MG_012j', 'tree_ZH_MG_0j','tree_ZH_powheg']
names = [ 'aMC@NLO 0-2j + Herwig', 'aMC@NLO + Herwig', 'Madgraph 0-2j + Pythia', 'Madgraph + Pythia', 'Powheg + Herwig']
colors = [2,4,8,9,1]
styles = [1,2,3,4,5]

outfile = ROOT.TFile('test.root')

vars = ['Z.M()','Z.Pt()','Z.Eta()','n_aJets','aJets[0].Pt()']
ranges = ['(50,40,140)','(50,0,250)','(50,-5,5)','(10,0,10)','(50,0,250)']
var_names = ['mass(Z) (GeV)','p_{T}(Z) (GeV)','Eta(Z)','#(additional jets)','p_{T}(leading jet) (GeV)']

for var,range,var_name in zip(vars,ranges,var_names):

    opt = 'norm'

    c1 = ROOT.TCanvas("c1", "c1", 800, 600)
    c1.SetLogy()
    ROOT.gPad.SetTicks(1,1)

    l = ROOT.TLegend(0.55, 0.7,0.88,0.88)
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
    for histo in histos[1:]:
        histo.Draw('same')
    l.Draw()
    f_name = var
    for char in '()[].':
        f_name = f_name.replace(char,'')
    print f_name
    c1.Print('var_plots/%s.pdf'%f_name)
