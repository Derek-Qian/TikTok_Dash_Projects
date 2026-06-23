# Get Category Rules

Retrieve the additional requirements (beyond mandatory product attributes) for listing a product in a particular category based on your shop's location. Requirements may include product certifications, size charts, dimensions and more.
Use this API to determine the supporting information that you must prepare before listing a product.
Note: It must be a leaf category that corresponds to the category tree type specified in the category_version property.

GET product/202309/categories/{category_id}/rules

## Request
### Example

curl -X GET \
 'https://open-api.tiktokglobalshop.com/product/202309/categories/600001/rules?sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1623812664&shop_cipher=GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3&category_version=v1&locale=es-MX&app_key=38abcd' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json'

## Response 
### Example

{
  "code": 0,
  "data": {
    "product_certifications": [
      {
        "id": "602362",
        "name": "SNI Certificate",
        "is_required": true,
        "document_details": "Upload a user manual or instructions in the official local language.\\n\\nWhere there are multiple items sold as a part of a bundle, please clearly indicate which specific product the certification pertains to in the uploaded file or image.",
        "sample_image_url": "https://p-boei18n.byted.org/tos-boei18n-i-jvtte31kaf/80b32f2896829eeb69d4b278c4f3aa75.jpg~tplv-jvtte31kaf-origin-jpeg.jpeg",
        "requirement_conditions": [
          {
            "condition_type": "VALUE_ID_MATCH",
            "attribute_id": "101610",
            "attribute_value_id": "1024358"
          }
        ],
        "expiration_date": {
          "is_required": true
        }
      }
    ],
    "size_chart": {
      "is_supported": true,
      "is_required": true
    },
    "cod": {
      "is_supported": true
    },
    "package_dimension": {
      "is_required": true
    },
    "epr": {
      "is_required": false
    },
    "responsible_person": {
      "is_required": false
    },
    "manufacturer": {
      "is_required": false
    },
    "allowed_special_product_types": "\"PRE_ORDER\"",
    "fees": [
      {
        "type": "PFAND",
        "is_required": true
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
| 12052217 | All region shops must use V2 categories. Check the documentation for further details. |
| 12052220 | This category is prohibited or unsupported on TikTok Shop. Select another category. |
| 12052223 | This category is restricted. To sell in this category, apply through the Qualification Center in Seller Center. |
| 12052226 | This category is restricted. To sell in this category, apply through the Qualification Center in Seller Center. |
| 12052230 | Category version and categoryID are not matched. |
| 12052446 | Category is not open in this market |
| 36009003 | Internal error. Please try again. If the issue persists after multiple attempts, please contact platform support. |
