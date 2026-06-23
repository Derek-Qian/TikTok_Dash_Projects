# Get Active Shops

Retrieves all active shops that belong to a seller.
You can use this API to check the activation status of shops.
Target seller: All

GET /seller/202309/shops

## Request
### Example

curl -X GET \
 'https://open-api.tiktokglobalshop.com/seller/202309/shops?app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1623812664' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json'

## Response
### Example

{
  "code": 0,
  "data": {
    "shops": [
      {
        "id": "36123502970007",
        "region": "GB"
      }
    ]
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}


