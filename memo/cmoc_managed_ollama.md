
# cmoc managed ollama

## サービス生存確認

```bash
systemctl --user is-active cmoc-ollama
```

active と出れば service は起動中です。

## サービス終了コード判定

```bash
systemctl --user is-active --quiet cmoc-ollama && echo "running" || echo "not running"
```

## サービスのステータスを見る

```bash
systemctl --user status cmoc-ollama
```

## サービスの MainPID を確認する

```bash
systemctl --user show cmoc-ollama --property=MainPID --value
```

## サービスが実際に cmoc 管理下の ollama 実行ファイルで起動しているか確認する

```bash
pid="$(systemctl --user show cmoc-ollama --property=MainPID --value)"
tr '\0' ' ' < "/proc/$pid/cmdline"
echo
```

期待される実行ファイルはだいたいの場合 `$HOME/.cmoc/ollama/bin/ollama serve`

## HTTP API が応答するか確認する

```bash
curl -fsS http://127.0.0.1:11434/api/tags
```

## cmoc が使う環境に近い形で ollama CLI から確認する

```bash
OLLAMA_HOST=127.0.0.1:11434 \
OLLAMA_MODELS="$HOME/.cmoc/ollama/models" \
"$HOME/.cmoc/ollama/bin/ollama" list
```

## サービスを一時停止する:

```bash
systemctl --user stop cmoc-ollama
```


## サービスを停止できたか確認する

```bash
systemctl --user is-active cmoc-ollama
```

`inactive` や `failed` など、`active` 以外なら停止状態

## HTTP 側も止まっているか見る

```bash
curl -fsS http://127.0.0.1:11434/api/tags
```

これは停止後は失敗するのが自然

## 自動起動設定も外したい

```bash
systemctl --user disable cmoc-ollama
```
