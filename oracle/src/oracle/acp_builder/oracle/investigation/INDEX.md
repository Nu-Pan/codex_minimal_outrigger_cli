# `launch_tui.py`

## Summary
- `cmoc oracle investigation` の TUI 起動パラメータを構築する入口。oracle 調査用の完全 prompt、読み取り専用のファイルアクセス範囲、エディタ入力引き渡し、indexing preflight の設定を扱う。

## Read this when
- `cmoc oracle investigation` の TUI 起動時に渡す prompt や固定パラメータを確認したいとき
- oracle file 調査 agent call の読み取り専用範囲、ユーザー指示の埋め込み、エディタ入力引き渡し、indexing preflight の設定を確認したいとき

## Do not read this when
- oracle file の調査対象や調査結果の正本仕様を確認したいとき
- TUI 起動パラメータではなく、完全 prompt の共通生成処理や構造化ドキュメントのレンダリング処理を直接確認すべきとき

## hash
- a915ebc1b99d4cece9f4e55d8c8b39da8080a01eeb43f3eb2651281e4a964a8b
