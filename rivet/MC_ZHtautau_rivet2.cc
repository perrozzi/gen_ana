// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Analyses/MC_JetAnalysis.hh"
#include "Rivet/Projections/ZFinder.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/VetoedFinalState.hh"

namespace Rivet {

  using namespace Cuts;

  class MC_ZHtautau : public Analysis {
  public:

    /// Constructor
    MC_ZHtautau()
      : Analysis("MC_ZHtautau")
    {    
    }

    /// Book histograms and initialise projections before the run
    void init() {

        Cut cut = etaIn(-5,5) & (pT >= 0.0*GeV);

        // # of jets for the jet ana
        njets = 4;

        // initialise projections
        FinalState fs;
        addProjection(fs, "fs");
        // find Higgs
        ZFinder hfinder(fs, cut, PID::TAU, 50*GeV, 200*GeV, 0.0, ZFinder::NOCLUSTER);
        addProjection(hfinder, "hfinder");
        // fish out higgs
        VetoedFinalState zeeinput;
        zeeinput.addVetoOnThisFinalState(hfinder);
        // find Zee
        ZFinder zeefinder(zeeinput, cut, PID::ELECTRON, 65*GeV, 115*GeV, 0.2);
        addProjection(zeefinder, "zeefinder");
        // fish out Zee and higgs
        VetoedFinalState zmminput;
        zmminput.addVetoOnThisFinalState(hfinder);
        zmminput.addVetoOnThisFinalState(zeefinder);
        // find Zmm
        ZFinder zmmfinder(zmminput, cut, PID::MUON, 65*GeV, 115*GeV, 0.2);
        addProjection(zmmfinder, "zmmfinder");
        // fish out Zee and Zmm and higgs
        VetoedFinalState jetproinput;
        jetproinput.addVetoOnThisFinalState(zeefinder);
        jetproinput.addVetoOnThisFinalState(zmmfinder);
        jetproinput.addVetoOnThisFinalState(hfinder);
        // make jets
        FastJets jetpro(jetproinput, FastJets::ANTIKT, 0.5);
        addProjection(jetpro, "jetpro");
        // jets for differential jet rates
        FastJets jetpro_kt(jetproinput, FastJets::KT, 0.7);
        addProjection(jetpro_kt, "jetpro_kt");


        // ---- HISTOS ----
        int nbins =100;

        // jets
        for (size_t i=0; i < njets; ++i) {
            string dname = "log10_d_" +to_str(i) + to_str(i+1);
            _h_log10_d.push_back(bookHisto1D(dname, nbins, 0.2, 4));
            dname = "aJet_pT" +to_str(i);
            _h_ajets_pT.push_back(bookHisto1D(dname,logspace(nbins,5,300)));
            dname = "aJet_eta" +to_str(i);
            _h_ajets_eta.push_back(bookHisto1D(dname,nbins,-5,5));
        }

        // Z properties
        _h_Z_mass = bookHisto1D("Z_mass",nbins,51,131);
        _h_Z_eta = bookHisto1D("Z_eta",nbins,-5,5);
        _h_Z_pT = bookHisto1D("Z_pT",logspace(nbins,5,300));

        // dijet properties
        _h_dijet_mass = bookHisto1D("dijet_mass",nbins,60,140);
        _h_dijet_eta = bookHisto1D("dijet_eta",nbins,-5,5);
        _h_dijet_pT = bookHisto1D("dijet_pT",logspace(nbins,5,300));

        // H+Z properties
        _h_HZ_eta = bookHisto1D("HZ_eta",nbins,-5,5);
        _h_HZ_pT = bookHisto1D("HZ_pT",logspace(nbins,5,300));

        // higgs jets
        for (size_t i=0; i < 2; ++i) {
            string dname = "h_dau_eta" + to_str(i);
            _h_dau_eta.push_back(bookHisto1D(dname,nbins,-5,5));
            dname = "h_dau_pT" + to_str(i);
            _h_dau_pT.push_back(bookHisto1D(dname,logspace(nbins,5,300)));
        }

        // angles
        _h_dR_jj = bookHisto1D("dR_jj",nbins,0,5);
        _h_dphi_jj = bookHisto1D("dphi_jj",nbins,0,3.2);
        _h_deta_jj = bookHisto1D("deta_jj", nbins,0,5);

        _h_dR_HZ = bookHisto1D("dR_HZ",nbins,0,5);
        _h_dphi_HZ = bookHisto1D("dphi_HZ",nbins,0,3.2);
        _h_deta_HZ = bookHisto1D("deta_HZ", nbins,0,5);
        
        // nJets
        _h_najets = bookHisto1D("najets",10,0,10);
        _h_nbjets = bookHisto1D("nbjets",10,0,10);


    }

