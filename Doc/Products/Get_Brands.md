# Get Brands 

Retrieve all available brands for your shop, including the built-in brands and any custom brands created using the Create Custom Brands API. Pass the returned brand ID when creating or editing a product to associate the brand with the product.
- To check if a brand is fully authorized for use in a specific product category, specify the category ID.
- To obtain the full list of brands that your shop can potentially use and their authorization status, omit the category ID. We recommend that you specify the brand name to narrow down the list of brands returned.
Key concept
Whether you can select and display a brand depends on the brand's authorization status, the categories authorized for the brand, and whether the brand is classified as T1 (internationally renowned brands that require prior brand authorization).
- Brand selection rules: You can only select the following types of brands during product creation/editing.
   - Authorized brands which contain the desired category (authorized_status=AUTHORIZED and brand_status=AVAILABLE)
   - Unauthorized non-T1 brands (authorized_status=UNAUTHORIZED and is_t1_brand=false)
- Brand display rules: Note however that brands will only appear on the product display page if the brand is authorized (authorized_status=AUTHORIZED) and available in the desired category (brand_status=AVAILABLE). This means that you need to obtain brand authorization for unauthorized non-T1 brands before they can be displayed. Obtain brand authorization or add categories to an authorized brand through TikTok Shop Seller Center > Qualification Center > Brand qualification.
For Tokopedia sellers: You can select and display any returned brand on Tokopedia regardless of these rules.


GET /product/202309/brands

## Request
### Example

curl -X GET \
 'https://open-api.tiktokglobalshop.com/product/202309/brands?app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1623812664&category_id=600006&is_authorized=false&page_size=100&page_token=b2Zmc2V0PTAK&category_version=v1&shop_cipher=GCP_XF90igAAAABh00qsWgtvOiGFNqyubMt3&brand_name=Teas' \
-H 'content-type: application/json' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k'

## Response
### Example

{
  "code": 0,
  "data": {
    "brands": [
      {
        "id": "7082427311584347905",
        "name": "Teas",
        "authorized_status": "AUTHORIZED",
        "is_t1_brand": true,
        "brand_status": "AVAILABLE"
      }
    ],
    "total_count": 10000,
    "next_page_token": "b2Zmc2V0PTAK"
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}


## Error Code

| Code | Message |
|------|---------|
| 12019108 | page number is invalid |
| 12019109 | page size is invalid |
| 12019123 | product of pageSize and pageNumber exceeds the maximum limit |
| 12019124 | pageSize and pageNumber need to be used together |
| 12052023 | Category does not exist |
| 12052217 | All region shops must use V2 categories. Check the documentation for further details. |
| 12052230 | Category version and categoryID are not matched. |
| 12052700 | The seller is inactive. |
| 12052704 | seller id not exist |
| 36009003 | Internal error. Please try again. If the issue persists after multiple attempts, please contact platform support. |
