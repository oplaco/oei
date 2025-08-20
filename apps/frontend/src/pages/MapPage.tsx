import { useEffect, useState } from "react";
import MapViewer from "../components/MapViewer";
import GeoJsonUploader from "../components/GeoJsonUploader";
import SatelliteDropdown from "../components/SatelliteDropdown";
import TleIngestCard from "../components/TleIngestCard";
import PassCompute from "../components/PassCompute";

export default function MapPage() {
  const [geojson, setGeojson] = useState<GeoJSON.GeoJsonObject | null>(null);
  const [aoiId, setAoiId] = useState<number | null>(null);
  const [satelliteId, setSatelliteId] = useState<number | null>(null);
  const [passes, setPasses] = useState<any[]>([]);

  useEffect(() => {}, [aoiId, satelliteId]);

  return (
    <div className="min-h-screen bg-gray-100 p-6 text-primary-blue">
      <h1 className="text-3xl font-bold mb-4">Satellite Pass Demo</h1>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* LEFT COLUMN */}
        <div className="lg:w-1/4 w-full space-y-4">
          <GeoJsonUploader
            onUploadSuccess={(aoi) => {
              setGeojson(aoi.geometry);
              setAoiId(aoi.id);
            }}
          />

          <SatelliteDropdown onSelect={(sat) => setSatelliteId(sat ? sat.id : null)} />

          <TleIngestCard />

          <PassCompute satelliteId={satelliteId} aoiId={aoiId} onResults={(r) => setPasses(r)} />
        </div>

        {/* RIGHT COLUMN */}
        <div className="lg:w-3/4 w-full h-[80vh]">
          <MapViewer geojsonData={geojson} tracks={passes.map((p) => p.track_geojson)} />
        </div>
      </div>
    </div>
  );
}
