# Get Attributes

Retrieve the standard built-in product and sales attributes for listing a product in a particular category based on your shop's location.
Products on TikTok Shop are grouped into categories predefined by TikTok Shop, and each category is associated with a standard set of product attributes and sales attributes.
- Sales attributes (e.g. size, color, length) define product variants and are optional if your product is straightforward and has no variants.
- Product attributes (e.g. manufacturer, country of origin, materials used) describe the product as a whole, regardless of variant. Some product attributes are mandatory based on listing policies.
Use this API to determine the mandatory and optional attributes before listing a product.
Note: It must be a leaf category that corresponds to the category tree type specified in the category_version property.

GET /product/202309/categories/{category_id}/attributes

## Request
### Example

curl -X GET \
 'https://open-api.tiktokglobalshop.com/product/202309/categories/600001/attributes?timestamp=1623812664&shop_cipher=GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3&locale=en-US&category_version=v1&app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json'

## Response
### Example

{
  "code": 0,
  "data": {
    "attributes": [
      {
        "id": "100392",
        "name": "Occasion",
        "type": "PRODUCT_PROPERTY",
        "is_requried": false,
        "values": [
          {
            "id": "1001533",
            "name": "Birthday",
            "icon_url": "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/37a9d5d39c27480d9870f73a2ad7cc95~tplv-aphluv4xwc-origin-jpeg.jpeg?dr=11254&from=3455097676&height=956&idc=no1a&ps=933b5bde&shcp=9b759fb9&shp=cdf09b4c&t=555f072d&width=1000"
          }
        ],
        "value_data_format": "POSITIVE_INT_OR_DECIMAL",
        "is_customizable": true,
        "requirement_conditions": [
          {
            "condition_type": "VALUE_ID_MATCH",
            "attribute_id": "101610",
            "attribute_value_id": "1024358"
          }
        ],
        "is_multiple_selection": true
      }
    ]
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}

## Error Code

| Code | Message |
|------|---------|
| 12052023 | Category does not exist |
| 12052024 | Category is not final category |
| 12052025 | The category is invalid |
| 12052217 | All region shops must use V2 categories. Check the documentation for further details. |
| 12052230 | Category version and categoryID are not matched. |
| 12052704 | seller id not exist |
| 36009003 | Internal error. Please try again. If the issue persists after multiple attempts, please contact platform support. |
