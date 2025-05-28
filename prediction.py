# prediction.py

import geopandas as gpd
import folium
from shapely.geometry import MultiPolygon, Polygon
import pandas as pd

# Charger les données
commune = gpd.read_file("data/commune.geojson")
predictions = gpd.read_file("data/prediction.geojson")

# S'assurer que toutes les couches sont dans le même CRS
commune = commune.to_crs(epsg=4326)
predictions = predictions.to_crs(epsg=4326)

# Calcul du centroïde pour centrer la carte
center = commune.to_crs(epsg=3857).geometry.centroid.to_crs(epsg=4326).iloc[0].coords[0][::-1]

# Créer la carte Folium
m = folium.Map(location=center, zoom_start=13)

# Ajouter la commune
folium.GeoJson(
    commune,
    name="Commune",
    style_function=lambda x: {
        "fillColor": "none",
        "color": "black",
        "weight": 2,
        "fillOpacity": 0
    },
    tooltip=folium.GeoJsonTooltip(fields=["nom"], aliases=["Commune :"])
).add_to(m)

# Définir les couleurs pour les classes
couleurs = {
    "faible": "green",
    "moyenne": "orange",
    "forte": "red"
}

# Ajouter chaque classe de prédiction
for classe, couleur in couleurs.items():
    sous_couche = predictions[predictions["prediction"] == classe]
    if not sous_couche.empty:
        folium.GeoJson(
            sous_couche,
            name=f"Risque {classe}",
            style_function=lambda x, col=couleur: {
                "fillColor": col,
                "color": col,
                "weight": 0.5,
                "fillOpacity": 0.4
            },
            tooltip=folium.GeoJsonTooltip(fields=["prediction"], aliases=["Risque :"])
        ).add_to(m)

# Ajouter une légende personnalisée
legend_html = '''
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 110px; 
     border:2px solid grey; z-index:9999; font-size:14px; background:white; padding:10px;">
<b>Légende</b><br>
<i style="background:green; width:10px; height:10px; display:inline-block;"></i> Faible<br>
<i style="background:orange; width:10px; height:10px; display:inline-block;"></i> Moyenne<br>
<i style="background:red; width:10px; height:10px; display:inline-block;"></i> Forte<br>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Ajouter les contrôles de calques
folium.LayerControl().add_to(m)

# Enregistrer la carte
m.save("prediction_map.html")
print("✅ Carte interactive générée : prediction_map.html")
