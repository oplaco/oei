import { useEffect, useState } from "react";
import GeoJsonUploader from "../components/GeoJsonUploader";
import SatelliteDropdown from "../components/SatelliteDropdown";
import TleIngestCard from "../components/TleIngestCard";
import PassCompute from "../components/PassCompute";
import MapViewer from "../components/MapViewer";

const API_BASE = import.meta.env.VITE_API_BASE_URL as string;

type Satellite = {
  id: number;
  name: string;
  norad_id?: number;
};

export default function MapPage() {
  const [geojson, setGeojson] = useState<GeoJSON.GeoJsonObject | null>(null);
  const [aoiId, setAoiId] = useState<number | null>(null);
  const [satelliteId, setSatelliteId] = useState<number | null>(null);
  const [satellites, setSatellites] = useState<Satellite[]>([]);
  const [passes, setPasses] = useState<any[]>([]);

  async function refreshSatellites() {
    try {
      const res = await fetch(`${API_BASE}/satellites?limit=1000`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const items: Satellite[] = Array.isArray(data) ? data : (data.items ?? []);
      setSatellites(items);
    } catch (e) {
      console.error("Failed to load satellites:", e);
    }
  }

  useEffect(() => {
    refreshSatellites();
  }, []);

  return (
    <div className="h-screen bg-primary-red text-primary-blue flex">
      {/* LEFT COLUMN */}
      <div className="w-full lg:w-1/4 overflow-y-auto p-6 space-y-4">
        <GeoJsonUploader
          onUploadSuccess={(aoi) => {
            setGeojson(aoi.geometry);
            setAoiId(aoi.id);
          }}
        />

        <SatelliteDropdown
          sats={satellites}
          onSelect={(sat) => setSatelliteId(sat ? sat.id : null)}
        />

        <TleIngestCard onSuccess={refreshSatellites} />

        <PassCompute
          satelliteId={satelliteId}
          aoiId={aoiId}
          onResults={(r) => setPasses(r)}
          results={passes}
        />
      </div>

      {/* RIGHT COLUMN */}
      <div className="hidden lg:block w-3/4 h-screen">
        <MapViewer geojsonData={geojson} tracks={passes.map((p) => p.track_geojson)} />
      </div>
    </div>
  );
}
