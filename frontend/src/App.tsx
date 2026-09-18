// YOUR TASK. The fleet page.
//
// Numbered to match Task 3 in the README.
//
//   1. A search input, a status filter, and a site filter. The site list
//      comes from GET /api/sites.
//   2. Fetch GET /api/devices with the active filters.
//   3. Debounce the search 300ms. `useDebounce` is provided.
//   4. A loading state.
//   5. An error state with a retry, including the 400s your own API returns.
//   6. An empty state.
//   7. A grid of <DeviceCard />.
//   8. Previous and Next pagination driven by `total` and `pageSize`.
//   9. Reset to page 1 when a filter changes.
//  10. Ignore stale responses. If the user changes a filter or page while a
//      request is in flight, the older response landing later must never
//      overwrite newer data. Use AbortController, a request-sequence guard,
//      or a library with cancellation built in. Your call, but defend it.
//  11. Poll every 10 seconds so the view stays current, and show how fresh
//      the data is. A poll must not flash the loading state over good data,
//      must not fight the user's typing, and should stop while the tab is
//      hidden.
//
// How you fetch is up to you. Native fetch in an effect, a custom hook, RTK
// Query, TanStack Query. If you reach for a library, npm install it and say
// what it buys you here.
//
// StrictMode is on in main.tsx, so effects run twice in dev. That's
// deliberate. It breaks exactly the code that items 10 and 11 are about.

import { useState } from "react";
import { SearchIcon } from "lucide-react";

import { DeviceCard } from "@/components/fleet/device-card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { useDebounce } from "@/hooks/use-debounce";
import { DEVICE_STATUSES, type DeviceStatus, type Site } from "@/types/device";

export default function App() {
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);

  // TODO: state for status filter, site filter, data, loading, error

  const debouncedSearch = useDebounce(search, 300);

  // TODO: fetch /api/sites once for the site filter
  // TODO: fetch /api/devices when debouncedSearch / status / site / page change
  // TODO: derive totalPages from total and pageSize

  return (
    <div className="min-h-svh w-full">
      <main className="container mx-auto w-full max-w-7xl px-4 py-8">
        <header className="mb-6 flex flex-wrap items-baseline justify-between gap-2">
          <h1 className="text-3xl font-bold">Fleet Monitor</h1>
          {/* TODO: data freshness, like "updated 3s ago" */}
        </header>

        <div className="flex w-full flex-col gap-6">
          <div className="flex w-full flex-wrap gap-3">
            {/* TODO: wire up search */}
            <div className="relative flex min-w-64 flex-1 items-center">
              <SearchIcon className="pointer-events-none absolute left-2 size-4 text-muted-foreground" />
              <Input
                className="pl-8"
                placeholder="Search devices or sites..."
                aria-label="Search devices"
              />
            </div>

            {/* TODO: status filter, single or multi-select, your call */}
            <Select aria-label="Filter by status" defaultValue="">
              <option value="">All statuses</option>
              {DEVICE_STATUSES.map((status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ))}
            </Select>

            {/* TODO: site filter, populated from /api/sites */}
            <Select aria-label="Filter by site" defaultValue="">
              <option value="">All sites</option>
            </Select>
          </div>

          {/* TODO: loading state */}
          {/* TODO: error state with retry */}
          {/* TODO: empty state */}

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {/* TODO: map devices to <DeviceCard /> */}
          </div>

          {/* TODO: pagination */}
          <div className="flex items-center justify-between gap-4">
            <Button variant="outline" size="sm" disabled>
              Previous
            </Button>
            <span className="text-xs text-muted-foreground">Page 1</span>
            <Button variant="outline" size="sm" disabled>
              Next
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
}
