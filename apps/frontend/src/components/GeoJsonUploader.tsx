import { useState } from 'react';

interface Props {
  onUploadSuccess: (geojson: GeoJSON.GeoJsonObject) => void;
}

export default function GeoJsonUploader({ onUploadSuccess }: Props) {
  const [name, setName] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !file) {
      setError('Name and GeoJSON file are required.');
      return;
    }

    setError(null);
    setLoading(true);

    const formData = new FormData();
    formData.append('name', name);
    formData.append('file', file);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/aois/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Upload failed.');
      }

      const data = await response.json();
      onUploadSuccess(data.geometry);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4 bg-white rounded shadow">
      <div>
        <label className="block mb-1 font-semibold">Name</label>
        <input
          type="text"
          className="w-full border border-gray-300 p-2 rounded"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>

      <div>
        <label className="block mb-1 font-semibold">GeoJSON File</label>
        <input
          type="file"
          accept=".geojson,application/json"
          className="w-full"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
      </div>

      {error && <p className="text-red-600">{error}</p>}

      <button
        type="submit"
        disabled={loading}
        className="primaryRed text-white px-4 py-2 rounded hover:bg-red-800"
      >
        {loading ? 'Uploading...' : 'Upload AOI'}
      </button>
    </form>
  );
}
