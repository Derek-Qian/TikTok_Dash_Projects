# Create Product

Create and list products intended for sale exclusively in local shops.
You can create products in AVAILABLE categories. (US sellers can also create products in INVITE_ONLY categories). After creation, it will be sent for audit review by TikTok Shop. Use the Product status change webhook to keep track of the review status.
Note:
- This API is applicable for all sellers.
- Global sellers who have migrated to use the local replication listing method can use this API to create products. Otherwise, they can continue to use the Create Global Product API to create global products.
- Before calling this API, we recommend that you prepare the necessary information by following the usage flow for your region.
- There may be a limit to the number of products you can list per day. We recommend prioritizing the creation of key products first to ensure they get published. Refer to TikTok Shop Academy for details on the limit.
- The language used in the product content must align with the target market's language (e.g. don't use Chinese), otherwise the listing will fail or be rejected.

POST /product/202309/products

## Request
### Example

curl -X POST \
 'https://open-api.tiktokglobalshop.com/product/202309/products?timestamp=1623812664&app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&shop_cipher=GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json' \
-d '{
  "save_mode": "LISTING",
  "description": " \u003cp\u003ePlease check the measurements before purchase.\u003c/p\u003e\u003cul\u003e   \u003cli\u003eM-Size\u003c/li\u003e  \u003cli\u003eXL-Size\u003c/li\u003e\u003c/ul\u003e \u003cimg src=\"https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/181595ea7d26489284b5667488d708c1~tplv-o3syd03w52-origin-jpeg.jpeg?from=1432613627\" width='100' height='100' /\u003e ",
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
          "value_id": "1729592969712207000",
          "value_name": "Red",
          "sku_img": {
            "uri": "tos-maliva-i-o3syd03w52-us/c668cdf70b7f483c94dbe"
          },
          "name": "Color",
          "supplementary_sku_images": [
            {
              "uri": "tos-maliva-i-o3syd03w52-us/c668cdf70b7f483c94dbe"
            }
          ]
        }
      ],
      "inventory": [
        {
          "warehouse_id": "7068517275539719942",
          "quantity": 999,
          "backorder_quantity": 888,
          "handling_time": 5
        }
      ],
      "seller_sku": "Color-Red-XM001",
      "price": {
        "amount": "1.21",
        "currency": "USD",
        "sale_price": "1.21",
        "starting_bid_price": "2.22"
      },
      "external_sku_id": "1729592969712207012",
      "identifier_code": {
        "code": "10000000000000",
        "type": "GTIN"
      },
      "combined_skus": [
        {
          "product_id": "1729582718312380123",
          "sku_id": "2729382476852921560",
          "sku_count": 1
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
          "handling_duration_days": 7,
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
        "value": "1,32",
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
          "name": "brand_cert.PDF",
          "format": "PDF"
        }
      ],
      "expiration_date": 1741234626
    }
  ],
  "package_dimensions": {
    "length": "10",
    "width": "10",
    "height": "10",
    "unit": "CENTIMETER"
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
  "package_weight": {
    "value": "1.32",
    "unit": "KILOGRAM"
  },
  "video": {
    "id": "v09e40f40000cfu0ovhc77ub7fl97k4w"
  },
  "external_product_id": "172959296971220002",
  "delivery_option_ids": [
    "1729592969712203232"
  ],
  "size_chart": {
    "image": {
      "uri": "tos-maliva-i-o3syd03w52-us/c668cdf70b7f483c94dbe"
    },
    "template": {
      "id": "7267563252536723205"
    }
  },
  "primary_combined_product_id": "1729582718312380123",
  "is_not_for_sale": true,
  "category_version": "v1",
  "manufacturer_ids": [
    "172959296971220002"
  ],
  "responsible_person_ids": [
    "172959296971220003"
  ],
  "listing_platforms": [
    "TIKTOK_SHOP"
  ],
  "shipping_insurance_requirement": "REQUIRED",
  "minimum_order_quantity": 1,
  "is_pre_owned": false,
  "idempotency_key": "create202208291503530001100220033",
  "shipping_template_id": "7552764259994699538",
  "scheduled_sale": {
    "is_enabled_scheduled_sale": false,
    "schedule_sale_time": 1768899145000
  },
  "locale": "en-US",
  "auto_translate_enabled": false,
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
      "enable": false
    }
  ]
}'


## Response
### Example

