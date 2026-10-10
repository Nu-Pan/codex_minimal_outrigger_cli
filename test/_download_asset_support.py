"""並行取得の子 process を、CLI と pytest の初期化から分離する。"""

import fcntl
import io
import urllib.request
import urllib.response
from email.message import Message

import commons.runtime_download_asset_cache as cache_module
from commons.runtime_download_asset_cache import DownloadAssetCache


def download_response(url, body, code=200, location=None):
    """urllib の redirect と通信記録を通す HTTP 応答を作る。"""
    headers = Message()
    headers["Content-Length"] = str(len(body))
    if location:
        headers["Location"] = location
    response = urllib.response.addinfourl(io.BytesIO(body), headers, url, code)
    response.msg = "fixture response"
    return response


def process_obtain(cache_root, root, asset, destination, waiting, count, result):
    """実 lock の競合を待って取得し、独立 process の結果と取得回数を返す。"""
    cache_module.asset_cache_directory = lambda: cache_root
    flock = fcntl.flock

    def observe_lock(fd, operation):
        try:
            return flock(fd, operation)
        except BlockingIOError:
            waiting.set()
            raise

    fcntl.flock = observe_lock

    def transport(_handler, request):
        with count.get_lock():
            count.value += 1
        # 実 lock の競合まで応答を保留し、固定 sleep に依存せず待機後の再利用を通す。
        assert waiting.wait(10), "no concurrent cache waiter"
        return download_response(request.full_url, b"model bytes")

    urllib.request.HTTPHandler.http_open = transport
    try:
        result.send(DownloadAssetCache(root).obtain(asset, destination))
    finally:
        result.close()
