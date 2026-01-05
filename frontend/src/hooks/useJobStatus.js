import { useEffect, useState } from "react";
import { fetchJobStatus } from "../api/client";

export const useJobStatus = (jobId, onComplete) => {
  const [job, setJob] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!jobId) return;

    const interval = setInterval(async () => {
      try {
        const res = await fetchJobStatus(jobId);
        setJob(res.data);

        if (res.data.status === "completed") {
          clearInterval(interval);
          onComplete?.();
        }

        if (res.data.status === "failed") {
          clearInterval(interval);
        }
      } catch (err) {
        setError("Failed to fetch job status");
        clearInterval(interval);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [jobId]);

  return { job, error };
};
