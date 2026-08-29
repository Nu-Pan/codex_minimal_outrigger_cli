# `launch_tui.py`

## Summary
- `cmoc oracle investigation` 用の調査担当 prompt と、Codex CLI の TUI 起動に渡す固定パラメータを構築する関数。
- ユーザー指示を完全 prompt の原文として組み込み、oracle ツリー限定の読み取り専用調査、根拠提示、未定義事項の明示を指定する入口。

## Read this when
- oracle investigation の TUI 起動時に、調査用 prompt の構成やファイルアクセスモードを確認したいとき。
- ユーザー指示を prompt に引き渡す方法や、リポジトリルートを基準にした起動パラメータを確認したいとき。

## Do not read this when
- 共通の完全 prompt 生成規則そのものを確認したいときは、prompt builder の定義を直接読む。
- oracle file の調査対象や開発環境・設計ルールの内容を確認したいときは、対応する oracle file を直接読む。

## hash
- 5ace71c88215111020e0022c923899009cafc6d9cd12177a1a398a91b9b90f21
