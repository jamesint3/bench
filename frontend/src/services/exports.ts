export function exportJson(payload: unknown): string {
  return JSON.stringify(payload, null, 2);
}
