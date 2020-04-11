from __future__ import division
from numpy import *
from matplotlib.mlab import *
import sys
from scipy.stats import *
import seaborn as sns
from scikits import bootstrap
from pickle import dump
sys.path.insert(0, './helpers/')
from circ_stats import *
from helpers import *
from matplotlib  import gridspec
from constants import *



font = { 'style': 'italic',
        'weight': 'bold',
        'fontsize': 20
        }

set_printoptions(precision=4)
sns.set_context("talk", font_scale=1.3)
sns.set_style("ticks")





# LOAD DATA


f=open("Data/simulated_many_to_stim.pickle")
subjects = load(f,allow_pickle=True)
f.close()

n_subjects = 200 #len(subjects)
all_sbias_folded = zeros([3,2,n_subjects,len(xxx_f)])
all_sbias_unfolded = zeros([3,2,n_subjects,len(xxx_uf)])

figure(figsize=(15,13))
for bias_type in range(3):
    C=[]
    CR=[]
    P = []

    C_ub=[]
    CR_ub=[]
    P_ub = []
    for bi,bias in enumerate([0,0.025,2]):
        for si,subject in enumerate(subjects[:n_subjects]):

            cues = subject[2]
            prev_cues = subject[0]
            prev_report = subject[1]
            curr_report = subject[3].copy()


            sys_bias = 0.4*cos(4*cues)
            prevstim_curr = circdist(prev_report,cues)
            # introduce bias
            if bias > 0:
                if bias_type==0:
                    curr_report = circdist(curr_report, 0.025)                
                elif bias_type==1:
                    curr_report = circdist(curr_report,-sys_bias)
                else:
                    curr_report = circdist(curr_report, 0.025)
                    curr_report = circdist(curr_report,-sys_bias)
                if bias > 1:
                     curr_report = rem_sys_err2(curr_report,cues,0.15)[0]
                else:
                    C.append(cues)
                    CR.append(curr_report)
                    P.append(prevstim_curr)
            else:
                C_ub.append(cues)
                CR_ub.append(curr_report)
                P_ub.append(prevstim_curr)


            prevstim_curr = circdist(prev_report,cues)
            prevreport_curr = circdist(prev_report,cues)
            # folded
            sbias_stim = compute_serial(curr_report,cues,prevstim_curr,xxx_f,True)
            sbias_report = compute_serial(curr_report,cues,prevreport_curr,xxx_f,True)
            all_sbias_folded[bi,0,si,:] = degrees(sbias_stim[2])
            all_sbias_folded[bi,1,si,:] = degrees(sbias_report[2])
            #unfolded
            sbias_stim = compute_serial(curr_report,cues,prevstim_curr,xxx_uf,False)
            sbias_report = compute_serial(curr_report,cues,prevreport_curr,xxx_uf,False)
            all_sbias_unfolded[bi,0,si,:] = degrees(sbias_stim[2])
            all_sbias_unfolded[bi,1,si,:] = degrees(sbias_report[2])

    # PLOT FOR SYSTEMATIC ERROR SIMULATED
    cr = concatenate(CR)
    c = concatenate(C)
    p = concatenate(P)
    err = circdist(cr,c)
    err_f = sign(p)*err

    subplot(3,3,1+3*bias_type)
    if bias_type == 0: 
        title("simulated subjects",fontdict=font)
    if bias_type == 1: 
        ylabel(r"error in current trial ($^\circ$)")
    if bias_type == 2:
        xlabel(r"stimulus (color)")
    plot(c,degrees(err),".",color="gray",alpha=0.2) 
    plot([0,2*pi],[0,0],"white",linestyle="--")
    xticks([])
    yticks([-90,0,90])
    ylim((-164.19848918319892, 166.9099662462212))
    tick_params(direction='in')

    sns.despine()


    # FOLDED / UNFOLDED SIMULATED DATA
    subplot(3,3,2+3*bias_type)
    if bias_type <1: 
        title("unfolded",fontdict=font)

    plot(xxx2_uf,mean(all_sbias_unfolded[0],1)[0],"k--",lw=3)
    plot(xxx2_uf,mean(all_sbias_unfolded[1],1)[0],"k", alpha=0.5,lw=3)
    plot(xxx2_uf,all_sbias_unfolded[1][0].T,"k-",lw=3,alpha=0.025)

    plot(xxx2_uf,zeros(len(xxx2_uf)),"k--",alpha=0.5,lw=3)
    plot([0,0],[-30,30],"k--",alpha=0.5)
    ylim(-10,10)
    tick_params(direction='in')
    xlim(xxx2_uf[0],abs(xxx2_uf[0]))
    xticks([-100,0,100],"")
    if bias_type == 2:
        xlabel("relative color of\nprevious trial"r" ($^\circ$)")
        xticks([-100,0,100],["100","0","-100"])
    subplot(3,3,3+3*bias_type)
    
    plot(xxx2_f,mean(all_sbias_folded[0],1)[0],"k--",lw=3,label="without bias")
    plot(xxx2_f,mean(all_sbias_folded[2],1)[0],"k-.", alpha=0.5,lw=3,label="low-pass (wo bias)")
    plot(xxx2_f,mean(all_sbias_folded[1],1)[0],"k", alpha=0.5,lw=3,label="with bias")
    plot(xxx2_f,zeros(len(xxx2_f)),"k--",alpha=0.5)
    ylim(-0.5,2)
    tick_params(direction='in')
    xlim(xxx2_f[0],180)
    xticks([50,100,150],"")
    yticks([0,1,2])
    if bias_type <1:
        title("folded",fontdict=font) 
        legend(frameon=False,loc="upper right",fontsize=15)
    if bias_type == 2:
        xlabel("relative color of\nprevious trial"r" ($^\circ$)")
        xticks([50,100,150],["50","100","150"])
    sns.despine()


tight_layout()
show()