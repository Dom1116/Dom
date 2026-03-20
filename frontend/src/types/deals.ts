export type RetailerCode = 'homedepot' | 'costco' | 'walmart' | 'target';

export interface DealRow {
  id: string;
  retailer: RetailerCode;
  storeName: string;
  storeNumber?: string;
  city: string;
  state: string;
  productTitle: string;
  brand?: string;
  sku: string;
  upc?: string;
  currentPrice: number;
  originalPrice?: number;
  discountPercent: number;
  clearanceLabel?: string;
  stockLevel?: number;
  confidence: number;
  productUrl: string;
  imageUrl: string;
  estimatedProfit: number;
  estimatedRoi: number;
  updatedAt: string;
}
