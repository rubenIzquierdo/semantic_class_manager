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
rm -rf BLC_Wordnet-3.0


#########
#BLC-wn30
#########
wget -O blc_wn30.tgz "http://adimen.si.ehu.es/web/modules/pubdlcnt/pubdlcnt.php?file=http://adimen.si.ehu.es/web/files/BLC/Wordnet-3.0.tar.gz&nid=12"
tar xzf blc_wn30.tgz
mv Wordnet-3.0/ BLC_Wordnet-3.0/
rm blc_wn30.tgz
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

