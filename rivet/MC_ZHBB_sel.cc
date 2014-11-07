// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Analyses/MC_JetAnalysis.hh"
#include "Rivet/Projections/ZFinder.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/VetoedFinalState.hh"

namespace Rivet {

  //using namespace Cuts;

  class MC_ZHBB : public Analysis {
  public:

    /// Constructor
    MC_ZHBB()
      : Analysis("MC_ZHBB")
    {    
    }

    /// Book histograms and initialise projections before the run
    void init() {

        // # of jets for the jet ana
        njets = 4;

        // initialise projections
        FinalState fs;
        addProjection(fs, "fs");
        // find Zee
        ZFinder zeefinder(fs, -2.5, 2.5, 20.0*GeV, ELECTRON, 76*GeV, 106*GeV, 0.2, true, true);
        addProjection(zeefinder, "zeefinder");
        // fish out Zee
        VetoedFinalState zmminput;
        zmminput.addVetoOnThisFinalState(zeefinder);
        // find Zmm
        ZFinder zmmfinder(zmminput, -2.5, 2.5, 20.0*GeV, MUON, 76*GeV, 106*GeV, 0.2, true, true);
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
            stringstream ptname;
            ptname << "aJet_pT" << i;
            _h_ajets_pT.push_back(bookHistogram1D(ptname.str(),logspace(nbins,20,300)));
            stringstream etaname;
            etaname << "aJet_eta" << i;
            _h_ajets_eta.push_back(bookHistogram1D(etaname.str(),nbins,-2.5,2.5));
        }

        // Z properties
        _h_Z_mass = bookHistogram1D("Z_mass",nbins,76,106);
        _h_Z_eta = bookHistogram1D("Z_eta",nbins,-2.5,2.5);
        _h_Z_pT = bookHistogram1D("Z_pT",logspace(nbins,100,300));

        // dijet properties
        _h_dijet_mass = bookHistogram1D("dijet_mass",nbins,60,140);
        _h_dijet_eta = bookHistogram1D("dijet_eta",nbins,-2.5,2.5);
        _h_dijet_pT = bookHistogram1D("dijet_pT",logspace(nbins,20,300));

        // H+Z properties
        _h_HZ_eta = bookHistogram1D("HZ_eta",nbins,-5,5);
        _h_HZ_pT = bookHistogram1D("HZ_pT",logspace(nbins,20,300));

        // higgs jets
        for (size_t i=0; i < 2; ++i) {
            stringstream etaname;
            etaname << "h_dau_eta" << i;
            _h_dau_eta.push_back(bookHistogram1D(etaname.str(),nbins,-2.5,2.5));
            stringstream ptname;
            ptname << "h_dau_pT" << i;
            _h_dau_pT.push_back(bookHistogram1D(ptname.str(),logspace(nbins,20,300)));
        }

        // angles
        _h_dR_jj = bookHistogram1D("dR_jj",nbins,0,5);
        _h_dphi_jj = bookHistogram1D("dphi_jj",nbins,0,3.2);
        _h_deta_jj = bookHistogram1D("deta_jj", nbins,0,5);

        _h_dR_HZ = bookHistogram1D("dR_HZ",nbins,0,5);
        _h_dphi_HZ = bookHistogram1D("dphi_HZ",nbins,0,3.2);
        _h_deta_HZ = bookHistogram1D("deta_HZ", nbins,0,5);
        
        // nJets
        _h_najets = bookHistogram1D("najets",10,0,10);
        _h_nbjets = bookHistogram1D("nbjets",10,0,10);


    }

