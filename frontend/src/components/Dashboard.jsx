import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE;


/* ---------- Helper to format disease name ---------- */
const formatDiseaseName = (name) => {
  if (!name) return "";
  return name
    .replace(/___/g, " – ")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
};

/* ---------- Disease Info Card (RIGHT SIDE) ---------- */
const DiseaseInfoCard = ({ symptoms, prevention }) => {
  if (!symptoms?.length && !prevention?.length) return null;

  return (
    <div className="w-[360px] bg-white/80 backdrop-blur-lg rounded-2xl shadow-2xl p-6 border border-green-200 animate-slide-in">
      <h2 className="text-xl font-bold text-green-800 mb-4 text-center">
        Disease Information
      </h2>

      <div className="mb-4">
        <h3 className="font-semibold text-gray-800 mb-2">
          🌿 Symptoms
        </h3>
        <ul className="list-disc list-inside text-gray-700 space-y-1">
          {symptoms.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      </div>

      <div>
        <h3 className="font-semibold text-gray-800 mb-2">
          🛡️ Prevention
        </h3>
        <ul className="list-disc list-inside text-gray-700 space-y-1">
          {prevention.map((p, i) => (
            <li key={i}>{p}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

/* ---------- Main Dashboard ---------- */
export default function Dashboard() {
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setPreview(URL.createObjectURL(file));
    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await fetch(`${API_BASE}/api/predict/`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Prediction failed");
      }

      const data = await response.json();
      console.log("API RESPONSE:", data);
      setResult(data);
    } catch (err) {
      setError("Failed to get prediction. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`min-h-screen ${
    result
      ? "grid grid-cols-2 place-items-center gap-10 px-10"
      : "flex items-center justify-center"
  }`}>

      {/* LEFT SIDE: Upload + Result Card */}
      <div className="w-[420px] bg-white/85 backdrop-blur-md rounded-2xl shadow-xl p-6">
        <h1 className="text-2xl font-bold text-center text-green-800 mb-2">
          Plant Leaf Disease Detection
        </h1>

        <p className="text-center text-gray-600 mb-4">
          Upload a plant leaf image to detect disease
        </p>

        {/* Upload Box */}
        <label className="flex flex-col items-center justify-center border-2 border-dashed border-green-400 rounded-xl p-4 cursor-pointer hover:bg-green-50 transition">
          <input
            type="file"
            accept="image/*"
            className="hidden"
            onChange={handleChange}
          />
          <p className="text-green-700 font-medium">
            Click or drag image to upload
          </p>
          <span className="text-sm text-gray-500 mt-1">
            JPG, JPEG, PNG
          </span>
        </label>

        {/* Image Preview */}
        {preview && (
          <div className="mt-4 flex justify-center">
            <img
              src={preview}
              alt="preview"
              className="rounded-lg object-contain"
              style={{
                maxWidth: "302px",
                maxHeight: "302px",
              }}
            />
          </div>
        )}

        {/* Loading */}
        {loading && (
          <p className="mt-4 text-center text-green-700 font-medium">
            Predicting disease...
          </p>
        )}

        {/* Error */}
        {error && (
          <p className="mt-4 text-center text-red-600">
            {error}
          </p>
        )}

        {/* Prediction Result */}
        {result && (
        <div className="mt-4 bg-green-100 p-3 rounded-lg text-center">
          <p className="font-semibold text-green-800 mb-2">
            Prediction Result
          </p>
          <p>
            <b>Disease:</b>{" "}
            {formatDiseaseName(result.disease)}
          </p>
          <p>
            <b>Confidence:</b> {result.confidence}
          </p>
          <p className="mt-2">
            <b>Severity:</b>{" "}
            <span
              className={
                result.severity === "High"
                  ? "text-red-600 font-bold"
                  : result.severity === "Medium"
                  ? "text-yellow-600 font-bold"
                  : "text-green-600 font-bold"
              }
            >
              {result.severity}
            </span>
          </p>
          <p className="mt-2 text-blue-700 font-semibold">
            📝 {result.recommendation}
          </p>
        </div>
      )}
      </div>

      {/* RIGHT SIDE: Disease Info Card */}
      {result && (
        <DiseaseInfoCard
          symptoms={result.symptoms}
          prevention={result.prevention}
        />
      )}

    </div>
  );
}
