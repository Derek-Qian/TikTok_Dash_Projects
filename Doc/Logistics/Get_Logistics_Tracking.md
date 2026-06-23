# Get Logistics Tracking *

This API can use the order number to obtain the corresponding logistics tracking information. This API can obtain more comprehensive logistics tracking information, which is more detailed than the Get tracking API.

GET /logistics/202604/orders/{order_id}/tracking

## Request
### Example

curl -X GET \
 'https://open-api.tiktokglobalshop.com/logistics/202604/orders/576461413038785752/tracking?timestamp=1623812664&shop_cipher=GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3&app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json'


## Response
### Example

{
  "code": 0,
  "data": {
    "order_id": "577071607420326620",
    "logistics_details": [
      {
        "newest_tracking_no": "861651122474",
        "carrier_name": "J&T Express",
        "track_list": [
          {
            "description": "Package has been delivered!\\n",
            "tracking_no": "861651122474",
            "update_time_millis": 1694686949000,
            "action_code": 50101,
            "action_code_name": "signed_personally"
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
| 36009003 | Internal error. Please try again. If the issue persists after multiple attempts, please contact platform support. |
| 11007009 | This order is not in supported business scenes |
| 11007010 | System is busy, please try again later. |
