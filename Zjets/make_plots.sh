rivet-mkhtml -n 16 -c plot.conf -o ATLAS \
ATLAS_2013_I1230812.yoda \
powheg/ATLAS.yoda:Scale=0.0097:ErrorBandColor=red:"Title=Powheg + Pythia8" \
NLO_5f/ATLAS.yoda:Scale=0.022:ErrorBandColor=blue:"Title=aMC@NLO + Pythia8" \
LO_5f/ATLAS.yoda:Scale=0.014:ErrorBandColor=green:"Title=MG + Pythia8"
#LO_5f/ATLASold.yoda:Scale=0.014:ErrorBandColor=orange:"Title=MG + Pythia8 old"

rivet-mkhtml -n 16 -c CMS_2013_I1258128.plot -o CMS2 \
CMS_2013_I1258128.yoda \
powheg/CMS2.yoda:ErrorBands=1:ErrorBandOpacity=0.2:ErrorBandColor=red:"Title=Powheg + Pythia8" \
NLO_5f/CMS2.yoda:ErrorBands=1:ErrorBandOpacity=0.2:ErrorBandColor=blue:"Title=aMC@NLO + Pythia8" \
LO_5f/CMS2.yoda:ErrorBands=1:ErrorBandOpacity=0.2:ErrorBandColor=green:"Title=MG + Pythia8"
#LO_5f/CMS2old.yoda:ErrorBands=1:ErrorBandOpacity=0.2:ErrorBandColor=orange:"Title=MG + Pythia8 old"

rivet-mkhtml -n 16 -c plot.conf -o CMS3 \
CMS_2013_I1209721_fix.yoda \
powheg/CMS3.yoda:NormalizeToIntegral=1:ErrorBandColor=red:"Title=Powheg + Pythia8" \
NLO_5f/CMS3.yoda:NormalizeToIntegral=1:ErrorBandColor=blue:"Title=aMC@NLO + Pythia8" \
LO_5f/CMS3.yoda:NormalizeToIntegral=1:ErrorBandColor=green:"Title=MG + Pythia8"
#LO_5f/CMS3old.yoda:NormalizeToIntegral=1:ErrorBandColor=orange:"Title=MG + Pythia8 old"

#rivet-mkhtml -n 16 -c plot.conf -o SMP \
#CMS_SMP_12_017.yoda \
#LO_5f/CMS1.yoda:Scale=1.27:ErrorBandColor=green:"Title=MG + Pythia8"
#NLO_5f/CMS1.yoda:Scale=1.27:ErrorBandColor=blue:"Title=aMC@NLO + Pythia8" \

#rivet-mkhtml -n 16 -c plot.conf -o MC \
#LO_5f/MC.yoda:Scale=1.27:ErrorBandColor=green:"Title=MG + Pythia8"
#NLO_5f/MC.yoda:Scale=1.27:ErrorBandColor=blue:"Title=aMC@NLO + Pythia8" \
