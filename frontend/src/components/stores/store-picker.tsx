'use client';

import { StoreOption } from '@/types/deals';

interface StorePickerProps {
  zipCode: string;
  radius: number;
  selectedStore: string;
  stores: StoreOption[];
  onZipCodeChange: (value: string) => void;
  onRadiusChange: (value: number) => void;
  onStoreChange: (value: string) => void;
}

export function StorePicker(props: StorePickerProps) {
  return (
    <section className="grid gap-3 rounded-xl bg-white p-4 shadow-sm md:grid-cols-4">
      <input className="rounded-md border p-2" placeholder="ZIP code" value={props.zipCode} onChange={(e) => props.onZipCodeChange(e.target.value)} />
      <select className="rounded-md border p-2" value={props.radius} onChange={(e) => props.onRadiusChange(Number(e.target.value))}>
        {[5, 10, 25, 50].map((miles) => (
          <option key={miles} value={miles}>{miles} miles</option>
        ))}
      </select>
      <select className="rounded-md border p-2 md:col-span-2" value={props.selectedStore} onChange={(e) => props.onStoreChange(e.target.value)}>
        <option value="all">All stores</option>
        {props.stores.map((store) => (
          <option key={store.id} value={String(store.id)}>
            {store.retailer_name} #{store.store_number} - {store.city}, {store.state} ({store.distance_miles.toFixed(1)} mi)
          </option>
        ))}
      </select>
    </section>
  );
}
