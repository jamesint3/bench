export const authConfig = {
  tokenKey: "gexable_token",
  userHeader: "X-User-Email",
  tenantHeader: "X-Tenant-ID",
};

export function getStoredToken(): string {
  return localStorage.getItem(authConfig.tokenKey) ?? "";
}
