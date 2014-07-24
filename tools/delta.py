import ROOT
import math

def deltaRpT(vec1,vec2):
    dEta = vec1.Eta() - vec2.Eta()
    dPhi = ROOT.TVector2.Phi_mpi_pi(vec1.Phi() - vec2.Phi())
    dPt = vec1.Pt() - vec2.Pt()
    return math.sqrt(dEta*dEta + dPhi*dPhi + dPt*dPt)

def deltaR(vec1,vec2):
    return vec1.DeltaR(vec2)
