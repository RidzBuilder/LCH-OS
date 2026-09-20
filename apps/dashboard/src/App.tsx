import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import CreatorsPage from "./pages/CreatorsPage";
import SessionsPage from "./pages/SessionsPage";
import MonitorPage from "./pages/MonitorPage";

export default function App() {
  return (
    <BrowserRouter>
      <div className="shell">
        <aside className="sidebar">
          <h1>LCH-OS</h1>
          <nav>
            <NavLink to="/creators">AI Creators</NavLink>
            <NavLink to="/sessions">Live Sessions</NavLink>
            <NavLink to="/monitor">Monitor</NavLink>
          </nav>
        </aside>
        <main>
          <Routes>
            <Route path="/" element={<CreatorsPage />} />
            <Route path="/creators" element={<CreatorsPage />} />
            <Route path="/sessions" element={<SessionsPage />} />
            <Route path="/monitor" element={<MonitorPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
