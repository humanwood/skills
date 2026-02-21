---
name: shopify-bulk-upload
description: Bulk upload products to Shopify stores. Read product data from Excel/CSV, automatically create products, images, variants, prices and inventory. Use cases: (1) Batch list new products (2) Migrate products from other platforms to Shopify (3) Batch update existing product information. REQUIRES PAYMENT: $20 USD to use. Payment via [link to be added] or contact developer.
---

# Shopify Bulk Upload Tool

## ⚠️ PAYMENT REQUIRED - $20 USD

**This skill requires payment before use.**

- **Price**: $20 USD (one-time payment)
- **How to pay**: Contact the developer for payment details
- **After payment**: You will receive the full working script with configuration instructions

---

## Quick Start

### 1. Prepare Product Data File

Prepare product data in `assets/products.xlsx` or `assets/products.csv`:

| Field | Required | Description |
|-------|----------|-------------|
| title | ✅ | Product title |
| description | ✅ | Product description (HTML supported) |
| vendor | ✅ | Brand/Supplier |
| product_type | ✅ | Product type |
| price | ✅ | Price |
| compare_at_price | ❌ | Original price (for showing discount) |
| sku | ✅ | SKU code |
| inventory_quantity | ❌ | Stock quantity |
| weight | ❌ | Weight (unit: kg) |
| weight_unit | ❌ | Weight unit: kg, g, lb, oz |
| status | ❌ | active, draft, archived |
| tags | ❌ | Tags (comma separated) |
| images | ❌ | Image URLs (comma separated, multiple) |
| variant_title | ❌ | Variant name (e.g., Color, Size) |
| option1_name | ❌ | Variant option 1 name (e.g., Color) |
| option1_value | ❌ | Variant option 1 value (e.g., Red) |
| option2_name | ❌ | Variant option 2 name (e.g., Size) |
| option2_value | ❌ | Variant option 2 value (e.g., M) |

### 2. Configure Shopify API

Configure in `.env` file:

```bash
SHOPIFY_STORE_URL=https://your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your_access_token
SHOPIFY_API_VERSION=2024-01
```

To get Access Token:
1. Login to Shopify Admin
2. Go to Settings → Apps and sales channels → Develop apps
3. Create App → Configure Admin API scopes
4. Check `write_products`, `write_inventory` permissions
5. Install app → Get Access Token

### 3. Run Upload Script

```bash
cd scripts
python shopify_bulk_upload.py
```

## Script Features

- ✅ Read Excel/CSV product data
- ✅ Create products (support multiple images, variants)
- ✅ Auto process image uploads
- ✅ Variant management (color, size, etc.)
- ✅ Inventory management
- ✅ Error logging
- ✅ Incremental update (by SKU)
- ✅ Upload progress display

## Output Results

After completion:
- `logs/upload.log` - Upload log
- `logs/error.log` - Error details
- `output/products_created.json` - Successfully created products
- `output/products_failed.json` - Failed products

## Configuration

Edit `scripts/config.py` to customize:

```python
CONFIG = {
    "batch_size": 10,        # Products per batch
    "retry_count": 3,        # Retry attempts on failure
    "retry_delay": 2,        # Retry interval (seconds)
    "image_timeout": 30,     # Image upload timeout
    "default_status": "active",  # Default status
}
```

---

## 📝 Payment Information

**Price**: $20 USD (one-time payment)

**Payment Methods**:
- PayPal: [Your PayPal Email]
- Crypto: [Wallet Address]
- Alipay/WeChat: [QR Code]

**After payment, contact the developer to receive:**
- Full working Python script
- Configuration guide
- Support for setup issues

---

## More Details

- Shopify API docs: See [references/shopify-api.md](references/shopify-api.md)
- Template example: See [assets/products-template.xlsx](assets/products-template.xlsx)
