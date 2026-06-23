# Get Warehouse Delivery Options

This API is used to obtain a list of delivery options available through the seller's designated warehouse.

GET /logistics/202309/warehouses/{warehouse_id}/delivery_options

## Request
### Example

curl -X GET \
 'https://open-api.tiktokglobalshop.com/logistics/202309/warehouses/6966568648651605766/delivery_options?app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1623812664&shop_cipher=GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3&scope=PRODUCT' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json'

## Response
### Example

{
  "code": 0,
  "data": {
    "delivery_options": [
      {
        "id": "6955034615128000261",
        "name": "LSV-TTS-STD",
        "type": "STANDARD",
        "description": "LSV-TTS-STD  S",
        "dimension_limit": {
          "max_height": 100,
          "max_length": 100,
          "max_width": 100,
          "unit": "INCH"
        },
        "weight_limit": {
          "max_weight": 100,
          "min_weight": 100,
          "unit": "GRAM"
        },
        "platform": [
          "TOKOPEDIA",
          "TIKTOK_SHOP"
        ]
      }
    ]
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}

## Error Code
36009003 Internal error. Please try again. If the issue persists after multiple attem
