import React, { useState } from "react";
import ObjectsPage from "./components/ObjectsPage.jsx";
import AssessmentsPage from "./components/AssessmentsPage.jsx";
import Dashboard from "./components/Dashboard.jsx";
import OverviewDashboard from "./components/OverviewDashboard.jsx";

export default function App() {
  const [selectedObject, setSelectedObject] = useState(null);

  return (
    <div style={{ padding: "16px", fontFamily: "sans-serif" }}>
      <h1>Система анализа защищенности объектов</h1>

      <OverviewDashboard />

      <ObjectsPage onSelectObject={setSelectedObject} />

      {selectedObject && (
        <>
          <hr />
          <h2>Оценки и аналитика объекта: {selectedObject.object_name}</h2>
          <AssessmentsPage objectId={selectedObject.object_id} />
          <Dashboard objectId={selectedObject.object_id} />
        </>
      )}
    </div>
  );
}
