## Código desenvolvido para projeto de Pesquisa do Grupo de Investigação em Medicina Nuclear
## Mais informações no README

## Leitura de imagens com formato RAW 
## Imagens exemplo foram obtidas com o simulador GATE

## Importando bibliotecas já desenvolvidas

import numpy as np #biblioteca para leitura de arrays
import matplotlib.pyplot as plt #biblioteca para transformar matriz em imagem
import math, time, cv2, os, sys
import tomopy

## Importando bibliotecas próprias

import complementares as cm
import wiener
import chang

## MAIN ##

msize1=128
msize2=128
imagem = np.zeros ((256,msize1,msize2))
b = np.zeros ((256,msize1,msize2))
a = np.zeros ((256,msize1,msize2))
ImgPerf = np.zeros((128,128))

## Abrindo as imagens no formato array para que possamos manipulá-las

for o in range (1,129): 
    f = open('SPECTdew'+ str(o) +'.sin', 'rb')
    img_str = f.read()
    raw_image = np.frombuffer(img_str, np.uint16)
    k = np.size(raw_image)
    z = int(k)/128/128

    raw_image.shape = (int(z),128,128)

    ## Montando diferentes imagens
    if o>65:
        
       ## Imagem da janela principal
        b[0:int(z),:,:]=b[0:int(z),:,:]+raw_image[0:int(z),:,:]
        
    else: 
        
        ## Imagem da janela secundária
        a[0:int(z),:,:]=a[0:int(z),:,:]+raw_image[0:int(z),:,:]

    
## Método da Dual Energy Window
n=0.575

imagem = cm.metodo_dew(b,a,n)

w=cm.signaltonoise(imagem, axis=None)
print(w)


## Reconstrução 3D com Tomopy

angulos=np.linspace(0,2*math.pi,128)

rot_center=None

iteracoes =3

tamanho_subset=16

subset=imagem.shape[2]//tamanho_subset

reconstrucao_osem = tomopy.recon(imagem, angulos, center=rot_center, sinogram_order=False, algorithm='osem', num_iter=iteracoes, num_block=subset)


## Desenho da circunferência que define a imagem para Filtro de Chang.
recon = tomopy.circ_mask(reconstrucao_osem, axis=0, ratio=0.925) 

## Adição de outros filtros em cada imagem pós reconstrução
for l in range (0,128):
    
    cm.mostrar_imagem3d(reconstrucao_osem,"Osem e DEW", l, "gray")
    
    ## Método de Wiener
    GamaC = 5*10^4
    sigma = 0.75
    Img_Wiener=wiener.wiener(reconstrucao_osem,l,sigma,GamaC)
    cm.mostrar_imagem2d(Img_Wiener,"Osem,wiener e DEW", l, "gray")

    ## Filtro de Chang ##
    resol = 0.04
    constmi = 0.12
    
    Img_Chang=chang.chang(recon, l, resol, constmi)
        
    ## Divisão de arrays para implantação do filtro de chang:
    ImgCorFinal=np.multiply(Img_Chang,Img_Wiener)

    ## ### ###
    cm.mostrar_imagem2d(ImgCorFinal,"Img Final", l, "gray")
    
    if ((l>=39) and (l<=49)):
        ImgPerf=ImgPerf+ImgCorFinal
        
        
cm.mostrar_imagem2d(ImgPerf,"End", l, "gray")