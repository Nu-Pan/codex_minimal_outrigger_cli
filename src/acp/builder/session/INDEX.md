# `join`

## Summary
- `cmoc session join` のうち、merge conflict marker 解消を AI エージェントへ依頼するための呼び出しパラメータ構築を扱う領域。
- 解消対象パスの実パス解決、対象一覧や作業範囲を含む完了プロンプト生成、編集禁止事項や oracle file 例外、commit 禁止、marker 残存禁止などの制約をエージェントへ渡す入口になる。
- 通常の join 処理そのものではなく、conflict marker 解消タスクを別エージェントに任せる際の role、summary、goal、補助プロンプト、モデル設定、ファイルアクセス方針を確認するための下位要素を含む。

## Read this when
- `cmoc session join` で検出された merge conflict marker を解消するため、AI エージェントへ渡す呼び出し内容を確認・変更したいとき。
- conflict 解消対象ファイル一覧、作業範囲、完了条件、編集禁止事項、oracle file 例外をどのようにプロンプトへ含めるかを調べたいとき。
- merge conflict 解消タスクで使うエージェントの role、summary、goal、補助プロンプト、モデル設定、reasoning 設定、ファイルアクセス方針を調整したいとき。
- 通常は編集禁止の oracle file に conflict marker がある場合だけ、必要最小限の編集を許可する扱いを確認したいとき。

## Do not read this when
- `cmoc session join` の通常の join 処理、git 操作、branch 操作、worktree 操作を調べたいとき。
- merge conflict marker の検出処理そのものや、検出後の join 全体の制御フローを調べたいとき。
- conflict marker を実際に解消するアルゴリズム、解消後の検証、テスト実行、残存 marker チェックを探しているとき。
- 汎用的な markdown prompt rendering、構造化ドキュメント表現、path model、work root 解決、実パス解決の詳細仕様を調べたいとき。

## hash
- 53f7c2a619ad1fe2dc649785825ad617a867006419881f90090b32ffe974c98a
