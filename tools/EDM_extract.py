import sys
import ROOT
from array import array
ROOT.gSystem.Load('libFWCoreFWLite.so')
ROOT.AutoLibraryLoader.enable()
ROOT.gSystem.Load('libDataFormatsFWLite.so')
ROOT.gSystem.Load('libDataFormatsPatCandidates.so')
print 'loaded libraries'

edm_file_name = sys.argv[1]
out_file_name = sys.argv[2]

edm_file = ROOT.TFile(edm_file_name)
out_file = ROOT.TFile(out_file_name,'RECREATE')

out_file.cd()

edm_tree = edm_file.Get('Events')
ak5_tree = ROOT.TTree('AK5','AK5')
particles_tree = ROOT.TTree('Particles','Particles')

edm_ak5_size = ROOT.TTreeFormula('isize','recoGenJets_ak5GenJets__GEN.@obj.size()',edm_tree)
ak5_size = array('i',[0])
ak5_tree.Branch('ak5_size',ak5_size,'ak5_size/I')

edm_particles_size = ROOT.TTreeFormula('isize','recoGenParticles_genParticles__GEN.@obj.size()',edm_tree)
particles_size = array('i',[0])
particles_tree.Branch('particles_size',particles_size,'particles_size/I')

vars = ['pt','eta','phi','mass','pdgId','status','qx3']
types = ['f','f','f','f','i','i','i']
AK5Formulas = {}
ParticlesFormulas = {}
AK5Arrays = {}
ParticlesArrays = {}
for var,type in zip(vars,types):
    AK5Formulas[var] = ROOT.TTreeFormula('i%s'%var,'recoGenJets_ak5GenJets__GEN.obj.%s_'%var,edm_tree)
    ParticlesFormulas[var] = ROOT.TTreeFormula('i%s'%var,'recoGenParticles_genParticles__GEN.obj.%s_'%var,edm_tree)
    AK5Arrays[var] = array(type,[0]*100)
    ParticlesArrays[var] = array(type,[0]*10000)
    ak5_tree.Branch(var,AK5Arrays[var],'ak5_%s[ak5_size]/%s'%(var,type.upper()))
    particles_tree.Branch(var,ParticlesArrays[var],'particles_%s[particles_size]/%s'%(var,type.upper()))

n = edm_tree.GetEntries()
#n=100

for e in range(n):
    # print progress
    sys.stdout.write("progress: %d%%   \r" % (float(e)*100./(n)) )
    sys.stdout.flush()
    edm_tree.GetEvent(e)
    ak5_size[0] = int(edm_ak5_size.EvalInstance())
    particles_size[0] = int(edm_particles_size.EvalInstance())
    for var in vars:
        AK5Formulas[var].GetNdata()
        ParticlesFormulas[var].GetNdata()
    for i in range(ak5_size[0]):
        for var,type in zip(vars,types):
            if type == 'i':
                AK5Arrays[var][i] = int(AK5Formulas[var].EvalInstance(i))
            else:
                AK5Arrays[var][i] = AK5Formulas[var].EvalInstance(i)
    for i in range(particles_size[0]):
        for var,type in zip(vars,types):
            if type == 'i':
                ParticlesArrays[var][i] = int(ParticlesFormulas[var].EvalInstance(i))
            else:
                ParticlesArrays[var][i] = ParticlesFormulas[var].EvalInstance(i)
    ak5_tree.Fill()
    particles_tree.Fill()

print 'done!'

ak5_tree.AutoSave()
particles_tree.AutoSave()

edm_file.Close()
out_file.Close()
