import numpy as np

from src.core.base import dist
from src.core import features

def recognition(img, method, param, database_data, g_range, i_range):
    print(f"START 'Recognition'. Method '{method}'[{param}]")
    img_features, img_vec = features.HANDLER[method](img, param)

    rec_img = None
    rec_img_features = None
    d_min = float("inf")
    for g_i in range(*g_range):
        for im_i in range(*i_range):
            tmp_img = database_data[g_i][im_i]
            tmp_img_features, tmp_img_vec = features.HANDLER[method](tmp_img, param)
            if (d := dist(img_vec, tmp_img_vec)) < d_min:
                d_min = d ; rec_img = tmp_img ; rec_img_features = tmp_img_features
    print('END')
    return img_features, rec_img, rec_img_features
