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
from constants import *
import warnings
warnings.filterwarnings("ignore")


font = { 'style': 'italic',
        'weight': 'bold',
        'fontsize': 15
        }

set_printoptions(precision=4)
sns.set_context("talk", font_scale=0.9)
sns.set_style("ticks")

f = bz2.BZ2File('Data/all_studies_data.pickle')
[data_sets,all_computed,df_slopes,all_exp]=load(f)
f.close()

# DO BUILD-UP
# wins = [75,200]
# w1=1
# All_f_err=[]
# All_err=[]
# All_outlier=[]

# for d_i,data_X in enumerate([data_sets[0],data_sets[5]]):
# 	if d_i<1: w = 75 
# 	else: w = 200
# 	all_f_err=[]
# 	all_err=[]
# 	all_outliers=[]
# 	outliers=[]
# 	for s, data in data_X.groupby("subject"):
# 		print s
# 		f_err=[]
# 		err=[]
# 		outliers=[]
# 		for beg in arange(data.trial.min(),data.trial.max()-w+w1,w1):
# 			end = beg+w
# 			idx=(data.trial>beg) & (data.trial<=end)
# 			idx_out = data[idx].error.abs()>radians(90)
# 			f_err.append(mean(data[idx & ~idx_out].flip_err))
# 			outliers.append(sum(idx_out))
# 			err.append(mean(data[idx & ~idx_out].error**2))

# 		all_f_err.append(f_err)
# 		all_err.append(err)
# 		all_outliers.append(outliers)

# 	All_f_err.append(all_f_err)
# 	All_err.append(all_err)
# 	All_outlier.append(all_outliers)

# f=open("all_err.pickle", "w")
# dump(All_err,f)
# f.close()


# f=open("all_outlier.pickle", "w")
# dump(All_outlier,f)
# f.close()

# f=open("all_f_err.pickle", "w")
# dump(All_f_err,f)
# f.close()

f=open("Data/all_f_err.pickle")
All_f_err = load(f,allow_pickle=True)
w_s=4
fig=figure(figsize=(2*w_s,3*w_s))


# CAM CAN
subplot(3,2,1)
title(all_exp[0],fontdict=font)
plot_serial(all_computed[0][1],"k",label="first third")
plot_serial(all_computed[0][3],"g",label="last third")
plot_sigs(all_computed[0][1],"k",all_computed[0][3],upper=[2*0.95,2])
legend()
tick_params(direction='in')
xlim(xxx2[0],180)
ylim(-1,2)

subplot(3,2,3)
all_f_err=degrees(All_f_err[0])
xxx_b = arange(len(all_f_err[0]))+75/2
ci_cc = array([bootstrap.ci(a,n_samples=1000,statfunction=nanmean) for a in array(all_f_err).T])
p_values = find(ci_cc[:,0]>0)
stderr_cc = array([bootstrap.ci(a,n_samples=1000,statfunction=nanmean,alpha=0.32) for a in array(all_f_err).T])
plot(xxx_b,nanmean(all_f_err,0),"k")
fill_between(xxx_b,stderr_cc[:,0],stderr_cc[:,1], color="k",alpha=0.5,label="95% C.I.")
plot(xxx_b,zeros(len(xxx_b)),"k--")
sig_bar(p_values,xxx_b,[1*0.95,1],"black")
xlim(xxx_b[0],xxx_b[-1])
xticks(arange(50,xxx_b[-1],50))
ylim(-1/3,1)
sns.despine()
tick_params(direction='in')
xlabel("time (trials)")

#FOSTER I
subplot(3,2,2)
title(all_exp[5],fontdict=font)
plot_serial(all_computed[5][1],"k")
plot_serial(all_computed[5][3],"g")
plot_sigs(all_computed[5][1],"k",all_computed[5][3],upper=[4*0.95,4])

tick_params(direction='in')
ylabel("")
xlabel("")
xlim(xxx2[0],180)
ylim(-2,4)

subplot(3,2,4)
all_f_err= array(list(map(degrees,All_f_err[1])))
i=min(map(len,all_f_err))
all_f_err = [a[:i] for a in all_f_err]
xxx_b = arange(len(all_f_err[0]))+100
ci_f = array([bootstrap.ci(a,n_samples=1000,statfunction=nanmean) for a in array(all_f_err).T])
p_values = find(ci_f[:,0]>0)
stderr_f = array([bootstrap.ci(a,n_samples=1000,statfunction=nanmean,alpha=0.32) for a in array(all_f_err).T])

sig_bar(p_values,xxx_b,[3*0.95,3],"black")
plot(xxx_b,mean(all_f_err,0),"k")
fill_between(xxx_b,stderr_f[:,0],stderr_f[:,1], color="k",alpha=0.5)
plot(xxx_b,zeros(len(xxx_b)),"k--")

xlim(xxx_b[0],xxx_b[-1])
ylim(-1,3)
xticks(arange(100,xxx_b[-1],200))
sns.despine()
ylabel("")
tick_params(direction='in')


subplot(3,1,3)
#subplot(3,1,1)


#
df_slopes["sbias_trend"]=degrees(df_slopes.sbias_trend)*100

p_values = df_slopes.groupby("experiment").sbias_trend.apply(lambda x: ttest_1samp(x,0)[1])

colors = sns.color_palette("tab10", len(all_computed))

sbias_trend = df_slopes.groupby("experiment").mean().sbias_trend.values
sbias_trend_std = df_slopes.groupby("experiment").std().sbias_trend.values
sbias_trend_count = sqrt(df_slopes.groupby("experiment").count().sbias_trend.values)

sbias_stderr= df_slopes.groupby("experiment").sbias_trend.apply(lambda a: bootstrap.ci(a,alpha=1-0.68,output="errorbar"))

s_idx = argsort(sbias_trend)[::-1]
p_values = append(p_values[s_idx],boot_test(sbias_trend,0))
sbias_trend=append(sbias_trend[s_idx],mean(sbias_trend))
colors=row_stack([array(colors)[s_idx],[0,0,0]])
all_exp = append(array(all_exp)[s_idx],"All")
sbias_stderr=sbias_stderr[s_idx]

bar(range(len(all_exp)),sbias_trend,color=colors)
errorbar(range(len(all_exp)-1),sbias_trend[:-1],concatenate(sbias_stderr.values,1),
	color="gray",fmt="none")

cis = bootstrap.ci(df_slopes.groupby("experiment").mean().sbias_trend.values,output="errorbar")
errorbar(len(all_exp)-1,sbias_trend[-1],cis,color="r")
plot(len(all_exp)-1,sbias_trend[-1],"ro",ms=5)
ylabel(r"slope ($^\circ$ / 100 trials)")
sns.despine()
xticks([])
plot([-1,9],[0,0],"k--")
xlim(-1,9)

show()