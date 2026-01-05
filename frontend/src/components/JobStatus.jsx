import "./JobStatus.css";

export default function JobStatus({ job, error }) {
  if (error) {
    return <p className="job-error">{error}</p>;
  }

  if (!job) return null;

  return (
    <div className="job-status-card">
      <h3>Import Job #{job.job_id}</h3>

      <p className={`job-status ${job.status}`}>
        Status: {job.status.toUpperCase()}
      </p>

      <p className="job-progress">
        Progress: {job.processed_items} / {job.total_items}
      </p>

      {job.status === "failed" && (
        <p className="job-error">
          Import failed. Please try again.
        </p>
      )}
    </div>
  );
}
