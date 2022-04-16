import sqlite3
import math
from colour import Color
import pandas as pd
import numpy as np
import wcag_contrast_ratio as contrast


def query_db(dataframe_query):
    con = sqlite3.connect('D:\language\project database\pyScript\dbtest  (1).db')

    con.commit()
    data = pd.read_sql('SELECT * FROM clothes', con)
    y = data.query(dataframe_query)

    return y
    pass


def colorDistance(rgb1, rgb2):
    rm = 0.5 * (rgb1[0] + rgb2[0])
    d = sum((2 + rm, 4, 3 - rm) * (rgb1 - rgb2) ** 2) ** 0.5

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

    for rule in range(1, 5):
        # Color rule
        if rule == 1:
            c1 = Color("%s" % str(piece_features["Color"].iloc[0])).rgb
            c2 = Color("%s" % str(pieces["Color"].iloc[0])).rgb
            ed = colorDistance(np.array(c1), np.array(c2))
            if 0 <= ed <= 0.5:
                score.append(int("%d" % 100))

            else:
                m = contrast.rgb(c1, c2)
                if m * 10 > 100:
                    score.append(int("%d" % 100))
                else:
                    score.append(int("%d" % math.floor(m * 10)))

        # Style rule
        if rule == 2:

            s1 = str(piece_features["Style"].iloc[0])
            s2 = str(pieces["Style"].iloc[0])
            if s1 == s2:
                match = 100
            else:
                match = 30

            score.append(match)

        # Print rule
        if rule == 3:
            p1 = str(piece_features["Print"].iloc[0])
            p2 = str(pieces["Print"].iloc[0])
            if p1 == p2 and p1 == "solid":
                s1 = str(piece_features["Style"].iloc[0])
                s2 = str(pieces["Style"].iloc[0])
                if s1 == "soiree" or s2 == "soiree":
                    score.append(80)
                else:
                    score.append(30)
            elif p1 == "solid" or p2 == "solid":
                score.append(80)
            elif p1 == "written on it" or p1 == "printed drawing" and p2 == "floral":
                score.append(50)

            else:
                score.append(30)
        # Fit rule
        if rule == 4:
            f1 = str(piece_features["Fit"].iloc[0])
            f2 = str(pieces["Fit"].iloc[0])
            if f1 == "slim" or f2 == "slim ":
                score.append(100)
            elif (f1 == "flowing swing" or f2 == "flowing swing") and (f1 == "regular" or f2 == "regular"):
                score.append(80)
            elif (f1 == "oversized" or f2 == "oversized") and (f1 == "regular" or f2 == "regular"):
                score.append(70)
            else:
                score.append(30)

    return score


def sort_pieces(ok_pieces, scores):
    pieces = []

    for i in range(ok_pieces.shape[0]):
        pieces.append(ok_pieces["id"].iloc[i])

    scores, pieces = (list(t) for t in zip(*sorted(zip(scores, pieces), reverse=True)))

    return pieces[:5]
    pass


def recommender(piece_id: int):
    piece_features = query_db('id==%d' % piece_id)
    # print("user select : \n",piece_features)

    if piece_features["Match"].iloc[0] == "3":
        ok_pieces = query_db('Match=="1" or Match=="2" ')
    else:
        ok_pieces = query_db('Match=="3" or Match != "%d" ' % int(piece_features["Match"].iloc[0]))

    scores = []

    for i in range(ok_pieces.shape[0]):
        scores.append(get_score(piece_features, ok_pieces["id"].iloc[i]))
    sorted_pieces = sort_pieces(ok_pieces, scores)  # sort ok_pieces according to scores list ...
    # for i in range(len(sorted_pieces)):
    #     sort_query = query_db('id==%d' % sorted_pieces[i])
    #     print("sorted pieces : \n",sort_query)
    return sorted_pieces


print(recommender(16))
