# `launch_tui.py`

## Summary
- `cmoc tui` 用の完全プロンプトを構築し、リポジトリ書き込み権限・エディタ入力引き継ぎ・インデックス事前処理を含む Codex CLI TUI 起動パラメータを生成する。

## Read this when
- `cmoc tui` の起動パラメータ、プロンプト構築、起動時のパスコンテキストや実行前処理を確認・変更するとき。

## Do not read this when
- TUI の画面表示や個別ウィジェットの実装を確認するとき。
- 共通の完全プロンプト生成規則そのものを調べるときは、直接 `complete_prompt` の実装を読む。

## hash
- 2b300becbdd5415cea02a02f128eed378ccc4d514305a1477dbbf585a9dc685a