{
  "code": 0,
  "data": {
    "product_id": "1729592969712207008",
    "skus": [
      {
        "id": "1729592969712207012",
        "seller_sku": "Color-Red-XM001",
        "sales_attributes": [
          {
            "id": "100000",
            "value_id": "1729592969712207123"
          }
        ],
        "external_sku_id": "1729592969712207234",
        "fees": [
          {
            "type": "PFAND",
            "amount": "1.01",
            "additional_attribute": "SINGLE_USE"
          }
        ]
      }
    ],
    "warnings": [
      {
        "message": "The [brand_id]:123 field is incorrect and has been automatically cleared by the system. Reason: [Brand does not exist]. You can edit it later."
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
| 12019012 | product package size is invalid |
| 12019013 | brand id is invalid |
| 12019059 | seller sku is invalid |
| 12019061 | Product weight or dimensions unit does not support the imperial units on non-US local products. |
| 12019095 | `pre_sale_fulfillment_type` is missing or empty |
| 12019096 | The value for `pre_sale_type` is missing |
| 12019097 | `pre_sale_fulfillment_type.release_date` must be set to a non-zero value |
| 12019098 | `pre_sale_fulfillment_type.handling_duration_days` must be set to a non-zero value |
| 12019099 | The specified `pre_sale_type` is not supported in your region. Refer to the API documentation for details. |
| 12019100 | All SKUs of a product must have the same `pre_sale_type`. Do not assign different values. |
| 12019215 | deposit balance is not enough |
| 12052002 | Incorrect category format |
| 12052003 | Incorrect parcel height format |
| 12052004 | Incorrect parcel width format |
| 12052005 | Incorrect parcel length format |
| 12052006 | Incorrect parcel weight format |
| 12052013 | The product description cannot exceed maximum characters |
| 12052015 | The product description is required |
| 12052023 | Category does not exist |
| 12052024 | Category is not final category |
| 12052025 | The category is invalid |
| 12052026 | Brand does not exist |
| 12052028 | Main product image is required |
| 12052034 | This product doesn't belong to this shop |
| 12052048 | You cannot edit the specified product(s) as it isn't listed in your account or shop. |
| 12052050 | A single product cannot have more than 100 different SKUs |
| 12052051 | The product name exceed max limit characters |
| 12052054 | The seller SKU text length cannot exceed max limit characters |
| 12052055 | The SKU inventory quantity for the warehouse must be within allowed limits. |
| 12052056 | The num of image in description cannot exceed max limit |
| 12052073 | The product price is invalid |
| 12052084 | The provided currency is not available for this shop/region |
| 12052092 | product sale price is invalid |
| 12052093 | Exceeded the product listing limit for the seller. |
| 12052094 | No multiple warehouse permission |
| 12052096 | Unable to update the price for SKUs with no warehouse. Assign a warehouse and try again. |
| 12052097 | The warehouse does not exist |
| 12052104 | property is required |
| 12052105 | required qualification miss |
| 12052109 | number of requests from merchants over limit |
| 12052115 | seller has no warehouse |
| 12052116 | product package size is invalid |
| 12052128 | Size chart not found |
| 12052144 | platform warehouse not support to edit |
| 12052151 | product property value contain restricted words |
| 12052152 | sale property name contains restricted words |
| 12052153 | sale property value contains restricted words |
| 12052159 | unique item total quantity must be one |
| 12052162 | unique item sku count must be one and disable variables |
| 12052172 | sale type is invalid |
| 12052181 | The package weight of the product can not be zero. |
| 12052182 | The `{{sub_property_name}}` field is required as you've selected `{{parent_property_value}}` for `{{parent_property_name}}`. |
| 12052183 | The `{{sub_property_name}}` field should be left empty as you've selected `{{parent_property_value}}` for `{{parent_property_name}}`. |
| 12052200 | brand is expired |
| 12052201 | You are not authorized to sell this brand in this category. To do so, apply through the Qualification Center in Seller Center. |
| 12052207 | receipt brand not support warehouse |
| 12052208 | A brand authorization is required to publish this listing. |
| 12052217 | All region shops must use V2 categories. Check the documentation for further details. |
| 12052219 | instant product not support not for sale |
| 12052220 | This category is prohibited or unsupported on TikTok Shop. Select another category. |
| 12052221 | Only whitelisted sellers are permitted to trade under current category |
| 12052222 | category do not support cod |
| 12052223 | This category is restricted. To sell in this category, apply through the Qualification Center in Seller Center. |
| 12052225 | You are not authorized to sell in this category because it does not fall under your shop's main category. Contact your account manager for help or select another category. |
| 12052226 | This category is restricted. To sell in this category, apply through the Qualification Center in Seller Center. |
| 12052227 | the category is unauthorized or unavailable |
| 12052228 | combo product not support not for sale |
| 12052229 | pre order product not support not for sale |
| 12052230 | Category version and categoryID are not matched. |
| 12052235 | The format of url is invalid |
| 12052236 | The protocol of the url is unsafe |
| 12052237 | The path of url is unsafe |
| 12052238 | The length of the url is greater than 200 |
| 12052240 | Do not support custom property. |
| 12052241 | attribute name or attribute id is empty. |
| 12052242 | The attribute name characters cannot exceed max_limit |
| 12052243 | The product attribute or sale attribute name characters contain Chinese. |
| 12052244 | The attribute name duplicate. |
| 12052245 | The product attributes contained invalid characters. Please modify and re-submit. |
| 12052246 | The {{property_type}} not support multi selected, attribute id is :{{property_id}}. |
| 12052247 | Do not support custom product attribute. |
| 12052248 | The {{property_type}} value name or attribute value id is empty. |
| 12052249 | The {{property_type}} value name characters cannot exceed {{max_limit}}, attribute value name is :{{property_value_name}}. |
| 12052250 | The {{property_type}} value name characters contain Chinese. |
| 12052251 | Duplicated attribute values found for an attribute. Remove or modify the duplicated value. |
| 12052253 | Duplicate attribute value id |
| 12052254 | Duplicate attribute id |
| 12052256 | The {{property_name}} value need to be positive integers or positive decimals . |
| 12052260 | The product ID does not exist |
| 12052261 | product name is empty |
| 12052262 | Chinese characters are not supported in product name |
| 12052263 | product name prefix illegal |
| 12052268 | seller does not support pre sale |
| 12052269 | The selected time is outside the limit |
| 12052274 | pre-sale and pre-order modes are mutually exclusive. |
| 12052275 | sku's mto day is invalid |
| 12052278 | seller does not support make to order |
| 12052282 | Product manufacturer is required. |
| 12052283 | The number of manufacturers cannot exceed the allowed limits. |
| 12052284 | Manufacturer ID {{manufacturer_id}} is not found |
| 12052285 | Manufacturer ID {{manufacturer_id}} is not associated with the seller |
| 12052287 | Product responsible person is required |
| 12052288 | The number of responsible person ids cannot exceed {{max_limit}}, and cannot less {{min_limit}}. |
| 12052289 | Responsible person ID {{rp_id}} is not found |
| 12052290 | Responsible person ID {{rp_id}} is not associated with the seller |
| 12052291 | Extra identification code information is not supported in this region. |
| 12052293 | When identifier code is not filled in, extra identification code is not allowed to be filled in. |
| 12052294 | The format of the extra identification code is incorrect. |
| 12052295 | Duplicate manufacturer IDs associated with the same product |
| 12052296 | Duplicate responsible person IDs associated with the same product |
| 12052300 | product main image uri illegal |
| 12052301 | Width and length of main image must be at least {{min_limit}}, check uri {{uri}} |
| 12052302 | The main images size exceed limit. |
| 12052304 | Main product image format not support. |
| 12052305 | The main images aspect ratio cannot exceed max limit. |
| 12052306 | main product images count exceed limit |
| 12052309 | The seller does not have backorder permission. |
| 12052310 | The futures information filled in by the seller does not meet the requirements. |
| 12052311 | The number of backorder product exceeds the limit max_num, or the proportion of backorder product exceeds the limit max_ratio |
| 12052313 | This product does not allow backorder inventory. |
| 12052316 | product second hand not applicable in this sale platform |
| 12052324 | Product description image file format is not supported |
| 12052330 | product is not supported to list in designated sale platform |
| 12052332 | The seller center is locked during shop integration, only editing stock and price is allowed |
| 12052340 | product description image uri illegal |
| 12052341 | The description images size cannot exceed limit. |
| 12052342 | The description images space cannot exceed limit. |
| 12052343 | Product description image format not support. |
| 12052344 | The product description html syntax with error |
| 12052345 | The product description html tag not support. |
| 12052346 | The product description has Chinese characters |
| 12052348 | The product description html tag required attribute is miss. |
| 12052349 | The product description html tag not support nest. |
| 12052350 | The product description html tag contain illegal attribute. |
| 12052352 | The product description nest exceeding limit |
| 12052356 | The number of 'supplementary_sku_images' for the sales attribute value exceeds the maximum limit |
| 12052357 | 'supplementary_sku_images' is only allowed when 'sku_img' is specified. Add an image to 'sku_img' and try again. |
| 12052358 | Tokopedia platform doesn't support this kind of product |
| 12052360 | The video id is not exist. |
| 12052361 | This base unit value count is not supported. The supported base unit values can be obtained from the Get Attribute API. |
| 12052362 | SKU unit count is required. |
| 12052364 | The warehouse is unavailable because this product cannot be shipped to the target market from this warehouse. |
| 12052365 | The manufacturer lacks language version information for this market. |
| 12052366 | The responsible person lacks language version information for this market. |
| 12052369 | external_id length check fail |
| 12052372 | Generate EU energy label image failed |
| 12052375 | product list price is invalid |
| 12052376 | list price not support |
| 12052382 | Can't edit Dilayani Tokopedia warehouse quantity |
| 12052383 | product list price exceed limit |
| 12052385 | Please enter valid certificate expiration date |
| 12052402 | seller shipping template is empty |
| 12052403 | The warehouse does not support fulfillment for the current shop. |
| 12052404 | multi-warehouse not support customize logistics service |
| 12052405 | The warehouse has not opened the subscribed logistics service |
| 12052419 | The shop tasks necessary for posting products have not been completed. Please go to complete them |
| 12052420 | warehouse didn't set logistics service |
| 12052424 | Missing 'sale price' value |
| 12052446 | Category is not open in this market |
| 12052488 | This region doesn't support save draft after product submitted |
| 12052490 | The handling time must be within the allowed limits. |
| 12052495 | Pfand packaging type is required |
| 12052497 | Pfand field is not supported in this country |
| 12052498 | Pfand amount should not be filled. |
| 12052520 | product sale property image uri illegal |
| 12052521 | The sale property images size over limit. |
| 12052522 | Product sale property image is required |
| 12052523 | Product sale property image format not support. |
| 12052524 | The sale property image aspect ratio invalid |
| 12052525 | The attribute max num cannot exceed 3. |
| 12052526 | The attribute value max num over limit. |
| 12052527 | The sale attribute id not exist. |
| 12052528 | You can add images to only 1 product variation, which will serve as the primary variation for display in the product options gallery. |
| 12052529 | The property value id not exist. |
| 12052530 | The warehouse '{{warehouse ID}}' does not belong to this shop/seller. |
| 12052531 | The warehouse is disabled. |
| 12052532 | the warehouse not delivery warehouse |
| 12052535 | Couldn't publish this product as you haven't set the return warehouse for your shop. Add the return warehouse information on TikTok Shop Seller Center first and try again. |
| 12052543 | Products that support pfand are not supported in the creation of Virtual Bundles. |
| 12052549 | The current shipping template is unavailable due to the unavailability of shipping method. Please change the shipping template. |
| 12052550 | SKU property must contain all properties |
| 12052554 | sku name contain Chinese characters |
| 12052555 | The warehouse id is duplicate |
| 12052560 | The SKU contains duplicate sales attribute. |
| 12052570 | product price exceed limit |
| 12052571 | Missing price for SKU(s) |
| 12052574 | unit price config is invalid |
| 12052585 | deposit balance is not enough |
| 12052591 | Invalid number of digits of identifier code |
| 12052592 | Identifier code already entered, cannot enter the same code twice |
| 12052598 | Only the last digit supports input X |
| 12052600 | The identifier code type must be selected |
| 12052603 | Scheduled listing is not supported |
| 12052604 | The scheduled listing time is invalid |
| 12052650 | product qualification image uri illegal |
| 12052655 | qualification id not exist |
| 12052656 | qualification id duplicate |
| 12052657 | qualification image and pdf file is out of limit. |
| 12052658 | product qualification file uri illegal |
| 12052670 | The size chart image URI is invalid. Note: API users must use the URI generated by the Upload Product Image API. |
| 12052671 | The sizechart images size over limit. |
| 12052673 | Product sizechart image is required |
| 12052700 | The seller is inactive. |
| 12052701 | do not support cross-boarder seller create local product directly |
| 12052702 | seller does not support pre-order |
| 12052703 | Invalid seller tax number |
| 12052704 | seller id not exist |
| 12052706 | The minimum sales quantity should not be exceed limit |
| 12052707 | Setting minimum sales quantity is not supported |
| 12052712 | sku's pre_order is invalid |
| 12052722 | The image URI does not exist in TikTok Shop. |
| 12052830 | The number of sub-products contained in each combo cannot exceed {{max_limit}}. |
| 12052831 | The number of sub-skus contained in each combo sku cannot exceed {{max_limit}}. |
| 12052832 | The sub-SKU coefficient associated with each combo SKU cannot exceed {{max_limit}}, and cannot less {{min_limit}}. |
| 12052833 | The number of combo associated with a product cannot exceed the max limit. |
| 12052834 | The number of combo sku associated with a sku cannot exceed limit. |
| 12052835 | Sub product ID not exist |
| 12052836 | The category of the combo is inconsistent with the category of the main sub-product. |
| 12052837 | The category of the combo is not in the set of restricted categories. |
| 12052838 | The first-level categories of the sub-products in the combo are inconsistent |
| 12052840 | Sub-skus in a combo sku cannot be duplicated |
| 12052841 | The sub-sku relationship corresponding to different combo sku cannot be duplicated. |
| 12052842 | The combo does not include the main sub-product |
| 12052844 | The sub-sku is not in the sub-product |
| 12052845 | Failed to create, does not support non-live status product |
| 12052846 | combo does not support adding this product type |
| 12052848 | Combo cannot set minimum sale quantity |
| 12052849 | You don't have the permission to operate combo. |
| 12052851 | The warehouse of combo sku is empty. |
| 12052853 | The sale property of combo mismatch. |
| 12052854 | The sale property of combo is not unique. |
| 12052855 | The warehouse of combo mismatch. |
| 12052856 | The combo does not support customize logistics service |
| 12052857 | Combined products and normal products cannot be converted to each other. |
| 12052858 | The SKU of a combined product cannot be associated with the SKU of other combined products. |
| 12052859 | When the combined SKU is only associated with one sub-SKU, the coefficient of this sub-SKU cannot be less than 2. |
| 12052861 | The price of combined SKU cannot exceed the sum of the prices of the sub-SKUs. |
| 12052862 | The brand of the combined product must be within the range of sub-product brands. |
| 12052863 | All SKU of a combined product need to be the combined SKU. |
| 12052864 | Unable to add deactivated SKUs to the combined product. |
| 12052881 | identity internal error |
| 12052910 | Invalid input parameters. Refer to the API documentation for details. |
| 12052915 | package weight unit and dimension unit miss match |
| 12052923 | contact info required |
| 12052931 | The title must follow these formatting rules: it cannot contain HTML escape characters (e.g., `&nbsp;`), emojis, or ASCII control characters (e.g., `\u007F`). It also cannot consist solely of symbols (e.g., `///` or `@#$%&`), nor can it have more than 9 consecutive repeated characters (e.g., `aaaaaaaaa` or `111111111`). |
| 12052932 | The description must follow these formatting rules: it cannot contain HTML escape characters (e.g., `&nbsp;`), emojis, or ASCII control characters (e.g., `\u007F`). It also cannot consist solely of symbols (e.g., `///` or `@#$%&`), nor can it have more than 9 consecutive repeated characters (e.g., `aaaaaaaaa` or `111111111`). |
| 12052933 | Sales attribute names must follow these formatting rules: it cannot contain HTML escape characters (e.g., `&nbsp;`), emojis, or ASCII control characters (e.g., `\u007F`). It also cannot consist solely of symbols (e.g., `///` or `@#$%&`), nor can it have more than 9 consecutive repeated characters (e.g., `aaaaaaaaa` or `111111111`). |
| 12052934 | Sales attribute value names must follow these formatting rules: it cannot contain HTML escape characters (e.g., `&nbsp;`), emojis, or ASCII control characters (e.g., `\u007F`). It also cannot consist solely of symbols (e.g., `///` or `@#$%&`), nor can it have more than 9 consecutive repeated characters (e.g., `aaaaaaaaa` or `111111111`). |
| 12052935 | Product attribute value names must follow these formatting rules: it cannot contain HTML escape characters (e.g., `&nbsp;`), emojis, or ASCII control characters (e.g., `\u007F`). It also cannot consist solely of symbols (e.g., `///` or `@#$%&`), nor can it have more than 9 consecutive repeated characters (e.g., `aaaaaaaaa` or `111111111`). |
| 12052990 | The check failed. |
| 12052992 | no permission to create gift product |
| 12052994 | seller is not toko seller |
| 12052995 | seller has not finished onboarding to tts |
| 12052996 | external_id duplicated |
| 33001002 | internal error |
| 36009002 | Too many requests. You've made too many requests in a short period of time. |
| 36009003 | Internal error. Please try again. If the issue persists after multiple attempts, please contact platform support. |
| 36009004 | invalid param error |
| 98001004 | Parameter {{param_name}} is invalid. Reason: {{reason}}. Expected: {{expected_value}} |
