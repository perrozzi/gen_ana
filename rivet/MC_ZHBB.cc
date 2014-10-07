// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Analyses/MC_JetAnalysis.hh"
#include "Rivet/Projections/ZFinder.hh"
#include "Rivet/Projections/FastJets.hh"
/// @todo Include more projections as required, e.g. ChargedFinalState, FastJets, ZFinder...

namespace Rivet {

  using namespace Cuts;

  class MC_ZHBB : public Analysis {
  public:

    /// Constructor
    MC_ZHBB()
      : Analysis("MC_ZHBB")
    {    
    }


    /// @name Analysis methods
    //@{

    /// Book histograms and initialise projections before the run
    void init() {

        //Cut cut = etaIn(-10,10) & (pT >= 0.0*GeV);
        Cut cut = pT >= 0.0*GeV;

        // # of jets for the jet ana
        njets = 4;

        // initialise projections
        FinalState fs;
        addProjection(fs, "fs");
        // find Zee
        ZFinder zeefinder(fs, cut, PID::ELECTRON, 65*GeV, 115*GeV, 0.2);
        addProjection(zeefinder, "zeefinder");
        // find Zmm
        ZFinder zmmfinder(zeefinder.remainingFinalState(), cut, PID::MUON, 65*GeV, 115*GeV, 0.2);
        addProjection(zmmfinder, "zmmfinder");
        // make jets
        FastJets jets(zmmfinder.remainingFinalState(), FastJets::ANTIKT, 0.5);
        addProjection(jets, "jets");

        // ---- HISTOS ----

        // differential jet rates
        for (size_t i=0; i < njets; ++i) {
            const string dname = "log10_d_" +to_str(i) + to_str(i+1);
            _h_log10_d.push_back(bookHisto1D(dname, 100, 0.2, 4));
        }

        // Z properties
        _h_Z_mass = bookHisto1D("Z_mass",80,51,131);
        _h_Z_pT = bookHisto1D("Z_pT",logspace(100,5,300));

        // dijet properties
        _h_dijet_mass = bookHisto1D("dijet_mass",80,60,140);
        _h_dijet_pT = bookHisto1D("dijet_pT",logspace(100,5,300));

    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
        const double weight = event.weight();

        float jets_pt_cut = 0.0*GeV;

        const ZFinder& zeefinder = applyProjection<ZFinder>(event, "zeefinder");
        const ZFinder& zmmfinder = applyProjection<ZFinder>(event, "zmmfinder");
        const Particles zll = zeefinder.bosons() + zmmfinder.bosons();
        const FastJets& jets = applyProjection<FastJets>(event,"jets");
        const Jets& alljets = jets.jetsByPt(jets_pt_cut);
       
        // only continue if a Z has been found
        if (zll.empty()) vetoEvent;

        Jets bjets;
        Jets ajets;
        Jet h0, h1; 
        FourMomentum  dijet;

        foreach (const Jet& jet, alljets) {
            if (jet.bTagged()) bjets.push_back(jet);
            else ajets.push_back(jet);
            }

        if (bjets.size() < 2) vetoEvent;

        // construct highest dijet pt b-jet pair
        double max_pt = 0.0*GeV;
        size_t idx0 = 0;
        size_t idx1 = 0;
        for (size_t i = 0; i < bjets.size()-1; ++i) {
            for (size_t j = i+1; j < bjets.size(); ++j) {
                dijet = bjets[i].momentum() + bjets[j].momentum();
                if (dijet.pT() > max_pt) {
                    max_pt = dijet.pT();
                    idx0 = i;
                    idx1 = j;
                    }
                }
            }

        // add everything else to the ajets 
        for (size_t i = 0; i < bjets.size(); ++i) {
            // for now identify the first two b-jets as higgs
            if (i == idx0) h0 = bjets[i];
            else if (i == idx1) h1 = bjets[i];
            else ajets.push_back(bjets[i]);
            }

        // final highest pt dijet pair
        dijet = h0.momentum() + h1.momentum();

        // fill histos
        _h_Z_mass->fill(zll[0].mass(),weight);
        _h_Z_pT->fill(zll[0].pT(),weight);

        _h_dijet_mass->fill(dijet.mass(),weight);
        _h_dijet_pT->fill(dijet.pT(),weight);


        // Jet resolutions and integrated jet rates
        double d_ij;
        const fastjet::ClusterSequence* seq = jets.clusterSeq();
        if (seq != NULL) {
            for (size_t i = 0; i < njets; ++i) {
                 // Jet resolution i -> j
                 d_ij = log10(sqrt(seq->exclusive_dmerge_max(i)));

                // Fill differential jet resolution
                _h_log10_d[i]->fill(d_ij, weight);
            }
        }

    }


    /// Normalise histograms etc., after the run
    void finalize() {

        /// @todo Normalise, scale and otherwise manipulate histograms here
        for (size_t i = 0; i < njets; ++i) {
            scale(_h_log10_d[i], crossSection()/sumOfWeights());
        }
        scale(_h_Z_mass, crossSection()/sumOfWeights());
        scale(_h_dijet_mass, crossSection()/sumOfWeights());
        scale(_h_Z_pT, crossSection()/sumOfWeights());
        scale(_h_dijet_pT, crossSection()/sumOfWeights());


        // scale(_h_YYYY, crossSection()/sumOfWeights()); // norm to cross section
        // normalize(_h_YYYY); // normalize to unity
      
        // Scale the d{eta,phi,R} histograms

    }

    //@}


  private:

    // Data members like post-cuts event weight counters go here


    /// @name Histograms
    //@{
    size_t njets;
    //Profile1DPtr _h_XXXX;
    //Histo1DPtr _h_deta_jets, _h_dphi_jets, _h_dR_jets;
    std::vector<Histo1DPtr> _h_log10_d;
    Histo1DPtr _h_Z_mass, _h_Z_pT, _h_dijet_pT, _h_dijet_mass;
    //@}


  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(MC_ZHBB);

}
