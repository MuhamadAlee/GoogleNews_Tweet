from semantic_text_similarity.models import WebBertSimilarity

class Similarity:
    def __init__(self):
        self.model = WebBertSimilarity(device='cpu', batch_size=10) 

    def get_similarity(self,text1,text2):
        return self.model.predict([("She won an olympic gold medal","The women is an olympic champion")])[0]