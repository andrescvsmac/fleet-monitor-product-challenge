// YOUR TASK. The device card.
//
// Takes one Device and renders:
//   * name and site
//   * status, one of online / degraded / offline, and NOT in color alone.
//     A color-blind operator has to be able to read it.
//   * last seen, relative: "42s ago", "14m ago", "5h ago". Use the `now` prop,
//     which is the server's `generatedAt`, rather than Date.now(), so the card
//     can't disagree with the payload it came from.
//   * latest temperature in FAHRENHEIT, since `tempC` is Celsius, plus
//     humidity. `latestReading` is null for a device that has never reported.
//   * battery. `batteryPct` is null on mains-powered devices. Flag a low one.
//   * an offline device should look different from an online one.
//
// Semantic HTML, and real alt or aria text where it earns its place.

import type { Device } from "@/types/device";

interface DeviceCardProps {
  device: Device;
  now: string; // ISO 8601, the server clock from DevicesResponse.generatedAt
}

export function DeviceCard({ device, now }: DeviceCardProps) {
  // TODO: implement
  return <div>{device.name}</div>;
}
