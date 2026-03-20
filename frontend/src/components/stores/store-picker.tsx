'use client';

interface StorePickerProps {
  zipCode: string;
  radius: number;
  selectedStore: string;
  onZipCodeChange: (value: string) => void;
  onRadiusChange: (value: number) => void;
  onStoreChange: (value: string) => void;
}

const STORE_OPTIONS = [
  { value: 'all', label: 'All stores' },
  { value: 'wm-1001', label: 'Walmart #1001 - Austin, TX' },
  { value: 'tg-204', label: 'Target #T-204 - Austin, TX' },
  { value: 'hd-402', label: 'Home Depot #402 - Austin, TX' },
  { value: 'co-18', label: 'Costco #18 - Austin, TX' },
];

export function StorePicker(props: StorePickerProps) {
  return (
    <section className="grid gap-3 rounded-xl bg-white p-4 shadow-sm md:grid-cols-4">
      <input
        className="rounded-md border p-2"
        placeholder="ZIP code"
        value={props.zipCode}
        onChange={(event) => props.onZipCodeChange(event.target.value)}
      />
      <select
        className="rounded-md border p-2"
        value={props.radius}
        onChange={(event) => props.onRadiusChange(Number(event.target.value))}
      >
        {[5, 10, 25, 50].map((miles) => (
          <option key={miles} value={miles}>{miles} miles</option>
        ))}
      </select>
      <select
        className="rounded-md border p-2 md:col-span-2"
        value={props.selectedStore}
        onChange={(event) => props.onStoreChange(event.target.value)}
      >
        {STORE_OPTIONS.map((store) => (
          <option key={store.value} value={store.value}>{store.label}</option>
        ))}
      </select>
    </section>
  );
}
