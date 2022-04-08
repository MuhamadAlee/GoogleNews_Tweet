import torch
import gensim
from transformers import pipeline

import warnings
warnings.filterwarnings("ignore")

class NewsSummary:

    def __init__(self):

        # pre-trained model from hugging face
        self.summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base")

    def summerize(self,news_article):

        """
        returns the summerized version of the news article
        given to it.
        """
        
        text=self.summarizer(news_article,early_stopping=False, max_length=68, min_length=35, do_sample=False)
        result=text[0]['summary_text']
        result=". ".join(result.split(".")[:-1])
        return result+". "
