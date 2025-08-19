import { MapContainer, TileLayer, GeoJSON, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useEffect, useRef } from "react";

type MapViewerProps = {
  geojsonData: GeoJSON.GeoJsonObject | null;
};

function InvalidateOnResize({ observe }: { observe: Element | null }) {
  const map = useMap();

  useEffect(() => {
    if (!observe) return;
    const ro = new ResizeObserver(() => {
      map.invalidateSize();
    });
    ro.observe(observe);
    // initial kick (in case parent starts collapsed/zero height)
    setTimeout(() => map.invalidateSize(), 0);
    return () => ro.disconnect();
  }, [map, observe]);

  return null;
}

export default function MapViewer({ geojsonData }: MapViewerProps) {
  const wrapperRef = useRef<HTMLDivElement | null>(null);

  return (
    // Parent with explicit height
    <div ref={wrapperRef} className="h-[500px] w-full rounded shadow overflow-hidden">
      <MapContainer
        center={[0, 0]}
        zoom={2}
        scrollWheelZoom
        className="h-full w-full"        // fill the parent
        style={{ height: "100%", width: "100%" }} // (defensive)
      >
        <InvalidateOnResize observe={wrapperRef.current} />

        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        {geojsonData && <GeoJSON data={geojsonData} />}
      </MapContainer>
    </div>
  );
}
