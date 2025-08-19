import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE_URL as string;

type Props = {
  satelliteId: number | null;
  aoiId: number | null;
  onResults: (results: any[]) => void;
};

export default function PassComputeCard({ satelliteId, aoiId, onResults }: Props) {
  const [loading, setLoading] = useState(false);

  async function compute() {
    if (!satelliteId || !aoiId) return;
    setLoading(true);
    try {
      const payload = {
        satellite_id: satelliteId,
        aoi_id: aoiId,
        window: {
          start: new Date().toISOString(),
          end: new Date(Date.now() + 24 * 3600 * 1000).toISOString(),
        },
        min_elevation_deg: 10,
      };

      const res = await fetch(`${API_BASE}/passes/compute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      onResults(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded shadow bg-white p-4">
      <h2 className="text-xl font-semibold mb-3">Compute Passes</h2>
      <button
        className="px-4 py-2 rounded bg-primaryBlue text-white disabled:opacity-50"
        disabled={!satelliteId || !aoiId || loading}
        onClick={compute}
      >
        {loading ? "Computing…" : "Compute"}
      </button>
    </div>
  );
}