    // Perform the per-event analysis
    void analyze(const Event& event) {
        const double weight = event.weight();

        double jets_pt_cut = 20.0*GeV;
        double Zboost = 100.0*GeV;

        // apply the projections
        const ZFinder& zeefinder = applyProjection<ZFinder>(event, "zeefinder");
        const ZFinder& zmmfinder = applyProjection<ZFinder>(event, "zmmfinder");
        ParticleVector zll = zeefinder.bosons();
        zll.insert(zll.end(),zmmfinder.bosons().begin(),zmmfinder.bosons().end());
        const FastJets& jetpro = applyProjection<FastJets>(event,"jetpro");
        const Jets alljets = jetpro.jetsByPt(jets_pt_cut);
       
        // only continue if a Z has been found
        if (zll.empty()) vetoEvent;
        FourMomentum Z;
        Z = zll[0].momentum();
        if (Z.pT() < Zboost) vetoEvent;

        Jets ajets;
        ajets.clear();
        Jet h0, h1; 
        FourMomentum  dijet, HZ;
        std::vector<size_t> b_indices;
        b_indices.clear();
        int na = 0;
        int nb = 0;

        // find all jets with bs
        for (size_t i = 0; i < alljets.size(); ++i) {
            if (alljets[i].containsBottom()) {
                if (abs(alljets[i].momentum().eta()) < 2.5) {
                    b_indices.push_back(i);
                    nb++;
                }
            }
        }

        // require at least to b jets
        if (b_indices.empty()) vetoEvent;
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
        

        // HZ system
        HZ = dijet + Z;
        
        // add everything else to the ajets 
        for (size_t i = 0; i < alljets.size(); ++i) {
            if (i != idx0 && i != idx1){
                if (abs(alljets[i].momentum().eta()) < 2.5) {
                    ajets.push_back(alljets[i]);
                    na++;
                }
            }
        }

        // fill histos
        _h_dau_eta[0]->fill(h0.eta(),weight);
        _h_dau_eta[1]->fill(h1.eta(),weight);
        _h_dau_pT[0]->fill(h0.momentum().pT(),weight);
        _h_dau_pT[1]->fill(h1.momentum().pT(),weight);

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

        _h_dR_jj->fill(deltaR(h0,h1),weight);
        _h_deta_jj->fill(deltaEta(h0,h1),weight);
        _h_dphi_jj->fill(deltaPhi(h0,h1),weight);

        _h_dR_HZ->fill(deltaR(dijet,Z),weight);
        _h_deta_HZ->fill(deltaEta(dijet,Z),weight);
        _h_dphi_HZ->fill(deltaPhi(dijet,Z),weight);

        for (int i = 0; (i < na && i < (int)njets); ++i) {
            //fill aJet pT histos
            _h_ajets_pT[i]->fill(ajets[i].momentum().pT(),weight);
            _h_ajets_eta[i]->fill(ajets[i].eta(),weight);
        }
    }


    /// Normalise histograms etc., after the run
    void finalize() {

        for (size_t i = 0; i < njets; ++i) {
            scale(_h_ajets_pT[i], 1.0/sumOfWeights());
            scale(_h_ajets_eta[i], 1.0/sumOfWeights());
        }

        for (size_t i = 0; i < 2; ++i) {
            scale(_h_dau_eta[i], 1.0/sumOfWeights());
            scale(_h_dau_pT[i], 1.0/sumOfWeights());
        }

        scale(_h_Z_mass, 1.0/sumOfWeights());
        scale(_h_Z_eta, 1.0/sumOfWeights());
        scale(_h_Z_pT, 1.0/sumOfWeights());
        scale(_h_dijet_mass, 1.0/sumOfWeights());
        scale(_h_dijet_eta, 1.0/sumOfWeights());
        scale(_h_dijet_pT, 1.0/sumOfWeights());
        scale(_h_HZ_pT, 1.0/sumOfWeights());
        scale(_h_HZ_eta, 1.0/sumOfWeights());

        scale(_h_dR_jj, 1.0/sumOfWeights());
        scale(_h_deta_jj, 1.0/sumOfWeights());
        scale(_h_dphi_jj, 1.0/sumOfWeights());

        scale(_h_dR_HZ, 1.0/sumOfWeights());
        scale(_h_deta_HZ, 1.0/sumOfWeights());
        scale(_h_dphi_HZ, 1.0/sumOfWeights());

        scale(_h_najets, 1.0/sumOfWeights());
        scale(_h_nbjets, 1.0/sumOfWeights());
    }

  private:

    size_t njets;
    std::vector<AIDA::IHistogram1D*> _h_ajets_pT;
    std::vector<AIDA::IHistogram1D*> _h_ajets_eta;
    std::vector<AIDA::IHistogram1D*> _h_dau_eta;
    std::vector<AIDA::IHistogram1D*> _h_dau_pT;
    AIDA::IHistogram1D *_h_Z_mass, *_h_Z_pT, *_h_Z_eta, *_h_dijet_pT, *_h_dijet_mass, *_h_dijet_eta;
    AIDA::IHistogram1D *_h_HZ_pT, *_h_HZ_eta;
    AIDA::IHistogram1D *_h_najets, *_h_nbjets;
    AIDA::IHistogram1D *_h_dR_jj, *_h_dphi_jj, *_h_deta_jj;
    AIDA::IHistogram1D *_h_dR_HZ, *_h_dphi_HZ, *_h_deta_HZ;

  };

  DECLARE_RIVET_PLUGIN(MC_ZHBB);

}
