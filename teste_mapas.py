
# coding: utf-8

# ## links
# https://app.dominodatalab.com/u/r00sj3/crimemaps/browse?
# 
# https://georgetsilva.github.io/posts/mapping-points-with-folium/
# 
# https://python-graph-gallery.com/391-radar-chart-with-several-individuals/
# 
# https://www.latlong.net/
# 
# https://www.kaggle.com/rachan/how-to-folium-for-maps-heatmaps-time-analysis
# 
# https://dzone.com/articles/building-a-data-science-portfolio-storytelling-wit
# 
# https://nbviewer.jupyter.org/github/python-visualization/folium/tree/master/examples/
# 
# https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0
# 
# https://python-graph-gallery.com/

# In[1]:


import urllib
import json
import os
import cufflinks as cf

import pandas as pd
from pandas.io.json import json_normalize

import seaborn as sns

import folium
from folium.plugins import MiniMap
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap

from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

# For Notebooks
init_notebook_mode(connected=True)

# For offline use
cf.go_offline()

get_ipython().run_line_magic('matplotlib', 'inline')


# In[11]:


coop = pd.read_excel('apoio_pontos.xlsx',sheet_name='coop')
ag = pd.read_excel('apoio_pontos.xlsx',sheet_name="Unidades")


# In[12]:


teste = json.load(open('poa.json'))


# In[13]:


with open('geojs-sc.json') as geojson_file:
    data = json.load(geojson_file)


# # Teste marker cooperativas
# ## Livre admissão e Segmentadas

# In[14]:


coops_mapa = folium.Map(location=[coop['latitude'].mean(),coop['longitude'].mean()], zoom_start=5)

for i in range(0,len(coop)):
    pop = str(coop.iloc[i]['COOP']) + ': ' + coop.iloc[i]['NOME']
    if (coop.iloc[i]['ASSOCIACAO']=="Segmentada"):
        folium.Marker([coop.iloc[i]['latitude'], coop.iloc[i]['longitude']], popup=pop,icon=folium.Icon(color='red', icon='info-sign')).add_to(coops_mapa)
    else:
        folium.Marker([coop.iloc[i]['latitude'], coop.iloc[i]['longitude']], popup=pop).add_to(coops_mapa)


# In[15]:


coops_mapa


# # Teste clustermarker

# In[17]:


"""schools_map = folium.Map(location=[full['lat'].mean(), full['lon'].mean()], zoom_start=10)
marker_cluster = folium.MarkerCluster().add_to(schools_map)
for name, row in full.iterrows():
    folium.Marker([row["lat"], row["lon"]], popup="{0}: {1}".format(row["DBN"], row["school_name"])).add_to(marker_cluster)
schools_map.create_map('schools.html')
schools_map


    if (coop.iloc[i]['A
    SSOCIACAO']=="Segmentada"):
        folium.Marker([coop.iloc[i]['latitude'], coop.iloc[i]['longitude']], popup=pop,icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
    else:
        folium.Marker([coop.iloc[i]['latitude'], coop.iloc[i]['longitude']], popup=pop).add_to(m)"""

coops_mapa = folium.Map(location=[coop['latitude'].mean(),coop['longitude'].mean()], zoom_start=5)
marker_cluster = MarkerCluster().add_to(coops_mapa)

for name, row in coop.iterrows():
    if(row['ASSOCIACAO']== 'Segmentada'):
        folium.Marker([row["latitude"], row["longitude"]], popup="{0}: {1}".format(row["COOP"], row["NOME"]),icon=folium.Icon(color='red', icon='info-sign')).add_to(marker_cluster)
    else:
        folium.Marker([row["latitude"], row["longitude"]], popup="{0}: {1}".format(row["COOP"], row["NOME"])).add_to(marker_cluster)
    
coops_mapa.save('cluster.html')


# In[19]:


coops_mapa = folium.Map(location=[coop['latitude'].mean(),coop['longitude'].mean()], zoom_start=5)
marker_cluster_RS = MarkerCluster().add_to(coops_mapa)
marker_cluster_SC = MarkerCluster().add_to(coops_mapa)
marker_cluster_MG = MarkerCluster().add_to(coops_mapa)

