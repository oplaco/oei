// src/components/MapViewer.tsx
import { MapContainer, TileLayer, GeoJSON, useMap } from "react-leaflet";
import type * as GeoJSONTypes from "geojson";
import { useEffect } from "react";
import "leaflet/dist/leaflet.css";

type Props = {
  geojsonData: GeoJSONTypes.GeoJsonObject | null; // AOI
  tracks?: GeoJSONTypes.LineString[]; // pass tracks
};

function FitOnData({ aoi, tracks }: { aoi: any; tracks?: any[] }) {
  const map = useMap();
  useEffect(() => {
    const layers: any[] = [];
    if (aoi) layers.push(aoi);
    tracks?.forEach((t) => layers.push(t));
    if (!layers.length) return;
    // Build a tiny FeatureCollection to get bounds
    const fc = {
      type: "FeatureCollection",
      features: layers.map((g) => ({ type: "Feature", properties: {}, geometry: g })),
    };
    // @ts-ignore leaflet GeoJSON has getBounds via addData
    const gj = L.geoJSON(fc);
    map.fitBounds(gj.getBounds(), { padding: [20, 20] });
  }, [aoi, tracks, map]);
  return null;
}

export default function MapViewer({ geojsonData, tracks = [] }: Props) {
  return (
    <div className="h-[500px] w-full rounded shadow overflow-hidden">
      <MapContainer center={[0, 0]} zoom={2} scrollWheelZoom className="h-full w-full">
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <FitOnData aoi={geojsonData} tracks={tracks} />

        {geojsonData && <GeoJSON data={geojsonData} style={{ color: "#840032", weight: 2 }} />}

        {tracks.map((line, i) => (
          <GeoJSON
            key={i}
            data={
              {
                type: "Feature",
                geometry: line,
                properties: {},
              } as GeoJSON.Feature<GeoJSON.LineString>
            }
            style={{ color: "#ff0000 ", weight: 3 }}
          />
        ))}
      </MapContainer>
    </div>
  );
}
