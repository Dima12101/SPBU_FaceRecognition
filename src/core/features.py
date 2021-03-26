import numpy as np
import math

from .base import dist 

def scale(img, l=2):
    '''Экстракция признаков методом Scale'''
    M, N = img.shape
    m, n = M // l, N // l
    X = img.copy().astype(np.int32)
    img_sc = np.zeros((m,n))
    for i in range(m):
        for j in range(n):
            img_sc[i, j] = np.sum(X[i*l:min((i+1)*l,M),j*l:min((j+1)*l,N)])
    return img_sc, np.asarray(img_sc).reshape(-1)

# TODO: Wavelet transform

# def sc_ds(img, n=2):
#     img_sc = img.copy()
#     is_axis_h = True
#     for _ in range(n):
#         img_sc = img_sc[0:-1:2, :] if is_axis_h else img_sc[:, 0:-1:2]
#         is_axis_h = not is_axis_h
#     return img_sc

def _spec_zigzag(C, P):
    return np.array([C[y+1-k,k] for y in range(P) for k in range(y, 0, -1)])

def spec_dft(img, P=20):
    '''Экстракция признаков методом DFT (Двумерное дискретное преобразование Фурье)'''
    # return np.abs(np.fft.fft2(img)[0:P, 0:P])
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
    C = np.sqrt(np.abs(C_real) + C_imag ** 2)
    return C, _spec_zigzag(C, P)
    

def spec_dct(img, P=20):
    '''Экстракция признаков методом DCT (Двумерное дискретное косинус-преобразование)'''
    M, N = img.shape
    X = img.copy().astype(np.int32)
    t = lambda S, i, j: math.sqrt(2/S)*math.cos(math.pi*(2*j+1)*i/(2*S))
    T_P_M = np.array([[t(M, p, m) if p != 0 else 1/math.sqrt(M) for m in range(M)] for p in range(P)])
    T_N_P = np.array([[t(N, p, n)if p != 0 else 1/math.sqrt(N) for p in range(P)] for n in range(N)])
    C = np.dot(np.dot(T_P_M, X), T_N_P)
    return C, _spec_zigzag(C, P)

def hist(img, BIN=16):
    '''Экстракция признаков методом Hist (Гистограмма яркости)'''
    # return np.histogram(img, bins=BIN, normed=True)
    M, N = img.shape
    top_hist = np.array([np.sum(np.array(img[:M//2,:] >= b*(256//BIN)) & np.array(img[:M//2,:] <= (b+1)*(256//BIN)-1)) for b in range(BIN)]) / M*N
    bottom_hist = np.array([np.sum(np.array(img[M//2:,:] >= b*(256//BIN)) & np.array(img[M//2:,:] <= (b+1)*(256//BIN)-1)) for b in range(BIN)]) / M*N
    h = np.concatenate((top_hist, bottom_hist))
    return (np.array(range(2*BIN)), h), h
    

def grad(img, W=16):
    '''Экстракция признаков методом Gradient'''
    M, _ = img.shape
    X = img.copy().astype(np.int32)
    grads = []
    for x in range(W,M-W):
        top = X[x-W:x,:]
        bottom = np.flip(X[x:x+W,:], axis=1)
        grads.append(dist(top, bottom))
    grads = np.array(grads)
    return (np.array(range(len(grads))), grads), grads

HANDLER = {
    scale.__name__: scale,
    hist.__name__: hist,
    grad.__name__: grad,
    spec_dft.__name__: spec_dft,
    spec_dct.__name__: spec_dct
}