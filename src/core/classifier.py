import numpy as np
import cv2

from src.core.base import dist
from src.core import features
from src.configs import DATABASE_CONF

def recognition(img, method, param, database, g_range, i_range):
    img_features, img_vec = features.HANDLER[method](img, param)

    rec_img = None
    rec_img_features = None
    d_min = float("inf")
    for g_i in range(*g_range):
        for im_i in range(*i_range):
            tmp_img = cv2.imread(DATABASE_CONF[database]['img_path'].format(g=g_i+1, im=im_i+1), -1)
            tmp_img_features, tmp_img_vec = features.HANDLER[method](tmp_img, param)
            if d := dist(img_vec, tmp_img_vec) < d_min:
                d_min = d ; rec_img = tmp_img ; rec_img_features = tmp_img_features
    return img_features, rec_img, rec_img_features
