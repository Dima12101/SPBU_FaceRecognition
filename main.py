import cv2
import glob
import imageio
import numpy as np
import matplotlib.pyplot as plt

DATABASE_CONF = {
    'ORL': {
        'number_group': 40,
        'number_img': 10,
        'img_path': './data/ORL/s{g}/{im}.pgm'
    },
    'Yale_faces': {
        'number_group': 15,
        'number_img': 11,
        'img_path': './data/Yale_faces/subject{g}.*'
    },
}

DATABASE_NAME = 'ORL' # Yale_faces

def get_features_sc_scale(img, l=2):
    M, N = img.shape
    m, n = M // l, N // l
    img_sc = np.zeros((m,n))
    for i in range(m):
        for j in range(n):
            img_sc[i, j] = np.sum(img[i*l:min((i+1)*l,M),j*l:min((j+1)*l,N)])
    return img_sc
    # return np.asarray(img_sc).reshape(-1)

# TODO: Wavelet transform

def get_features_sc_ds(img, n=2):
    img_sc = img.copy()
    is_axis_h = True
    for _ in range(n):
        img_sc = img_sc[0:-1:2, :] if is_axis_h else img_sc[:, 0:-1:2]
        is_axis_h = not is_axis_h
    return img_sc



if __name__ == '__main__':
    if DATABASE_NAME == 'ORL':
        source_img = cv2.imread(DATABASE_CONF[DATABASE_NAME]['img_path'].format(g=1, im=1), -1)
    else:
        source_img = imageio.imread(list(glob.glob(DATABASE_CONF[DATABASE_NAME]['img_path'].format(g=1)))[2])
    print(source_img)

    # 
    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(source_img, cmap='gray')
    # ax[1].imshow(get_features_sc_scale(source_img, l=4), cmap='gray')
    ax[1].imshow(get_features_sc_ds(source_img, n=4), cmap='gray')
    # cv2.waitKey(0)
    plt.show()
