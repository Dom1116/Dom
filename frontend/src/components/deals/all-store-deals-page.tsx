'use client';

import { useEffect, useMemo, useState } from 'react';

import { DealRow, RetailerCode } from '@/types/deals';
import { StorePicker } from '@/components/stores/store-picker';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000/api/v1';

export function AllStoreDealsPage() {
  const [retailer, setRetailer] = useState<'all' | RetailerCode>('all');
  const [storeId, setStoreId] = useState('all');
  const [zipCode, setZipCode] = useState('78701');
  const [radius, setRadius] = useState(25);
  const [sortBy, setSortBy] = useState('highest_roi');
  const [rows, setRows] = useState<DealRow[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const run = async () => {
      setLoading(true);
      const body = {
        retailer_codes: retailer === 'all' ? [] : [retailer],
        zip_code: zipCode,
        radius_miles: radius,
        store_ids: storeId === 'all' ? [] : [storeId],
        sort_by: sortBy,
      };

      const response = await fetch(`${API_BASE}/deals/all-store`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      const data = (await response.json()) as DealRow[];
      setRows(data);
      setLoading(false);
    };

    run();
  }, [retailer, storeId, zipCode, radius, sortBy]);

  const summary = useMemo(() => {
    const totalProfit = rows.reduce((sum, deal) => sum + Number(deal.estimated_resale_profit), 0);
    const avgRoi = rows.length ? rows.reduce((sum, deal) => sum + Number(deal.estimated_roi), 0) / rows.length : 0;
    return { totalProfit, avgRoi };
  }, [rows]);

  return (
    <main className="mx-auto flex max-w-7xl flex-col gap-4 p-6">
      <h1 className="text-2xl font-bold">All Store Deals</h1>
      <p className="text-sm text-slate-600">Personal deal finder: pick stores and immediately rank by discount, profit, ROI, or stock.</p>

      <StorePicker
        zipCode={zipCode}
        radius={radius}
        selectedStore={storeId}
        onZipCodeChange={setZipCode}
        onRadiusChange={setRadius}
        onStoreChange={setStoreId}
      />

      <section className="flex flex-wrap items-center gap-2">
        {(['all', 'homedepot', 'costco', 'walmart', 'target'] as const).map((tab) => (
          <button
            key={tab}
            className={`rounded-full px-3 py-1 text-sm ${retailer === tab ? 'bg-slate-900 text-white' : 'bg-white'}`}
            onClick={() => setRetailer(tab)}
          >
            {tab}
          </button>
        ))}

        <select className="ml-auto rounded-md border p-2" value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="biggest_discount">Biggest discount</option>
          <option value="highest_profit">Highest profit</option>
          <option value="highest_roi">Highest ROI</option>
          <option value="newest">Newest markdown</option>
          <option value="most_stock">Most stock</option>
        </select>
      </section>

      <section className="grid grid-cols-1 gap-3 md:grid-cols-3">
        <div className="rounded-lg bg-white p-3 shadow-sm">Deals: <strong>{rows.length}</strong></div>
        <div className="rounded-lg bg-white p-3 shadow-sm">Total Est Profit: <strong>${summary.totalProfit.toFixed(2)}</strong></div>
        <div className="rounded-lg bg-white p-3 shadow-sm">Avg ROI: <strong>{summary.avgRoi.toFixed(1)}%</strong></div>
      </section>

      {loading ? <div>Loading deals…</div> : <DealsTable rows={rows} />}
    </main>
  );
}

function DealsTable({ rows }: { rows: DealRow[] }) {
  return (
    <div className="overflow-x-auto rounded-xl bg-white shadow-sm">
      <table className="min-w-full text-sm">
        <thead className="bg-slate-100 text-left">
          <tr>
            <th className="p-3">Retailer</th>
            <th className="p-3">Store</th>
            <th className="p-3">Product</th>
            <th className="p-3">Price</th>
            <th className="p-3">Discount</th>
            <th className="p-3">Stock</th>
            <th className="p-3">Profit</th>
            <th className="p-3">ROI</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={`${row.retailer_name}-${row.sku_item_id}-${row.store_number}`} className="border-t">
              <td className="p-3">{row.retailer_name}</td>
              <td className="p-3">{row.store_location}</td>
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
