import os
import urllib.request
# import matplotlib.pyplot as plt
from scipy import spatial
from sklearn.manifold import TSNE
import numpy as np                    




# emmbed_dict = {}
# with open('IRProject4/glove.6B.200d.txt','r') as f:
#   for line in f:
#     values = line.split()
#     word = values[0]
#     vector = np.asarray(values[1:],'float32')
#     emmbed_dict[word]=vector


class Glover:
  def __init__(self):
    self.emmbed_dict = {}
    with open('IRProject4/glove.6B.200d.txt','r') as f:
      for line in f:
        values = line.split()
        word = values[0]
        vector = np.asarray(values[1:],'float32')
        self.emmbed_dict[word]=vector
        
    self.emmbed_dict.popitem()
    
    # print("glover1.emmbed_dict: ", self.emmbed_dict)
    
    self.technology_embeddings = self.find_similar_word('technology')[1:1000]
    self.education_embeddings = self.find_similar_word('education')[1:1000]
    self.healthcare_embeddings = self.find_similar_word('healthcare')[1:1000]
    self.politic_embeddings = self.find_similar_word('politic')[1:1000]
    self.environment_embeddings = self.find_similar_word('environment')[1:1000]
    
    
    # print("\n ---------------------------------------------------------- \n")
    # print("self.technology_embeddings: ", self.technology_embeddings)
    # print("\n ---------------------------------------------------------- \n")
    # print("self.education_embeddings: ", self.education_embeddings)
    # print("\n ---------------------------------------------------------- \n")
    # print("self.healthcare_embeddings: ", self.healthcare_embeddings)
    # print("\n ---------------------------------------------------------- \n")
    # print("self.politic_embeddings: ", self.politic_embeddings)
    # print("\n ---------------------------------------------------------- \n")
    # print("self.environment_embeddings: ", self.environment_embeddings)
    # print("\n ---------------------------------------------------------- \n")
    
      
  def find_similar_word(self, word):
    nearest = []
    print("word in glover: ", word)
    # print("self.emmbed_dict type: ", type(self.emmbed_dict))
    if self.emmbed_dict.get(word) is None:
          return nearest
    else:
      emmbedes = self.emmbed_dict[word]
      nearest = sorted(self.emmbed_dict.keys(), key=lambda word: spatial.distance.euclidean(self.emmbed_dict[word], emmbedes))

    # nearest = sorted(self.emmbed_dict.keys(), key=lambda word: spatial.distance.euclidean(self.emmbed_dict[word], emmbedes))
    return nearest
  
  def intersection(self, lst1, lst2):
      lst3 = [value for value in lst2 if value in lst1]
      return lst3
    
  def compare(self, lst):
      inter_tech = self.intersection(self.technology_embeddings, lst)
      inter_edu = self.intersection(self.education_embeddings, lst)
      inter_health = self.intersection(self.healthcare_embeddings, lst)
      inter_env = self.intersection(self.environment_embeddings, lst)
      inter_poli = self.intersection(self.politic_embeddings, lst)
      
      intersections = [inter_tech, inter_edu, inter_env, inter_health, inter_poli]
      
      max = inter_tech
      # max_name = str("", inter_tech)
      for inter in intersections:
        if len(max) < len(inter):
          max = inter
        
      return max


if __name__ == "__main__":
  glover1 = Glover()
  # word = np.matrix(emmbed_dict['river'])
  # words = np.array(glover.emmbed_dict['river']).flatten()
  
  # print("dict len: ", len(glover.emmbed_dict))
  # print("word len: ", len(words))
  
  # technology_embeddings = glover.find_similar_word(glover.emmbed_dict['technology'])[1:1000]
  # if glover1.emmbed_dict.get('a') is None:
  #       print('not in glover1.emmbed_dict:')
  # else:
  #       print('is in glover1.emmbed_dict:')
        
  # print("glover1.emmbed_dict: ", glover1.emmbed_dict)
  
  embeddings2 = glover1.find_similar_word('how')[1:100]
  
  # inter = glover1.compare(embeddings2)

  print("embeddings: ", embeddings2)
  
  
  # for word in glover.emmbed_dict.keys():
  #   if len(glover.emmbed_dict[word]) != 200:
  #     print("  ", len(glover.emmbed_dict[word]))
    