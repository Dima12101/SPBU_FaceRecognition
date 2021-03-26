import cv2
import glob
import imageio
import numpy as np
import math
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
    X = img.copy().astype(np.int32)
    img_sc = np.zeros((m,n))
    for i in range(m):
        for j in range(n):
            img_sc[i, j] = np.sum(X[i*l:min((i+1)*l,M),j*l:min((j+1)*l,N)])
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

def spec_zigzag(C, p):
    return np.array([C[y+1-k,k] for y in range(p) for k in range(y, 0, -1)])

def get_features_spec_dft(img, P=20):
    '''Двумерное дискретное преобразование Фурье'''
    M, N = img.shape
    X = img.copy().astype(np.int32)
    w_sin = lambda L, S: math.sin(2*math.pi*L/S)
    w_cos = lambda L, S: math.cos(2*math.pi*L/S)
    F_cos_P_M = np.array([[w_cos(j*i, M) for j in range(M)] for i in range(P)])
    F_sin_P_M = np.array([[w_sin(j*i, M) for j in range(M)] for i in range(P)])
    F_cos_N_P = np.array([[w_cos(j*i, N) for j in range(P)] for i in range(N)])
    F_sin_N_P = np.array([[w_sin(j*i, N) for j in range(P)] for i in range(N)])
    C_real = np.dot(np.dot(F_cos_P_M, X), F_cos_N_P) - np.dot(np.dot(F_sin_P_M, X), F_sin_N_P)
    C_imag = np.dot(np.dot(F_cos_P_M, X), F_sin_N_P) + np.dot(np.dot(F_sin_P_M, X), F_cos_N_P)
    return np.sqrt(np.abs(C_real) + C_imag ** 2)

def get_features_spec_dct(img, P=20):
    '''Двумерное дискретное косинус-преобразование'''
    M, N = img.shape
    X = img.copy().astype(np.int32)
    t = lambda S, i, j: math.sqrt(2/S)*math.cos(math.pi*(2*j+1)*i/(2*S))
    T_P_M = np.array([[t(M, p, m) if p != 0 else 1/math.sqrt(M) for m in range(M)] for p in range(P)])
    T_N_P = np.array([[t(N, p, n)if p != 0 else 1/math.sqrt(N) for p in range(P)] for n in range(N)])
    return np.dot(np.dot(T_P_M, X), T_N_P)

def get_features_hist(img, BIN=16):
    M, N = img.shape
    top_hist = np.array([np.sum(np.array(img[:M//2,:] >= b*(256//BIN)) & np.array(img[:M//2,:] <= (b+1)*(256//BIN)-1)) for b in range(BIN)]) / M*N
    bottom_hist = np.array([np.sum(np.array(img[M//2:,:] >= b*(256//BIN)) & np.array(img[M//2:,:] <= (b+1)*(256//BIN)-1)) for b in range(BIN)]) / M*N
    return np.concatenate((top_hist, bottom_hist))
    # return np.histogram(img, bins=BIN, normed=True)

def get_features_grad(img, W=16):
    M, _ = img.shape
    X = img.copy().astype(np.int32)
    grads = []
    for x in range(W,M-W):
        top = X[x-W:x,:]
        bottom = np.flip(X[x:x+W,:], axis=1)
        grads.append(np.sqrt(np.sum((top - bottom)**2)))
    return np.array(grads)

if __name__ == '__main__':
    if DATABASE_NAME == 'ORL':
        source_img = cv2.imread(DATABASE_CONF[DATABASE_NAME]['img_path'].format(g=1, im=1), -1)
    else:
        source_img = imageio.imread(list(glob.glob(DATABASE_CONF[DATABASE_NAME]['img_path'].format(g=1)))[2])
    print(source_img)

    # features = get_features_sc_scale(source_img, l=4)
    # features = get_features_sc_ds(source_img, n=4)
    # features = get_features_spec_dft(source_img, P=20)
    # features = get_features_spec_dct(source_img, P=20)

    fig, ax = plt.subplots(2, 3)
    ax[0,0].imshow(source_img, cmap='gray')
    ax[0,1].imshow(get_features_spec_dft(source_img, P=20), cmap='gray')
    ax[0,2].imshow(get_features_spec_dct(source_img, P=20), cmap='gray')
    ax[1,0].imshow(get_features_sc_scale(source_img, l=4), cmap='gray')
    BIN=32
    ax[1,1].bar(list(range(2*BIN)), get_features_hist(source_img, BIN=BIN))
    grads = get_features_grad(source_img, W=10)
    ax[1,2].plot(list(range(len(grads))), grads)
    plt.show()
