import axios from "axios";

const api = axios.create({
  baseURL: "/api"
});

export async function getObjects() {
  const res = await api.get("/objects/");
  return res.data;
}

export async function createObject(payload) {
  const res = await api.post("/objects/", payload);
  return res.data;
}

export async function createAssessment(payload) {
  const res = await api.post("/assessments/", payload);
  return res.data;
}

export async function getIntegralSeries(objectId) {
  const res = await api.get(`/analytics/integral-time-series/${objectId}`);
  return res.data;
}

export async function getCriticalVulnerabilities() {
  const res = await api.get("/analytics/critical-vulnerabilities");
  return res.data;
}

export async function getAnalyticsOverview(limit = 5) {
  const res = await api.get(`/analytics/overview?limit=${limit}`);
  return res.data;
}

export default api;
