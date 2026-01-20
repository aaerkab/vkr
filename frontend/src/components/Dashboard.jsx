import React, { useEffect, useState } from "react";
import { getIntegralSeries, getCriticalVulnerabilities } from "../api.js";

export default function Dashboard({ objectId }) {
  const [series, setSeries] = useState([]);
  const [vulns, setVulns] = useState([]);

  useEffect(() => {
    getIntegralSeries(objectId).then(setSeries);
    getCriticalVulnerabilities().then(setVulns);
  }, [objectId]);

  return (
    <div>
      <h3>Дашборд</h3>

      <h4>Динамика интегрального показателя</h4>
      <ul>
        {series.map((p) => (
          <li key={p.date}>
            {p.date}: {p.overall_score?.toFixed(2)}
          </li>
        ))}
      </ul>

      <h4>Критические уязвимости</h4>
      <ul>
        {vulns.map((v) => (
          <li key={v.vulnerability_id}>
            {v.name} (severity {v.severity_level})
          </li>
        ))}
      </ul>
    </div>
  );
}
