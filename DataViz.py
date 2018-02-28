
#[paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Ferreira_Fisher_Sample_Oriented_Tasks.pdf) the authors describe the challenges users face when trying to make judgements about probabilistic data generated through samples. As an example, they look at a bar chart of four years of data (replicated below in Figure 1). Each year has a y-axis value, which is derived from a sample of a larger dataset. For instance, the first value might be the number votes in a given district or riding for 1992, with the average being around 33,000. On top of this is plotted the 95% confidence interval for the mean (see the boxplot lectures for more information, and the yerr parameter of barcharts).
#Implement the bar coloring as described in the paper,
#where the color of the bar is actually based on the amount of data covered
#(e.g. a gradient ranging from dark blue for the distribution being certainly below this y-axis, to white if the value is certainly contained,
#to dark red if the value is certainly not contained as the distribution is above the axis).

import pandas as pd
import numpy as np

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
df.T.describe()


# In[3]:


from scipy.stats import sem
means = df.mean(axis=1)
#set the confidence interval to 95%
ci95 = 1.96 * df.sem(axis=1)


# In[23]:


from scipy.stats import sem
import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import matplotlib.cm as cm

plt.figure()

# soften all labels by turning grey
plt.xlabel('Year', alpha=0.7)
plt.title('A bar chart with 95% confidence intervals representing the mean value over a dataset', alpha=0.7)
# clean up ticks (both axes)
plt.xticks(df.index, rotation='45')
#user input a threshold and plot it on top
threshold=input('Enter a Threshold: ')
try: threshold = int(threshold)
except:
    print('Input must be a number. Defaulting to 42000')
    threshold = 42000
plt.axhline(y = threshold, color = 'grey', alpha = 0.8)
#set custom color palette
cm1 = mcol.LinearSegmentedColormap.from_list("Likelihood",["darkblue", "white", "darkred"])
cpick = cm.ScalarMappable(cmap=cm1)
cpick.set_array([])
# plot bars with color representing likelihood of threshold in set for a plotted year
percentages = []
low = means - ci95
high = means + ci95
percentages = ((high-threshold)/(high-low))*100
for i in range (1992,1996):
    if percentages.loc[i]>100: percentages.loc[i] = 100
    if percentages.loc[i]<0: percentages.loc[i] = 0
cpick.to_rgba(percentages)
# Plot bars with color representing likelihood of threshold in set for a plotted year including viz of scale
_ = plt.bar(df.index, means, yerr=ci95, capsize=10,color = cpick.to_rgba(percentages), align='center')
plt.colorbar(cpick, ticks=None, drawedges=False, label='Chance of Data Set Covered at Given Threshold')
plt.show()

