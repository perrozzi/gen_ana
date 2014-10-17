import FWCore.ParameterSet.Config as cms

process = cms.Process("runRivetAnalysis")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(10)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    )

#process.content = cms.EDAnalyzer("EventContentAnalyzer")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:aMCNLO_pythia8.root'),
    #fileNames = cms.untracked.vstring('/store/group/phys_smp/Wmass/perrozzi/philipp/pythia8ex7.root'),
)

process.options = cms.untracked.PSet(SkipEvent = cms.untracked.vstring('ProductNotFound'))

process.rivetAnalyzer = cms.EDAnalyzer('RivetAnalyzer',
  AnalysisNames = cms.vstring('MC_ZHBB'),
  HepMCCollection = cms.InputTag('generator',''),
  UseExternalWeight = cms.bool(False),
  GenEventInfoCollection = cms.InputTag('generator'),
  CrossSection = cms.double(1000),
  Process = cms.vstring('0'),
  DoFinalize = cms.bool(True),
  ProduceDQMOutput = cms.bool(False),
  OutputFile = cms.string('out.aida')
)
process.p = cms.Path(process.rivetAnalyzer)
#process.p = cms.Path(process.content * process.rivetAnalyzer)
