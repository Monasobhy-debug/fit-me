import sqlite3
import pandas as pd
from PIL import Image

from colour import Color
import colorsys
from math import comb

import matplotlib.pyplot as plt

clothes = 'SELECT * FROM clothes'
style = 'SELECT * FROM Style'
printT = 'SELECT * FROM Print'
fit = 'SELECT * FROM Fit'


def query_db(dataframe_query, table):
    con = sqlite3.connect('D:\language\project database\pyScript\my_data.db')
    con.commit()
    data = pd.read_sql(table, con)
    return data.query(dataframe_query)


def get_score(piece_features, ok_pieces):
    score = 0
    # iterate over rules and assign score
    for rule in get_recommender_rules(piece_features, ok_pieces):
        score += rule
    return score


def get_recommender_rules(piece_features, ok_pieces):
    score = []
    pieces = query_db('id==%d' % ok_pieces, clothes)

    for rule in range(1, 5):
        # Color rule
        if rule == 1:
            color_score = color_matching(piece_features, pieces)
            # print(f'Color Matching Score: {color_score}')

            score.append(color_score)

        # Style rule
        if rule == 2:
            p1_style_id = piece_features["StyleId"].iloc[0]
            get_style1_by_id = query_db('id == %d' % p1_style_id, style)
            p1_style = get_style1_by_id["Style"].iloc[0]

            p2_style_id = pieces["StyleId"].iloc[0]
            get_style2_by_id = query_db('id == %d' % p2_style_id, style)
            p2_style = get_style2_by_id["Style"].iloc[0]

            score_style = query_db('Style == "%s" ' % p1_style, style)['%s' % p2_style].iloc[0]

            if score_style < 0.3:
                score.append(0)
            else:
                score.append(score_style)

        # Print rule
        if rule == 3:
            p1_print_id = piece_features["PrintId"].iloc[0]
            get_print1_by_id = query_db('id == %d' % p1_print_id, printT)
            p1_print = get_print1_by_id["Print"].iloc[0]

            p2_print_id = pieces["PrintId"].iloc[0]
            get_print2_by_id = query_db('id == %d' % p2_print_id, printT)
            p2_print = get_print2_by_id["Print"].iloc[0]

            score_print = query_db('Print == "%s" ' % p1_print, printT)['%s' % p2_print].iloc[0]

            if score_print < 0.3:
                score.append(0)
            else:
                score.append(score_print)
        # Fit rule
        if rule == 4:
            p1_fit_id = piece_features["FitId"].iloc[0]
            get_fit1_by_id = query_db('id == %d' % p1_fit_id, fit)
            p1_fit = get_fit1_by_id["Fit"].iloc[0]

            p2_fit_id = pieces["FitId"].iloc[0]
            get_fit2_by_id = query_db('id == %d' % p2_fit_id, fit)
            p2_fit = get_fit2_by_id["Fit"].iloc[0]

            score_fit = query_db('Fit == "%s" ' % p1_fit, fit)['%s' % p2_fit].iloc[0]

            if score_fit < 0.3:
                score.append(0)
            else:
                score.append(score_fit)

    return score


def sort_pieces(ok_pieces, scores):
    pieces = []

    for i in range(ok_pieces.shape[0]):
        pieces.append(ok_pieces["id"].iloc[i])

    scores, pieces = (list(t) for t in zip(*sorted(zip(scores, pieces), reverse=True)))

    return pieces[:5]
    pass


def recommender(piece_id: int):
    # quarry input piece by id
    piece_features = query_db('id==%d' % piece_id, clothes)
    # find the suitable pieces for the input piece
    if piece_features["Match"].iloc[0] == "3":
        ok_pieces = query_db('Match=="1" or Match=="2" ', clothes)
    else:
        ok_pieces = query_db('Match=="3" or Match != "%d" ' % int(piece_features["Match"].iloc[0]), clothes)

    scores = []

    for i in range(ok_pieces.shape[0]):
        scores.append(get_score(piece_features, ok_pieces["id"].iloc[i]))  # get score of every piece
    sorted_pieces = sort_pieces(ok_pieces, scores)  # sort ok_pieces according to scores list ...
    return sorted_pieces


