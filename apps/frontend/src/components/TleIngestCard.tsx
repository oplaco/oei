import { useState } from "react";
import ActionButton from "./ActionButton";

const API_BASE = import.meta.env.VITE_API_BASE_URL as string;

type TleIngestCardProps = {
  onSuccess?: () => void;
};

export default function TleIngestCard({ onSuccess }: TleIngestCardProps) {
  const [text, setText] = useState("");
  const [status, setStatus] = useState<"idle" | "sending" | "ok" | "error">("idle");
  const [message, setMessage] = useState<string>("");

  async function submit() {
    setStatus("sending");
    setMessage("");
    try {
      const res = await fetch(`${API_BASE}/tles/ingest`, {
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
      onSuccess?.();
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
        placeholder={`Paste raw TLE text here\n(e.g. 2 or 3-line sets, multiple allowed)`}
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <ActionButton
        onClick={submit}
        disabled={!text.trim()}
        loading={status === "sending"}
        label="Upload"
        loadingLabel="Uploading…"
        status={status}
        message={message}
      />
    </div>
  );
}
