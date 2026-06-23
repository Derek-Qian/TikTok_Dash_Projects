# Update Shop Webhook

PUT /event/202309/webhooks

## Request
### Example

curl -X PUT \
 'https://open-api.tiktokglobalshop.com/event/202309/webhooks?sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1623812664&shop_cipher=GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3&app_key=38abcd' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json' \
-d '{
  "address": "https://partner.tiktokshop.com",
  "event_type": "ORDER_STATUS_CHANGE"
}'


## Response
### Example

{
  "code": 0,
  "data": {},
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}