for name, row in coop.iterrows():
    if(row['UF'] == 'RS'):
        if(row['ASSOCIACAO'] == 'Segmentada'):
            folium.Marker([row["latitude"], row["longitude"]], popup="{0}: {1}".format(row["COOP"], row["NOME"]),icon=folium.Icon(color='red', icon='info-sign')).add_to(marker_cluster_RS)
        else:
            folium.Marker([row["latitude"], row["longitude"]], popup="{0}: {1}".format(row["COOP"], row["NOME"])).add_to(marker_cluster_RS)
    elif(row['UF'] == 'SC'):
        if(row['ASSOCIACAO'] == 'Segmentada'):
            folium.Marker([row["latitude"], row["longitude"]], popup="{0}: {1}".format(row["COOP"], row["NOME"]),icon=folium.Icon(color='red', icon='info-sign')).add_to(marker_cluster_SC)
        else:
            folium.Marker([row["latitude"], row["longitude"]], popup="{0}: {1}".format(row["COOP"], row["NOME"])).add_to(marker_cluster_SC)
    else:
        if(row['ASSOCIACAO'] == 'Segmentada'):
            folium.Marker([row["latitude"], row["longitude"]], popup="{0}: {1}".format(row["COOP"], row["NOME"]),icon=folium.Icon(color='red', icon='info-sign')).add_to(marker_cluster_MG)
        else:
            folium.Marker([row["latitude"], row["longitude"]], popup="{0}: {1}".format(row["COOP"], row["NOME"])).add_to(marker_cluster_MG)
coops_mapa.save('cluster2.html')


# # Teste Heatmap

# In[20]:


def map_points(df, lat_col='latitude', lon_col='longitude', zoom_start=11,                 plot_points=False, pt_radius=15,                 draw_heatmap=False, heat_map_weights_col=None,                 heat_map_weights_normalize=True, heat_map_radius=15):
    """Creates a map given a dataframe of points. Can also produce a heatmap overlay
    Arg:
        df: dataframe containing points to maps
        lat_col: Column containing latitude (string)
        lon_col: Column containing longitude (string)
        zoom_start: Integer representing the initial zoom of the map
        plot_points: Add points to map (boolean)
        pt_radius: Size of each point
        draw_heatmap: Add heatmap to map (boolean)
        heat_map_weights_col: Column containing heatmap weights
        heat_map_weights_normalize: Normalize heatmap weights (boolean)
        heat_map_radius: Size of heatmap point
    Returns:
        folium map object
    """

    ## center map in the middle of points center in
    middle_lat = df[lat_col].median()
    middle_lon = df[lon_col].median()

    curr_map = folium.Map(location=[middle_lat, middle_lon],tiles = "Stamen Toner",
                          zoom_start=zoom_start)

    # INCLUI AGENCIAS
    if plot_points:
        for _, row in df.iterrows():
            folium.CircleMarker([row[lat_col], row[lon_col]],
                                radius=pt_radius,
                                popup="Agencia:{0} / Cidade:{1} / Evento:{2}".format(row['Chave'],row['Cidade'],row['Mapa']),
                                fill_color="#3db7e4", # divvy color
                               ).add_to(curr_map)
            """folium.Marker([row[lat_col], row[lon_col]]
                          , popup="Agencia:{0} / Cidade:{1} / Evento:{2}".format(row['Chave'],row['Cidade'],row['Mapa'])
                          ,icon=folium.Icon(color='red', icon='info-sign')).add_to(curr_map)"""

    # add heatmap
    if draw_heatmap:
        # convert to (n, 2) or (n, 3) matrix format
        if heat_map_weights_col is None:
            stations = zip(df[lat_col], df[lon_col])
        else:
            # if we have to normalize
            if heat_map_weights_normalize:
                df[heat_map_weights_col] =                     df[heat_map_weights_col] / df[heat_map_weights_col].sum()

            stations = zip(df[lat_col], df[lon_col], df[heat_map_weights_col])

        curr_map.add_child(HeatMap(stations, radius=heat_map_radius))

    return curr_map.save('heat.html')


# In[ ]:


incidentes.head()


# In[21]:


incidentes = pd.read_excel('Incidentes Central Sicredi Sul-Sudeste 2018.xlsx')


# In[23]:


map_points(incidentes,draw_heatmap=True,zoom_start=5)

