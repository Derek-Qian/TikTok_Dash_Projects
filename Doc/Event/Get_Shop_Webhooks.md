# Get Shop Webhooks
Retrieves a shop's webhooks and the corresponding webhook URLs.

GET /event/202309/webhooks

## Request
### Example 

curl -X GET \
 'https://open-api.tiktokglobalshop.com/event/202309/webhooks?app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1623812664&shop_cipher=GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json'

## Response
### Example

{
  "code": 0,
  "data": {
    "webhooks": [
      {
        "event_type": "ORDER_STATUS_CHANGE",
        "address": "https://partner.tiktokshop.com",
        "create_time": 1635338186,
        "update_time": 1635338186
      }
    ],
    "total_count": 1
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}
