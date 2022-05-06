import numpy as np
import matplotlib.pyplot as plt
## Código para SNR
def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)

## Gaussiana 2D em Python, assim como Matlab:
def matlab_style_gauss2D(shape,sigma):
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

## Dual Energy Window
def metodo_dew(imagem_jan1,imagem_jan2,constante): 
    c=np.multiply(imagem_jan2,constante)
    resultado=(imagem_jan1[:,:,:])-c[:,:,:]
    return resultado

## Mostrar imagem:

def mostrar_imagem2d(array,texto, variavel, x):
    plt.title(texto + str(variavel))
    plt.imshow(array[:, :], cmap=x)
    return plt.show()
    
def mostrar_imagem3d(array,texto, variavel, x):
    plt.title(texto + str(variavel))
    plt.imshow(array[variavel,:, :], cmap=x)
    return plt.show() 
