import { useEffect, useRef, useState } from "react";

export default function MonitorPage() {
  const [sessionId, setSessionId] = useState("");
  const [logs, setLogs] = useState<any[]>([]);
  const wsRef = useRef<WebSocket | null>(null);

  const connect = () => {
    wsRef.current?.close();
    const proto = location.protocol === "https:" ? "wss" : "ws";
    const ws = new WebSocket(`${proto}://${location.host}/v1/sessions/${sessionId}/stream`);
    ws.onmessage = (e) => setLogs((prev) => [...prev.slice(-199), JSON.parse(e.data)]);
    wsRef.current = ws;
  };
  useEffect(() => () => wsRef.current?.close(), []);

  return (
    <div>
      <h2>Monitor Sesi Real-time</h2>
      <div className="form">
        <input placeholder="session_id" value={sessionId} onChange={(e) => setSessionId(e.target.value)} />
        <button onClick={connect}>Hubungkan</button>
      </div>
      <div className="feed">
        {logs.map((l, i) => <div key={i} className="feed-item"><pre>{JSON.stringify(l)}</pre></div>)}
      </div>
    </div>
  );
}
