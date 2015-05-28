//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu May 28 15:00:54 2015 by ROOT version 5.32/00
// from TTree Particles/Particles
// found on file: test_christoph.root
//////////////////////////////////////////////////////////

#ifndef test_christoph_h
#define test_christoph_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

// Fixed size dimensions of array or collections stored in the TTree if any.

class test_christoph {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   Int_t           particles_size;
   Int_t           particles_mother[1376];   //[particles_size]
   Float_t         pt[1376];   //[particles_size]
   Float_t         eta[1376];   //[particles_size]
   Float_t         phi[1376];   //[particles_size]
   Float_t         mass[1376];   //[particles_size]
   Int_t           pdgId[1376];   //[particles_size]
   Int_t           status[1376];   //[particles_size]
   Int_t           qx3[1376];   //[particles_size]

   // List of branches
   TBranch        *b_particles_size;   //!
   TBranch        *b_particles_mother;   //!
   TBranch        *b_pt;   //!
   TBranch        *b_eta;   //!
   TBranch        *b_phi;   //!
   TBranch        *b_mass;   //!
   TBranch        *b_pdgId;   //!
   TBranch        *b_status;   //!
   TBranch        *b_qx3;   //!

   test_christoph(TTree *tree=0);
   virtual ~test_christoph();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef test_christoph_cxx
test_christoph::test_christoph(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("test_christoph.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("test_christoph.root");
      }
      f->GetObject("Particles",tree);

   }
   Init(tree);
}

test_christoph::~test_christoph()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t test_christoph::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t test_christoph::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void test_christoph::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("particles_size", &particles_size, &b_particles_size);
   fChain->SetBranchAddress("particles_mother", particles_mother, &b_particles_mother);
   fChain->SetBranchAddress("pt", pt, &b_pt);
   fChain->SetBranchAddress("eta", eta, &b_eta);
   fChain->SetBranchAddress("phi", phi, &b_phi);
   fChain->SetBranchAddress("mass", mass, &b_mass);
   fChain->SetBranchAddress("pdgId", pdgId, &b_pdgId);
   fChain->SetBranchAddress("status", status, &b_status);
   fChain->SetBranchAddress("qx3", qx3, &b_qx3);
   Notify();
}

Bool_t test_christoph::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void test_christoph::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t test_christoph::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef test_christoph_cxx
