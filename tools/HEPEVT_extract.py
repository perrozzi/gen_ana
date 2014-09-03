import sys
import ROOT
from array import array
import warnings
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='transvers momentum = 0*')

hepevt_file_name = sys.argv[1]
out_file_name = sys.argv[2]

out_file = ROOT.TFile(out_file_name,'RECREATE')
hepevt_file = open(hepevt_file_name)

particles_tree = ROOT.TTree('Particles','Particles')

particles_size = array('i',[0])
particles_tree.Branch('particles_size',particles_size,'particles_size/I')

vars = ['pt','eta','phi','mass','pdgId','status','particles_mother']
types = ['f','f','f','f','i','i','i']
ParticlesArrays = {}
for var,type in zip(vars,types):
    ParticlesArrays[var] = array(type,[0]*10000)
    particles_tree.Branch(var,ParticlesArrays[var],'particles_%s[particles_size]/%s'%(var,type.upper()))


particle = ROOT.TLorentzVector()

while True:
    line = hepevt_file.readline()
    if not line:
        break
    # new event
    n_event,n_particles = [int(x) for x in line.split()]
    # print progress
    sys.stdout.write("progress: %d   \r" % (float(n_event)) )
    sys.stdout.flush()
    particles_size[0] = n_particles
    PIDs = [0]*n_particles
    for p in xrange(n_particles):
        line = hepevt_file.readline()
        # ids
        n_particle,status,idhep,MO1,MO2,DA1,DA2 = [int(x) for x in line.split()]
        n_particle -=1
        assert p == n_particle
        PIDs[n_particle] = idhep
        Mother1 = PIDs[MO1]
        # kinematics
        line = hepevt_file.readline()
        x,y,z,e,m = [float(x) for x in line.split()]
        line = hepevt_file.readline()
        particle.SetPxPyPzE(x,y,z,e)
        ParticlesArrays['pt'][n_particle] = particle.Pt()
        ParticlesArrays['eta'][n_particle] = particle.Eta()
        ParticlesArrays['phi'][n_particle] = particle.Phi()
        ParticlesArrays['mass'][n_particle] = particle.M()
        ParticlesArrays['pdgId'][n_particle] = idhep
        ParticlesArrays['status'][n_particle] = status
        ParticlesArrays['particles_mother'][n_particle] = Mother1

    particles_tree.Fill()

print 'done!'

out_file.cd()

particles_tree.AutoSave()

hepevt_file.close()
out_file.Close()
