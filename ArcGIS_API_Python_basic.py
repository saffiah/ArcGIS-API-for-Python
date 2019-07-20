# coding: utf-8

# This script explores basic functionality of the ArcGIS API for Python
# It is a jupyter notebook project that has been downloaded into a stand-alone python script.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Summary: This script reads in a feature layer of generators within California. It it intersects
# 		this layer with the polygon of District 7 (Los Angeles and Ventura Counties).
# 		I then load the result in a webmap in my organizational ArcGIS Online account.
# 		Ultimately, I would have liked to apply the same rendering or drawing info from the original
#		data on to my new web map. 

# In[49]:


from arcgis.gis import GIS
import arcgis
from arcgis.geometry import filters

gens = arcgis.features.FeatureLayer("https://services3.arcgis.com/bWPjFyq029ChCGur/arcgis/rest/services/Generator/FeatureServer/0/")
ct_dist = arcgis.features.FeatureLayer("http://services2.arcgis.com/hvBNq5JdIeoqdAq9/arcgis/rest/services/CaltransDistricts/FeatureServer/0/")
dist7 = ct_dist.query(where="DIST=7")
origRendInfo = gens.properties.drawingInfo #good to use when finally drawing geometries!
print(type(origRendInfo))
# print(origRendInfo)
print(origRendInfo['renderer'])

polygon = dist7.features[0].geometry
#create a geometry object from the geometry property of the json object
geomObj = arcgis.geometry.Geometry(polygon)
print(geomObj.type)

gensD7 = gens.query(geometry_filter=filters.intersects(geomObj))
print(len(gensD7),type(gensD7),type(gens))
print(gensD7.features[0])

gensD7_Layer = arcgis.features.FeatureCollection(gensD7.to_dict())
print(type(gensD7_Layer)) 


# In[53]:


my_gis = GIS()
map1 = my_gis.map()
map1.center = [34.2,-118.5]
map1.zoom = 9

map1.add_layer(gensD7,origRendInfo['renderer'])
#map1.add_layer(dist7)
map1


# In[17]:


print(gensD7.drawing_info)


# In[4]:


#Make a connection to my portal
gis2 = GIS("https://caltrans.maps.arcgis.com","Saffia.Hossainzadeh")


# In[6]:

# Create a web map of this new data:
# Generators from CEC intersected by District 7's polygon
from arcgis.mapping import WebMap, WebScene
wm = WebMap()
wm.definition


# In[7]:


wm.add_layer(gensD7)


# In[10]:


web_map_properties = {'title':'Generators within District 7',
                     'snippet': 'This map service shows the generators that are within the Caltrans district 7 jurisdiction. The original data source is the California Energy Commission',
                     'tags': 'webmap creation from arcgis api for python'}
web_map_item = wm.save(item_properties = web_map_properties)


# In[11]:


web_map_item


# In[19]:


wm.definition

