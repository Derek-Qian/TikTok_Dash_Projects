# Get Categories

Retrieve the list of product categories available for your shop.
Product categories are updated frequently, so it's recommended to call the API in real time to ensure you are using the latest category data. Caching category data locally may result in using outdated information, leading to errors when creating products.
For the Indonesia market: To list a product on both TikTok Shop and Tokopedia, you must use only categories that are available on both platforms. Please call this API twice to identify the overlapping categories.

GET /product/202309/categories

## Request
### Example

curl -X GET \
 'https://open-api.tiktokglobalshop.com/product/202309/categories?shop_cipher=GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3&locale=en-US&category_version=v1&listing_platform=TIKTOK_SHOP&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&app_key=38abcd&keyword=electronics&include_prohibited_categories=false&timestamp=1623812664' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json'

## Response
### Example

{
  "code": 0,
  "data": {
    "categories": [
      {
        "id": "600002",
        "parent_id": "600001",
        "local_name": "Home Supplies",
        "is_leaf": false,
        "permission_statuses": [
          "INVITE_ONLY",
          "NON_MAIN_CATEGORY"
        ]
      }
    ]
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}

## Error Code
12019210 publish param invalid
12052023 Category does not exist
12052217 All region shops must use V2 categories. Check the documentation for further details.
12052230 Category version and categoryID are not matched.
12052700 The seller is inactive.
12052704 seller id not exist
36009003 Internal error. Please try again. If the issue persists after multiple attempts, please contact platform support.
