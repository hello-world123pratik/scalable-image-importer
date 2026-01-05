import { useState } from "react";
import { createImportJob } from "../api/client";
import './ImportForm.css';

export default function ImportForm({ onJobCreated }) {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await createImportJob(url);
      onJobCreated(res.data.job_id);
      setUrl("");
    } catch (err) {
      setError(err.response?.data?.error || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="import-form" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Google Drive folder URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        className="import-input"
        required
      />
      <button type="submit" className="import-button" disabled={loading}>
        {loading ? "Submitting..." : "Import"}
      </button>
      {error && <p className="import-error">{error}</p>}
    </form>
  );
}
