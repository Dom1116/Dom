'use client';

import { useEffect, useMemo, useState } from 'react';

import { StorePicker } from '@/components/stores/store-picker';
import { DealRow, RetailerCode, StoreOption } from '@/types/deals';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000/api/v1';

export function AllStoreDealsPage() {
  const [retailer, setRetailer] = useState<'all' | RetailerCode>('all');
  const [storeId, setStoreId] = useState('all');
  const [zipCode, setZipCode] = useState('78701');
  const [radius, setRadius] = useState(25);
  const [sortBy, setSortBy] = useState('highest_roi');
  const [search, setSearch] = useState('');
  const [clearanceOnly, setClearanceOnly] = useState(false);
  const [highResaleOnly, setHighResaleOnly] = useState(false);
  const [stores, setStores] = useState<StoreOption[]>([]);
  const [deals, setDeals] = useState<DealRow[]>([]);

  useEffect(() => {
    const params = new URLSearchParams({ zip_code: zipCode, radius_miles: String(radius) });
    fetch(`${API_BASE}/stores/nearby?${params.toString()}`)
      .then((response) => response.json())
      .then((data: StoreOption[]) => setStores(data))
      .catch(() => setStores([]));
  }, [zipCode, radius]);

  useEffect(() => {
    const payload = {
      zip_code: zipCode,
      radius_miles: radius,
      retailer_codes: retailer === 'all' ? [] : [retailer],
      store_ids: storeId === 'all' ? [] : [Number(storeId)],
      sort_by: sortBy,
      search: search || null,
      clearance_only: clearanceOnly,
      high_resale_only: highResaleOnly,
    };

    fetch(`${API_BASE}/deals/all-store`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
      .then((response) => response.json())
      .then((data: DealRow[]) => setDeals(data))
      .catch(() => setDeals([]));
  }, [zipCode, radius, retailer, storeId, sortBy, search, clearanceOnly, highResaleOnly]);

  const totalProfit = useMemo(() => deals.reduce((sum, d) => sum + d.estimated_resale_profit, 0), [deals]);

  return (
    <main className="mx-auto flex max-w-7xl flex-col gap-4 p-6">
      <h1 className="text-2xl font-bold">All Store Deals</h1>
      <p className="text-sm text-slate-600">Live API-backed deals for Home Depot, Costco, Walmart, and Target.</p>

      <StorePicker
        zipCode={zipCode}
        radius={radius}
        selectedStore={storeId}
        stores={stores}
        onZipCodeChange={setZipCode}
        onRadiusChange={setRadius}
        onStoreChange={setStoreId}
      />

      <section className="flex flex-wrap gap-2">
        {['all', 'homedepot', 'costco', 'walmart', 'target'].map((tab) => (
          <button key={tab} className={`rounded-full px-3 py-1 text-sm ${retailer === tab ? 'bg-slate-900 text-white' : 'bg-white'}`} onClick={() => setRetailer(tab as 'all' | RetailerCode)}>
            {tab}
          </button>
        ))}
        <input className="rounded-md border p-2" placeholder="Search title or brand" value={search} onChange={(e) => setSearch(e.target.value)} />
        <select className="rounded-md border p-2" value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="biggest_discount">Biggest discount</option>
          <option value="highest_profit">Highest profit</option>
          <option value="highest_roi">Highest ROI</option>
          <option value="newest">Newest markdown</option>
          <option value="most_stock">Most stock</option>
        </select>
      </section>

      <section className="flex gap-2 text-sm">
        <button className={`rounded-md px-3 py-1 ${!clearanceOnly ? 'bg-slate-900 text-white' : 'bg-white'}`} onClick={() => setClearanceOnly(false)}>All deals</button>
        <button className={`rounded-md px-3 py-1 ${clearanceOnly ? 'bg-slate-900 text-white' : 'bg-white'}`} onClick={() => setClearanceOnly(true)}>Clearance only</button>
        <button className={`rounded-md px-3 py-1 ${highResaleOnly ? 'bg-slate-900 text-white' : 'bg-white'}`} onClick={() => setHighResaleOnly((v) => !v)}>High resale potential</button>
        <span className="ml-auto text-slate-500">Deals: {deals.length} • Est total profit: ${totalProfit.toFixed(2)}</span>
      </section>

      <DealsTable rows={deals} />
    </main>
  );
}

function DealsTable({ rows }: { rows: DealRow[] }) {
  return (
    <div className="overflow-x-auto rounded-xl bg-white shadow-sm">
      <table className="min-w-full text-sm">
        <thead className="bg-slate-100 text-left">
          <tr>
            <th className="p-3">Retailer</th><th className="p-3">Store</th><th className="p-3">Product</th><th className="p-3">Price</th><th className="p-3">Discount</th><th className="p-3">Stock</th><th className="p-3">Profit</th><th className="p-3">ROI</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={`${row.store_id}-${row.sku_item_id}`} className="border-t">
              <td className="p-3">{row.retailer_name}</td>
              <td className="p-3">#{row.store_number} {row.store_location}</td>
              <td className="p-3">{row.product_title}</td>
              <td className="p-3">${Number(row.current_price).toFixed(2)}</td>
              <td className="p-3">{Number(row.discount_percent).toFixed(1)}%</td>
              <td className="p-3">{row.stock_level ?? '-'}</td>
              <td className="p-3">${Number(row.estimated_resale_profit).toFixed(2)}</td>
              <td className="p-3">{Number(row.estimated_roi).toFixed(1)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
