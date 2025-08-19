import { useEffect, useState } from "react";

type Satellite = {
  id: number;
  name: string;
  norad_id?: number;
};

type Props = {
  onSelect?: (sat: Satellite | null) => void;
};

const API_BASE = import.meta.env.VITE_API_BASE_URL as string; 
export default function SatelliteDropdown({ onSelect }: Props) {
  const [sats, setSats] = useState<Satellite[]>([]);
  const [loading, setLoading] = useState(true);
  const [selId, setSelId] = useState<string>("");

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const res = await fetch(`${API_BASE}/satellites?limit=1000`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        // Accept either {items: [...] } or just [...]
        const items: Satellite[] = Array.isArray(data) ? data : (data.items ?? []);
        if (!cancelled) setSats(items);
      } catch (e) {
        console.error("Failed to load satellites:", e);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => { cancelled = true; };
  }, []);

  const selected = sats.find(s => String(s.id) === selId) ?? null;

  return (
    <div className="rounded shadow bg-white p-4">
      <h2 className="text-xl font-semibold mb-3">Select Satellite</h2>

      {loading ? (
        <p className="text-sm text-gray-500">Loading…</p>
      ) : (
        <select
          className="w-full border rounded p-2"
          value={selId}
          onChange={(e) => {
            const id = e.target.value;
            setSelId(id);
            onSelect?.(sats.find(s => String(s.id) === id) ?? null);
          }}
        >
          <option value="">— choose —</option>
          {sats.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}{s.norad_id ? ` (NORAD ${s.norad_id})` : ""}
            </option>
          ))}
        </select>
      )}
    </div>
  );
}
