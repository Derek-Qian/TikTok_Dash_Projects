# Check Product Listing

Identify any issues with your product properties in advance to ensure your product is ready for listing.
Every product must meet TikTok Shop requirements before it can be listed. Before listing, you can submit all relevant product information to this API to check whether a listing meets these requirements. You'll receive a list of issues to resolve before listing. This process helps reduce the risk of failure when creating products.
Note:
- The language used in the product content must align with the target market's language (e.g. don't use Chinese), otherwise the listing will fail or be rejected.


POST /product/202309/products/listing_check

## Request
### Example

curl -X POST \
 'https://open-api.tiktokglobalshop.com/product/202309/products/listing_check?timestamp=1623812664&app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&shop_cipher=GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3&is_diagnosis_required=true' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json' \
-d '{
  "description": "\u003cp\u003ePlease compare above detailed size with your measurement before purchase.\u003c/p\u003e\u003cul\u003e   \u003cli\u003eM-Size\u003c/li\u003e  \u003cli\u003eXL-Size\u003c/li\u003e\u003c/ul\u003e \u003cimg src=\"https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/181595ea7d26489284b5667488d708c1~tplv-o3syd03w52-origin-jpeg.jpeg?from=1432613627\" /\u003e",
  "category_id": "600001",
  "brand_id": "7082427311584347905",
  "main_images": [
    {
      "uri": "tos-maliva-i-o3syd03w52-us/c668cdf70b7f483c94dbe"
    }
  ],
  "skus": [
    {
      "sales_attributes": [
        {
          "id": "100089",
          "name": "Specification",
          "value_id": "1729592969712207000",
          "value_name": "XL",
          "sku_img": {
            "uri": "tos-maliva-i-o3syd03w52-us/c668cdf70b7f483c94dbe"
          },
          "supplementary_sku_images": [
            {
              "uri": "tos-maliva-i-o3syd03w52-us/c668cdf70b7f483c94dbe"
            }
          ]
        }
      ],
      "seller_sku": "Color-Red-XM01",
      "price": {
        "amount": "1.23",
        "currency": "USD",
        "sale_price": "1.21",
        "starting_bid_price": "2.3"
      },
      "external_sku_id": "1729592969712207012",
      "identifier_code": {
        "code": "10000000000000",
        "type": "GTIN"
      },
      "inventory": [
        {
          "warehouse_id": "7068517275539719942",
          "quantity": 999,
          "backorder_quantity": 888,
          "handling_time": 5
        }
      ],
      "combined_skus": [
        {
          "product_id": "1729582718312380123",
          "sku_id": "1729582718312380123",
          "sku_count": 11
        }
      ],
      "sku_unit_count": "100.00",
      "external_urls": [
        "https://example.com/path1",
        "https://example.com/path2"
      ],
      "extra_identifier_codes": [
        "00012345678905",
        "9780596520687"
      ],
      "pre_sale": {
        "type": "PRE_ORDER",
        "fulfillment_type": {
          "handling_duration_days": 24,
          "release_date": 1619611761
        }
      },
      "list_price": {
        "amount": "1",
        "currency": "USD"
      },
      "external_list_prices": [
        {
          "source": "SHOPIFY_COMPARE_AT_PRICE",
          "amount": "1",
          "currency": "USD"
        }
      ],
      "fees": [
        {
          "type": "PFAND",
          "amount": "1.01",
          "additional_attribute": "SINGLE_USE"
        }
      ],
      "sku_dimensions": {
        "length": "10",
        "width": "10",
        "height": "10",
        "unit": "CENTIMETER"
      },
      "sku_weight": {
        "value": "1.32",
        "unit": "KILOGRAM"
      }
    }
  ],
  "title": "Men'\''s Fashion Sports Low Cut Cotton Breathable Ankle Short Boat Invisible Socks",
  "is_cod_allowed": false,
  "certifications": [
    {
      "id": "7182427311584347905",
      "images": [
        {
          "uri": "tos-maliva-i-o3syd03w52-us/c668cdf70b7f483c94dbe"
        }
      ],
      "files": [
        {
          "id": "v09ea0g40000cj91373c77u3mid3g1s0",
          "name": "SNI.PDF",
          "format": "PDF"
        }
      ],
      "expiration_date": 1741234626
    }
  ],
  "package_weight": {
    "value": "1.32",
    "unit": "KILOGRAM"
  },
  "product_attributes": [
    {
      "id": "100392",
      "values": [
        {
          "id": "1001533",
          "name": "Birthday"
        }
      ]
    }
  ],
  "size_chart": {
    "image": {
      "uri": "tos-maliva-i-o3syd03w52-us/c668cdf70b7f483c94dbe"
    },
    "template": {
      "id": "7267563252536723205"
    }
  },
  "package_dimensions": {
    "length": "10",
    "width": "10",
    "height": "10",
    "unit": "CENTIMETER"
  },
  "external_product_id": "172959296971220002",
  "delivery_option_ids": [
    "1729592969712203232"
  ],
  "video": {
    "id": "v09e40f40000cfu0ovhc77ub7fl97k4w"
  },
  "primary_combined_product_id": "1729582718312380123",
  "manufacturer_ids": [
    "172959296971220002"
  ],
  "responsible_person_ids": [
    "172959296971220003"
  ],
  "listing_platforms": [
    "TIKTOK_SHOP"
  ],
  "shipping_insurance_requirement": "NOT_SUPPORTED",
  "is_pre_owned": false,
  "minimum_order_quantity": 4,
  "shipping_template_id": "7552764259994699538",
  "option": {
    "need_trigger_gne_async_check": false,
    "gne_async_check_session_id": "20260122085233268"
  },
  "scheduled_sale": {
    "is_enabled_scheduled_sale": false,
    "schedule_sale_time": 1768899145000
  },
  "search_terms": [
    "sneakers",
    "running shoes",
    "athletic"
  ],
  "key_product_features": [
    "Breathable mesh upper",
    "Cushioned foam midsole"
  ],
  "product_tag_operations": [
    {
      "product_tag": "AUCTION",
      "enable": true
    }
  ],
  "locale": "en-US"
}'


