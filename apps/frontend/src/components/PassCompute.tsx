import { useState } from "react";
import ActionButton from "./ActionButton";

const API_BASE = import.meta.env.VITE_API_BASE_URL as string;

type Pass = {
  start_time: string;
  end_time: string;
  max_elevation_deg: number;
  track_geojson: any;
};

type Props = {
  satelliteId: number | null;
  aoiId: number | null;
  onResults: (results: Pass[]) => void;
  results: Pass[];
};

export default function PassCompute({ satelliteId, aoiId, onResults, results }: Props) {
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [touched, setTouched] = useState(false);

  const compute = async () => {
    if (!satelliteId || !aoiId) return;
    setTouched(true);
    setLoading(true);
    setErr(null);
    onResults([]); // 🔁 clear previous results before new compute

    try {
      const now = new Date();
      const payload = {
        satellite_id: satelliteId,
        aoi_id: aoiId,
        window: {
          start: now.toISOString(),
          end: new Date(now.getTime() + 24 * 3600 * 1000).toISOString(),
        },
        min_elevation_deg: 10,
      };

      const res = await fetch(`${API_BASE}/passes/compute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error(await res.text());

      const data: Pass[] = await res.json();
      onResults(data);
    } catch (err: any) {
      console.error("Pass compute failed:", err);
      setErr(err?.message || "Failed to compute passes");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rounded shadow bg-white p-4">
      <h2 className="text-xl font-semibold mb-3">Compute Passes</h2>
      <ActionButton
        onClick={compute}
        disabled={!satelliteId || !aoiId}
        loading={loading}
        label="Compute"
        loadingLabel="Computing…"
        status={err ? "error" : undefined}
        message={err ?? undefined}
      />
      {results.length > 0 && (
        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-sm text-left border">
            <thead className="bg-gray-100 text-xs uppercase">
              <tr>
                <th className="px-4 py-2">Start</th>
                <th className="px-4 py-2">End</th>
                <th className="px-4 py-2">Max Elevation</th>
              </tr>
            </thead>
            <tbody>
              {results.map((p, i) => (
                <tr key={i} className="border-t">
                  <td className="px-4 py-2">{new Date(p.start_time).toLocaleString()}</td>
                  <td className="px-4 py-2">{new Date(p.end_time).toLocaleString()}</td>
                  <td className="px-4 py-2">{p.max_elevation_deg.toFixed(1)}°</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {!loading && touched && results.length === 0 && err === null && (
        <p className="text-sm text-gray-500 mt-4 italic">
          No passes found for the current parameters.
        </p>
      )}
    </div>
  );
}
