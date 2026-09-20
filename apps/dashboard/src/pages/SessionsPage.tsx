import { useState } from "react";
import { createSession } from "../api";

export default function SessionsPage() {
  const [form, setForm] = useState({ blueprint_id: "", platform: "tiktok", account_ref: "", title: "" });
  const [result, setResult] = useState<any>(null);
  const submit = async () => setResult(await createSession(form));
  return (
    <div>
      <h2>Buat Sesi Live</h2>
      <div className="form">
        <input placeholder="blueprint_id" value={form.blueprint_id}
          onChange={(e) => setForm({ ...form, blueprint_id: e.target.value })} />
        <select value={form.platform} onChange={(e) => setForm({ ...form, platform: e.target.value })}>
          {["tiktok", "youtube", "instagram", "twitch", "shopee"].map((p) => <option key={p}>{p}</option>)}
        </select>
        <input placeholder="account_ref" value={form.account_ref}
          onChange={(e) => setForm({ ...form, account_ref: e.target.value })} />
        <input placeholder="judul live" value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })} />
        <button onClick={submit}>Go Live</button>
      </div>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
