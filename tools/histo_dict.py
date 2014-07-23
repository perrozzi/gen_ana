import ROOT

class histo_dict(dict):
    def __init__(self,*args,**kwargs):
        super(histo_dict, self).__init__(*args, **kwargs)

    def add(self,name,*args):
        assert len(args) > 0 and len(args) < 4
        if len(args) == 1:
            self[name] = ROOT.TH1F(name,name,args[0],0,args[0])
        elif len(args) == 2:
            self[name] = ROOT.TH1F(name,name,args[1]-args[0],args[0],args[1])
        else:
            bins = round((args[1]-args[0])/args[2])
            self[name] = ROOT.TH1F(name,name,int(bins),args[0],args[1])

    def dump(self,list=None,format='pdf',prefix=''):
        c = ROOT.TCanvas('c','c',600,400)
        if not list:
            for key,histo in self.items():
                histo.Draw()
                c.SaveAs('%s%s.%s'%(prefix,key,format))
        else:
            for key in list:
                self[key].Draw()
                c.SaveAs('%s%s.%s'%(prefix,key,format))

    def write(self,list=None):
        if not list:
            for key,histo in self.items():
                histo.Write()
        else:
            for key in list:
                self[key].Write()

    def normalize(self,list=None):
        if not list:
            for key,histo in self.items():
                scale = histo.Integral()
                if not scale == 0:
                    histo.Scale(1./scale)
        else:
            for key in list:
                scale = self[key].Integral()
                if not scale == 0:
                    self[key].Scale(1./scale)

if __name__ == '__main__':
    histos = histo_dict()
    histos.add('test',10)
    histos['test'].Fill(5)
    histos.dump()
