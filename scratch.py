import sqlite3
import math
from colour import Color
import pandas as pd
import numpy as np
import wcag_contrast_ratio as contrast


def query_db(dataframe_query):
    con = sqlite3.connect('D:\language\project database\pyScript\dbtest (1).db')
    # cursor = con.cursor()
    con.commit()
    data = pd.read_sql('SELECT * FROM clothes', con)
    y = data.query(dataframe_query)
    # print(y)
    return y
    pass


# ok_pieces = query_db(3)
# piece_features = query_db(2)


# print(ok_pieces)
# print(piece_features)

def ColorDistance(rgb1, rgb2):
    rm = 0.5 * (rgb1[0] + rgb2[0])
    d = sum((2 + rm, 4, 3 - rm) * (rgb1 - rgb2) ** 2) ** 0.5
    # print(d)
    return d


def get_score(piece_features, ok_pieces):
    score = 0
    # iterate over rules and assign score
    for rule in get_recommender_rules(piece_features, ok_pieces):
        score += rule
    return score


def get_recommender_rules(piece_features, ok_pieces):
    score = []
    pieces = query_db('id==%d' % ok_pieces)
    # print(ok_pieces)
    for rule in range(1, 3):
        if rule == 1:
            c1 = Color("%s" % str(piece_features["Color"].iloc[0])).rgb
            c2 = Color("%s" % str(pieces["Color"].iloc[0])).rgb
            ed = ColorDistance(np.array(c1), np.array(c2))
            if 0 <= ed <= 0.5:
                score.append(float("%.3f" % ed))

            else:
                m=contrast.rgb(c1, c2)
                score.append(float("%.3f" %(m*10)))


            # print(piece_features["Color"].iloc[0])
            # print(ok_pieces)

            # c1=Color('black').rgb
            # c2=Color('blue').rgb
            # print(np.array(c2))
            # print(np.array(c1))
            # m = ColorDistance(np.array(c1), np.array(c2))
            # print(m)
            # score.append(float("%.3f" % m))

        if rule == 2:
            # print(piece_features["Style"].iloc[0])
            # print(ok_pieces["Style"].iloc[0])
            s1 = str(piece_features["Style"].iloc[0])
            s2 = str(pieces["Style"].iloc[0])
            if s1 == s2:
                match = 100
            else:
                match = 0
            # print("ok2")

            score.append(match)

    # print(score)
    return score


#
# s = get_score(piece_features, ok_pieces)
# print(s)


def sort_pieces(ok_pieces, scores):
    # for i in range(len(ok_pieces)):
    # ok_pieces = ["sweater","Trauser", "shirt"]

    # columns = list(zip(*ok_pieces))
    #
    # print(columns[1])

    print("ok")
    ok_pieces, scores = (list(i) for i in zip(*sorted(zip(ok_pieces, scores))))
    # ok_pieces =[8,5,2]
    # ok_pieces=[query_db(8),query_db(2), query_db(5)]
    # print(ok_pieces)
    print(scores)
    return ok_pieces
    pass


def recommender(piece_id: int):
    piece_features = query_db('id==%d' % piece_id)
    # print(piece_features)
    # print(piece_features["Match"].iloc[0])
    ok_pieces = query_db('Match=="3" or Match != "%d" ' % int(piece_features["Match"].iloc[0]))
    # print(ok_pieces)
    scores = []
    # print([ok_pieces["id"].iloc[1],ok_pieces["id"].iloc[2],ok_pieces["id"].iloc[3],ok_pieces["id"].iloc[4],ok_pieces["id"].iloc[5]])
    for i in range(ok_pieces.shape[0]):
        scores.append(get_score(piece_features, ok_pieces["id"].iloc[i]))
    sorted_pieces = sort_pieces(ok_pieces, scores)  # sort ok_pieces according to scores list ...
    return sorted_pieces


print(recommender(3))
