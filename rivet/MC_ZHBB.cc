// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Analyses/MC_JetAnalysis.hh"
#include "Rivet/Projections/ZFinder.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/VetoedFinalState.hh"

namespace Rivet {

  using namespace Cuts;

  class MC_ZHBB : public Analysis {
  public:

    /// Constructor
    MC_ZHBB()
      : Analysis("MC_ZHBB")
    {    
    }

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
        // fish out Zee
        VetoedFinalState zmminput;
        zmminput.addVetoOnThisFinalState(zeefinder);
        // find Zmm
        ZFinder zmmfinder(zmminput, cut, PID::MUON, 65*GeV, 115*GeV, 0.2);
        addProjection(zmmfinder, "zmmfinder");
        // fish out Zee and Zmm
        VetoedFinalState jetproinput;
        jetproinput.addVetoOnThisFinalState(zeefinder);
        jetproinput.addVetoOnThisFinalState(zmmfinder);
        // make jets
        FastJets jetpro(jetproinput, FastJets::ANTIKT, 0.5);
        addProjection(jetpro, "jetpro");


        // ---- HISTOS ----
        int nbins =100;

        // jets
        for (size_t i=0; i < njets; ++i) {
            string dname = "log10_d_" +to_str(i) + to_str(i+1);
            _h_log10_d.push_back(bookHisto1D(dname, nbins, 0.2, 4));
            dname = "aJet_pT" +to_str(i);
            _h_ajets_pT.push_back(bookHisto1D(dname,logspace(nbins,5,300)));
        }

        // Z properties
        _h_Z_mass = bookHisto1D("Z_mass",nbins,51,131);
        _h_Z_eta = bookHisto1D("Z_eta",nbins,-5,5);
        _h_Z_pT = bookHisto1D("Z_pT",logspace(nbins,5,300));

        // dijet properties
        _h_dijet_mass = bookHisto1D("dijet_mass",nbins,60,140);
        _h_dijet_eta = bookHisto1D("dijet_eta",nbins,-5,5);
        _h_dijet_pT = bookHisto1D("dijet_pT",logspace(nbins,5,300));

        // higgs jets
        for (size_t i=0; i < 2; ++i) {
            string dname = "h_dau_mass" + to_str(i);
            _h_dau_mass.push_back(bookHisto1D(dname,nbins,0,160));
            dname = "h_dau_eta" + to_str(i);
            _h_dau_eta.push_back(bookHisto1D(dname,nbins,-5,5));
            dname = "h_dau_pT" + to_str(i);
            _h_dau_pT.push_back(bookHisto1D(dname,logspace(nbins,5,300)));
        }

    }

