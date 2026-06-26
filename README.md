# Codex Minimal Outrigger CLI

## これを読みに来た AI へ

- 詳しくは `AGENTS.md` を参照

## Codex Minimal Outrigger CLI とは

- Codex CLI を用いた開発を補助する最小限度の外部ツール
- cmoc と略す

## 初期セットアップ

1. clone して中に入る
    ```bash
    git clone git@github.com:Nu-Pan/codex_minimal_outrigger_cli.git
    cd codex_minimal_outrigger_cli
    ```
2. python 仮想環境セットアップ
    ``` bash
    /usr/bin/python3 -m venv .venv
    ./.venv/bin/python -m pip install -e .
    ```
3. （任意） `cmoc` コマンドにパスを通す
    - `~/.bashrc` を手動編集するのがおすすめ
    - e.g. コマンドで書くなら
        ```bash
        cat <<EOF >> ~/.bashrc
        export PATH="$PWD/bin:\$PATH"
        EOF
        ```

## 基本ワークフロー

- `<cmoc-root>/oracle/doc/app_spec/usage.md` を参照

## Tips

### Ctrl+S によるターミナルロック

ターミナルに Ctrl+S を入力するとプロセスの実行が止まってしまう。
Ctrl+S はエディタ上で連打するようなショートカットなので、かなり誤爆しやすい。
そのくせ、誤爆すると数時間停止に気づかないこともザラ。

`~/.bashrc` に以下を追記すれば Ctrl+S によるターミナルロックを無効化出来る。
```bash
# Disable terminal locking by Ctrl+S 
if [[ -t 0 ]]; then
    stty stop undef
    stty start undef
fi
```
