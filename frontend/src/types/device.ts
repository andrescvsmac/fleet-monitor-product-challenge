// PROVIDED. Do not modify.
// These mirror the wire format of the FastAPI models in backend/app/models.py.

export type DeviceStatus = "online" | "degraded" | "offline";

export const DEVICE_STATUSES: DeviceStatus[] = [
  "online",
  "degraded",
  "offline",
];

export type SortOption = "last_seen_desc" | "last_seen_asc" | "name_asc";

export interface Reading {
  recordedAt: string; // ISO 8601, UTC
  tempC: number; // Celsius. The UI shows Fahrenheit.
  humidityPct: number;
}

export interface Device {
  id: string;
  name: string;
  siteId: string;
  siteName: string;
  status: DeviceStatus;
  firmware: string;
  batteryPct: number | null; // null = mains-powered, no battery to show
  lastSeenAt: string; // ISO 8601, UTC
  latestReading: Reading | null; // null = has never reported
}

export interface Site {
  id: string;
  name: string;
  location: string;
}

export interface DevicesResponse {
  data: Device[];
  total: number; // matches before pagination
  page: number;
  pageSize: number;
  generatedAt: string; // server clock. Use it as "now" for relative times.
}

export interface DevicesQuery {
  search?: string;
  status?: DeviceStatus[];
  siteId?: string;
  staleMinutes?: number;
  sort?: SortOption;
  page?: number;
  pageSize?: number;
}
