import numpy as np
import complementares as cm
import matplotlib.pyplot as plt

def wiener (reconstrucao_osem,l,sigma,GamaC):
    psf = reconstrucao_osem[l,:,:]
    r = np.amax(psf)

    ## Normalização das imagens reconstruídas

    psfnorm = np.divide(psf,r)

    psf_fft = np.fft.fftshift(np.fft.fft2(psfnorm))

    ## Produção do filtro gaussiano

    psfgauss=cm.matlab_style_gauss2D(shape=[128,128],sigma=sigma)

    ## Aplica a segunda Transformada de Fourier e determina seu centro como sendo o zero

    psfgaussfft=np.fft.fftshift(np.fft.fft2(psfgauss))

    ## Aplicação das fórmulas do Método de Wiener

    Im = psf_fft[:,:]
    Hestrela=np.conj(psfgaussfft)
    Hquad=abs(np.multiply(psfgaussfft,psfgaussfft))
    U=Hquad+GamaC
    T=np.divide(Hestrela,U)
    Im=np.multiply(Im,T)
    new_=Im

    new_=np.fft.ifft2(np.fft.ifftshift(new_))
    new_2=np.divide(new_,np.amax(new_))
    new_final=np.fft.ifftshift(new_2)
    new_final=new_final.real
    
    return new_final