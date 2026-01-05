import './ImageCard.css';

export default function ImageCard({ image }) {
  return (
    <div className="image-card">
      <img src={image.storage_path} alt={image.name} className="image-img" />
      <div className="image-info">
        <p className="image-name">{image.name}</p>
        <p className="image-size">{(image.size / 1024).toFixed(2)} KB</p>
      </div>
    </div>
  );
}
