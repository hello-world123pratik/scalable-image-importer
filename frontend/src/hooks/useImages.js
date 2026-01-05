import { useEffect, useState } from "react";
import { fetchImages } from "../api/client";

const PAGE_SIZE = 20;

export const useImages = () => {
  const [allImages, setAllImages] = useState([]);
  const [images, setImages] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const totalPages = Math.ceil(allImages.length / PAGE_SIZE);

  const paginate = (data, page) => {
    const start = (page - 1) * PAGE_SIZE;
    return data.slice(start, start + PAGE_SIZE);
  };

  const loadImages = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetchImages();
      setAllImages(res.data);
      setImages(paginate(res.data, 1));
      setPage(1);
    } catch {
      setError("Failed to load images");
    } finally {
      setLoading(false);
    }
  };

  const nextPage = () => {
    if (page < totalPages) {
      const next = page + 1;
      setPage(next);
      setImages(paginate(allImages, next));
    }
  };

  const prevPage = () => {
    if (page > 1) {
      const prev = page - 1;
      setPage(prev);
      setImages(paginate(allImages, prev));
    }
  };

  useEffect(() => {
    loadImages();
  }, []);

  return {
    images,
    loading,
    error,
    page,
    totalPages,
    nextPage,
    prevPage,
    reload: loadImages,
  };
};
