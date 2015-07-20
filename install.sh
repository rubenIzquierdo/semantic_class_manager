wget -O blc_wn30.tgz "http://adimen.si.ehu.es/web/modules/pubdlcnt/pubdlcnt.php?file=http://adimen.si.ehu.es/web/files/BLC/Wordnet-3.0.tar.gz&nid=12"

mv Wordnet-3.0/ BLC_Wordnet-3.0/

#INSTALL WN20 in resources/WordNet-2.0

wget http://wordnetcode.princeton.edu/3.0/WordNet-3.0.tar.gz
tar xvzf WordNet-3.0.tar.gz

git clone https://github.com/MartenPostma/WordNetMapper
