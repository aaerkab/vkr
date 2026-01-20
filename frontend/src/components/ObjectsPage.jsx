import React, { useEffect, useState } from "react";
import { getObjects, createObject } from "../api.js";

export default function ObjectsPage({ onSelectObject }) {
  const [objects, setObjects] = useState([]);
  const [form, setForm] = useState({
    object_name: "",
    object_type: "",
    location: "",
    owner_organization: ""
  });

  async function load() {
    const data = await getObjects();
    setObjects(data);
  }

  useEffect(() => {
    load();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    await createObject(form);
    setForm({
      object_name: "",
      object_type: "",
      location: "",
      owner_organization: ""
    });
    await load();
  }

  return (
    <div>
      <h2>Объекты</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: "12px" }}>
        <input
          placeholder="Название"
          value={form.object_name}
          onChange={(e) => setForm({ ...form, object_name: e.target.value })}
        />
        <input
          placeholder="Тип"
          value={form.object_type}
          onChange={(e) => setForm({ ...form, object_type: e.target.value })}
        />
        <input
          placeholder="Расположение"
          value={form.location}
          onChange={(e) => setForm({ ...form, location: e.target.value })}
        />
        <input
          placeholder="Организация"
          value={form.owner_organization}
          onChange={(e) =>
            setForm({ ...form, owner_organization: e.target.value })
          }
        />
        <button type="submit">Добавить</button>
      </form>

      <ul>
        {objects.map((o) => (
          <li key={o.object_id}>
            <button type="button" onClick={() => onSelectObject(o)}>
              {o.object_name} ({o.object_type})
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
