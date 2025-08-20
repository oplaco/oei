import { useState } from "react";

type Satellite = {
  id: number;
  name: string;
  norad_id?: number;
};

type SatelliteDropdownProps = {
  sats: Satellite[];
  onSelect?: (sat: Satellite | null) => void;
};

export default function SatelliteDropdown({ sats, onSelect }: SatelliteDropdownProps) {
  const [selId, setSelId] = useState<string>("");
  const selected = sats.find((s) => String(s.id) === selId) ?? null;

  return (
    <div className="rounded shadow bg-white p-4">
      <h2 className="text-xl font-semibold mb-3">Select Satellite</h2>
      {sats.length === 0 ? (
        <p className="text-sm text-gray-500">No satellites found.</p>
      ) : (
        <select
          className="w-full border rounded p-2"
          value={selId}
          onChange={(e) => {
            const id = e.target.value;
            setSelId(id);
            onSelect?.(sats.find((s) => String(s.id) === id) ?? null);
          }}
        >
          <option value="">— choose —</option>
          {sats.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
              {s.norad_id ? ` (NORAD ${s.norad_id})` : ""}
            </option>
          ))}
        </select>
      )}
    </div>
  );
}
