# `oracle`

## Summary
- agent call の呼び出し種別、論理的なファイルアクセスモード、完全な prompt、Structured Output schema、cwd、indexing preflight の実行有無を一つの不変データクラスへ集約する入口。

## Read this when
- agent call に設定される実行条件やパラメータ構造を確認するとき。
- 呼び出し種別、アクセスモード、prompt、schema、cwd、preflight 設定の集約方法を確認するとき。

## Do not read this when
- 各ファイルアクセスモードの意味や Codex CLI sandbox との対応を確認するとき。
- Agent Call Parameter の生成・利用、個別 builder の実装、または実際の agent call 実行処理を確認するとき。

## hash
- 89e1fdb33909870fc0431ce8fe0343524b64cf3e4b5400d6974b9d7ff902d574
