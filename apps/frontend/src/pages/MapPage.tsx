import { useState } from "react";
import MapViewer from "../components/MapViewer";
import GeoJsonUploader from "../components/GeoJsonUploader";

export default function MapPage() {
  const [geojson, setGeojson] = useState<GeoJSON.GeoJsonObject | null>(null);

  return (
    <div className="min-h-screen bg-gray-100 p-6 space-y-6 text-primaryBlue">
      <h1 className="text-3xl font-bold">Satellite Pass Demo</h1>

      <GeoJsonUploader onUploadSuccess={(geometry) => setGeojson(geometry)} />
      <MapViewer geojsonData={geojson} />
    </div>
  );
}
