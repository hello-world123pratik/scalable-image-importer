import ImageCard from "./ImageCard";
import "./ImageGrid.css";

export default function ImageGrid({ images }) {
  if (images.length === 0) {
    return (
      <p style={{ textAlign: "center", marginTop: "2rem" }}>
        No images imported yet.
      </p>
    );
  }

  return (
    <div className="image-grid">
      {images.map((img) => (
        <ImageCard key={img.id} image={img} />
      ))}
    </div>
  );
}
