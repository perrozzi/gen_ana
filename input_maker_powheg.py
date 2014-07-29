#!/usr/bin/env python
import ROOT
import sys
import math
from tools.progbar import progbar
import warnings
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='.*TCompare*')
import array


outfile = ROOT.TFile('../data/sparty_input_powheg.root','RECREATE')
outfile.cd()

mytree = ROOT.TTree('mytree','mytree')

# weight branch
size = array.array('i',[0])
mytree.Branch('size',size,'size/I')

pt = array.array('f',[0]*10000)
mytree.Branch('pt',pt,'pt[size]/F')
eta = array.array('f',[0]*10000)
mytree.Branch('eta',eta,'eta[size]/F')
phi = array.array('f',[0]*10000)
mytree.Branch('phi',phi,'phi[size]/F')
mass = array.array('f',[0]*10000)
mytree.Branch('mass',mass,'mass[size]/F')
pdgId = array.array('f',[0]*10000)
mytree.Branch('pdgId',pdgId,'pdgId[size]/F')


# parse filenames and open
infilename = '../data/input/ZllHbb_Powheg.root'
infile = ROOT.TFile(infilename)

particles= infile.Get('Particles')

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
    n = 0

    for p in xrange(particles.particles_size):
        # from hard interaction
        status = particles.status[p]
        if not status == 1:
            continue
        pdg = particles.pdgId[p]
        mother = particles.particles_mother[p]
        if (mother == 23 and (abs(pdg) == 11 or abs(pdg) ==13)):
            continue
        pt[n] = particles.pt[p]
        eta[n] = particles.eta[p]
        phi[n] = particles.phi[p]
        mass[n] = particles.mass[p]
        pdgId[n] = pdg
        n+=1

    size[0] = n
    mytree.Fill()


infile.Close()
    
mytree.AutoSave()
outfile.Close()

