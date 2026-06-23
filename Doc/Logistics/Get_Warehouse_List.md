# Get Warehouse List

This API retrieves all warehouse information associated with the seller. Warehouse information includes name, status, address, and other details.

GET /logistics/202309/warehouses

## Request
### Example

curl -X GET \
 'https://open-api.tiktokglobalshop.com/logistics/202309/warehouses?app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1623812664&shop_cipher=GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3' \
-H 'content-type: application/json' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k'

## Response
### Example

{
  "code": 0,
  "data": {
    "warehouses": [
      {
        "id": "7000714532876273410",
        "entity_id": "7395366865142499073",
        "name": "Guangzhou",
        "effect_status": "ENABLED",
        "type": "SALES_WAREHOUSE",
        "sub_type": "DOMESTIC_WAREHOUSE",
        "is_default": true,
        "address": {
          "region": "China",
          "state": "GuangDong",
          "city": "GuanZhou",
          "distict": "HuaDu",
          "town": "town",
          "contact_person": "Lee",
          "first_name": "新一",
          "last_name": "工藤",
          "first_name_local_script": "くどう",
          "last_name_local_script": "しんいち",
          "postal_code": "510000",
          "full_address": "South Sea 11 floor",
          "region_code": "CN",
          "phone_number": "188****2234",
          "address_line1": "Bairro/Distrito",
          "address_line2": "Caminho Trinta e Três",
          "address_line3": "3",
          "address_line4": "11 floor",
          "geolocation": {
            "latitude": "45.41634",
            "longitude": "-75.6868"
          }
        }
      }
    ]
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}

## Error Code
36009003  Internal error. Please try again. If the issue persists after multiple attem
