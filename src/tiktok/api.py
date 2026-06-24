from __future__ import annotations

import hashlib
import hmac
import json
import logging
import time
from typing import Any
from urllib.parse import urlencode

import httpx

logger = logging.getLogger(__name__)

TIKTOK_API_BASE = "https://open-api.tiktokglobalshop.com"


def _build_sign(
    method: str,
    path: str,
    query_params: dict[str, str],
    body: dict[str, Any] | None,
    app_secret: str,
) -> str:
    excluded = {"sign", "access_token"}
    sorted_keys = sorted(k for k in query_params if k not in excluded)
    param_str = "".join(f"{k}{query_params[k]}" for k in sorted_keys)

    sign_str = f"{path}{param_str}"

    if method.upper() == "POST" and body:
        body_raw = json.dumps(body, separators=(",", ":"), ensure_ascii=False)
        sign_str += body_raw

    wrapped = f"{app_secret}{sign_str}{app_secret}"

    h = hmac.new(app_secret.encode("utf-8"), wrapped.encode("utf-8"), hashlib.sha256)
    return h.hexdigest()


_MAX_RETRIES = 3
_BACKOFF = 1.0


class TikTokApiClient:
    def __init__(
        self,
        app_key: str,
        app_secret: str,
        access_token: str,
        shop_cipher: str,
    ) -> None:
        self._app_key = app_key
        self._app_secret = app_secret
        self._access_token = access_token
        self._shop_cipher = shop_cipher

    def _base_query(self, include_cipher: bool = True) -> dict[str, str]:
        q: dict[str, str] = {
            "app_key": self._app_key,
            "timestamp": str(int(time.time())),
        }
        if include_cipher and self._shop_cipher:
            q["shop_cipher"] = self._shop_cipher
        return q

    def _headers(self, is_multipart: bool = False) -> dict[str, str]:
        if is_multipart:
            return {"x-tts-access-token": self._access_token}
        return {
            "Content-Type": "application/json",
            "x-tts-access-token": self._access_token,
        }

    def _sign_and_build_url(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None,
        include_cipher: bool = True,
    ) -> str:
        params = self._base_query(include_cipher)
        params["sign"] = _build_sign(method, path, params, body, self._app_secret)
        query = urlencode(params)
        return f"{TIKTOK_API_BASE}{path}?{query}"

    async def create_product(self, product_data: dict[str, Any]) -> dict[str, Any] | None:
        path = "/product/202309/products"
        body = product_data
        url = self._sign_and_build_url("POST", path, body)
        return await self._post(url, body)

    async def get_warehouses(self) -> dict[str, Any] | None:
        path = "/logistics/202309/warehouses"
        url = self._sign_and_build_url("GET", path, None)
        return await self._get(url)

    async def upload_image(self, image_data: bytes, filename: str = "image.jpg") -> dict[str, Any] | None:
        path = "/product/202309/images/upload"
        url = self._sign_and_build_url("POST", path, None, include_cipher=False)
        last_exc: Exception | None = None
        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                async with httpx.AsyncClient(timeout=60) as client:
                    headers = self._headers(is_multipart=True)
                    files = {"data": (filename, image_data, "image/jpeg")}
                    resp = await client.post(url, files=files, headers=headers)
                result = resp.json()
                if resp.status_code == 200 and result.get("code") == 0:
                    data: dict[str, Any] = result["data"]
                    logger.info("图片上传成功: %s", data.get("uri"))
                    return data
                msg = result.get("message", "")
                logger.warning("图片上传失败: code=%s msg=%s", result.get("code"), msg)
                return {"error": f"code={result.get('code')} msg={msg}"}
            except (httpx.TimeoutException, httpx.RequestError) as e:
                last_exc = e
                logger.warning("图片上传 %s (attempt %d/%d)", type(e).__name__, attempt, _MAX_RETRIES)
                if attempt < _MAX_RETRIES:
                    await _sleep_with_backoff(attempt)
        return {"error": f"max retries exceeded: {last_exc}"}

    async def recommend_category(
        self,
        title: str,
        description: str,
        image_uris: list[str],
        locale: str = "en-US",
    ) -> str | None:
        path = "/product/202309/categories/recommend"
        body: dict[str, Any] = {
            "product_title": title,
            "description": description,
            "images": [{"uri": u} for u in image_uris],
            "category_version": "v2",
            "listing_platform": "TIKTOK_SHOP",
            "include_prohibited_categories": False,
            "locale": locale.split("-")[0],
        }
        url = self._sign_and_build_url("POST", path, body)
        result = await self._post(url, body)
        if result and "error" not in result:
            cat_id = result.get("leaf_category_id") or ""
            if cat_id:
                logger.info("推荐类目: %s", cat_id)
                return str(cat_id)
        logger.warning("推荐类目失败: %s", result)
        return None

    async def get_v2_categories(
        self,
        keyword: str = "",
        locale: str = "en-US",
    ) -> str | None:
        path = "/product/202309/categories"
        all_cats = await self._fetch_categories(path, locale, keyword)
        if not all_cats:
            return None

        leaf_cats = [
            c for c in all_cats if c.get("is_leaf") and "INVITE_ONLY" not in (c.get("permission_statuses") or [])
        ]
        logger.info("V2 类目总数=%d, 可用叶子=%d", len(all_cats), len(leaf_cats))

        if leaf_cats:
            cat_id = str(leaf_cats[0].get("id", ""))
            logger.info("选中 V2 类目: %s (%s)", cat_id, leaf_cats[0].get("local_name"))
            return cat_id
        if all_cats:
            cat_id = str(all_cats[0].get("id", ""))
            logger.info("无叶子类目, 回退: %s", cat_id)
            return cat_id
        return None

    async def _fetch_categories(self, path: str, locale: str, keyword: str) -> list[dict[str, Any]] | None:
        query_params = self._base_query(include_cipher=True)
        query_params["locale"] = locale
        query_params["category_version"] = "v2"
        query_params["listing_platform"] = "TIKTOK_SHOP"
        query_params["include_prohibited_categories"] = "false"
        if keyword:
            query_params["keyword"] = keyword
        query_params["sign"] = _build_sign("GET", path, query_params, None, self._app_secret)
        url = f"{TIKTOK_API_BASE}{path}?{urlencode(query_params)}"
        result = await self._get(url)
        if result and "error" not in result:
            return result.get("categories") or []
        logger.warning("获取类目失败: %s", result)
        return None

    async def _get(self, url: str) -> dict[str, Any] | None:
        last_exc: Exception | None = None
        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    resp = await client.get(url, headers=self._headers())
                return self._handle_response(resp)
            except (httpx.TimeoutException, httpx.RequestError) as e:
                last_exc = e
                logger.warning("TikTok API %s (attempt %d/%d)", type(e).__name__, attempt, _MAX_RETRIES)
                if attempt < _MAX_RETRIES:
                    await _sleep_with_backoff(attempt)
        return {"error": f"max retries exceeded: {last_exc}"}

    async def _post(self, url: str, body: dict[str, Any]) -> dict[str, Any] | None:
        last_exc: Exception | None = None
        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                async with httpx.AsyncClient(timeout=60) as client:
                    resp = await client.post(url, json=body, headers=self._headers())
                return self._handle_response(resp)
            except (httpx.TimeoutException, httpx.RequestError) as e:
                last_exc = e
                logger.warning("TikTok API %s (attempt %d/%d)", type(e).__name__, attempt, _MAX_RETRIES)
                if attempt < _MAX_RETRIES:
                    await _sleep_with_backoff(attempt)
        return {"error": f"max retries exceeded: {last_exc}"}

    @staticmethod
    def _handle_response(resp: httpx.Response) -> dict[str, Any] | None:
        import json as _json

        if resp.status_code == 200:
            result: dict[str, Any] = resp.json()
            if result.get("code") == 0:
                data: dict[str, Any] = result["data"]
                return data
            code = result.get("code")
            msg = result.get("message", "")
            logger.warning(
                "TikTok API 业务错误 [%s] %s full=%s", code, msg, _json.dumps(result, ensure_ascii=False)[:500]
            )
            return {"error": f"code={code} msg={msg}"}
        resp_body = resp.text[:500]
        logger.warning("TikTok API HTTP %d: %s", resp.status_code, resp_body)
        return {"error": f"http={resp.status_code} body={resp_body}"}


async def _sleep_with_backoff(attempt: int) -> None:
    import asyncio

    await asyncio.sleep(_BACKOFF * (2 ** (attempt - 1)))
