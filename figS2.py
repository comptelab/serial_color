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



font = { 'style': 'italic',
        'weight': 'bold',
        'fontsize': 15
        }

set_printoptions(precision=4)
sns.set_context("talk", font_scale=1.3)
sns.set_style("ticks")

f = bz2.BZ2File('Data/all_studies_data.pickle')
[data_sets,all_computed,df_slopes,all_exp]=load(f)
f.close()

colors = sns.color_palette("tab10", len(all_computed))


w= 8

fig=figure(figsize=(2*w,1*w))


G1 = gridspec.GridSpec(2, 4)
sbias_trend_all = df_slopes.groupby("experiment").mean().sbias_trend.values
for sbi,data in enumerate(all_computed):
	ax = subplot(G1[(sbi) // 4 , (sbi) % 4 ])
	title(all_exp[sbi],fontdict=font)
	#plot(mean(data[1],0))
	plot_serial(data[1],"k")
	# plot(xxx2,degrees(mean(data[2],0)),alpha=0.25,color=colors[sbi],lw=3) 
	plot_serial(data[3],"g")
	plot_sigs(data[1],"k",data[3],upper=[3.9,4])
	tick_params(direction='in')
	if (sbi != 0) & (sbi != 4):
		xlabel("")
		yticks(yticks()[0],[])
		ylabel("")
	xlim(xxx2[0],180)
	ylim(-2,4)
	#bar(50,degrees(sbias_trend_all[sbi])

show()