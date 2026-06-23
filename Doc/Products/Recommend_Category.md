# Recommend Category 

Retrieve the recommended category for a candidate product based on its title, description, and images.
If you are syncing product catalogs from an external system to TikTok Shop, use this API to facilitate product categorization.
Note: The language used in text fields such as descriptions and titles must align with the target market's language (e.g. don't use Chinese).

POST /product/202309/categories/recommend

## Request
### Example

curl -X POST \
 'https://open-api.tiktokglobalshop.com/product/202309/categories/recommend?app_key=38abcd&shop_cipher=GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1623812664' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json' \
-d '{
  "product_title": "Men'\''s Fashion Sports Low Cut Cotton Breathable Ankle Short",
  "description": "\u003cp\u003ePlease check the measurements before purchase.\u003c/p\u003e\u003cul\u003e  \u003cli\u003eM-Size\u003c/li\u003e  \u003cli\u003eXL-Size\u003c/li\u003e\u003c/ul\u003e \u003cimg src=\"https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/181595ea7d26489284b5667488d708c1~tplv-o3syd03w52-origin-jpeg.jpeg?from=1432613627\" width='100' height='100' /\u003e  ",
  "images": [
    {
      "uri": "tos-maliva-i-o3syd03w52-us/c668cdf70b7f483c94dbe"
    }
  ],
  "category_version": "v1",
  "listing_platform": "TIKTOK_SHOP",
  "include_prohibited_categories": false,
  "locale": "en"
}'

## Response
### Example

{
  "code": 0,
  "data": {
    "leaf_category_id": "605254",
    "categories": [
      {
        "id": "605254",
        "name": "Teas",
        "level": 1,
        "is_leaf": true,
        "permission_statuses": [
          "INVITE_ONLY"
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
| 12019006 | product description is invalid |
| 12019009 | product image list is invalid |
| 12019064 | No matching categories. Provide the full name of your product, edit its product properties, and try again. |
| 12052013 | The product description cannot exceed maximum characters |
| 12052051 | The product name exceed max limit characters |
| 12052056 | The num of image in description cannot exceed max limit |
| 12052217 | All region shops must use V2 categories. Check the documentation for further details. |
| 12052230 | Category version and categoryID are not matched. |
| 12052261 | product name is empty |
| 12052262 | Chinese characters are not supported in product name |
| 12052266 | The product name contains non-English characters. |
| 12052300 | product main image uri illegal |
| 12052301 | Width and length of main image must be at least {{min_limit}}, check uri {{uri}} |
| 12052305 | The main images aspect ratio cannot exceed max limit. |
| 12052306 | main product images count exceed limit |
| 12052340 | product description image uri illegal |
| 12052341 | The description images size cannot exceed limit. |
| 12052343 | Product description image format not support. |
| 12052345 | The product description html tag not support. |
| 12052346 | The product description has Chinese characters |
| 12052348 | The product description html tag required attribute is miss. |
| 12052349 | The product description html tag not support nest. |
| 12052350 | The product description html tag contain illegal attribute. |
| 12052351 | The product description contains non-English characters. |
| 12052352 | The product description nest exceeding limit |
| 12052700 | The seller is inactive. |
| 12052704 | seller id not exist |
| 12052722 | The image URI does not exist in TikTok Shop. |
| 36009003 | Internal error. Please try again. If the issue persists after multiple attempts, please contact platform support. |
| 12052912 | No matching category found within your account's main category. Check your main category in the seller profile on Seller Center and ensure your product falls within its scope. |
