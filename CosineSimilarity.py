from sentence_transformers import SentenceTransformer, util
import torch

class Similarity:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.device = torch.device("cpu")
        self.model = self.model.to(self.device)

    def get_similarity(self,sent1,sent2):
        """
        results in how two texts are similar to each other
        """
        
        embedding_1= self.model.encode(sent1, convert_to_tensor=True)
        embedding_2 = self.model.encode(sent2, convert_to_tensor=True)
        result=util.pytorch_cos_sim(embedding_1, embedding_2)
        return result.cpu().numpy()[0][0]