# Upload Product Image

Upload local images to TikTok Shop for use as product images, variant images, size charts, certification images and so on.

Note:
- All images used in TikTok Shop products must be uploaded through this API. You will not be able to use any image URLs that are not hosted by TikTok Shop.
- You must store the response body to retrieve the ID or URL required to associate the image with a product during product creation or editing.

POST /product/202309/images/upload

## Request
### Example

curl -X POST \
 'https://open-api.tiktokglobalshop.com/product/202309/images/upload?app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1623812664' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: multipart/form-data' \
-F 'data=@"file"' \
-F 'use_case=MAIN_IMAGE'

## Response
### Example

{
  "code": 0,
  "data": {
    "uri": "tos-maliva-i-o3syd03w52-us/c668cdf70b7f483c94dbe",
    "url": "https://p-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/c668cdf70b7f483c94dbe\n",
    "height": 720,
    "width": 720,
    "use_case": "MAIN_IMAGE"
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}

## Error Code

| Code | Message |
|------|---------|
| 11050001 | invalid param |
| 12019116 | The image dimensions exceed the allowed limits. |
| 36009003 | Internal error. Please try again. If the issue persists after multiple attempts, please contact platform support. |
| 12038002 | Invalid upload file. Please ensure you are passing the correct file data. |
| 12038004 | Failed to process the image. The format or content is not supported. |
| 12038005 | The file size exceeds the maximum allowed size. |
| 12038014 | The image dimensions exceed the allowed limits. Allowed dimensions (width x height in pixels): {{min_width}} x {{min_height}} to {{max_width}} x {{max_height}} |
| 12038015 | Failed to process the image. The format or content is not supported. Supported formats: {{formats}} |
