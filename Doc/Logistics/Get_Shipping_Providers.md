# Get Shipping Providers

This API is used to obtain the shipping provider corresponding to the specified delivery option

GET /logistics/202309/delivery_options/{delivery_option_id}/shipping_providers

## Request
### Example

curl -X GET \
 'https://open-api.tiktokglobalshop.com/logistics/202309/delivery_options/6955034615128000261/shipping_providers?buyer_region=DE&app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1623812664&shop_cipher=GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3&warehouse_region=ES' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json'

## Response
### Example

{
  "code": 0,
  "data": {
    "shipping_providers": [
      {
        "id": "7117858858072016686",
        "name": "USPS"
      }
    ]
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}

## Error Code
| Code | Message |
|------|---------|
| 36009003 | Internal error. Please try again. If the issue persists after multiple attempts, please contact platform support. |
| 21008116 | No Subscription without specified delivery option. |
| 21008117 | The delivery of the specified delivery_option_id is fulfilled by TikTok. No shipping provider will be returned. |