    /// Perform the per-event analysis
    void analyze(const Event& event) {
        const double weight = event.weight();

        double jets_pt_cut = 20.0*GeV;

        // apply the projections
        const ZFinder& hfinder = applyProjection<ZFinder>(event, "hfinder");
        const ZFinder& zeefinder = applyProjection<ZFinder>(event, "zeefinder");
        const ZFinder& zmmfinder = applyProjection<ZFinder>(event, "zmmfinder");
        const Particles zll = zeefinder.bosons() + zmmfinder.bosons();
        const FastJets& jetpro = applyProjection<FastJets>(event,"jetpro");
        const FastJets& jetpro_kt = applyProjection<FastJets>(event,"jetpro_kt");
        const Jets alljets = jetpro.jetsByPt();

        Log& log = getLog();
       
        // only continue if a Z has been found
        if (zll.empty()) {
            vetoEvent;
            log << Log::DEBUG << "veto: no Z(ll) found" << std::endl;
        }
        // not 1 higgs -> veto
        if (hfinder.bosons().size() != 1) {
            vetoEvent;
            log << Log::DEBUG << "veto: n Higgs = " << hfinder.bosons().size() << std::endl;
        }

        log << Log::DEBUG << "products found" << std::endl;

        Jets ajets;
        ajets.clear();
        //Jet h0, h1; 
        FourMomentum  dijet,Z, HZ;
        std::vector<size_t> b_indices;
        int na = 0.0;
        int nb = 0.0;

        // find all jets with bs
        for (size_t i = 0; i < alljets.size(); ++i) {
            if (alljets[i].containsBottom()) {
                b_indices.push_back(i);
                if (alljets[i].pT() > jets_pt_cut) nb++;
            }
        }

        // require at least to b jets
        //if (b_indices.size() < 2) vetoEvent;

        // construct highest dijet pt b-jet pair
        //double max_pt = 0.0*GeV;
        //size_t idx0 = 0;
        //size_t idx1 = 0;
        // pairwise iterate
        //for (size_t i = 0; i < b_indices.size()-1; ++i) {
        //    for (size_t j = i+1; j < b_indices.size(); ++j) {
        //        dijet = alljets[b_indices[i]].momentum() + alljets[b_indices[j]].momentum();
        //        if (dijet.pT() > max_pt) {
        //            max_pt = dijet.pT();
        //            idx0 = b_indices[i];
        //            idx1 = b_indices[j];
        //            }
        //        }
        //    }

        //h0 = alljets[idx0];
        //h1 = alljets[idx1];
        // final highest pt dijet pair
        dijet = hfinder.bosons()[0].momentum();
        
        Z = zll[0].momentum();

        // HZ system
        HZ = dijet + Z;
        
        // add everything else to the ajets 
        for (size_t i = 0; i < alljets.size(); ++i) {
            //if (i != idx0 && i != idx1){
            ajets.push_back(alljets[i]);
            if (alljets[i].pT() > jets_pt_cut) na++;
            //}
        }

        // fill histos
        //_h_dau_eta[0]->fill(h0.eta(),weight);
        //_h_dau_eta[1]->fill(h1.eta(),weight);
        //_h_dau_pT[0]->fill(h0.pT(),weight);
        //_h_dau_pT[1]->fill(h1.pT(),weight);

        _h_Z_mass->fill(Z.mass(),weight);
        _h_Z_eta->fill(Z.eta(),weight);
        _h_Z_pT->fill(Z.pT(),weight);

        _h_dijet_mass->fill(dijet.mass(),weight);
        _h_dijet_eta->fill(dijet.eta(),weight);
        _h_dijet_pT->fill(dijet.pT(),weight);

        _h_HZ_eta->fill(HZ.eta(),weight);
        _h_HZ_pT->fill(HZ.pT(),weight);

        _h_najets->fill(na,weight);
        _h_nbjets->fill(nb,weight);

        //_h_dR_jj->fill(deltaR(h0,h1),weight);
        //_h_deta_jj->fill(deltaEta(h0,h1),weight);
        //_h_dphi_jj->fill(deltaPhi(h0,h1),weight);

        _h_dR_HZ->fill(deltaR(dijet,Z),weight);
        _h_deta_HZ->fill(deltaEta(dijet,Z),weight);
        _h_dphi_HZ->fill(deltaPhi(dijet,Z),weight);

        // Jet resolutions and integrated jet rates
        double d_ij;
        const fastjet::ClusterSequence* seq = jetpro_kt.clusterSeq();
        if (seq != NULL) {
            for (size_t i = 0; i < njets; ++i) {
                 // Jet resolution i -> j
                 d_ij = log10(sqrt(seq->exclusive_dmerge_max(i)));

                // Fill differential jet resolution
                _h_log10_d[i]->fill(d_ij, weight);

                //fill aJet pT histos
                _h_ajets_pT[i]->fill(ajets[i].pT(),weight);
                _h_ajets_eta[i]->fill(ajets[i].eta(),weight);
            }
        }
    }