## Response
### Example

{
  "code": 0,
  "data": {
    "check_result": "FAILED",
    "fail_reasons": [
      {
        "code": 12052700,
        "message": "Product title invalid"
      }
    ],
    "warnings": {
      "message": "Your product will not be sent for review. "
    },
    "listing_quality": {
      "current_tier": "POOR",
      "remaining_recommendations": 3
    },
    "diagnoses": [
      {
        "field": "TITLE",
        "diagnosis_results": [
          {
            "code": "TITLE_LESS_THAN_40_CHARACTERS",
            "how_to_solve": "Names must be at least 40 characters long and contain product-identifying information, such as \"hiking boots\" or \"lipstick\".",
            "quality_tier": "POOR"
          }
        ],
        "suggestions": {
          "seo_words": [
            {
              "text": "dress"
            }
          ],
          "smart_texts": [
            {
              "text": "this is a good title"
            }
          ],
          "images": [
            {
              "uri": "tos-maliva-i-o3syd03w52-us/53b55d6e8cdf1f315affa7e70b45707d",
              "url": "https://p16-graph-va.ibyteimg.com/tos-maliva-i-1por3rr4fy-us/v2/53b55d6e8cdf1f315affa7e70b45707d~tplv-1por3rr4fy-image.webp",
              "optimized_uri": "tos-maliva-i-o3syd03w52-us/0266127022264e54ad2f639f5e0fb5e6",
              "optimized_url": "https://p16-graph-va.ibyteimg.com/tos-maliva-i-1por3rr4fy-us/v2/0266127022264e54ad2f639f5e0fb5e6~tplv-1por3rr4fy-image.webp",
              "height": 600,
              "width": 600
            }
          ]
        }
      }
    ],
    "pre_check_results": [
      {
        "pre_check_item": "INCOMPLETE_INFO",
        "pre_check_details": [
          {
            "short_reason": "Insufficient or Incomplete Product Information",
            "long_reason": "Ensure product title and description contain complete information that accurately describes the product",
            "related_fields": [
              "PRE_CHECK_FIELD_TITLE"
            ]
          }
        ]
      }
    ]
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}

## Error Code

| Code | Message |
|------|---------|
| 12001000 | product api internal error |
| 12019006 | product description is invalid |
| 12019011 | product package weight is invalid |
| 12019095 | `pre_sale_fulfillment_type` is missing or empty |
| 12019097 | `pre_sale_fulfillment_type.release_date` must be set to a non-zero value |
| 12019098 | `pre_sale_fulfillment_type.handling_duration_days` must be set to a non-zero value |
| 12019099 | The specified `pre_sale_type` is not supported in your region. Refer to the API documentation for details. |
| 12019121 | calculate price error |
| 12052003 | Incorrect parcel height format |
| 12052004 | Incorrect parcel width format |
| 12052005 | Incorrect parcel length format |
| 12052023 | Category does not exist |
| 12052024 | Category is not final category |
| 12052084 | The provided currency is not available for this shop/region |
| 12052220 | This category is prohibited or unsupported on TikTok Shop. Select another category. |
| 12052223 | This category is restricted. To sell in this category, apply through the Qualification Center in Seller Center. |
| 12052226 | This category is restricted. To sell in this category, apply through the Qualification Center in Seller Center. |
| 12052300 | product main image uri illegal |
| 12052356 | The number of 'supplementary_sku_images' for the sales attribute value exceeds the maximum limit |
| 12052357 | 'supplementary_sku_images' is only allowed when 'sku_img' is specified. Add an image to 'sku_img' and try again. |
| 12052446 | Category is not open in this market |
| 12052520 | product sale property image uri illegal |
| 12052650 | product qualification image uri illegal |
| 12052670 | The size chart image URI is invalid. Note: API users must use the URI generated by the Upload Product Image API. |
| 12052700 | The seller is inactive. |
| 12052722 | The image URI does not exist in TikTok Shop. |
| 12052881 | identity internal error |
| 36009003 | Internal error. Please try again. If the issue persists after multiple attempts, please contact platform support. |
| 12052910 | Invalid input parameters. Refer to the API documentation for details. |
| 12052915 | package weight unit and dimension unit miss match |
| 12052916 | The package unit is not supported in the current region. |
| 12052928 | The title must follow these formatting rules: it cannot contain HTML escape characters (e.g., `&nbsp;`), emojis, or ASCII control characters (e.g., `\u007F`). It also cannot consist solely of symbols (e.g., `///` or `@#$%&`), nor can it have more than 9 consecutive repeated characters (e.g., `aaaaaaaaa` or `111111111`). |
| 12052929 | The description must follow these formatting rules: it cannot contain HTML escape characters (e.g., `&nbsp;`), emojis, or ASCII control characters (e.g., `\u007F`). It also cannot consist solely of symbols (e.g., `///` or `@#$%&`), nor can it have more than 9 consecutive repeated characters (e.g., `aaaaaaaaa` or `111111111`). |
| 12052933 | Sales attribute names must follow these formatting rules: it cannot contain HTML escape characters (e.g., `&nbsp;`), emojis, or ASCII control characters (e.g., `\u007F`). It also cannot consist solely of symbols (e.g., `///` or `@#$%&`), nor can it have more than 9 consecutive repeated characters (e.g., `aaaaaaaaa` or `111111111`). |
| 12052934 | Sales attribute value names must follow these formatting rules: it cannot contain HTML escape characters (e.g., `&nbsp;`), emojis, or ASCII control characters (e.g., `\u007F`). It also cannot consist solely of symbols (e.g., `///` or `@#$%&`), nor can it have more than 9 consecutive repeated characters (e.g., `aaaaaaaaa` or `111111111`). |
| 12052935 | Product attribute value names must follow these formatting rules: it cannot contain HTML escape characters (e.g., `&nbsp;`), emojis, or ASCII control characters (e.g., `\u007F`). It also cannot consist solely of symbols (e.g., `///` or `@#$%&`), nor can it have more than 9 consecutive repeated characters (e.g., `aaaaaaaaa` or `111111111`). |
