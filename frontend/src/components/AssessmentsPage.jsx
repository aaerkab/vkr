import React, { useState } from "react";
import { createAssessment } from "../api.js";

export default function AssessmentsPage({ objectId }) {
  const [criteriaScores, setCriteriaScores] = useState([
    { criteria_id: 1, score_value: 80, notes: "" }
  ]);
  const [result, setResult] = useState(null);

  function updateScore(index, field, value) {
    const copy = [...criteriaScores];
    copy[index] = { ...copy[index], [field]: value };
    setCriteriaScores(copy);
  }

  function addRow() {
    setCriteriaScores([
      ...criteriaScores,
      { criteria_id: 1, score_value: 50, notes: "" }
    ]);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const payload = {
      object_id: objectId,
      scores: criteriaScores.map((s) => ({
        criteria_id: Number(s.criteria_id),
        score_value: Number(s.score_value),
        notes: s.notes
      }))
    };
    const res = await createAssessment(payload);
    setResult(res);
  }

  return (
    <div>
      <h3>Проведение оценки</h3>
      <form onSubmit={handleSubmit}>
        {criteriaScores.map((row, idx) => (
          <div key={idx} style={{ marginBottom: "4px" }}>
            <input
              style={{ width: "60px" }}
              type="number"
              min="1"
              placeholder="ID критерия"
              value={row.criteria_id}
              onChange={(e) => updateScore(idx, "criteria_id", e.target.value)}
            />
            <input
              style={{ width: "80px" }}
              type="number"
              min="0"
              max="100"
              placeholder="Баллы"
              value={row.score_value}
              onChange={(e) => updateScore(idx, "score_value", e.target.value)}
            />
            <input
              style={{ width: "200px" }}
              placeholder="Примечание"
              value={row.notes}
              onChange={(e) => updateScore(idx, "notes", e.target.value)}
            />
          </div>
        ))}
        <button type="button" onClick={addRow}>
          Добавить критерий
        </button>{" "}
        <button type="submit">Сохранить оценку</button>
      </form>

      {result && (
        <div style={{ marginTop: "8px" }}>
          <p>Оценка сохранена, ID: {result.assessment_id}</p>
          <p>Интегральный показатель: {result.overall_score.toFixed(2)}</p>
          <p>Уровень защищенности: {result.security_level}</p>
        </div>
      )}
    </div>
  );
}
