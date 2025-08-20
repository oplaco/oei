import { useRef, useState } from "react";
import type * as GeoJSON from "geojson";
import ActionButton from "./ActionButton";

type AoiResponse = { id: number; name: string; geometry: GeoJSON.GeoJsonObject };

type Props = {
  onUploadSuccess: (aoi: AoiResponse) => void;
};

export default function GeoJsonUploader({ onUploadSuccess }: Props) {
  const [name, setName] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null); // browser does not triger onChange if same file is selected again.

  async function submit() {
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

      onUploadSuccess(data);
      setName("");
      setFile(null);
      if (fileInputRef.current) fileInputRef.current.value = ""; // <-- reset file input
    } catch (e: any) {
      setErr(e?.message ?? "Upload failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-4 bg-white rounded shadow space-y-3">
      <input
        className="w-full border p-2 rounded"
        placeholder="AOI name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="file"
        ref={fileInputRef}
        accept=".geojson,application/json"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
      />
      <ActionButton
        onClick={submit}
        disabled={loading}
        loading={loading}
        label="Upload AOI"
        loadingLabel="Uploading…"
        status={err ? "error" : undefined}
        message={err ?? undefined}
      />
    </div>
  );
}
