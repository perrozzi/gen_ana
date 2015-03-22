XSECBR=0.0336
XSEC=0.0583
#rivet-mkhtml \
#powheg_HZ_inc.aida:Scale=$XSEC:"Title:Powheg HZ + Pythia8" \
#powheg_HZJ_inc.aida:Scale=$XSEC:"Title:Powheg HZJ + Pythia8" \
#amc_pythia_inc.aida:Scale=$XSEC:"Title:aMC@NLO 0,1j + Pyhtia8" \
#aMC_pythia_0j_norm.aida:Scale=$XSEC:"Title:aMC@NLO 0j + Pyhtia8" \
#ZH_merged_norm.yoda:Scale=$XSECBR:"Title:aMC@NLO 0,1,2j + Herwig6" \
#ZH_inclusive_norm.yoda:Scale=$XSECBR:"Title:aMC@NLO 0j + Herwig6" \
#Sherpa_Hll_inc.yoda:Scale=0.08:"Title:Sherpa-MC@NLO 0j" \
#Sherpa_012j.yoda:Scale=$XSECBR:"Title:Sherpa-MC@NLO 0,1,2j" \
#Sherpa_LOPS.yoda:Scale=$XSECBR:"Title:Sherpa LO+PS" \
#--mc-errs -c config.plot -n 16 -o all
#rivet-mkhtml --mc-errs -c config.plot -n 16 \
#powheg_HZ_inc.aida:Scale=$XSEC:ErrorBandColor=red:"Title:Powheg HZ + Pythia8" \
#powheg_HZJ_inc.aida:Scale=$XSEC:ErrorBandColor=red:"Title:Powheg HZJ + Pythia8" \
#amc_pythia_inc.aida:Scale=$XSEC:ErrorBandColor=red:"Title:aMC@NLO + Pyhtia8" \
#ZH_merged_norm.yoda:Scale=$XSECBR:"Title:aMC@NLO + Herwig6" \
#Sherpa_multijet_inc.yoda:Scale=0.00176:"Title:Sherpa MEPS@NLO" \
#Sherpa_multijet_inc_noMPI.yoda:Scale=0.000176:"Title:Sherpa no UE" \
#-o inc
rivet-mkhtml \
powheg_HZ_sel.aida:Scale=$XSEC:"Title:Powheg HZ + Pythia8" \
powheg_HZJ_sel.aida:Scale=$XSEC:"Title:Powheg HZJ + Pythia8" \
amc_pythia_sel.aida:Scale=$XSEC:"Title:aMC@NLO 0,1j + Pyhtia8" \
Sherpa_multijet_sel.yoda:Scale=0.00176:"Title:Sherpa MEPS@NLO" \
--mc-errs -c sel.plot -n 16 -o sel
#rivet-mkhtml \
#powheg_HZ_sel.aida:Scale=$XSEC:"Title:Powheg HZ + Pythia8" \
#powheg_HZJ_sel.aida:Scale=$XSEC:"Title:Powheg HZJ + Pythia8" \
#amc_pythia_sel.aida:Scale=$XSEC:"Title:aMC@NLO 0,1j + Pyhtia8" \
#aMC_pythia_0j_sel.aida:Scale=$XSEC:"Title:aMC@NLO 0j + Pyhtia8" \
#ZH_merged_sel.yoda:Scale=$XSECBR:"Title:aMC@NLO 0,1,2j + Herwig6" \
#ZH_inclusive_sel.yoda:Scale=$XSECBR:"Title:aMC@NLO 0j + Herwig6" \
#Sherpa_Hll_sel.yoda:Scale=0.0022:"Title:Sherpa-MC@NLO 0j" \
#Sherpa_LOPS_sel.yoda:Scale=$XSECBR:"Title:Sherpa LO+PS" \
#Sherpa_012j_sel.yoda:Scale=$XSECBR:"Title:Sherpa-MC@NLO 0,1,2j" \
#--mc-errs -c sel.plot -n 16 -o selall
#rivet-mkhtml \
#Sherpa_norm.yoda:"Title:Sherpa-MC@NLO 0j" \
#Sherpa_LOPS.yoda:"Title:Sherpa LO+PS" \
#Sherpa_LOPS_tautau_mcbb.yoda:Scale=45:"Title:Sherpa LO+PS tautau" \
#-c config.plot -n 16 -o bb_tautau
#rivet-mkhtml \
#Sherpa_norm.yoda:"Title:Sherpa-MC@NLO 0j" \
#aMC_pythia_50_norm.aida:Scale=$XSEC:"Title:aMC@NLO 0,1j + Pyhtia8" \
#aMC_pythia_0j_norm.aida:Scale=$XSEC:"Title:aMC@NLO 0j + Pyhtia8" \
#Sherpa_LOPS.yoda:"Title:Sherpa LO+PS" \
#Sherpa_LOPS_VAR.yoda:"Title:Sherpa LO+PS var scales" \
#-c config.plot -n 16 -o sherpa_pythia
#rivet-mkhtml \
#aMC_pythia_50_norm.aida:Scale=$XSEC:"Title:aMC@NLO + Pyhtia8, FxFx 50 GeV" \
#aMC_pythia_30_norm.aida:Scale=$XSEC:"Title:aMC@NLO + Pyhtia8, FxFx 30 GeV" \
#aMC_pythia_70_norm.aida:Scale=$XSEC:"Title:aMC@NLO + Pyhtia8, FxFx 70 GeV" \
#-c config.plot -n 16 -o merge_pythia
#rivet-mkhtml \
#ZH_merged_norm.yoda:"Title:FxFx merged at 50 GeV" \
#ZH_norm.yoda:"Title:aMC@NLO 0j + Herwig 6" \
#ZHj_norm.yoda:"Title:aMC@NLO 1j + Herwig 6" \
#ZHjj_norm.yoda:"Title:aMC@NLO 2j + Herwig 6" \
#-c config.plot -n 16 -o merge_herwig
#rivet-mkhtml \
