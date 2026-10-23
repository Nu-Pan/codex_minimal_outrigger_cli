"""代替 HTTP 配布元と、fork した process の並行取得 worker を用意する。"""

import io
import ssl
import urllib.request
import urllib.response
from email.message import Message

import commons.runtime_download_asset_cache as cache_module
from commons.runtime_download_asset_cache import DownloadAssetCache


def http_distribution_opener():
    """代替 HTTP 配布元に不要な CA 読み込みを省く opener factory を返す。"""
    # 配布元は HTTP のみ。通常の handler 構成と取得ごとの通信記録は保つ。
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    build_opener = urllib.request.build_opener

    def opener(*handlers):
        return build_opener(*handlers, urllib.request.HTTPSHandler(context=context))

    return opener


def download_response(url, body, code=200, location=None):
    """urllib の redirect と通信記録を通す HTTP 応答を作る。"""
    headers = Message()
    headers["Content-Length"] = str(len(body))
    if location:
        headers["Location"] = location
    response = urllib.response.addinfourl(io.BytesIO(body), headers, url, code)
    response.msg = "fixture response"
    return response


def process_obtain(cache_root, root, asset, destination, downloading, waiting, result):
    """取得開始を親へ知らせ、実 lock の競合後に結果と取得回数を返す。"""
    cache_module.asset_cache_directory = lambda: cache_root
    count = 0

    def transport(_handler, request):
        nonlocal count
        count += 1
        downloading.set()
        # 実 lock の競合まで応答を保留し、固定 sleep に依存せず待機後の再利用を通す。
        assert waiting.wait(10), "no concurrent cache waiter"
        return download_response(request.full_url, b"model bytes")

    # HTTP opener は親の fixture を継承し、取得の応答と回数だけを分離する。
    urllib.request.HTTPHandler.http_open = transport
    try:
        action = DownloadAssetCache(root).obtain(asset, destination)
        result.send((action, count))
    finally:
        result.close()
