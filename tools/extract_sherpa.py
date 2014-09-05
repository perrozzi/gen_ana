import hepmc
import ROOT

import sys
import ROOT
from array import array
import warnings
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='transvers momentum = 0*')

hepmc_file_name = sys.argv[1]
out_file_name = sys.argv[2]

out_file = ROOT.TFile(out_file_name,'RECREATE')

particles_tree = ROOT.TTree('Particles','Particles')

particles_size = array('i',[0])
particles_tree.Branch('particles_size',particles_size,'particles_size/I')

vars = ['pt','eta','phi','mass','pdgId','status','particles_mother']
types = ['f','f','f','f','i','i','i']
ParticlesArrays = {}
for var,type in zip(vars,types):
    ParticlesArrays[var] = array(type,[0]*10000)
    particles_tree.Branch(var,ParticlesArrays[var],'particles_%s[particles_size]/%s'%(var,type.upper()))


hepmc_file = hepmc.IO_GenEvent(hepmc_file_name,'r')
evtnum = 0
evt = hepmc.GenEvent()
hepmc_file.fill_next_event(evt)


#while evt.particles_size():
while evtnum < 10:
    # print progress
    sys.stdout.write("progress: %d   \r" % (float(evtnum)) )
    sys.stdout.flush()
    evtnum += 1

    vecs = []
    pdgid = []
    status = []
    v_in = []
    v_out = []
    mo = []

    particles_size[0] = evt.particles_size()

    for p in evt.particles():
        pdgid.append(p.pdg_id())
        status.append(p.status())
        vecs.append(ROOT.TLorentzVector())
        vec4 = p.to_vec4()
        vecs[-1].SetPxPyPzE(vec4.px(),vec4.py(),vec4.pz(),vec4.e())
        v = p.production_vertex()
        if v:
            v_in.append(v.barcode())
        else:
            v_in.append(0)
        e = p.end_vertex()
        if e:
            v_out.append(e.barcode())
        else:
            v_out.append(0)
 


    for v in v_in:
        idx = v_out.index(v)
        if idx:
            mo.append(pdgid[idx])
        else:
            mo.append(0)

    #for i,s in enumerate(status):
    #    if pdgid[i] ==11:
    #        if s == 3:
    #            print 'search:',vecs[i].Pt()
    #            print mo[i]
    #        else:
    #            print 'have:',vecs[i].Pt()
    #            print mo[i]

    #        #try:
    #        #    idx = [x.M() for x in vecs][:i].index(vecs[i].M())
    #        #except ValueError:
    #        #    idx = [x.M() for x in vecs][i+1:].index(vecs[i].M())
    #        #print pdgid[idx]
    #        #mo[pdgid]=23

    for i in range(particles_size[0]):
        ParticlesArrays['pt'][i] = vecs[i].Pt()
        ParticlesArrays['eta'][i] = vecs[i].Eta()
        ParticlesArrays['phi'][i] = vecs[i].Phi()
        ParticlesArrays['mass'][i] = vecs[i].M()
        ParticlesArrays['pdgId'][i] = pdgid[i]
        ParticlesArrays['status'][i] = status[i]
        ParticlesArrays['particles_mother'][i] = mo[i]

    particles_tree.Fill()

    evt.clear()
    evt = hepmc_file.get_next_event()

print 'done!'

out_file.cd()

particles_tree.AutoSave()
out_file.Close()
