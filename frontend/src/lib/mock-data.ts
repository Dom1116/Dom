import { DealRow } from '@/types/deals';

export const MOCK_DEALS: DealRow[] = [
  {
    id: '1', retailer: 'walmart', storeName: 'Walmart Supercenter', storeNumber: '1001', city: 'Austin', state: 'TX',
    productTitle: 'Cordless Impact Driver Kit', brand: 'HyperTough', sku: 'WM-123', upc: '012345678901',
    currentPrice: 49, originalPrice: 89, discountPercent: 44.94, clearanceLabel: 'Clearance', stockLevel: 8,
    confidence: 0.78, productUrl: '#', imageUrl: 'https://picsum.photos/300/300', estimatedProfit: 22, estimatedRoi: 44.9, updatedAt: '2026-03-20T00:00:00Z'
  },
  {
    id: '2', retailer: 'target', storeName: 'Target North', storeNumber: 'T-204', city: 'Austin', state: 'TX',
    productTitle: 'LEGO Creator Set', brand: 'LEGO', sku: 'TG-55', upc: '333222111999',
    currentPrice: 19.99, originalPrice: 39.99, discountPercent: 50, clearanceLabel: 'Sale', stockLevel: 3,
    confidence: 0.71, productUrl: '#', imageUrl: 'https://picsum.photos/301/300', estimatedProfit: 14, estimatedRoi: 70, updatedAt: '2026-03-20T00:00:00Z'
  }
];
