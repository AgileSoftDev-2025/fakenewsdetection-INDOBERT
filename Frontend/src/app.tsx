import { Routes, Route } from "react-router-dom";
import Dashboard from "./Dashboard.tsx"; // tolong bantu adjust path ke page dashboard nggih
import ListModelAI from "./ListModelAI2.tsx";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/admin/listmodelai" element={<ListModelAI />} />
    </Routes>
  );
}
