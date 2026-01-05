import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export const fetchHome = () => API.get("/");

export const fetchImages = () => API.get("/images");

export const createImportJob = (url) =>
  API.post("/import/google-drive", { url });

export const fetchJobStatus = (jobId) =>
  API.get(`/jobs/${jobId}`);

export const checkHealth = () =>
  API.get("/health/");
