import "./Pagination.css";

export default function Pagination({ page, totalPages, nextPage, prevPage }) {
  if (totalPages <= 1) return null;

  return (
    <div className="pagination">
      <button onClick={prevPage} disabled={page === 1}>
        Previous
      </button>

      <span>
        Page {page} of {totalPages}
      </span>

      <button onClick={nextPage} disabled={page === totalPages}>
        Next
      </button>
    </div>
  );
}
