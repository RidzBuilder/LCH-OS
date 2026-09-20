import { useEffect, useState } from "react";
import { listCreators } from "../api";

export default function CreatorsPage() {
  const [creators, setCreators] = useState<any[]>([]);
  useEffect(() => { listCreators().then(setCreators); }, []);
  return (
    <div>
      <h2>AI Creators (dari PBOS)</h2>
      <table>
        <thead><tr><th>Nama</th><th>Tipe</th><th>Niche</th><th>Versi</th></tr></thead>
        <tbody>
          {creators.map((c) => (
            <tr key={`${c.blueprint_id}@${c.version}`}>
              <td>{c.name}</td><td>{c.type}</td><td>{c.niche}</td><td>v{c.version}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="muted">Kirim blueprint baru via <code>POST /v1/genesis/ingest</code> (lihat docs/PBOS_INTEGRATION.md).</p>
    </div>
  );
}
