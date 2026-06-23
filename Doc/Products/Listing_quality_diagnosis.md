# Listing quality diagnosis

High-quality product listings are essential for improving visibility and building customer trust.
TikTok Shop provides APIs that diagnose product content and offer recommendations for optimization, covering areas such as text, image, and search engine optimization (SEO).

For unlisted new products

    Check Product Listing API (v202309): Use this API to diagnose new products in advance before listing.

For existing products

    Product Information Issue Diagnosis API (v202405): Use this API to diagnose live products that are already listed in the shop catalog.

Note: For developers servicing the US market, you can use the Search Products API (v202312) to first retrieve products that fall under a certain listing quality tier before running Product Information Issue Diagnosis API (v202405) to identify the recommendations. After which, you can use Get Product API (v202309) to retrieve a product's existing property values (including its listing quality tier) and pinpoint the ones that need to be edited.

# Diagnosis results and recommendations

The diagnosis is performed on the following product fields:
- Title: The product title (API property: title)
- Description: The product description (API property: description)
- Attributes: The product attributes (API property: product_attributes or skus.sales_attributes)
- Size chart: The size chart image (API property: size_chart)
- Product images: The product images displayed in the image gallery (API property: main_images)

Refer to the following region-based tables for the diagnosis results/codes returned in the APIs and the actionable recommendations to optimize your listings effectively.
Note: Codes marked as "Retired" indicate that they are no longer recommended and will not appear anymore.

# United States

In the US, product listings are evaluated based on a tiered system that includes listing quality tiers such as "POOR", FAIR", and "GOOD". Each diagnosis code corresponds to a specific recommendation and is assigned a quality tier, such as "FAIR" or "GOOD". Implementing the recommendations can help your listing progress through these tiers to achieve better quality and visibility. For example, a product will reach the "GOOD" tier once all "FAIR" and "GOOD" recommendations are addressed or implemented.
For more information about the listing quality tiers and criteria, refer to Listing Quality Guidelines.

# Rest of World

For regions outside the US, product listings are evaluated based on key recommendations. The following table provides the list of diagnosis codes along with actionable recommendations to improve your product listing's overall quality and visibility.
