# std

# cmoc
from oracle.other.cmoc_config import CmocConfig
from oracle.other.struct_doc import ntqs


def ensure_cmoc_managed_ollama(
    cmoc_config: CmocConfig,
):
    """cmoc managed ollama を利用可能な状態を保証する関数

    conc_config: CmocConfig
        cmoc 設定
    """
    # cmoc managed ollama が必要とされてなければ何もしない
    use_cmoc_managed_ollama = any(
        spec.model_provider == "cmoc" for spec in cmoc_config.codex.model.values()
    )
    if not use_cmoc_managed_ollama:
        return

    # 既に通るなら何もしない
    # TODO `http://127.0.0.1:11434/api/tags` に対する疎通確認をする

    # ollama archive を取得
    # TODO `https://ollama.com/download/ollama-linux-amd64.tar.zst` から取得し `/tmp/ollama-linux-amd64.tar.zst` に保存

    # ollama archive を展開
    # TODO ollama archive を `~/.cmoc/ollama` へ展開 (`~/.cmoc/ollama/bin/ollama` が通るように)

    # モデルディレクトリを作成
    # TODO モデルディレクトリは `~/.cmoc/ollama/models`

    # サービスをデプロイ
    service_body = ntqs("""
    [Unit]
    Description=CMOC Ollama user service
    After=network-online.target

    [Service]
    Type=simple
    ExecStart=%h/.cmoc/ollama/bin/ollama serve
    Restart=always
    RestartSec=3
    Environment=OLLAMA_HOST=127.0.0.1:11434
    Environment=OLLAMA_MODELS=%h/.cmoc/ollama/models
    Environment=PATH=%h/.cmoc/ollama/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

    [Install]
    WantedBy=default.target
    """)
    # TODO `~/.config/systemd/user/cmoc-ollama.service` に service_body を書き込む

    # ollama をユーザー空間サービスとして起動
    # TODO
    #   `systemctl --user daemon-reload`
    #   `systemctl --user status cmoc-ollama`

    # ollama サービスの状態を確認
    # TODO `systemctl --user status ollama` でチェック。タイムアウト 10sec

    # ollama 接続可能チェック
    # TODO `http://127.0.0.1:11434/api/tags` に対する疎通確認をする

    # モデルをインストール
    for spec in cmoc_config.codex.model.values():
        if spec.model_provider == "cmoc":
            # TODO `spec.model` を `ollama pull <slm-name>` でロードする
            pass
