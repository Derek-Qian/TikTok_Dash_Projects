# Get Global Seller Warehouse

This API retrieves all global warehouse information associated with the seller. Warehouse information includes global warehouse ID, warehouse name, and warehouse ownership.

GET /logistics/202309/global_warehouses

## Request
### Example

curl -X GET \
 'https://open-api.tiktokglobalshop.com/logistics/202309/global_warehouses?timestamp=1623812664&app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: application/json'

## Response
### Example

{
  "code": 0,
  "data": {
    "global_warehouses": [
      {
        "id": "7000714532876273411",
        "name": "Guangzhou",
        "ownership": "SELLER"
      }
    ]
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}
