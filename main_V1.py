import nltk
nltk.download('punkt')

from datetime import datetime
from newspaper import Article
from GoogleNewsScrapper import GoogleNews
from Preprocessing import TextPreprocessing
from NewsSummarizer import NewsSummary
from NewsParaPhraser import ParaPhrase
from CosineSimilarity import Similarity

import warnings
warnings.filterwarnings("ignore")

class TweetGeneration:
    
    def __init__(self):
        """
        constructor to load necessary modules and dependencies.
        """

        self.gn=GoogleNews()
        self.tp=TextPreprocessing()
        self.phrase=ParaPhrase()
        self.summarizer=NewsSummary()
        self.sim=Similarity()

    def para_maker(self, article):
        """
        method that will try to break up the
        whole article in a five different portions
        """

        para_lst=[]
        article_sentences=article.split(".")
        # article=article[:-1]
        length=round(len(article_sentences)/5)
        for i in range(5):
            start=length*i
            end=start+length
            para_lst.append(". ".join(article_sentences[start:end]))
        return para_lst


    def reconcatenate(self,sententnce_list):
        """
        used to reconcatenate the sentences into some kind of paragraph
        """
        paragraph=""
        for sentence in sententnce_list:
            paragraph+=sentence+". "
        return paragraph

    def paraphrasing(self,cleaned_article):
        """
        makes the paraphrised version of the article
        """
        sentences=cleaned_article.split('.')
        paraphrised_article=""
        for sent in sentences:
            if len(sent)<20:
                continue
            out=self.phrase.rephrase(sent)
            paraphrised_article+=out+" "

        return paraphrised_article


    def summerization(self,para_lst):
        """
        used to summerize the paragraph list sequentially
        """
        result=""
        for para in para_lst:
            if len(para)<20:
                continue
            summerized_para=self.summarizer.summerize(para)
            summerized_para_lists=summerized_para.split('.')
            timmed_para=self.reconcatenate(summerized_para_lists[:-1])
            if len(timmed_para)<20:
                continue
            result+=timmed_para

        return result

    def post_processing(self,tweet):
        """
        performs some post processing on text 
        """

        tweet=tweet.replace(" .",".")
        tweet=" ".join(tweet.split())
        tweet='. '.join(map(lambda s: s.strip().capitalize(), tweet.split('.')))
        return tweet

    def create_log(self,content,keyword):
        """
        creates the data logs aginst every news
        and saves it into the textfiles
        """

        now=datetime.now()
        filename="logs/"+keyword+now.strftime("%d_%m_%Y_%H_%M_%S")
        f = open(filename+".txt", "w")
        f.write(content)
        f.close()
        
    def similarity(self,all_texts,new_text):
        """
        Compare results of all the previously generated 
        and current text
        """
        flag=True
        for text in all_texts:
           result=self.sim.get_similarity(text,new_text) 
           if(result>=0.5):
               flag=False
               break
        return flag

    def main_trigger(self,keyword):
        """
         method that sums upp all the modules together 
         to generate tweet against every tweet.
        """

        #get news from GoogleNewsScrapper utility.
        all_news=self.gn.get_latest_news(keyword)
        
        #to contain the tweet generated against every news article
        tweets=[]

        for news_url in all_news["link"]:
            try:
                #scrapping text against every news 
                article = Article(news_url, language="en")
                article.download()
                article.parse()
                article.nlp()
                article_text=article.text

                #applying some text pre-processing over the news article
                cleaned_article=self.tp.cleaner(article_text)

                #bi-passing poor quality content
                if len(cleaned_article)<150 or (cleaned_article.lower().count(keyword))<8:
                    continue
                
            
                #paraphrsing the content
                paraphrised_article=self.paraphrasing(cleaned_article)


                #Dividing article into 5 paragraphs
                para_lst=self.para_maker(paraphrised_article)

                #Summerizing the divided paragraphs
                summerized_article=self.summerization(para_lst)

                #tweet generation now
                tweet=self.summarizer.summerize_tweet(summerized_article)
                
                #applying post processing
                tweet=self.post_processing(tweet)


                #checking similarity
                if(self.similarity(tweets,tweet)):
                    tweets.append(tweet)
                    print("-"*100)
                    print(tweet)
                    #saving tweet to text file
                    self.create_log(tweet,keyword)
                
            except Exception as e:
                print(e)
                continue

        return tweets


if __name__ == "__main__":
    tg=TweetGeneration()
    generated_tweets=tg.main_trigger("metaverse")
    
