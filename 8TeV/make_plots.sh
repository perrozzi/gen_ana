rivet-mkhtml -n 16 -c ATLAS_2014_I1279489.plot -o NLO \
ATLAS_2014_I1279489.yoda \
amc.yoda:NormalizeToIntegral=1:ErrorBands=1:ErrorBandOpacity=0.2:ErrorBandColor=red:"Title=aMC@NLO + Pythia8"
rivet-mkhtml -n 16 -c ATLAS_2014_I1279489.plot -o LO \
ATLAS_2014_I1279489.yoda \
LO.yoda:NormalizeToIntegral=1:ErrorBands=1:ErrorBandOpacity=0.2:LineColor=blue:ErrorBandColor=blue:"Title=Madgraph + Pythia8"
rivet-mkhtml -n 16 -c ATLAS_2014_I1279489.plot -o Powheg \
ATLAS_2014_I1279489.yoda \
powheg_old.yoda:NormalizeToIntegral=1:ErrorBands=1:ErrorBandOpacity=0.2:LineColor=blue:ErrorBandColor=blue:"Title=Powheg + Pythia6"
rivet-mkhtml -n 16 -c ATLAS_2014_I1279489.plot -o MG \
ATLAS_2014_I1279489.yoda \
adgraph_old.yoda:NormalizeToIntegral=1:ErrorBands=1:ErrorBandOpacity=0.2:LineColor=blue:ErrorBandColor=blue:"Title=Madgraph + Pythia6"
rivet-mkhtml -n 16 -c bla -o MG-amc \
madgraph_old.yoda:NormalizeToIntegral=1:ErrorBands=1:ErrorBandOpacity=0.2:LineColor=blue:ErrorBandColor=blue:"Title=Madgraph + Pythia6" \
amc.yoda:NormalizeToIntegral=1:ErrorBands=1:ErrorBandOpacity=0.2:ErrorBandColor=red:"Title=aMC@NLO + Pythia8"