    /// Perform the per-event analysis
    void analyze(const Event& event) {
        const double weight = event.weight();

        double jets_pt_cut = 5.0*GeV;

        // apply the projections
        const ZFinder& zeefinder = applyProjection<ZFinder>(event, "zeefinder");
        const ZFinder& zmmfinder = applyProjection<ZFinder>(event, "zmmfinder");
        const Particles zll = zeefinder.bosons() + zmmfinder.bosons();
        const FastJets& jetpro = applyProjection<FastJets>(event,"jetpro");
        const Jets alljets = jetpro.jetsByPt();
       
        // only continue if a Z has been found
        if (zll.empty()) vetoEvent;

        Jets ajets;
        ajets.clear();
        Jet h0, h1; 
        FourMomentum  dijet;
        std::vector<size_t> b_indices;

        // find all jets with bs
        for (size_t i = 0; i < alljets.size(); ++i) {
            if (alljets[i].containsBottom())  b_indices.push_back(i);
            }

        // require at least to b jets
        if (b_indices.size() < 2) vetoEvent;

        // construct highest dijet pt b-jet pair
        double max_pt = 0.0*GeV;
        size_t idx0 = 0;
        size_t idx1 = 0;
        // pairwise iterate
        for (size_t i = 0; i < b_indices.size()-1; ++i) {
            for (size_t j = i+1; j < b_indices.size(); ++j) {
                dijet = alljets[b_indices[i]].momentum() + alljets[b_indices[j]].momentum();
                if (dijet.pT() > max_pt) {
                    max_pt = dijet.pT();
                    idx0 = b_indices[i];
                    idx1 = b_indices[j];
                    }
                }
            }

        h0 = alljets[idx0];
        h1 = alljets[idx1];
        // final highest pt dijet pair
        dijet = h0.momentum() + h1.momentum();
        
        // add everything else to the ajets 
        for (size_t i = 0; i < alljets.size(); ++i) {
            if (i != idx0 && i != idx1) ajets.push_back(alljets[i]);
            }

        // fill histos
        _h_dau_mass[0]->fill(h0.mass(),weight);
        _h_dau_mass[1]->fill(h1.mass(),weight);
        _h_dau_eta[0]->fill(h0.eta(),weight);
        _h_dau_eta[1]->fill(h1.eta(),weight);
        _h_dau_pT[0]->fill(h0.pT(),weight);
        _h_dau_pT[1]->fill(h1.pT(),weight);

        _h_Z_mass->fill(zll[0].mass(),weight);
        _h_Z_eta->fill(zll[0].eta(),weight);
        _h_Z_pT->fill(zll[0].pT(),weight);

        _h_dijet_mass->fill(dijet.mass(),weight);
        _h_dijet_eta->fill(dijet.eta(),weight);
        _h_dijet_pT->fill(dijet.pT(),weight);

        // Jet resolutions and integrated jet rates
        double d_ij;
        const fastjet::ClusterSequence* seq = jetpro.clusterSeq();
        if (seq != NULL) {
            for (size_t i = 0; i < njets; ++i) {
                 // Jet resolution i -> j
                 d_ij = log10(sqrt(seq->exclusive_dmerge_max(i)));

                // Fill differential jet resolution
                _h_log10_d[i]->fill(d_ij, weight);

                //fill aJet pT histos
                _h_ajets_pT[i]->fill(ajets[i].pT(),weight);
            }
        }
    }


    /// Normalise histograms etc., after the run
    void finalize() {

        /// @todo Normalise, scale and otherwise manipulate histograms here
        for (size_t i = 0; i < njets; ++i) {
            scale(_h_log10_d[i], crossSection()/sumOfWeights());
            scale(_h_ajets_pT[i], crossSection()/sumOfWeights());
        }

        for (size_t i = 0; i < 2; ++i) {
            scale(_h_dau_mass[i], crossSection()/sumOfWeights());
            scale(_h_dau_eta[i], crossSection()/sumOfWeights());
            scale(_h_dau_pT[i], crossSection()/sumOfWeights());
        }

        scale(_h_Z_mass, crossSection()/sumOfWeights());
        scale(_h_Z_eta, crossSection()/sumOfWeights());
        scale(_h_Z_pT, crossSection()/sumOfWeights());
        scale(_h_dijet_mass, crossSection()/sumOfWeights());
        scale(_h_dijet_eta, crossSection()/sumOfWeights());
        scale(_h_dijet_pT, crossSection()/sumOfWeights());

        // scale(_h_YYYY, crossSection()/sumOfWeights()); // norm to cross section
        // normalize(_h_YYYY); // normalize to unity

    }

  private:

    size_t njets;
    std::vector<Histo1DPtr> _h_log10_d;
    std::vector<Histo1DPtr> _h_ajets_pT;
    std::vector<Histo1DPtr> _h_dau_mass;
    std::vector<Histo1DPtr> _h_dau_eta;
    std::vector<Histo1DPtr> _h_dau_pT;
    Histo1DPtr _h_Z_mass, _h_Z_pT, _h_Z_eta, _h_dijet_pT, _h_dijet_mass, _h_dijet_eta;

  };

  DECLARE_RIVET_PLUGIN(MC_ZHBB);

}
