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
    <div className="h-screen bg-primary-red text-primary-blue flex">
      {/* LEFT COLUMN */}
      <div className="w-full lg:w-1/4 overflow-y-auto p-6 space-y-4">
        <GeoJsonUploader
          onUploadSuccess={(aoi) => {
            setGeojson(aoi.geometry);
            setAoiId(aoi.id);
          }}
        />

        <SatelliteDropdown onSelect={(sat) => setSatelliteId(sat ? sat.id : null)} />

        <TleIngestCard />

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
