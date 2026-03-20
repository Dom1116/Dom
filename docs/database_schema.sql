CREATE TABLE retailers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  code VARCHAR(32) NOT NULL UNIQUE,
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE stores (
  id SERIAL PRIMARY KEY,
  retailer_id INT NOT NULL REFERENCES retailers(id),
  store_number VARCHAR(64),
  name VARCHAR(128) NOT NULL,
  address_line1 VARCHAR(255) NOT NULL,
  city VARCHAR(100) NOT NULL,
  state VARCHAR(2) NOT NULL,
  zip_code VARCHAR(10) NOT NULL,
  latitude NUMERIC(10,7),
  longitude NUMERIC(10,7)
);

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  title VARCHAR(500) NOT NULL,
  brand VARCHAR(150),
  upc_gtin VARCHAR(32),
  model_number VARCHAR(100),
  category VARCHAR(120),
  image_url TEXT
);

CREATE TABLE store_products (
  id SERIAL PRIMARY KEY,
  store_id INT NOT NULL REFERENCES stores(id),
  product_id INT NOT NULL REFERENCES products(id),
  retailer_item_id VARCHAR(120) NOT NULL,
  current_price NUMERIC(10,2) NOT NULL,
  original_price NUMERIC(10,2),
  markdown_label VARCHAR(80),
  inventory_status VARCHAR(40),
  stock_level INT,
  pickup_available BOOLEAN NOT NULL DEFAULT FALSE,
  shipping_available BOOLEAN NOT NULL DEFAULT FALSE,
  quantity_text VARCHAR(120),
  product_url TEXT,
  last_seen_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE price_history (
  id SERIAL PRIMARY KEY,
  store_product_id INT NOT NULL REFERENCES store_products(id),
  observed_price NUMERIC(10,2) NOT NULL,
  observed_original_price NUMERIC(10,2),
  observed_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE marketplace_matches (
  id SERIAL PRIMARY KEY,
  store_product_id INT NOT NULL REFERENCES store_products(id),
  marketplace VARCHAR(50) NOT NULL,
  external_listing_id VARCHAR(120),
  estimated_sell_price NUMERIC(10,2),
  confidence NUMERIC(4,3) NOT NULL DEFAULT 0,
  match_factors JSONB NOT NULL DEFAULT '{}'
);

CREATE TABLE resale_estimates (
  id SERIAL PRIMARY KEY,
  store_product_id INT NOT NULL REFERENCES store_products(id),
  gross_profit NUMERIC(10,2) NOT NULL,
  net_profit NUMERIC(10,2) NOT NULL,
  roi_percent NUMERIC(8,2) NOT NULL,
  margin_percent NUMERIC(8,2) NOT NULL,
  risk_score NUMERIC(5,2) NOT NULL,
  opportunity_score NUMERIC(5,2) NOT NULL,
  confidence NUMERIC(4,3) NOT NULL DEFAULT 0
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  display_name VARCHAR(120)
);

CREATE TABLE alerts (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id),
  retailer_code VARCHAR(32),
  store_id INT REFERENCES stores(id),
  min_profit NUMERIC(10,2),
  min_roi NUMERIC(8,2),
  keyword VARCHAR(120),
  category VARCHAR(120),
  channel VARCHAR(20) NOT NULL DEFAULT 'email',
  destination VARCHAR(255) NOT NULL
);

CREATE TABLE watchlists (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id),
  store_product_id INT NOT NULL REFERENCES store_products(id),
  notes TEXT
);