    /// Normalise histograms etc., after the run
    void finalize() {

        for (size_t i = 0; i < njets; ++i) {
            scale(_h_log10_d[i], crossSection()/sumOfWeights());
            scale(_h_ajets_pT[i], crossSection()/sumOfWeights());
            scale(_h_ajets_eta[i], crossSection()/sumOfWeights());
        }

        for (size_t i = 0; i < 2; ++i) {
            scale(_h_dau_eta[i], crossSection()/sumOfWeights());
            scale(_h_dau_pT[i], crossSection()/sumOfWeights());
        }

        scale(_h_Z_mass, crossSection()/sumOfWeights());
        scale(_h_Z_eta, crossSection()/sumOfWeights());
        scale(_h_Z_pT, crossSection()/sumOfWeights());
        scale(_h_dijet_mass, crossSection()/sumOfWeights());
        scale(_h_dijet_eta, crossSection()/sumOfWeights());
        scale(_h_dijet_pT, crossSection()/sumOfWeights());
        scale(_h_HZ_pT, crossSection()/sumOfWeights());
        scale(_h_HZ_eta, crossSection()/sumOfWeights());

        scale(_h_dR_jj, crossSection()/sumOfWeights());
        scale(_h_deta_jj, crossSection()/sumOfWeights());
        scale(_h_dphi_jj, crossSection()/sumOfWeights());

        scale(_h_dR_HZ, crossSection()/sumOfWeights());
        scale(_h_deta_HZ, crossSection()/sumOfWeights());
        scale(_h_dphi_HZ, crossSection()/sumOfWeights());

        scale(_h_najets, crossSection()/sumOfWeights());
        scale(_h_nbjets, crossSection()/sumOfWeights());
    }

  private:

    size_t njets;
    std::vector<Histo1DPtr> _h_log10_d;
    std::vector<Histo1DPtr> _h_ajets_pT;
    std::vector<Histo1DPtr> _h_ajets_eta;
    std::vector<Histo1DPtr> _h_dau_eta;
    std::vector<Histo1DPtr> _h_dau_pT;
    Histo1DPtr _h_Z_mass, _h_Z_pT, _h_Z_eta, _h_dijet_pT, _h_dijet_mass, _h_dijet_eta;
    Histo1DPtr _h_HZ_pT, _h_HZ_eta;
    Histo1DPtr _h_najets, _h_nbjets;
    Histo1DPtr _h_dR_jj, _h_dphi_jj, _h_deta_jj;
    Histo1DPtr _h_dR_HZ, _h_dphi_HZ, _h_deta_HZ;

  };

  DECLARE_RIVET_PLUGIN(MC_ZHtautau);

}
