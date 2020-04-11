from __future__ import division
from numpy import *
from matplotlib.mlab import *
from scipy.io import loadmat
import sys
from scipy.stats import *
import seaborn as sns
sys.path.insert(0, './helpers/')
import statsmodels.formula.api as smf
import statsmodels.api as sm
from circ_stats import *
from helpers import *
from matplotlib  import gridspec
from constants import *
import warnings
warnings.filterwarnings("ignore")


font = { 'style': 'italic',
        'weight': 'bold',
        'fontsize': 15
        }

set_printoptions(precision=4)
sns.set_context("talk", font_scale=1.3)
sns.set_style("ticks")

def add_rep_to_axis(cues,report,bias,w):
    def decay(x,tau):
        return exp(-x*tau)
    report = report.copy()
    for axis in arange(0,2*pi,pi/2):
        idx = abs(circdist(cues,axis))<w
        report[idx] = circdist(report[idx],bias)
    return report 


w= 3
fig=figure(figsize=(5*w,2*w))
G1 = gridspec.GridSpec(2, 5)


# LOAD DATA

f = bz2.BZ2File('Data/all_studies_data.pickle')
[data_sets,all_computed,df_slopes,all_exp]=load(f)
f.close()
all_M=array(all_computed)[:,0]


f = bz2.BZ2File('Data/all_studies_data_unfolded.pickle')
[_,all_computed_unfolded,_,_]=load(f)
f.close()
all_M_uf=array(all_computed_unfolded)[:,0]

f=open("Data/simulated_many_to_stim.pickle")
subjects = load(f,allow_pickle=True)
f.close()

n_subjects = 100 #len(subjects)
all_sbias_folded = zeros([3,2,n_subjects,len(xxx_f)])
all_sbias_unfolded = zeros([3,2,n_subjects,len(xxx_uf)])

colors = sns.color_palette("tab10", len(data_sets))


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

        # idx = (curr_report>pi/5) & (curr_report<pi/2)
       	#curr_report = add_rep_to_axis(cues, curr_report, bias, 0.5)

        sys_bias = 0.2*cos(4*cues)
        prevstim_curr = circdist(prev_report,cues)
        # introduce bias
       	if bias > 0:
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

ax = subplot(G1[0, 2])

plot(c,degrees(err),".",color="gray",alpha=0.2)
plot([0,2*pi],[0,0],"white",linestyle="--")
sns.despine(bottom=True)
xticks([])
yticks([0])
title("simulated subjects",fontdict=font)
yticks([-90,0,90])
ylim((-164.19848918319892, 166.9099662462212))
tick_params(direction='in')


# PLOT FOR SYSTEMATIC ERROR FOSTER
f=open("Data/single_trials_foster.pickle")
[c,r,p]= load(f,allow_pickle=True)
c=concatenate(c)
r=concatenate(r)
p=concatenate(p)
s=loadmat("Data/colorwheel360.mat")
err = circdist(c,r)
color_i = array(degrees(c),dtype=int)
color_i[color_i == 360] = 0


ax = subplot(G1[1, 2])
title("Foster el al I (2017)",fontdict=font)
for i,ci in enumerate(c):
    ri = r[i]
    plot(ci,degrees(circdist(ci,ri)),".",color=s["fullcolormatrix"][color_i[i]]/255) 
plot([0,2*pi],[0,0],"white",linestyle="--")
sns.despine(bottom=True)
xticks([])
yticks([-90,0,90])
ylim(-90,90)
xlabel("stimulus \n (color)")
tick_params(direction='in')


# FOLDED / UNFOLDED SIMULATED DATA
ax = subplot(G1[0, 3])
title("unfolded",fontdict=font)
plot(xxx2_uf,mean(all_sbias_unfolded[0],1)[0],"k--",lw=3)
plot(xxx2_uf,mean(all_sbias_unfolded[1],1)[0],"k", alpha=0.5,lw=3)
plot(xxx2_uf,all_sbias_unfolded[1][0].T,"k-",lw=3,alpha=0.05)

plot(xxx2_uf,zeros(len(xxx2_uf)),"k--",alpha=0.5,lw=3)
plot([0,0],[-30,30],"k--",alpha=0.5)
ylim(-10,10)
tick_params(direction='in')
xlim(xxx2_uf[0],abs(xxx2_uf[0]))
xticks([-100,0,100],"")

ax = subplot(G1[0, 4])
title("folded",fontdict=font)
plot(xxx2_f,mean(all_sbias_folded[0],1)[0],"k--",lw=3,label="without bias")
plot(xxx2_f,mean(all_sbias_folded[1],1)[0],"k", alpha=0.5,lw=3,label="with bias")
# plot(xxx2_f,mean(all_sbias_folded[2],1)[0],"k-.", alpha=0.5,lw=3,label="low-pass")
plot(xxx2_f,zeros(len(xxx2_f)),"k--",alpha=0.5)
ylim(-1,2)
tick_params(direction='in')
xlim(xxx2_f[0],180)
xticks([50,100,150],"")
legend()
# xlabel(r"relative color of previous trial ($^\circ$)")
ylabel(r"error in current trial ($^\circ$)")
# savefig("figs4.svg",dpi=300)

# FOLDED / UNFOLDED FOSTER
ax = subplot(G1[1, 3])
plot(xxx2_uf,degrees(all_M_uf[-3]).T,'k',alpha=0.25)
plot_serial(all_M_uf[-3],"r",xk=xxx2_uf)
xlim(xxx2_uf[0],abs(xxx2_uf[0]))
plot([0,0],[-10,10],"k--",alpha=0.5)
ylim(-10,10)
tick_params(direction='in')
ylabel("")
xlabel("")

ax = subplot(G1[1, 4])
plot(xxx2,degrees(all_M[-3]).T,'k',alpha=0.25)
plot_serial(all_M[-3],"r")
xlim(xxx2[0],180)
ylim(-2,4)
ylabel("")
# xlabel("")
tick_params(direction='in')

# FOLDED ALL EXPERIMENTS
ax = subplot(G1[:, :2])
title("all experiments",fontdict=font)

plot_serial(array([mean(x,0) for x in all_M]),"k")
[plot(xxx2,degrees(sb),alpha=0.5,color=colors[i],label=all_exp[i],lw=3) for i,sb in enumerate([mean(x,0) for x in all_M])]
plot_sigs(array([mean(x,0) for x in all_M]),"k" ,upper=[2.9,3])
tick_params(direction='in')
xlim(xxx2[0],180)
xlabel("")
yticks([-2,-1,0,1,2,3])
ylim(-2,3)
legend()

# Only Cam-can
# ax = subplot(G1[:, :2])
# title("Cam-Can",fontdict=font)

# plot_serial(all_M[0],"k")
# plot_sigs(all_M[0],"k" ,upper=[3.9,4])
# tick_params(direction='in')
# xlim(xxx2[0],180)
# ylim(-1,2)
# xlabel("")
# yticks([-3,0,1,3])
# legend()


tp=array([ttest_1samp(a[:,0],0) for a in all_M])

for i,exp in enumerate(all_exp):
    print "%s: t(%i)=%.2f, p=%.2e; " % (exp, len(all_M[i])-1, tp[i,0], tp[i,1]),


ttest_1samp([mean(a[:,0],0) for a in all_M],0)
show()