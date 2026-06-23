# Get Authorized Shops

Retrieves the list of shops that a seller has authorized for an app.
Seller authorization is required before an app can access the data of a shop. Use this API to check which shops are currently authorized for an app and obtain the corresponding shop cipher for use as an input parameter in shop related APIs.
For more information about seller authorization, refer to Seller authorization guide.
Target seller: All

GET /authorization/202309/shops

## Request
### Example

curl -X GET \
 'https://open-api.tiktokglobalshop.com/authorization/202309/shops?timestamp=1623812664&app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json'


## Response
### Example

{
  "code": 0,
  "data": {
    "shops": [
      {
        "id": "7000714532876273420",
        "name": "Maomao beauty shop",
        "region": "GB",
        "seller_type": "CROSS_BORDER",
        "cipher": "GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3",
        "code": "CNGBCBA4LLU8"
      }
    ]
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}


## Error code

36009003 Internal error. Please try again. If the issue persists after multiple attempts, please contact platform support.

