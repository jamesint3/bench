import { apiGet } from "./api";

export function fetchMe() {
  return apiGet<{ id: number; email: string } | { user: null }>("/auth/me");
}