def color_matching(piece_features, pieces):
    colors_test = []
    # convert color of piece_features to rgb color
    (r1, g1, b1) = Color("%s" % str(piece_features["Color"].iloc[0])).rgb
    # convert color of pieces to rgb color
    (r2, g2, b2) = Color("%s" % str(pieces["Color"].iloc[0])).rgb
    # convert rgb color of piece_features to hsv color
    (h1, s1, v1) = colorsys.rgb_to_hsv(r1, g1, b1)
    # convert rgb color of pieces to hsv color
    (h2, s2, v2) = colorsys.rgb_to_hsv(r2, g2, b2)
    # set range of HSV colors   (0-360, 0-100, 0-100)
    c1_hsv = (int(h1 * 360), int(s1 * 100), int(v1 * 100))
    colors_test.append(c1_hsv)
    c2_hsv = (int(h2 * 360), int(s2 * 100), int(v2 * 100))
    colors_test.append(c2_hsv)

    def get_color_matching_score(col_list):
        scores = [get_color_score1(col_list),
                  get_color_score2(col_list),
                  get_color_score3(col_list)]
        # print(f'Scores: {scores}')
        return max(scores)

    def get_color_score1(col_list):
        score = 0
        n = len(col_list)
        for i in range(n - 1):
            for j in range(i + 1, n):
                # hue of the first piece
                color_i_hue = col_list[i][0]
                # hue of the second piece
                color_j_hue = col_list[j][0]
                # difference between hue of the first piece and hue of the second piece
                abs_hue_diff = abs(color_i_hue - color_j_hue)
                # Hue fall within 30° on the color wheel
                if abs_hue_diff <= 30 or 360 - abs_hue_diff <= 30:
                    score += 1 / n

        return score

    def get_color_score2(col_list):
        score = 0
        n = len(col_list)
        c = comb(n, 2)  # without repetition color and without order
        # for any pair of colors (color_i, color_j) increase the score if they are complementary
        for i in range(n - 1):
            for j in range(i + 1, n):
                color_i_hue = col_list[i][0]
                color_i_hue_comp = color_i_hue + 180
                if color_i_hue_comp >= 360:
                    color_i_hue_comp -= 360
                a = color_i_hue_comp - 30
                color_j_hue = col_list[j][0]
                if 0 <= color_j_hue - a <= 60:
                    score += 1 / c

        return score

    def get_color_score3(col_list):
        score = 0
        n = len(col_list)
        '''
     Group1: Gray-ish (Black to White):-          HSV any         0-0.1       0-1
     Group2: Brown-ish (beige, khaki, etc.):-     HSV 30-40       0.1-1.0     0.6-0.9
     Group3: Navy-ish (levels of dark blue):-     HSV 230-250     0.8-1.0     0.2-0.4
     '''
        neutral_colors = []
        for i in range(len(col_list) - 1, -1, -1):
            col = col_list[i]
            h = col[0]
            s = col[1]
            v = col[2]
            if (0 <= h < 360 and 0 <= s <= 10 and 0 <= v <= 100) \
                    or (30 <= h <= 40 and 10 <= s <= 100 and 55 <= v <= 90) \
                    or (230 <= h <= 250 and 80 <= s <= 100 and 20 <= v <= 40):
                neutral_colors.append(col)
                col_list.pop()

        score += len(neutral_colors) / n  # percentage of neutral colors
        if len(col_list) > 1:
            score += (len(col_list) / n) * max(get_color_score1(col_list),
                                               get_color_score2(col_list))
        else:
            score += len(col_list) / n

        return score

    def create_test_image(colors):
        width = 100 * len(colors)
        height = 100

        img = Image.new(mode="RGB", size=(width, height), color=0)
        for i in range(len(colors)):
            color = colorsys.hsv_to_rgb(colors[i][0] / 360, colors[i][1] / 100, colors[i][2] / 100)
            color = tuple(round(i * 255) for i in color)
            for x in range(height):
                for y in range(height):
                    img.putpixel((x + 100 * i, y), color)
        img.show()
    create_test_image(colors_test)
    return get_color_matching_score(colors_test)


def display_output(piece_id, recommendations_id):
    # assume input was piece with ID = 41
    # piece_id = 16
    # assume recommendation was pieces with ID = [1, 8, 12, 14]
    # recommendations_id = [36, 25, 18, 26, 3]

    image_path = 'display_images/' + str(piece_id) + '.jpg'
    image = plt.imread(image_path)
    plt.subplot(2, len(recommendations_id), 1)
    plt.title('Input')
    fig = plt.imshow(image)
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)

    for i in range(len(recommendations_id)):
        image_path = 'display_images/' + str(recommendations_id[i]) + '.jpg'
        image = plt.imread(image_path)
        plt.subplot(2, len(recommendations_id), len(recommendations_id) + i + 1)
        plt.title('Rec ' + str(i + 1))
        fig = plt.imshow(image)
        plt.axis('off')
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)

    plt.show()


print(recommender(39))
display_output(39, recommender(39))
# create_test_image(colors_test)
