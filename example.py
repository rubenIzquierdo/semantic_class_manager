#!/usr/bin/env python

from semantic_class_manager import *

if __name__ == '__main__':
    
    
    a = BLC(0,'all')
    print 'wn30 00021939', a.get_classes_for_synset_pos('00021939','n','30')
    print 'wn21 00020846', a.get_classes_for_synset_pos('00020846','n','21')
    print 'wn30 jimmy%2:35:00::', a.get_classes_for_lexkey('jimmy%2:35:00::','30')
    print 'wn30 artifact%1:03:00::', a.get_classes_for_lexkey('artifact%1:03:00::', '30')
    print 'wn21 artefact%1:03:00::', a.get_classes_for_lexkey('artifact%1:03:00::', '21')
    print 'Classes for house.n', a.get_classes_for_lemma_pos('house', 'n')
    print 'Classes for guitar.n', a.get_classes_for_lemma_pos('guitar', 'n')
    
    
    wnd_obj = WND()
    print '#'*20
    print 'WND'
    print 'wn20 00002287-a', wnd_obj.get_classes_for_synset_pos('00002287','a')
    print 'wn20 00012748-n', wnd_obj.get_classes_for_synset_pos('00012748', 'n')
    print 'wn21 00015024-n', wnd_obj.get_classes_for_synset_pos('00015024', 'n', '21')
    print 'wn20 acoustic_guitar%1:06:00::', wnd_obj.get_classes_for_lexkey('acoustic_guitar%1:06:00::')
    print 'wn16 acoustic_guitar%1:06:00::', wnd_obj.get_classes_for_lexkey('acoustic_guitar%1:06:00::','16')
    print 'Classes for house.n', wnd_obj.get_classes_for_lemma_pos('house', 'n')
    print 'Classes for guitar.n', wnd_obj.get_classes_for_lemma_pos('guitar', 'n')
    
    
    ss_obj = SuperSense()
    print '#'*20
    print 'SuperSense'
    print 'wn20 00002287-a', ss_obj.get_classes_for_synset_pos('00002287','a', '20')
    print 'wn20 00012748-n', ss_obj.get_classes_for_synset_pos('00012748', 'n', '20')
    print 'wn21 00015024-n', ss_obj.get_classes_for_synset_pos('00015024', 'n', '21')
    print 'wn20 acoustic_guitar%1:06:00::', ss_obj.get_classes_for_lexkey('acoustic_guitar%1:06:00::')
    print 'wn16 acoustic_guitar%1:06:00::', ss_obj.get_classes_for_lexkey('acoustic_guitar%1:06:00::','16')
    print 'Classes for house.n', ss_obj.get_classes_for_lemma_pos('house', 'n')
    print 'Classes for guitar.n', ss_obj.get_classes_for_lemma_pos('guitar', 'n')

