#Semantic Class Manager#

This repository contains the code and python classes to access and query to different sets of semantic classes
- Basic Level Concepts: http://adimen.si.ehu.es/web/BLC
- WordNet Domains: http://wndomains.fbk.eu/
- SuperSenses or Lexicographer files of WordNet: https://wordnet.princeton.edu/man/lexnames.5WN.html

It allows to install all these sets automatically and provides Python classes to query these semantic classes in different ways:
- Get the semantic class associated to a given synset offset in WordNet
- Get the semantic class associated to a given lexical key in WordNet
- Get all the semantic classes for all the senses of a certain lemma and pos-tag.

Besides to this, it makes use of the module WordNetMapper[https://github.com/MartenPostma/WordNetMapper] which maps automatically among WordNet versions, so you can use any wordnet version (BLC is aligned to WN3.0 and WordNet Domains to WN2.0).

##Installation##

The installation is fully performed by the `install.sh` script that is provided on this repository. It will create the required folders and it will download the necessary files. WordNet Domains is included in this repository as we comply with the Creative Commons 3.0 license under which this data is released.

These are the steps required to get this repository installed: 
```sh
$ cd YOUR_FOLDER
$ git clone https://github.com/rubenIzquierdo/semantic_class_manager
$ cd semantic_class_manager
$ . install.sh
```

##Usage##

Once installed you can start using the classes for querying. There are three main classes that inherit from the parent class `SemanticClassManager`. These classes are: `BLC`, `WND` and `SuperSense`. To query one of these repositories you have to create an object of your desired class, and then use the general methods inherited from `SemanticClassManager` which are basically:
- get_classes_for_synset_pos(synset,this_pos, this_wn_version=None): returns the list of classes belonging to that particular synset and pos-tag. The `this_wn_version` parameter specifies which is the WordNet version of the given synset. If it is not provided, it will be assumed to be the same version of the selected class (3.0 for BLC and SuperSense and 2.0 for WND). If this version is provided, the synset will be mapped to the corresposding one to get the correct semantic labels.
- get_classes_for_lexkey(self,lexkey,this_wn_version=None): same description as the previous one, but a lexical key is provided now.
- get_classes_for_lemma_pos(self,lemma,pos): gets the possible list of semantic classes for all the senses of the lemma.

For the `pos` tag you can use different formats and they will be internally mapped to a common set. The function that performs this mapping is:
```python
    def normalise_pos(this_pos):
        pos = None
        if this_pos.lower() in ['noun','n','1']:
            pos = self.NOUN     
        elif this_pos.lower() in ['verb','v','2']:
            pos = self.VERB     
        elif this_pos.lower() in ['adj','j','3','5','s','a']:
            pos = self.ADJ     
        elif this_pos.lower() in ['adv','r','4']:
            pos = self.ADV     
        return pos     
```

One example of usage of these classes would be:
```sh
from semantic_class_manager import *
wnd_obj = WND()
#the wn_version is noc inluded as the synset belongs to wn20 which is the same version thatn WND
print 'wn20 synset 00002287-a', wnd_obj.get_classes_for_synset_pos('00002287','a') 
print 'wn21 synset 00015024-n', wnd_obj.get_classes_for_synset_pos('00015024', 'n', '21')
print 'wn20 lexky acoustic_guitar%1:06:00::', wnd_obj.get_classes_for_lexkey('acoustic_guitar%1:06:00::')
print 'Classes for guitar.n', wnd_obj.get_classes_for_lemma_pos('guitar', 'n')
```

You can run the example file `example.py` which contains usage exmaples for the three semantic classes.

###WND ontology###
The WND labels are organized in an ontology. By default in this API, the WDN labels returned are the
leaves of the ontology. In some cases you might require to have the full ontology chain. You can do
this easily by creating the WND object as `wnd_obj = WND(hierarchy=True)`. The methods are the same,
with the difference that every class now is not a single string, but a list of strings (containing
all the classes for the chain. These are two examples of what you could get witout and with the ontology
option:
```sh
#WND with no ontology option
Classes for 00015024-n ['animals', 'biology']
Classes for acoustic_guitar%1:06:00:: ['music']
Classes for guitar.n ['music']

#WND with no ontology option
Classes for 00015024-n [[('animals', 2), ('pure_science', 1)], [('biology', 2), ('pure_science', 1)]]
Classes for acoustic_guitar%1:06:00:: [[('music', 3), ('art', 2), ('humanities', 1)]]
Classes for guitar.n [[('music', 3), ('art', 2), ('humanities', 1)]]
```

#
##Contact##
- Ruben Izquierdo
- Vrije University of Amsterdam
- ruben.izquierdobevia@vu.nl rubensanvi@gmail.com
- http://rubenizquierdobevia.com/
 
##License##
This repositority and code is distributed under the GNU GENERAL PUBLIC License, the terms can be found in the file `LICENSE` contained in this repository.

