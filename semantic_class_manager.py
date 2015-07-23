#!/usr/bin/env python

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


import os
import sys
from subprocess import check_output
from collections import defaultdict

from python_modules.supersense_list import SS as SUPERSENSE_LIST
__here__ = os.path.dirname(os.path.realpath(__file__))

class SemanticClassManager(object):
    def __init__(self):
        self.map_synset_pos_to_class = {}
        self.NOUN = 'n'
        self.VERB = 'v'
        self.ADJ = 'a'
        self.ADV = 'r'
        self.wn_version = None
        self.wn_mapper = None   #By default we will not use it
        self.synset_for_lexkey = None   # To be read by the subclasses    {lexkey} --> offset
        self.synsets_for_lemma_pos = None # To be read by subclasses    {(lemma,pos)} -> [s1,s2,s3,s4]
        
    def normalise_pos(self,this_pos):
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
    
    def get_classes_for_synset_pos(self,synset,this_pos, this_wn_version=None):
        if this_wn_version is None:
            #Then it's assumed to be using the proper wnversion for the selected semantic class (wn30 for BLC and wn21 for WND)
            pass
        elif this_wn_version != self.wn_version:
            #We need to map the synset from this_wn_Version to self.wn_version.
            if self.wn_mapper is None:
                from libs.WordNetMapper import WordNetMapper
                self.wn_mapper = WordNetMapper()
            synset, another_pos = self.wn_mapper.map_offset_to_offset(synset,this_wn_version,self.wn_version)
                #print 'Mapped synset wn30', synset
             
        pos = self.normalise_pos(this_pos)
        if pos is None:
            print>>sys.stderr,'Pos %s not recognized' % this_pos
            return None
        else:
            if pos in self.map_synset_pos_to_class:
                return self.map_synset_pos_to_class[pos].get(synset)
            
            
    def get_classes_for_lexkey(self,lexkey,this_wn_version=None):
        if this_wn_version is None:
            #Then it's assumed to be using the proper wnversion for the selected semantic class (wn30 for BLC and wn21 for WND)
            pass
        elif this_wn_version != self.wn_version:
            #We need to map the synset from this_wn_Version to self.wn_version.
            if self.wn_mapper is None:
                from libs.WordNetMapper import WordNetMapper
                self.wn_mapper = WordNetMapper()
            o = lexkey
            lexkey = self.wn_mapper.map_lexkey_to_lexkey(lexkey,this_wn_version,self.wn_version)
        ######
        #We get the pos from the lexkey: rock_hopper%1:05:00:
        p = lexkey.find('%')+1
        pos = self.normalise_pos(lexkey[p])
        this_class = None
        if pos is None:
            print>>sys.stderr,'Pos %s not recognized' % this_pos
        else:
            if pos in self.map_synset_pos_to_class:
                synset = self.synset_for_lexkey.get(lexkey)
                if synset is not None:
                    this_class = self.map_synset_pos_to_class[pos].get(synset)
        return this_class
    
    def get_classes_for_lemma_pos(self,lemma,pos):
        classes = []
        pos = self.normalise_pos(pos)
        for synset in self.synsets_for_lemma_pos[(lemma,pos)]:
            these_classes = self.get_classes_for_synset_pos(synset, pos)
            classes.extend(these_classes)
        return list(set(classes))
            
            
    def are_compatible(self,class1,class2):
        pass
            
        
    
                
      

      
##########################################################################################
##########################################################################################
##################   BLC SEMANTIC CLASSES             ####################################
##########################################################################################
##########################################################################################
  
  
class BLC(SemanticClassManager):
    def __init__(self, min_freq, type_relations):
        
        #Call constructor of the parent
        super(BLC, self).__init__()
        
        self.wn_version = '30'
        
        # Checking the min frequency
        valid_min_freq = [0,10,20,50]
        if min_freq not in valid_min_freq:
            print>>sys.stderr,'Min frequency "%d" not valid, Valid values: %s' % (min_freq,str(valid_min_freq))
            raise Exception('Min freq not valid')
        
        # Checking the type of relation
        valid_type_relations = ['all','hypo']
        if type_relations.lower() not in valid_type_relations:
            print>>sys.stderr,'Type relation "%s" not valid. Valid relations: %s' % (type_relations,str(valid_type_relations))
            raise Exception('Type relation not valid')
                                       
        self.load_blc(min_freq, type_relations)   
        
        
          
             
    def load_blc(self,min_freq,type_relations):
        friendly_blc_to_ili = self.__load_friendly_blc_from_ili__()                          
        blc_file = __here__+'/resources/BLC_Wordnet-3.0/'
        if min_freq == 0:
            blc_file += "sinfreqmin"
        else:
            blc_file += 'freqmin%d' % min_freq
        
        blc_file+='/'+type_relations.lower()
        
        for this_pos, this_file in [(self.NOUN,'BLCnoun.rel'),(self.VERB,'BLCverb.rel')]:
            self.map_synset_pos_to_class[this_pos] = {}
            whole_path = blc_file+'/'+this_file
            fd = open(whole_path,'r')
            for line in fd:
                this_synset_pos, this_blc = line.strip().split()
                this_synset = this_synset_pos[:-2]
                final_blc, freq = friendly_blc_to_ili[this_blc]
                self.map_synset_pos_to_class[this_pos][this_synset] = [final_blc]
        
        ###                                         

    def __load_friendly_blc_from_ili__(self):
        #ili_blc is like 02560585-v

        friendly_blc_to_ili = {}
        path_to_wn_index = __here__+'/resources/WordNet-3.0/dict/index.sense'
        
        fd = open(path_to_wn_index,'r')
        self.synset_for_lexkey = {}
        self.synsets_for_lemma_pos = defaultdict(list)
        
        for line in fd:
            #.22-caliber%3:01:00:: 03146310 1 0
            lexkey, synset, sense, freq = line.strip().split()
            self.synset_for_lexkey[lexkey] = synset
            p = lexkey.find('%')
            lemma = lexkey[:p]
            int_pos = lexkey[p+1]
            self.synsets_for_lemma_pos[(lemma,self.normalise_pos(int_pos))].append(synset)
            
            pos = None
            if int_pos == '1':
                pos = 'n'
            elif int_pos == '2':
                pos = 'v'
            
            if pos is not None:
                ili = synset+'-'+pos
                fr_blc = '%s.%s#%s' % (lexkey[:p],pos,sense)
                if ili not in friendly_blc_to_ili:
                    friendly_blc_to_ili[ili] = (fr_blc,freq)
                else:
                    _, prev_freq =  friendly_blc_to_ili[ili]
                    if freq > prev_freq:
                        friendly_blc_to_ili[ili] = (fr_blc,freq)
        return friendly_blc_to_ili
            
            
    def are_compatible(self,class1,class2):
        compatible = False
        if class1 == class2:
            compatible = False
        else:
            p1 = class1.rfind('#')
            pos_c1 = class1[p1-1]
            p2 = class2.rfind('#')
            pos_c2 = class1[p2-1]
            if pos_c1 == pos_c2:
                compatible = True
            else:
                compatible = False
        return compatible
            
            
