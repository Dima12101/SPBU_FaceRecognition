import glob
import cv2
import imageio
from src.configs import DATABASE_CONF

def load(database):
    database_data = []
    for g_i in range(DATABASE_CONF[database]['number_group']):
        database_group = []
        for im_i in range(DATABASE_CONF[database]['number_img']):
            if database == 'ORL':
                img = cv2.imread(DATABASE_CONF['ORL']['img_path'].format(g=g_i+1, im=im_i+1), -1)
            else:
                name_group = g_i+1 if g_i+1 >= 10 else f'0{g_i+1}'
                img = imageio.imread(list(glob.glob(DATABASE_CONF['Yale_faces']['img_path'].format(g=name_group)))[im_i])
            database_group.append(img)
        database_data.append(database_group)  
    return database_data