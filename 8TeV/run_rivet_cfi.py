import FWCore.ParameterSet.Config as cms
import sys

my_filename = sys.argv[2].split('.')[0]+'.root'
print my_filename
my_outname=my_filename.split('/')[-1].replace('.root','.yoda')
print my_outname

process = cms.Process("runRivetAnalysis")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(my_filename),
)

process.options = cms.untracked.PSet(SkipEvent = cms.untracked.vstring('ProductNotFound'))

process.rivetAnalyzer = cms.EDAnalyzer('RivetAnalyzer',
  AnalysisNames = cms.vstring('ATLAS_2014_I1279489'),
  HepMCCollection = cms.InputTag('generator',''),
  UseExternalWeight = cms.bool(False),
  GenEventInfoCollection = cms.InputTag('generator'),
  CrossSection = cms.double(-1),
  Process = cms.vstring('0'),
  DoFinalize = cms.bool(True),
  ProduceDQMOutput = cms.bool(False),
  OutputFile = cms.string(my_outname)
)
process.p = cms.Path(process.rivetAnalyzer)
