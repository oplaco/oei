type Props = {
  onClick: () => void;
  disabled?: boolean;
  loading?: boolean;
  label: string;
  loadingLabel?: string;
  status?: "idle" | "ok" | "error" | "sending";
  message?: string;
};

export default function ActionButton({
  onClick,
  disabled,
  loading,
  label,
  loadingLabel,
  status = "idle",
  message,
}: Props) {
  return (
    <div className="space-y-1">
      <button
        type="button"
        onClick={onClick}
        disabled={disabled || loading}
        className="w-full px-4 py-2 rounded bg-primary-blue text-white disabled:opacity-50"
      >
        {loading ? (loadingLabel ?? "Loading…") : label}
      </button>

      {status === "ok" && message && <p className="text-green-600 text-sm">{message}</p>}

      {status === "error" && message && <p className="text-red-600 text-sm">{message}</p>}
    </div>
  );
}
