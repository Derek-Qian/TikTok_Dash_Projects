# Get Authorized Category Assets

Retrieves the list of business category assets authorized by a partner for an app.
Partner authorization is required before an app can access the data of a partner, and this access is granted based on business categories. Use this API to check which business category assets are currently authorized for an app and obtain the corresponding category asset cipher for use as an input parameter in affiliate partner related APIs.
For more information about partner authorization, refer to Partner authorization guide.
Target partner: All

GET /authorization/202405/category_assets

## Request
### Example
curl -X GET \
 'https://open-api.tiktokglobalshop.com/authorization/202405/category_assets?app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1623812664' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json'

## Response
### Example

{
  "code": 0,
  "data": {
    "category_assets": [
      {
        "cipher": "TTP_XF90igAAAABh0sddwer0qsWgt233vOiG",
        "target_market": "US",
        "category": {
          "id": 3,
          "name": "Customer Support"
        }
      }
    ]
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}

