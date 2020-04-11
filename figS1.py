from __future__ import division
from numpy import *
from matplotlib.mlab import *
import sys
from scipy.stats import *
import seaborn as sns
from scikits import bootstrap
sys.path.insert(0, './helpers/')
from circ_stats import *
from helpers import *
from matplotlib  import gridspec
from constants import *

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Bitstream Vera Sans']

font = { 'style': 'italic',
        'weight': 'bold',
        'fontsize': 10
        }

set_printoptions(precision=4)
sns.set_context("talk", font_scale=0.9)
sns.set_style("ticks")


f = bz2.BZ2File('Data/all_studies_data.pickle')
[data_sets,all_computed,df_slopes,all_exp]=load(f)
f.close()
all_M=array(all_computed)[:,0]


f = bz2.BZ2File('Data/all_studies_data_unfolded.pickle')
[_,all_computed_unfolded,_,_]=load(f)
f.close()
all_M_uf=array(all_computed_unfolded)[:,0]

colors = sns.color_palette("tab10", len(data_sets))


w= 2.5
fig=figure(figsize=(8*w,3*w))

G1 =gridspec.GridSpec(3, 8)
G1.update(hspace=0.5,wspace=0.5) # set the spacing between axes.




for i, sub_unfold in enumerate(all_M_uf):
    print all_exp[i]
    if i > 0: 
        alpha=.1
    else:
        alpha=0.0
    ax = subplot(G1[0, i])
    title(all_exp[i],fontdict=font)
    sub_fold = all_M[i]
    xxx2_uf = degrees(arange(-pi,pi,w1) + w2/2)
    plot_serial(sub_unfold,colors[i],xk=xxx2_uf)
    plot(xxx2_uf,degrees(sub_unfold).T,'k',alpha=alpha)
    xlim(xxx2_uf[0],abs(xxx2_uf[0]))
    plot([0,0],[-10,10],"k--",alpha=0.5)
    tick_params(direction='in')
    ylim(-2,2)
    xlabel("\t\trelative color of previous trial ($^\circ$)".expandtabs())
    if i!= 2: xlabel("")
    if i>1: yticks([-10,0,10],"")
    if i > 0:
        ylim(-10,10)
        xticks([-100,0,100],"")
    sns.despine()
    ylabel("")

    ax = subplot(G1[1, i])
    plot_serial(sub_fold,colors[i],xk=xxx2_f)
    plot(xxx2_f,degrees(sub_fold).T,'k',alpha=alpha)
    ylabel("error in current trial ($^\circ$)",fontsize=20)
    xlabel("\t\trelative color of previous trial ($^\circ$)".expandtabs())
    xlim(xxx2_f[0],180)
    ylim(-1,1)
    if i!= 2: xlabel("")
    if i>1: yticks([-5,0,5],"")
    if i > 0:
        plot_sigs(array(sub_fold),"k" ,upper=[7.5*0.9,7.5])
        ylim(-7.5,7.5)
        xticks([50,100,150],"")
        ylabel("")
    else:
        plot_sigs(array(sub_fold),"k" ,upper=[0.9,1])
        ylim(-1,1)
    tick_params(direction='in')
    sns.despine()

    ax = subplot(G1[2, i])
    data = data_sets[i]
    if i==0: # subsample to only 100 subjects
        data = data[data.subject<100]
    plot((data.target+(2*pi)) % (2*pi),degrees(data.error),".",color="gray",alpha=max(alpha/10,0.005))
    plot([0,2*pi],[0,0],"white",linestyle="--")
    sns.despine(bottom=True)
    xticks([])
    yticks([-90,0,90])
    ylim(-150,150)
    xlabel("stimulus \n (color)")
    if i > 0:
        yticks([-90,0,90],"")
        xlabel("")
        ylabel("")


tick_params(direction='in')
sns.despine()
tight_layout()
show()