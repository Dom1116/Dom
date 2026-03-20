'use client';

import { useMemo, useState } from 'react';

import { MOCK_DEALS } from '@/lib/mock-data';
import { DealRow, RetailerCode } from '@/types/deals';
import { StorePicker } from '@/components/stores/store-picker';

const SORT_OPTIONS = ['biggest_discount', 'highest_profit', 'highest_roi', 'newest', 'most_stock'] as const;

export function AllStoreDealsPage() {
  const [retailer, setRetailer] = useState<'all' | RetailerCode>('all');
  const [storeId, setStoreId] = useState('all');
  const [zipCode, setZipCode] = useState('78701');
  const [radius, setRadius] = useState(25);
  const [sortBy, setSortBy] = useState<(typeof SORT_OPTIONS)[number]>('highest_roi');

  const filtered = useMemo(() => {
    let rows = [...MOCK_DEALS];

    if (retailer !== 'all') rows = rows.filter((deal) => deal.retailer === retailer);
    if (storeId !== 'all') rows = rows.filter((deal) => deal.id === (storeId === 'wm-1001' ? '1' : '2'));

    return rows.sort((a, b) => {
      switch (sortBy) {
        case 'biggest_discount':
          return b.discountPercent - a.discountPercent;
        case 'highest_profit':
          return b.estimatedProfit - a.estimatedProfit;
        case 'highest_roi':
          return b.estimatedRoi - a.estimatedRoi;
        case 'most_stock':
          return (b.stockLevel ?? 0) - (a.stockLevel ?? 0);
        default:
          return b.updatedAt.localeCompare(a.updatedAt);
      }
    });
  }, [retailer, storeId, sortBy]);

  return (
    <main className="mx-auto flex max-w-7xl flex-col gap-4 p-6">
      <h1 className="text-2xl font-bold">All Store Deals</h1>
      <p className="text-sm text-slate-600">Compare Home Depot, Costco, Walmart, and Target deals by local store.</p>

      <StorePicker
        zipCode={zipCode}
        radius={radius}
        selectedStore={storeId}
        onZipCodeChange={setZipCode}
        onRadiusChange={setRadius}
        onStoreChange={setStoreId}
      />

      <section className="flex flex-wrap gap-2">
        {['all', 'homedepot', 'costco', 'walmart', 'target'].map((tab) => (
          <button
            key={tab}
            className={`rounded-full px-3 py-1 text-sm ${retailer === tab ? 'bg-slate-900 text-white' : 'bg-white'}`}
            onClick={() => setRetailer(tab as 'all' | RetailerCode)}
          >
            {tab}
          </button>
        ))}

        <select className="ml-auto rounded-md border p-2" value={sortBy} onChange={(e) => setSortBy(e.target.value as (typeof SORT_OPTIONS)[number])}>
          <option value="biggest_discount">Biggest discount</option>
          <option value="highest_profit">Highest profit</option>
          <option value="highest_roi">Highest ROI</option>
          <option value="newest">Newest markdown</option>
          <option value="most_stock">Stock level</option>
        </select>
      </section>

      <DealsTable rows={filtered} />
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
            <th className="p-3">Est Profit</th>
            <th className="p-3">ROI</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id} className="border-t">
              <td className="p-3">{row.retailer}</td>
              <td className="p-3">{row.storeName}</td>
              <td className="p-3">{row.productTitle}</td>
              <td className="p-3">${row.currentPrice.toFixed(2)}</td>
              <td className="p-3">{row.discountPercent.toFixed(1)}%</td>
              <td className="p-3">{row.stockLevel ?? '-'}</td>
              <td className="p-3">${row.estimatedProfit.toFixed(2)}</td>
              <td className="p-3">{row.estimatedRoi.toFixed(1)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
