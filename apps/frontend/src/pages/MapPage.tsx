import { useEffect,useState } from "react";
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

    useEffect(() => {
        console.log("aoiId:", aoiId, "satelliteId:", satelliteId);
    }, [aoiId, satelliteId]);
    
  return (
    <div className="min-h-screen bg-gray-100 p-6 space-y-6 text-primaryBlue">
      <h1 className="text-3xl font-bold">Satellite Pass Demo</h1>

      {/* If your uploader returns { id, geometry }, this handles both cases */}
      <GeoJsonUploader
        onUploadSuccess={(res: any) => {
          const geom = res?.geometry ?? res; // support old shape
          setGeojson(geom);
          if (res?.id) setAoiId(res.id);
        }}
      />
      <GeoJsonUploader
        onUploadSuccess={(aoi: { id: number; geometry: GeoJSON.GeoJsonObject }) => {
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
      />

      <MapViewer geojsonData={geojson} />

      {/* Optional tiny list */}
      {passes.length > 0 && (
        <div className="rounded shadow bg-white p-4">
          <h2 className="text-xl font-semibold mb-2">Upcoming Passes</h2>
          <ul className="list-disc ml-5 text-sm">
            {passes.map((p, i) => (
              <li key={i}>
                {new Date(p.start_time).toLocaleString()} →{" "}
                {new Date(p.end_time).toLocaleString()} — max{" "}
                {p.max_elevation_deg.toFixed(1)}°
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
