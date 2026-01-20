import React, { useEffect, useMemo, useState } from "react";
import { getAnalyticsOverview } from "../api.js";

function Bar({ label, value, total }) {
  const pct = total > 0 ? Math.round((value / total) * 100) : 0;

  return (
    <div style={{ marginBottom: 10 }}>
      <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
        <span>{label}</span>
        <span>
          {value} ({pct}%)
        </span>
      </div>
      <div
        style={{
          height: 10,
          background: "#e9e9e9",
          borderRadius: 8,
          overflow: "hidden",
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${pct}%`,
            background: "#444",
          }}
        />
      </div>
    </div>
  );
}

export default function OverviewDashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  async function load() {
    try {
      setError(null);
      const res = await getAnalyticsOverview(5);
      setData(res);
    } catch (e) {
      setError(e);
    }
  }

  useEffect(() => {
    load();
  }, []);

  const bars = useMemo(() => {
    if (!data) return [];
    const total = data.total_objects ?? 0;
    const by = data.by_security_level || {};
    return [
      { label: "Высокий", key: "высокий", value: by["высокий"] ?? 0, total },
      { label: "Средний", key: "средний", value: by["средний"] ?? 0, total },
      { label: "Низкий", key: "низкий", value: by["низкий"] ?? 0, total },
      { label: "Нет данных", key: "нет данных", value: by["нет данных"] ?? 0, total },
    ];
  }, [data]);

  return (
    <div style={{ marginTop: 16, padding: 12, border: "1px solid #ddd", borderRadius: 10 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h2 style={{ margin: 0 }}>Сводный дашборд</h2>
        <button type="button" onClick={load}>
          Обновить
        </button>
      </div>

      {error && (
        <p style={{ marginTop: 12 }}>
          Ошибка загрузки сводки. Проверь, что бекенд запущен и доступен по /api.
        </p>
      )}

      {!data && !error && <p style={{ marginTop: 12 }}>Загрузка...</p>}

      {data && (
        <>
          <div style={{ marginTop: 10, display: "flex", flexWrap: "wrap", gap: 18 }}>
            <div>
              <div style={{ fontSize: 12, opacity: 0.7 }}>Всего объектов</div>
              <div style={{ fontSize: 26, fontWeight: 700 }}>{data.total_objects}</div>
            </div>
            <div>
              <div style={{ fontSize: 12, opacity: 0.7 }}>Средний балл (по последним оценкам)</div>
              <div style={{ fontSize: 26, fontWeight: 700 }}>
                {data.avg_latest_score == null ? "—" : Number(data.avg_latest_score).toFixed(2)}
              </div>
            </div>
          </div>

          <div style={{ marginTop: 12 }}>
            <h3 style={{ marginBottom: 8 }}>Распределение по уровням защищенности</h3>
            {bars.map((b) => (
              <Bar key={b.key} label={b.label} value={b.value} total={b.total} />
            ))}
          </div>

          <div style={{ marginTop: 12 }}>
            <h3 style={{ marginBottom: 8 }}>Наименее защищенные объекты</h3>
            {(!data.worst_objects || data.worst_objects.length === 0) && (
              <p>Пока нет оценок, чтобы построить рейтинг.</p>
            )}

            {data.worst_objects && data.worst_objects.length > 0 && (
              <ul>
                {data.worst_objects.map((o) => (
                  <li key={o.object_id} style={{ marginBottom: 6 }}>
                    <strong>{o.object_name}</strong>
                    {o.object_type ? ` (${o.object_type})` : ""} — {Number(o.overall_score).toFixed(2)}
                    {o.security_level ? `, уровень: ${o.security_level}` : ""}
                    {o.location ? `, ${o.location}` : ""}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </>
      )}
    </div>
  );
}
