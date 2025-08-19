import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE_URL as string;

export default function TleIngestCard() {
  const [text, setText] = useState("");
  const [status, setStatus] = useState<null | "idle" | "sending" | "ok" | "error">(null);
  const [message, setMessage] = useState<string>("");

  async function submit() {
    setStatus("sending");
    setMessage("");
    try {
      const res = await fetch(`${API_BASE}/ingest`, {
        method: "POST",
        headers: { "Content-Type": "text/plain" },
        body: text.trim(),
      });
      if (!res.ok) {
        const err = await res.text().catch(() => "");
        throw new Error(err || `HTTP ${res.status}`);
      }
      setStatus("ok");
      setMessage("TLEs uploaded successfully.");
      setText("");
    } catch (e: any) {
      setStatus("error");
      setMessage(e?.message ?? "Upload failed");
    }
  }

  return (
    <div className="rounded shadow bg-white p-4">
      <h2 className="text-xl font-semibold mb-3">Upload TLEs</h2>

      <textarea
        className="w-full border rounded p-2 h-40 font-mono text-sm"
        placeholder={`Paste raw TLE text here
(e.g. 2 or 3-line sets, multiple allowed)`}
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <div className="mt-3 flex items-center gap-3">
        <button
          onClick={submit}
          disabled={!text.trim() || status === "sending"}
          className="px-4 py-2 rounded bg-primaryBlue text-white disabled:opacity-50"
        >
          {status === "sending" ? "Uploading…" : "Upload"}
        </button>
        {status === "ok" && <span className="text-green-600 text-sm">{message}</span>}
        {status === "error" && <span className="text-red-600 text-sm">{message}</span>}
      </div>
    </div>
  );
}
