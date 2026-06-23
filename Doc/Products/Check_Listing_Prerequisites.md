# Check Listing Prerequisites


Check if a TikTok shop is ready to list products.
Each shop needs to satisfy a series of TikTok Shop requirements before you can start listing products. Before you proceed to list products, use this API to check if your shop has satisfied all requirements.
Tip: We recommend that you run this check before any bulk updates to avoid listing issues. For example, sellers may change the delivery option to "Shipped by seller" but fail to add a shipping template, thus blocking the shop from listing products. In this case, the API would return is_failed=true for the SHIPPING_TEMPLATE check item and you can prompt the seller to fix the problem.

GET /product/202312/prerequisites

## Request
### Example

curl -X GET \
 'https://open-api.tiktokglobalshop.com/product/202312/prerequisites?app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1623812664&shop_cipher=GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json'


## Response
### Example

{
  "code": 0,
  "data": {
    "check_results": [
      {
        "check_item": "RETURN_WAREHOUSE",
        "is_failed": true,
        "fail_reasons": [
          "Couldn't publish this product as you haven't set the return warehouse for your shop. Add the return warehouse information on TikTok Shop Seller Center first and try again."
        ]
      }
    ]
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}

## Error Code
36009003  Internal error. Please try again. If the issue persists after multiple attempts, please contact platform support.
33001002  internal error
