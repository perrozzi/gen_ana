#!/usr/bin/env python
# $Id: inputExample.py 545 2012-01-18 06:10:03Z cvermilion $
#----------------------------------------------------------------------
# Copyright (c) 2010-12, Pierre-Antoine Delsart, Kurtis Geerlings, Joey Huston,
#                 Brian Martin, and Christopher Vermilion
#
#----------------------------------------------------------------------
# This file is part of SpartyJet.
#
#  SpartyJet is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  SpartyJet is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SpartyJet; if not, write to the Free Software
#  Foundation, Inc.:
#      59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#----------------------------------------------------------------------
from spartyjet import *
import sys
#===============================================

# Ntuple
# (getInputMaker should usually get ROOT files right, but only if prefix starts with 'Input')
ntupleInput = SJ.NtupleInputMaker(SJ.NtupleInputMaker.EtaPhiPtM_array_float)
ntupleInput.set_prefix('')
ntupleInput.set_n_name('size')
ntupleInput.set_variables('eta', 'phi', 'pt', 'mass')
ntupleInput.setFileTree('../data/sparty_input_sherpa.root', 'mytree')
input = ntupleInput

# output ROOT file
outfile = "../data/output/Sherpa.root"

print "Now running on",input.name()

# Create a jet builder---------------------------
builder = SJ.JetBuilder(SJ.INFO)

# Set the input----------------------------------
builder.configure_input(input)

# Configure algorithms --------------------------
AK5 = SJ.FastJet.FastJetFinder('AK5', fastjet.antikt_algorithm, 0.5)
analysis = SJ.JetAnalysis(AK5)
builder.add_analysis(analysis)

# ignore neutrinos, muons and electrons
# mu and e with Pt > 20. rejected in input maker
#builder.add_jetTool_input(SJ.JetInputPdgIdSelectorTool(stdVector(-16,16,-14,14,-13,13,-12,12,-11,11)))
# no neutrinos
#builder.add_jetTool_input(SJ.JetInputPdgIdSelectorTool(stdVector(-16,16,-14,14,-12,12)))
#builder.add_jetTool_input(SJ.JetEtaCentralSelectorTool(-2.5,2.5))

# Configure output--------------------------------
builder.configure_output("AK5", outfile)

#ptmin
#builder.add_jetTool(SJ.FastJet.SelectorTool(fj.SelectorPtMin(10.0), 'PtCut'))

# Run SpartyJet
builder.process_events()
#builder.process_one_event(111)

# Save this script in the ROOT file (needs to go after process_events or it
#  gets over-written!)

