# Search Size Charts

Retrieve size charts that a seller has created.

POST /product/202407/sizecharts/search

## Request
### Example

curl -X POST \
 'https://open-api.tiktokglobalshop.com/product/202407/sizecharts/search?page_size=10&page_token=b2Zmc2V0PTAK&locales=en-US,es-ES&app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1623812664' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json' \
-d '{
  "ids": [
    "7362027385890244398"
  ],
  "keyword": "size chart"
}'

## Response
### Example

{
  "code": 0,
  "data": {
    "size_chart": [
      {
        "template_id": "7362027385890244398",
        "template_name": "size chart",
        "images": [
          {
            "uri": "tos-maliva-i-o3syd03w52-us/c668cdf70b7f483c94dbe",
            "url": "https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/6c8519a3663a4d728c4e3c131dc914b4~tplv-o3syd03w52-resize-jpeg:300:300.jpeg?from=522366036",
            "locale": "en-US"
          }
        ]
      }
    ],
    "next_page_token": "b2Zmc2V0PTAK",
    "total_count": 100
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}

## Error Code
12019108 page number is invalid
12019109 page size is invalid
36009003 Internal error. Please try again. If the issue persists after multiple attempts, please contact platform support.
