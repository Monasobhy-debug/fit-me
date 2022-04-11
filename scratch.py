import sqlite3
import math
from colour import Color
import pandas as pd
import numpy as np

# data = data[['Type', 'Material', 'Fit', 'Style', 'Print', 'Color', 'length']]
# data.head()

def query_db(id):
    con = sqlite3.connect('D:\language\project database\pyScript\dbtest (1).db')
    # cursor = con.cursor()
    con.commit()
    data = pd.read_sql('SELECT * FROM clothes',con)
    y = data.query('id == %d'%id)
    # print(y)
    return y
    pass
ok_pieces = query_db(3)
piece_features = query_db(2)
# print(ok_pieces)
# print(piece_features)

def ColorDistance(rgb1,rgb2):

    rm = 0.5*(rgb1[0]+rgb2[0])
    d = sum((2+rm,4,3-rm)*(rgb1-rgb2)**2)**0.5
    print(d)
    return d
def get_score(piece_features, ok_pieces):
    score = 0
    # iterate over rules and assign score
    for rule in get_recommender_rules(piece_features,  ok_pieces):
        score += rule
    return score


def get_recommender_rules(piece_features, ok_pieces):
    score=[]
    for rule in range(1,3):
        if(rule==1):
          print(piece_features["Color"].iloc[0])
          print(ok_pieces["Color"].iloc[0])
          c1 = Color("%s"%str(piece_features["Color"].iloc[0])).rgb
          c2=Color("%s"%str(ok_pieces["Color"].iloc[0])).rgb
          # c1=Color('black').rgb
          # c2=Color('white').rgb
          print(np.array(c2))
          print(np.array(c1))
          m=ColorDistance(np.array(c1),np.array(c2))
          print(m)
          score.append(math.floor(m))

        if(rule==2):
          print(piece_features["Style"].iloc[0])
          print(ok_pieces["Style"].iloc[0])
          s1= str(piece_features["Style"].iloc[0])
          s2=str(ok_pieces["Style"].iloc[0])
          if(s1==s2):
            match = 100
          else:
              match=0
          # print("ok2")

          score.append(match)

    print(score)
    return score
s=get_score(piece_features, ok_pieces)
print(s)


def sort_pieces(ok_pieces, scores):
    # we need to implement this
    pass

def recommender(piece_id: int):
    piece_features = query_db(3)
    ok_pieces = query_db(2)
    scores = []
    for i in range(ok_pieces.shape[0]):
        scores.append(get_score(piece_features, ok_pieces[i]))
    sorted_pieces = sort_pieces(ok_pieces, scores)  # sort ok_pieces according to scores list ...
    return sorted_pieces

