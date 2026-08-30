# `oracle`

## Summary
- cmoc の agent call に渡す prompt、起動パラメータ、パスコンテキスト、設定モデルを構築する定義のルートです。
- 共通の prompt 組み立て、構造化 Markdown のレンダリング、ファイルアクセス・routing・oracle・realization などの policy、およびサブコマンド別の agent call 構築へ進む入口を提供します。
- 設定集約、root path placeholder の解決、構造化文書の表現といった横断的な基盤責務も扱います。

## Read this when
- agent call の prompt、cwd、ファイルアクセス、path placeholder、Structured Output、editor input handoff の構築責務の所在を確認するとき。
- 特定の cmoc サブコマンドに対応する agent call 構築箇所や、oracle review・realization・feedback・session join の処理段階を読む入口を探すとき。
- cmoc の設定モデル、agent call ごとの Codex 設定、Git worktree に基づくパス解決、構造化文書の Markdown 化を調査・変更するとき。

## Do not read this when
- agent call の実行処理、サブコマンドの業務ロジック、Codex CLI sandbox との対応詳細を確認したいときは、対応する実行本体または参照される正本仕様を直接読む。
- 個別の policy、prompt 部品、サブコマンド別 builder、Structured Output schema、feedback state の具体的な契約や内容だけを確認したいときは、該当する下位対象を直接読む。
- oracle file や realization file の意味仕様、個別のレビュー結果、collector の保存・集約処理そのものを確認したいとき。

## hash
- cd25f09b1a616b64ae800eeac376b74af49a6237aacfcc6fa5eea5618623de3c
