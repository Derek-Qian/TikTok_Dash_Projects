# Get Seller Permissions

Retrieves the cross-border operations that a cross-border seller is permitted to perform.
You can use this API prior to listing products to check whether a seller has the ability to list global products.
Target seller: Cross-border sellers

GET /seller/202309/permissions

## Request
### Example

curl -X GET \
 'https://open-api.tiktokglobalshop.com/seller/202309/permissions?app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1623812664' \
-H 'content-type: application/json' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k'

## Response
### Example

{
  "code": 0,
  "data": {
    "permissions": [
      "MANAGE_GLOBAL_PRODUCT"
    ]
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}
