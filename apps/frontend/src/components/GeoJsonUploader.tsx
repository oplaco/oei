import { useState } from "react";
import type * as GeoJSON from "geojson";

type AoiResponse = { id: number; name: string; geometry: GeoJSON.GeoJsonObject };

type Props = {
  onUploadSuccess: (aoi: AoiResponse) => void;
};

export default function GeoJsonUploader({ onUploadSuccess }: Props) {
  const [name, setName] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!name || !file) return setErr("Name and file are required.");

    setErr(null);
    setLoading(true);

    const form = new FormData();
    form.append("name", name);
    form.append("file", file);

    try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/aois/upload`, {
        method: "POST",
        body: form,
      });
      if (!res.ok) throw new Error((await res.text()) || `HTTP ${res.status}`);
      const data: AoiResponse = await res.json();
      onUploadSuccess(data); // <- pass full AOI (has id + geometry)
      setName("");
      setFile(null);
    } catch (e: any) {
      setErr(e?.message ?? "Upload failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={submit} className="p-4 bg-white rounded shadow space-y-3">
      <input
        className="w-full border p-2 rounded"
        placeholder="AOI name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="file"
        accept=".geojson,application/json"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
      />
      {err && <p className="text-red-600 text-sm">{err}</p>}
      <button
        type="submit"
        disabled={loading}
        className="px-4 py-2 rounded bg-[#840032] text-white disabled:opacity-50"
      >
        {loading ? "Uploading…" : "Upload AOI"}
      </button>
    </form>
  );
}
