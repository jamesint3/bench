import { authConfig } from "../app/auth";

export const apiBase = "/api";

export async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${apiBase}${path}`, {
    headers: {
      [authConfig.userHeader]: localStorage.getItem("gexable_user") ?? "",
      [authConfig.tenantHeader]: localStorage.getItem("gexable_tenant") ?? "",
    },
  });
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return (await response.json()) as T;
}
