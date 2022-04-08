import nltk
nltk.download('punkt')

import os
import time
import dill
import random
import pandas as pd
from Url_Shortner import Url
from datetime import datetime
from newspaper import Article
from TwitterBot import Bot
from GoogleNewsScrapper import GoogleNews
from Preprocessing import TextPreprocessing
from NewsSummarizer import NewsSummary
from NewsParaPhraser import ParaPhrase
from CosineSimilarity import Similarity
from apscheduler.schedulers.blocking import BlockingScheduler
from concurrent.futures import ProcessPoolExecutor as Task_Manager
import warnings
warnings.filterwarnings("ignore")

class TweetGeneration:
    
    def __init__(self):
        """
        constructor to load necessary modules and dependencies.
        """

        self.gn=GoogleNews()
        self.tp=TextPreprocessing()

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
        return ". ".join(article_sentences[0:5])


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
        
        if(os.path.exists("models/phrase.pickle")):
            phrase=dill.load(open("models/phrase.pickle", "rb"))
        else:
            phrase=ParaPhrase()
            dill.dump(phrase, file = open("models/phrase.pickle", "wb"))

        sentences=cleaned_article.split('.')
        paraphrised_article=""
        for sent in sentences:
            if len(sent)<20:
                continue
            out=phrase.rephrase(sent)
            paraphrised_article+=out+" "

        return paraphrised_article


    def summerization(self,para_lst):
        """
        used to summerize the paragraph list sequentially
        """
        
        if(os.path.exists("models/summarizer.pickle")):
            summarizer=dill.load(open("models/summarizer.pickle", "rb"))
        else:
            summarizer=NewsSummary()
            dill.dump(summarizer, file = open("models/summarizer.pickle", "wb"))

        result=""
        for para in para_lst:
            if len(para)<20:
                continue
            summerized_para=summarizer.summerize(para)
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

    def create_log(self,tweets,urls,keyword):
        """
        creates the data logs aginst every news
        and saves it into the csv
        """
        df=pd.DataFrame(list(zip(tweets,urls)),columns=['Tweets','Urls'])
        df.to_csv("logs/"+keyword+".csv",index=False)


    def load_logs(self,keyword):
        """
        load the logs from local storage
        """
        df=pd.read_csv("logs/"+keyword+".csv")
        tweets=df["Tweets"].tolist()
        urls=df["Urls"].tolist()

        return tweets,urls

        
    def similarity(self,all_texts,new_text):
        """
        Compare results of all the previously generated 
        and current text
        """
        if(os.path.exists("models/sim.pickle")):
            sim=dill.load(open("models/sim.pickle", "rb"))
        else:
            sim=Similarity()
            dill.dump(sim, file = open("models/sim.pickle", "wb"))
        
        flag=True
        for text in all_texts:
           result=sim.get_similarity(text,new_text)
           if(result>=0.5) and ('blog' not in new_text.lower()) and ('article' not in new_text.lower()):
               flag=False
               break
        return flag


    def make_tiny_urls(self,main_url):
        """
        Make large urls smaller ones
        """
        url=Url()
        short_url=url.make_tiny_urls(main_url)

        return short_url


    def main_trigger(self,keyword):
        """
         method that sums upp all the modules together 
         to generate tweet against every tweet.
        """

        #get news from GoogleNewsScrapper utility.
        all_news=self.gn.get_latest_news(keyword)
        
        #to contain the tweet generated against every news article
        if(os.path.exists("logs/"+keyword+".csv")):
            tweets,urls=self.load_logs(keyword)
        else:
            tweets=[]
            urls=[]

        for i,news_url in enumerate(all_news["link"]):
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
                if len(cleaned_article)<250 or (cleaned_article.lower().count(keyword))<5:
                    continue
                                
                #Dividing article into paragraphs
                paragraph=self.para_maker(cleaned_article)

               
                

                # paraphrised_article=self.paraphrasing(paragraph)
                paraphrised_article=""
                with Task_Manager(max_workers=1) as executor:
                    paraphrised_article = executor.submit(self.paraphrasing,paragraph).result()

                #bi-passing poor quality content
                if len(paraphrised_article)<20:
                    continue

                #Summerizing the divided paragraphs
                summerized_article=""
                with Task_Manager(max_workers=1) as executor:
                    summerized_article = executor.submit(self.summerization,[paraphrised_article]).result()
                
                
                #bi-passing poor quality content
                if len(summerized_article)<20:
                    continue

                #applying post processing
                tweet=self.post_processing(summerized_article)

                #checking similarity
                flag=False
                with Task_Manager(max_workers=1) as executor:
                    flag = executor.submit(self.similarity,tweets,tweet).result()

                if(flag):

                    #to contain only 10 past tweets
                    if len(tweets)>=10:
                        tweets.pop(0)
                        urls.pop(0)

                    tweets.append(tweet)
                    tiny_url=self.make_tiny_urls(news_url)
                    urls.append(tiny_url)
                    tweet+="\n"+tiny_url
                    

                    bot=Bot()
                    # login to the twitter
                    login_flag=bot.twitter_login("your twitter email", "your twitter account")
                    
                    #check wether loggedin successfully or not

                    if not login_flag:
                        continue

                    #tweetposting flag
                    print(len(tweet))
                    posting_flag=bot.post_tweet(tweet)

                    #check wether Tweet posted successfully or not
                    if not posting_flag:
                        continue

                    #saving tweet to text file
                    self.create_log(tweets,urls,keyword)
                    
                    
                    break
                
            except Exception as e:
                print(e)
                continue

        

def job(keywords):
    tg=TweetGeneration()
    keyword=random.choice(keywords)
    generated_tweets=tg.main_trigger(keyword)
        

if __name__ == "__main__":


    keyword_list=["nft","metaverse"]
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval',hours=4, args=[keyword_list])
    scheduler.start()

