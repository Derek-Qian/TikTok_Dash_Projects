# Get Shop Group


Query the shop scope of product interoperability groups. For example, in the scenario of the United States and Mexico, which two shops have interoperable products.

GET /seller/202601/shop_groups

## Request
### Example

curl -X GET \
 'https://open-api.tiktokglobalshop.com/seller/202601/shop_groups?app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1623812664' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json'


## Response
### Example

{
  "code": 0,
  "data": {
    "shop_group_data": {
      "shop_group": {
        "source": "1",
        "shop_group_name": "shop group name A"
      },
      "shops": [
        {
          "shop_id": "1234",
          "seller_id": "12",
          "shop_name": "shop name A",
          "shop_region": "US"
        }
      ]
    }
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}
