BR=1.733
rivet-mkhtml \
ZH_merged_norm.yoda:"Title:aMC@NLO 0,1,2j + Herwig6, FxFx 50 GeV" \
ZH_inclusive_norm.yoda:"Title:aMC@NLO 0j + Herwig6" \
aMC_pythia_50_norm.aida:Scale=$BR:"Title:aMC@NLO 0,1j + Pyhtia8, FxFx 50 GeV" \
aMC_pythia_0j_norm.aida:Scale=$BR:"Title:aMC@NLO 0j + Pyhtia8" \
Sherpa_norm.yoda:"Title:Sherpa-MC@NLO 0j" \
Sherpa_LOPS.yoda:"Title:Sherpa LOPS" \
-c config.plot -n 16 -o all
rivet-mkhtml \
aMC_pythia_30_norm.aida:Scale=$BR:"Title:aMC@NLO 0,1j + Pyhtia8, FxFx 30 GeV" \
aMC_pythia_50_norm.aida:Scale=$BR:"Title:aMC@NLO 0,1j + Pyhtia8, FxFx 50 GeV" \
aMC_pythia_70_norm.aida:Scale=$BR:"Title:aMC@NLO 0,1j + Pyhtia8, FxFx 70 GeV" \
-c config.plot -n 16 -o merge_pythia
rivet-mkhtml \
ZH_merged_norm.yoda:"Title:aMC@NLO 0,1,2j + Herwig6, FxFx 50 GeV" \
ZH_norm.yoda:"Title aMC@NLO 0j" \
ZHj_norm.yoda:"Title aMC@NLO 1j" \
ZHjj_norm.yoda:"Title aMC@NLO 2j" \
-c config.plot -n 16 -o merge_herwig
rivet-mkhtml \
