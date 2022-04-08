from styleformer import Styleformer
import torch

import warnings
warnings.filterwarnings("ignore")


class ParaPhrase:

    def __init__(self):
        self.casual_model = Styleformer(style = 0) 
        

    def rephrase(self,source_sentence):
        """
        it will rephrase the text into formal version
        """
        
        target_sentence = self.casual_model.transfer(source_sentence)
        
        if target_sentence is None:
            target_sentence=source_sentence
        return target_sentence