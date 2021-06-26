#!/usr/bin/env python
# coding: utf-8

# In[3]:


import ee
from ipygee import*


# In[4]:


ee.Authenticate()


# In[5]:


# Initialize the library.
ee.Initialize()


# In[6]:


##Importing Library

import matplotlib.pyplot as plt
import folium


# In[65]:


#setting for location

Loc_1 =  ee.Geometry.Polygon(
[[[75.45157492160797,30.634404129904425],
[75.4524278640747,30.63372099804389],
[75.45236885547638,30.634399514164798],
[75.45157492160797, 30.634404129904425]]])

Loc_2 =  ee.Geometry.Polygon(
[[[85.85622847080231, 26.09425078918021], 
[85.85590660572052, 26.093581136401006], 
[85.85663080215454, 26.09337879451938 ], 
[85.85686147212981, 26.094009907326967], 
[85.85622847080231, 26.09425078918021]]])


Loc_3 =  ee.Geometry.Polygon(
[[[78.66571158170699, 17.66869116558751], 
[78.6662346124649, 17.6686911655875], 
[78.6662346124649, 17.66929686130703], 
[78.66571158170699, 17.66929686130703], 
[78.66571158170699, 17.66869116558751]]])


# In[8]:


##Calculating the Msavi II Index with mean

def Msavi2(aoi):
    Data =  ee.ImageCollection("LANDSAT/LC08/C01/T1_SR").filterDate('2020-01-01', '2020-6-1').filterBounds(aoi)
    Data_mean = Data.mean().divide(10000)
    msavi_2 = (Data_mean.select('B5').multiply(2).add(1).subtract(Data_mean.select('B5').multiply(2).add(1).pow(2)
     .subtract(Data_mean.select('B5').subtract(Data_mean.select('B4')).multiply(8)).sqrt()
      ).divide(2))
    return msavi_2


####Calculating the Msavi II Index with selecting one
'''''def Msavi2(aoi):
    Data =  ee.ImageCollection("LANDSAT/LC08/C01/T1_SR").filterDate('2020-01-01', '2020-6-1').filterBounds(aoi).first()
    msavi_2 = (Data.select('B5').multiply(2).add(1).subtract(Data.select('B5').multiply(2).add(1).pow(2)
     .subtract(Data.select('B5').subtract(Data.select('B4')).multiply(8)).sqrt()
      ).divide(2))
    return msavi_2'''''
    


# In[9]:


msavi_index_loc_1 = Msavi2(Loc_1)
msavi_index_loc_2 = Msavi2(Loc_2)
msavi_index_loc_3 = Msavi2(Loc_3)


# In[10]:


# Define a method for displaying Earth Engine image tiles to folium map.
def add_ee_layer(self, ee_image_object, vis_params, name):
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
    tiles = map_id_dict['tile_fetcher'].url_format,
    attr = 'Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
    name = name,
    overlay = True,
    control = True
  ).add_to(self)

# Add EE drawing method to folium.
folium.Map.add_ee_layer = add_ee_layer

# Set visualization parameters.
vis_params = {
  'min': -1,
  'max': 1,
  'palette': ['red', 'yellow', 'green']}

# Create a folium map object.
my_map = folium.Map(location=[30, 75], zoom_start=4)

# Add the elevation model to the map object.
my_map.add_ee_layer(msavi_index_loc_1, vis_params, 'MSAVI INDEX - Loc-1')
my_map.add_ee_layer(msavi_index_loc_2, vis_params, 'MSAVI INDEX - Loc-2')
my_map.add_ee_layer(msavi_index_loc_3, vis_params, 'MSAVI INDEX - Loc-3')

# Add a layer control panel to the map.
my_map.add_child(folium.LayerControl())

# Display the map.
display(my_map)


# In[ ]:


##For exporting Image

def export(Image,aoi):
    task = ee.batch.Export.image.toDrive(image=Image,
                                     description='Image',
                                     scale=30,
                                     region=aoi,
                                     crs='EPSG:4326',
                                     fileFormat='GeoTIFF')
    task.start()


# In[61]:


##MSavi II for image Collection

def Msavichart(img):
    msavi_C = (img.select('B5').multiply(2).add(1).subtract(img.select('B5').multiply(2).add(1).pow(2)
     .subtract(img.select('B5').subtract(img.select('B4')).multiply(8)).sqrt()
      ).divide(2))
    return img.addBands(msavi_C.rename('MSAVI II'))


# In[71]:


##Finction for Plotting time series

def chartPlot(aoi):
    Data =  ee.ImageCollection("LANDSAT/LC08/C01/T1_SR").filterDate('2020-01-01', '2020-06-10').filterBounds(aoi)
    Data = Data.map(Msavichart)

    plot_msavi2 = chart.Image.series(**{
       'imageCollection': Data, 
        'region': aoi,
        'bands': ['MSAVI II'],
        'reducer': ee.Reducer.mean(),
        'xProperty': 'system:time_start',
        'scale': 30,
        'label_properties':['MSAVI'],
        'title': 'MSAVI2 time series'})
    return plot_msavi2



# In[72]:


chartPlot(Loc_1).renderWidget(width='75%')


# In[73]:


chartPlot(Loc_2).renderWidget(width='75%')


# In[74]:


chartPlot(Loc_3).renderWidget(width='75%')


# In[ ]:




