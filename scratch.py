import sqlite3
import math

import wcag_contrast_ratio as contrast
from colour import Color
from pandas import DataFrame
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
print(ok_pieces)
print(piece_features)

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
          print(piece_features.iloc[0])
          blue = Color("blue").rgb
          red=Color("red").rgb
          m=contrast.rgb(blue, red)
          print(m)
          print("ok1")
          score.append(math.floor(m))

        if(rule==2):
          print("ok2")
          z=35
          score.append(z)

    print(score)
    return score
s=get_score(piece_features, ok_pieces)
print(s)
#
#
# def sort_pieces(ok_pieces, scores):
#     # we need to implement this
#     pass
#
# def recommender(piece_id: int):
#     piece_features = query_db(piece_id)
#     ok_pieces = query_db(piece_id)
#     scores = []
#     for i in range(ok_pieces.shape[0]):
#         scores.append(get_score(piece_features, ok_pieces[i]))
#     sorted_pieces = sort_pieces(ok_pieces, scores)  # sort ok_pieces according to scores list ...
#     return sorted_pieces

#def matchColor(c1,c2):
# c1=pink
# c2= green
#
