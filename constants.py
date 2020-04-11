from numpy import *
future=False
flip=True #True
type_ori = False #True # False
do_thirds = True
outlier_thr = 90



w2=pi/2
w1=pi/30

xxx_f=arange(0,pi,w1)
xxx2_f =xxx_f +w2/2 
xxx2_f = degrees(xxx2_f)

xxx_uf=arange(-pi,pi,w1)
xxx2_uf =xxx_uf +w2/2 
xxx2_uf = degrees(xxx2_uf)



if flip:
	xxx=xxx_f
else:
	xxx=xxx_uf



xxx2 =xxx +w2/2 #+w2/2
xxx2 = degrees(xxx2)
past_times=range(1,20)
