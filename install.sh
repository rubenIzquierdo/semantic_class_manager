#!/bin/bash

#####################################
#####################################
# Ruben Izquierdo Bevia
# VU University of Amsterdam
# ruben.izquierdobevia@vu.nl
# rubensanvi@gmail.com
# http://rubenizquierdobevia.com/
# Version 1.0
#####################################
#####################################

# Remove in case already exist (wndomains not removed)
cd resources
rm -rf WordNet-*
rm -rf basic_level_concepts


#########
#BLC
#########
git clone https://github.com/rubenIzquierdo/basic_level_concepts
########

#############
# Wordnet2.0
#############
wget http://wordnetcode.princeton.edu/2.0/WordNet-2.0.tar.gz
tar xzf WordNet-2.0.tar.gz
rm WordNet-2.0.tar.gz
#############
#############


#############
# Wordnet3.0
#############
wget http://wordnetcode.princeton.edu/3.0/WordNet-3.0.tar.gz
tar xzf WordNet-3.0.tar.gz
rm WordNet-3.0.tar.gz
#############
#############

cd .. #Back to the root

rm -rf libs
mkdir libs
cd libs
git clone https://github.com/MartenPostma/WordNetMapper
touch __init__.py

cd .. # Back to the root