##########################################################################################
##########################################################################################
##################   WND SEMANTIC CLASSES             ####################################
##########################################################################################
##########################################################################################
            
class WND(SemanticClassManager):
    def __init__(self):
        
        #Call constructor of the parent
        super(WND, self).__init__()
        
        self.wn_version = '20'
        self.__load_wnd__()
        self.__load_synset_for_lexkey__()
        
    def __load_wnd__(self):
        #Creates
        # self.map_synset_pos_to_class[this_pos][this_synset] = CLASS
        # self.synset_for_lexkey[lexkey] = synset
        wnd_file = __here__ + '/resources/wn-domains-3.2/wn-domains-3.2-20070223'
        fd = open(wnd_file,'r')
        for line in fd:
            #line -> 00001740-n    factotum
            fields = line.strip().split()
            synset_pos = fields[0]
            wnd_labels = fields[1:]
            
            synset = synset_pos[:-2]
            pos = synset_pos[-1]
            pos = self.normalise_pos(pos)
        
            
            if pos not in self.map_synset_pos_to_class:
                self.map_synset_pos_to_class[pos] = {}
            self.map_synset_pos_to_class[pos][synset] = wnd_labels
        fd.close()
        
    def __load_synset_for_lexkey__(self):
        self.synset_for_lexkey = {}
        self.synsets_for_lemma_pos = defaultdict(list)
        wn_index_file = __here__+'/resources/WordNet-2.0/dict/index.sense'
        fd = open(wn_index_file,'r')
        for line in fd:
            #.22-caliber%3:01:00:: 03146310 1 0
            lexkey, synset, sense, freq = line.strip().split()
            self.synset_for_lexkey[lexkey] = synset

            p = lexkey.find('%')
            lemma = lexkey[:p]
            int_pos = lexkey[p+1]
            self.synsets_for_lemma_pos[(lemma,self.normalise_pos(int_pos))].append(synset)  

        fd.close()
        
    
    def are_compatible(self,class1,class2):
        if class1 == class2:
            return False
        else:
            return True
        

                
##########################################################################################
##########################################################################################
##################   SUPERSENSE SEMANTIC CLASSES             ####################################
##########################################################################################
##########################################################################################

class SuperSense(SemanticClassManager):
    def __init__(self):
        
        #Call constructor of the parent
        super(SuperSense, self).__init__()
        self.wn_version = '30'
        self.__load_info__()
        
    def __load_info__(self):
        self.synset_for_lexkey = {}
        self.synsets_for_lemma_pos = defaultdict(list)
        wn_index_file = __here__+'/resources/WordNet-3.0/dict/index.sense'
        fd = open(wn_index_file,'r')
        for line in fd:
            #.22-caliber%3:01:00:: 03146310 1 0
            lexkey, synset, sense, freq = line.strip().split()
            self.synset_for_lexkey[lexkey] = synset

            p = lexkey.find('%')
            lemma = lexkey[:p]
            int_pos = lexkey[p+1]
            self.synsets_for_lemma_pos[(lemma,self.normalise_pos(int_pos))].append(synset) 
            
            parts = lexkey.split(':')
            int_supersense = parts[1]
            
            pos = self.normalise_pos(int_pos)
            if pos not in self.map_synset_pos_to_class:
                self.map_synset_pos_to_class[pos] = {}
            self.map_synset_pos_to_class[pos][synset] = [SUPERSENSE_LIST[int_supersense]] 

        fd.close()
        
    def are_compatible(self,class1,class2):
        if class1 == class2:
            return False
        else:
            p1 = class1.find('.')
            pos1 = class1[:p1]
            p2 = class2.find('.')
            pos2 = class2[:p2]
            if pos1 == pos2:
                return True
            else:
                return False