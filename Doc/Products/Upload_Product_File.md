# Upload Product File

Upload non-image files, such as PDF or video to TikTok Shop.
Use this API when you need to add videos to your product to improve the shopping experience, or submit certifications or reports to meet TikTok Shop requirements for listing restricted products.
Note: You must store the response body to retrieve the ID or URL required to associate the file with a product during product creation or editing.

POST /product/202309/files/upload

## Request
### Example

curl -X POST \
 'https://open-api.tiktokglobalshop.com/product/202309/files/upload?app_key=38abcd&sign=5361235029d141222525e303d742f9e38aea052d10896d3197ab9d6233730b8c&timestamp=1623812664' \
-H 'x-tts-access-token: TTP_pwSm2AAAAABmmtFz1xlyKMnwg74T2GJ5s0uQbS8jPjb_GkdFVCxPqzQXSyuyfXdQa0AqyDsea2tYFNVf4XeqgZHFfPyv0Vs659QqyLYfsGzanZ5XZAin3_ZkcIxxS0_In6u6XDeU96k' \
-H 'content-type: multipart/form-data' \
-F 'data=@"file"' \
-F 'name=SNI.pdf'

## Response
### Example

{
  "code": 0,
  "data": {
    "id": "v09e40f40000cfu0ovhc77ub7fl97k4w",
    "url": "https://p-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/c668cdf70b7f483c94dbe\n",
    "name": "SNI.PDF",
    "format": "PDF"
  },
  "message": "Success",
  "request_id": "202203070749000101890810281E8C70B7"
}

## Error Code

| Code | Message |
|------|---------|
| 12019103 | Couldn't upload file, the file is empty. |
| 12019104 | The file name is empty. |
| 12019105 | Failed to process the file. The format or content is not supported. |
| 12019122 | The video ratio must be between 9:16 and 16:9. |
| 12038002 | Invalid upload file. Please ensure you are passing the correct file data. |
| 12038004 | Failed to process the image. The format or content is not supported. |
| 12038005 | The file size exceeds the maximum allowed size. |
| 36009003 | Internal error. Please try again. If the issue persists after multiple attempts, please contact platform support. |
