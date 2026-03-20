export type RetailerCode = 'homedepot' | 'costco' | 'walmart' | 'target';

export interface DealRow {
  retailer_name: string;
  retailer_code: RetailerCode;
  store_id: number;
  store_location: string;
  store_number?: string;
  product_title: string;
  brand?: string;
  sku_item_id: string;
  upc_gtin?: string;
  current_price: number;
  original_price?: number;
  discount_percent: number;
  clearance_label?: string;
  stock_level?: number;
  deal_confidence: number;
  product_url: string;
  image_url: string;
  estimated_resale_profit: number;
  estimated_roi: number;
  updated_at: string;
}

export interface StoreOption {
  id: number;
  retailer_code: RetailerCode;
  retailer_name: string;
  store_number: string;
  name: string;
  city: string;
  state: string;
  zip_code: string;
  distance_miles: number;
}
