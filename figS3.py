from __future__ import division
from numpy import *
from scipy.stats import *
from scikits import bootstrap
from constants import *
from pickle import load
import sys
import seaborn as sns
import pandas as pd
sys.path.insert(0, '/home/joaob/Dropbox/Neuro/mypytools/')
sys.path.insert(0, '/Users/joaobarbosa/Dropbox/Neuro/mypytools/')
from circ_stats import *
from helpers import *
import statsmodels.formula.api as smf
import statsmodels.api as sm
set_printoptions(precision=4)
sns.set_context("talk", font_scale=1)
sns.set_style("ticks")



def plot_r(x,r):
	y = r[0]*x + r[1]
	return y

f = bz2.BZ2File('Data/all_studies_data.pickle')
[data_sets,all_computed,df_slopes,all_exp]=load(f)
f.close()
all_M=array(all_computed)[:,0]



df_slopes.sbias_trend = degrees(df_slopes.sbias_trend)*100
df_slopes.err_trend = degrees(df_slopes.err_trend)*100


# build-up not correlated with tireness within experiment or task familiarity
R=[]
for di,(d,d_slopes) in enumerate(df_slopes.groupby("experiment")):
	r_e=linregress(d_slopes.sbias_trend,d_slopes.err_trend)
	r_o=linregress(d_slopes.sbias_trend,d_slopes.outlier_trend)
	R.append([r_e,r_o])


ci_e=bootstrap.ci(array(R)[:,0][:,2],output="errorbar")
ci_o=bootstrap.ci(array(R)[:,1][:,2],output="errorbar")


figure(figsize=(4,4))
plot(zeros(8),array(R)[:,0][:,2],"k.",ms=15)
plot(ones(8)*0.2,array(R)[:,1][:,2],"k.",ms=15)

plot(0,mean(array(R)[:,0][:,2]),"rs",ms=10,alpha=0.5)
plot(0.2,mean(array(R)[:,1][:,2]),"gs",ms=10,alpha=0.5)

errorbar(0,mean(array(R)[:,0][:,2]),yerr=ci_e.T,color="r",label="95% C.I.")
errorbar(0.2,mean(array(R)[:,1][:,2]),yerr=ci_o.T,color="green")
plot([-0.1,0.3],[0,0],"k--",alpha=0.5)
xticks([0,0.2],["error", "guesses"])
legend()
sns.despine()
tight_layout()
ylabel("R-values")
xlabel("correlation between trends")
# or task familiarity

savefig("average_corr_sbias_tiredness.svg")

figure(figsize=(15,15))
suptitle("sbias build-up correlation w/ guesses trend")
p_values=[]
for di,(d,d_slopes) in enumerate(df_slopes.groupby("experiment")):
	#p_values.append(linregress(d_slopes.sbias_trend,d_slopes.outlier_trend)[3])
	p_values.append(linregress(d_slopes.sbias_trend,d_slopes.outlier_trend)[3])
	subplot(4,4,di+1)
	title(all_exp[di])
	plot(d_slopes.sbias_trend,d_slopes.outlier_trend,"k.",ms=5)
	ticklabel_format(style='sci', axis='x', scilimits=(0,0))
	ticklabel_format(style='sci', axis='y', scilimits=(0,0))
	sns.despine()
	x,y=d_slopes.sbias_trend,d_slopes.outlier_trend
	r=linregress(x,y)
	plot(x,plot_r(x,r),"r")
	text(max(x)/2,max(y)/2,"r=%.2f\np=%.3f" % (r[2],r[3]),color="r")
	plot(mean(x),min(y),"^",ms=10,color="k")
	plot(min(x),mean(y),">",ms=10,color="k")

ylabel("guesses trend")
xlabel("sbias trend")
tight_layout()

# savefig("all_data_guess_corr.svg")

# figure(figsize=(15,7.5))
suptitle("sbias build-up correlation w/ error trend")
p_values=[]
for di,(d,d_slopes) in enumerate(df_slopes.groupby("experiment")):
	#p_values.append(linregress(d_slopes.sbias_trend,d_slopes.outlier_trend)[3])
	p_values.append(linregress(d_slopes.sbias_trend,d_slopes.err_trend)[3])
	subplot(4,4,8+di+1)
	title(all_exp[di])
	plot(d_slopes.sbias_trend,d_slopes.err_trend,"k.",ms=5)
	ticklabel_format(style='sci', axis='x', scilimits=(0,0))
	ticklabel_format(style='sci', axis='y', scilimits=(0,0))
	sns.despine()
	x,y=d_slopes.sbias_trend,d_slopes.err_trend
	r=linregress(x,y)
	plot(x,plot_r(x,r),"r")
	text(max(x)/2,max(y)/2,"r=%.2f\np=%.3f" % (r[2],r[3]),color="r")
	plot(mean(x),min(y),"^",ms=10,color="k")
	plot(min(x),mean(y),">",ms=10,color="k")

ylabel(r"$err^2$"" trend\n(deg"r"$^2$"" / 100 trials)")
xlabel("sbias trend\n(deg / 100 trials)")
tight_layout()

show()