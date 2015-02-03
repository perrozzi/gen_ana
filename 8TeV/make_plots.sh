rivet-mkhtml -n 16 -c ATLAS_2014_I1279489.plot -o NLO \
ATLAS_2014_I1279489.yoda \
AMC_py8_resubmit.yoda:NormalizeToIntegral=1:ErrorBands=1:ErrorBandOpacity=0.2:ErrorBandColor=red:"Title=aMC@NLO + Pythia8"

rivet-mkhtml -n 16 -c ATLAS_2014_I1279489.plot -o LO \
ATLAS_2014_I1279489.yoda \
MG_py8_resubmit.yoda:NormalizeToIntegral=1:ErrorBands=1:ErrorBandOpacity=0.2:LineColor=blue:ErrorBandColor=blue:"Title=Madgraph + Pythia8"

rivet-mkhtml -n 16 -c ATLAS_2014_I1279489.plot -o Powheg \
ATLAS_2014_I1279489.yoda \
Powheg_resubmit.yoda:NormalizeToIntegral=1:ErrorBands=1:ErrorBandOpacity=0.2:LineColor=blue:ErrorBandColor=blue:"Title=Powheg + Pythia6"

rivet-mkhtml -n 16 -c ATLAS_2014_I1279489.plot -o MG \
ATLAS_2014_I1279489.yoda \
madgraph_old.yoda:NormalizeToIntegral=1:ErrorBands=1:ErrorBandOpacity=0.2:LineColor=blue:ErrorBandColor=blue:"Title=Madgraph + Pythia6"

rivet-mkhtml -n 16 -o all \
AMC_py8_resubmit.yoda:NormalizeToIntegral=1:ErrorBands=1:ErrorBandOpacity=0.2:ErrorBandColor=red:"Title=aMC@NLO + Pythia8" \
MG_py8_resubmit.yoda:NormalizeToIntegral=1:ErrorBands=1:ErrorBandOpacity=0.2:LineColor=blue:ErrorBandColor=blue:"Title=Madgraph + Pythia8" \
madgraph_old.yoda:NormalizeToIntegral=1:ErrorBands=1:ErrorBandOpacity=0.2:LineColor=green:ErrorBandColor=green:"Title=Madgraph + Pythia6" \
powheg_old.yoda:NormalizeToIntegral=1:ErrorBands=1:ErrorBandOpacity=0.2:LineColor=orange:ErrorBandColor=orange:"Title=Powheg + Pythia6"

rivet-mkhtml -n 16 -c Paladini.plot -o paladini \
Paladini.yoda \
AMC_py8_resubmit.yoda:Scale=0.0000086:ErrorBands=1:ErrorBandOpacity=0.2:ErrorBandColor=red:"Title=aMC@NLO + Pythia8" \
MG_py8_resubmit.yoda:Scale=0.082:ErrorBands=1:ErrorBandOpacity=0.2:LineColor=blue:ErrorBandColor=blue:"Title=Madgraph + Pythia8" \
MG_py6_resubmit.yoda:Scale=0.065:ErrorBands=1:ErrorBandOpacity=0.2:LineColor=green:ErrorBandColor=green:"Title=Madgraph + Pythia6" \
Powheg_resubmit.yoda:Scale=0.056:ErrorBands=1:ErrorBandOpacity=0.2:LineColor=orange:ErrorBandColor=orange:"Title=Powheg + Pythia6"
