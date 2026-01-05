import { useEffect, useState } from "react";
import { fetchHome } from "../api/client";
import { useImages } from "../hooks/useImages";
import { useJobStatus } from "../hooks/useJobStatus";

import ImportForm from "../components/ImportForm";
import ImageGrid from "../components/ImageGrid";
import Loader from "../components/Loader";
import JobStatus from "../components/JobStatus";
import Pagination from "../components/Pagination";

import "./Home.css";

export default function Home() {
  const {
    images,
    loading,
    error,
    page,
    totalPages,
    nextPage,
    prevPage,
    reload,
  } = useImages();

  const [jobId, setJobId] = useState(null);
  const [apiMessage, setApiMessage] = useState("");

  const { job, error: jobError } = useJobStatus(jobId, () => {
    reload(); // auto-refresh images on completion
  });

  useEffect(() => {
    fetchHome()
      .then((res) => setApiMessage(res.data.message))
      .catch(() => setApiMessage("Backend unavailable"));
  }, []);

  return (
    <div className="home-wrapper">
      <header className="home-header">
        <h1>Scalable Image Importer</h1>
        {apiMessage && <p className="api-status">{apiMessage}</p>}
      </header>

      <section className="card">
        <h2 className="section-title">Import Images</h2>
        <ImportForm onJobCreated={setJobId} />
        <JobStatus job={job} error={jobError} />
      </section>

      <section className="card">
        <h2 className="section-title">Imported Images</h2>

        {loading && <Loader />}

        {error && <p className="error-text">{error}</p>}

        {!loading && !error && images.length === 0 && (
          <p className="empty-text">
            No images have been imported yet.  
            Start by submitting a Google Drive folder above.
          </p>
        )}

        {!loading && !error && images.length > 0 && (
          <>
            <ImageGrid images={images} />
            <Pagination
              page={page}
              totalPages={totalPages}
              nextPage={nextPage}
              prevPage={prevPage}
            />
          </>
        )}
      </section>
    </div>
  );
}
