const BASE = "";

export async function listCreators() {
  const r = await fetch(`${BASE}/v1/creators`);
  return r.json();
}

export async function createSession(body: Record<string, string>) {
  const r = await fetch(`${BASE}/v1/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return r.json();
}

export async function controlSession(id: string, cmd: string) {
  const r = await fetch(`${BASE}/v1/sessions/${id}/control`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ cmd }),
  });
  return r.json();
}
