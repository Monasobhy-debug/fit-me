import sqlite3
import math
from colour import Color
import pandas as pd
import numpy as np
import wcag_contrast_ratio as contrast

clothes = 'SELECT * FROM clothes'
style = 'SELECT * FROM Style'
printT = 'SELECT * FROM Print'
fit = 'SELECT * FROM Fit'


def query_db(dataframe_query, table):
    con = sqlite3.connect('D:\language\project database\pyScript\dbtest  (1).db')

    con.commit()
    data = pd.read_sql(table, con)
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
    # print(score)
    return score


def get_recommender_rules(piece_features, ok_pieces):
    score = []
    pieces = query_db('id==%d' % ok_pieces, clothes)

    for rule in range(1, 5):
        # Color rule
        # if rule == 1:
        #     c1 = Color("%s" % str(piece_features["Color"].iloc[0])).rgb
        #     c2 = Color("%s" % str(pieces["Color"].iloc[0])).rgb
        #     ed = colorDistance(np.array(c1), np.array(c2))
        #     if 0 <= ed <= 0.5:
        #         score.append(int("%d" % 100))
        #
        #     else:
        #         m = contrast.rgb(c1, c2)
        #         if m * 10 > 100:
        #             score.append(int("%d" % 100))
        #         else:
        #             score.append(int("%d" % math.floor(m * 10)))

        # Style rule
        if rule == 2:
            p1_style_id = piece_features["StyleId"].iloc[0]
            get_style1_by_id = query_db('id == %d' % p1_style_id, style)
            p1_style = get_style1_by_id["Style"].iloc[0]
            print(p1_style, "ok1")

            p2_style_id = pieces["StyleId"].iloc[0]
            get_style2_by_id = query_db('id == %d' % p2_style_id, style)
            p2_style = get_style2_by_id["Style"].iloc[0]
            print(p2_style, "ok2")

            score_style = query_db('Style == "%s" ' % p1_style, style)['%s' % p2_style].iloc[0]

            print(score_style)
            score.append(score_style)

        # Print rule
        if rule == 3:
            p1_print_id = piece_features["PrintId"].iloc[0]
            get_print1_by_id = query_db('id == %d' % p1_print_id, printT)
            p1_print = get_print1_by_id["Print"].iloc[0]
            print(p1_print, "ok1")

            p2_print_id = pieces["PrintId"].iloc[0]
            get_print2_by_id = query_db('id == %d' % p2_print_id, printT)
            p2_print = get_print2_by_id["Print"].iloc[0]
            print(p2_print, "ok2")

            score_print = query_db('Print == "%s" ' % p1_print, printT)['%s' % p2_print].iloc[0]

            print(score_print)
            score.append(score_print)
        # Fit rule
        if rule == 4:
            p1_fit_id = piece_features["FitId"].iloc[0]
            get_fit1_by_id = query_db('id == %d' % p1_fit_id, fit)
            p1_fit = get_fit1_by_id["Fit"].iloc[0]
            print(p1_fit, "ok1")

            p2_fit_id = pieces["FitId"].iloc[0]
            get_fit2_by_id = query_db('id == %d' % p2_fit_id, fit)
            p2_fit = get_fit2_by_id["Fit"].iloc[0]
            print(p2_fit, "ok2")

            score_fit = query_db('Fit == "%s" ' % p1_fit, fit)['%s' % p2_fit].iloc[0]

            print(score_fit)
            score.append(score_fit)

    return score


def sort_pieces(ok_pieces, scores):
    pieces = []

    for i in range(ok_pieces.shape[0]):
        pieces.append(ok_pieces["id"].iloc[i])

    scores, pieces = (list(t) for t in zip(*sorted(zip(scores, pieces), reverse=True)))
    print(scores[:5])
    return pieces[:5]
    pass


def recommender(piece_id: int):
    piece_features = query_db('id==%d' % piece_id, clothes)
    # print("user select : \n",piece_features)

    if piece_features["Match"].iloc[0] == "3":
        ok_pieces = query_db('Match=="1" or Match=="2" ', clothes)
    else:
        ok_pieces = query_db('Match=="3" or Match != "%d" ' % int(piece_features["Match"].iloc[0]), clothes)

    scores = []

    for i in range(ok_pieces.shape[0]):
        scores.append(get_score(piece_features, ok_pieces["id"].iloc[i]))
    sorted_pieces = sort_pieces(ok_pieces, scores)  # sort ok_pieces according to scores list ...
    # for i in range(len(sorted_pieces)):
    #     sort_query = query_db('id==%d' % sorted_pieces[i])
    #     print("sorted pieces : \n",sort_query)
    return sorted_pieces


print(recommender(31))
