import numpy as np
import cv2
import math

## Filtro de Chang ##

def chang(recon,cte,resol,constmi):
    superficie = np.zeros ((128,128))
    Dfinal = np.zeros ((128,128))
    L = np.zeros((128,128))

    for i in range (0,128):
        
        for j in range (0,128):

            value = recon[cte,i,j]
            
            if value == 0:
                superficie[i,j]=0

            else:
                superficie[i,j]=1


    ## Desenho do Filtro de Chang. 
    ## Desenho das distâncias

    for s in range (0,128):
        
        for t in range (0,128):

            value = superficie[s,t]

            if value == 1:
                
                for k in range (0,127):

                    value1=superficie[k,t]
                    value2=superficie[k+1,t]

                    if ((value1==0) and (value2==1)):

                        dborda=k+1
                        break

                dpixel = s
                dfinal = abs(dborda-dpixel)/128

                dfinalreal = resol*dfinal

                Dfinal[s,t]=dfinalreal

            else:

                Dfinal[s,t]=0

        ## Rotação com soma do Filtro de Chang em 360 graus.
        ## Assim, temos uma circunferência com degradê em 360 graus.

    for m in range (0,360):
        row,col = Dfinal.shape
        center=tuple(np.array([row,col])/2)
        rot_mat = cv2.getRotationMatrix2D(center=center,angle=m,scale=1.0)
        new_image = cv2.warpAffine(Dfinal, rot_mat, (col,row))
        L[:,:]=L[:,:]+new_image

    ## implantação do Filtro de Chang na imagem escolhida

    Nang=128
    sizeRec=128
    dist=L[:,:]
    mi=round(sizeRec/2)
    mj=round(sizeRec/2)
    theta = np.linspace(0,360,360)
    C = np.zeros((128,128))

    ## uso da fórmula de Chang

    for u in range (0,sizeRec):

        for h in range (0,sizeRec):

            Somdist=0
            value=dist[u,h]


            if value > 0:

                for y in range (0,128):

                    factorexp = (-1)*constmi*dist[u,h]
                    somdist = math.exp(factorexp)
                    Somdist = Somdist + somdist

                c = Somdist*(1/128)

                C[u,h] = (1/c)

            else: 

                C[u,h]=1
                
    return C[:,:]
