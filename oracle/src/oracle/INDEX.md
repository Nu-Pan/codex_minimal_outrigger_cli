# `acp_builder`

## Summary
- 対象ディレクトリは、oracle 操作向け agent call の起動定義をまとめる領域です。oracle の編集・調査・レビューで使う prompt、モデルや権限などの実行パラメータ、Structured Output schema を確認するための入口になります。
- 下位には、oracle file の編集用、調査用、レビュー用の起動定義や出力契約があり、oracle 操作の種類に応じて対応する定義へ進みます。

## Read this when
- oracle file の編集・調査・レビューに使う agent call の prompt、実行パラメータ、作業範囲を確認または変更するとき
- oracle 操作用 agent call の Structured Output による出力契約や、builder と schema の対応を確認するとき

## Do not read this when
- oracle file の内容、編集対象の仕様、またはレビュー・調査結果そのものを確認したいとき
- agent call の共通データモデルや一般的な起動処理だけを確認したいとき
- oracle 操作以外の agent call 定義や実装を確認したいとき

## hash
- f2455bab083a3fcd15bc3b362b0317907bc4a9b5f531a2df391ac57515f53d54

# `feedback`

## Summary
- 対象ディレクトリは、agent が検出した問題を feedback reporter から collector へ渡すための入力契約を扱う領域です。問題の分類・重要度・影響、人間の対応が必要な理由、原因の確信度、再確認可能な根拠、作業継続状態を表現・検証する下位要素への入口になります。

## Read this when
- feedback reporter の入力形式や、検出した問題を人間向け feedback として構造化する処理を確認するとき。
- 入力契約を構成するスキーマや関連する検証定義を調査・変更するとき。

## Do not read this when
- collector 側の保存、集約、重複判定の仕様だけを確認したいとき。
- feedback の検出方法や、agent が作業を継続するかどうかの判断ロジックだけを確認したいとき。

## hash
- a86d0e0a2687a4eed300cd97383ba6e521f2347418e4446a2bfba702aedcd9ba

# `other`

## Summary
- cmoc の設定モデル、パス表記・ルート解決、構造化文書の Markdown レンダリングを扱う補助モジュール群。設定値や既定値、agent call のパス境界、文書要素の整形規則を確認する際の入口となる。

## Read this when
- cmoc の設定項目、Codex CLI 設定、oracle review のループ上限、設定値の JSON/TOML 表現を確認するとき
- agent call の cwd から work root・repository root を導出する規則や、ルートプレースホルダー付きパスの解決・変換を確認するとき
- 構造化された見出し、参照可能な cmoc ブロック、コードブロック、規定文を Markdown へレンダリングする挙動を確認するとき

## Do not read this when
- Codex CLI の実際の呼び出し処理や CLI 実装の責務を確認するとき
- oracle review のレビュー処理や所見生成ロジックそのものを確認するとき
- 設定ファイルの保存内容・人手による調整結果だけを確認するとき
- 具体的な正本仕様や生成文書の内容を確認する必要があり、別の仕様・呼び出し元を直接読むべきとき

## hash
- 6125a10678c23ca628f6b05330ed05e7e19dcdfdc72e272f7ec6c54533ce00a1

# `prompt_builder`

## Summary
- agent call 用の完全な prompt を組み立てる prompt builder 群。placeholder 共通型、完全 prompt 統合、エディタ初期入力、oracle／realization 説明、各種 policy 構築を扱い、prompt 生成仕様を実装から確認するための入口となる。

## Read this when
- agent call に渡す prompt の構成、統合順序、placeholder、エディタ初期入力、oracle／realization 説明、または適用 policy の実装を確認・変更するとき。
- 特定の prompt builder 部品の責務や、prompt builder 内で共通利用される型定義を追跡するとき。

## Do not read this when
- 正本仕様としての oracle 文書や realization 文書を確認する場合は、参照先の oracle file を直接読む。
- CLI の呼び出し側、通常の agent 実行処理、または prompt policy と無関係な実装を調べる場合は、該当する実装を直接読む。
- 特定の下位 policy や個別 builder の内容だけを確認する場合は、対象の下位ファイルを直接読む。

## hash
- 798fc10e4543bc4033abee8fb99ae658c5ef7c2943f1282f9f0f4682a4091576
