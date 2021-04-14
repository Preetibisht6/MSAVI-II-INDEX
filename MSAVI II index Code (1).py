#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing Libraries

import rasterio
from rasterio import plot
import matplotlib.pyplot as plt
import numpy as np
import os
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


os.chdir('F:/Preeti/intern/loc 1 15 june/')


# In[3]:


##calculating MSAVI2 INDEX

def msavi(band4,band5):
    red = rasterio.open(band4) #red
    nir = rasterio.open(band5) #nir
    red_f = red.read(1).astype('float64')
    nir_f = nir.read(1).astype('float64')
    red_f[red_f==0] = np.nan
    nir_f[nir_f==0] = np.nan
    MSAVI2 = (2 * (nir_f + 1) - np.sqrt((2 * nir_f + 1)**2 - 8 * (nir_f - red_f)))/2
    return(MSAVI2,red)



    


# In[4]:


#collecting band name

bandname = []
folder = 'F:/Preeti/intern/image_data/'
for band in os.listdir(folder):
    filename = folder + band
    bandname.append(filename)
    
print(bandname[6])



# In[5]:


#exporting msavi image
out_fol = 'F:/Preeti/intern/output/'
file = 'msaviImage'
end = '.tiff'
out_file =[]
for i in range (0,6):
    MSAVI,band = msavi(bandname[i], bandname[i+6])
    output = out_fol + file + str(i) + end
    out_file.append(output)
    msaviImage = rasterio.open(output,'w',driver='Gtiff',
                          width=band.width, 
                          height = band.height, 
                          count=1, crs=band.crs, 
                          transform=band.transform, 
                          dtype='float64')
    msaviImage.write(MSAVI,1)
    msaviImage.close()
    


# In[6]:


#Plotting msavi2 index for location 1
fig , (ax1, ax2) = plt.subplots(1,2, figsize=(10,7))
msavi1 = rasterio.open('F:/Preeti/intern/output/msaviImage0.tiff')
plot.show((msavi1), ax=ax1, title='Location 1 Jan')
msavi2 = rasterio.open('F:/Preeti/intern/output/msaviImage1.tiff')
plot.show((msavi2),ax=ax2, title='Location 1 June')   


# In[7]:


#Finding MSAVI INDEX 2 Avg Value for Time graph

msavi_value = []
for i in range(0,6):
    msavi_f = rasterio.open(out_file[i])
    msavi_n = msavi_f.read(1).astype('float64')
    mean = (np.nanmin(msavi_n) + np.nanmax(msavi_n))/2
    msavi_value.append(mean)

print(msavi_value)
    
     
    
    
    


# In[11]:


#setting plotting parameter
Location = ['Loc-1 (JAN)', 'Loc-1 (JUNE)', 'Loc-2 (JAN)', 'Loc-2 (JUNE)', 'Loc-3 (JAN)', 'Loc-3 (JUNE)']
plt.figure(figsize=(10,7))
plt.style.use('seaborn')
axes=plt.axes()
axes.set_xlabel('Location',size=17,color='blue') 
axes.set_ylabel('MSAVI II INDEX',size=15,color='blue') 
axes.set_title('TIME GRAPH MSAVI II INDEX',size=20,color='blue')


axes.plot(Location, msavi_value, color='blue',linewidth=3, marker='D',markerfacecolor='red',
         markeredgewidth=2,markersize=7,markeredgecolor='red')


# In[ ]:




