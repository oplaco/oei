import { useNavigate } from "react-router-dom";

export default function LandingCard() {
  const navigate = useNavigate();

  return (
    <div className="text-center max-w-md text-white">
      <h1 className="text-4xl font-bold text-white mb-4">Orbital Edge Imaging</h1>
      <p className="text-lg text-gray-200 mb-6">
        We deliver real-time satellite insights directly to your browser. Monitor areas of interest
        from space with unprecedented clarity.
      </p>
      <button
        className="bg-primary-red hover:bg-red-800 text-white font-bold py-2 px-6 rounded transition"
        onClick={() => navigate("/map")}
      >
        Try Demo
      </button>
    </div>
  );
}
