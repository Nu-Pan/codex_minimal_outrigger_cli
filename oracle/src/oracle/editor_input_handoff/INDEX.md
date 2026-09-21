# `body.py`

## Summary
- 項目別の依頼情報、oracle文書参照、送信元識別情報を検証済みMarkdown本文へ組み立てる正本実装。
- 送信元情報の必須識別子と絶対ログパスを検証し、入力項目・参照ファイル・機械的な送信元情報を所定の見出しで出力する。

## Read this when
- editor work fileへ渡すhandoff本文の構成や各セクションの生成内容を確認したいとき。
- 送信元識別子やサブコマンドログパスの入力条件、または空の自由記述項目に対する拒否条件を確認したいとき。
- oracle参照を本文へMarkdownとして配置する処理の入口を確認したいとき。

## Do not read this when
- 入力JSONのスキーマ検証、oracle参照の変換、target検証、ファイル書き込みの責務を確認したいときは、呼び出し側やoverwrite_input.jsonを直接読む。
- Markdownノードや文書参照の具体的なレンダリング仕様だけを確認したいときは、struct_docまたはdoc_ref_modelを直接読む。

## hash
- 12319c5ad75f95d87d65eb34af4f3283437dc76ff157c2bf2d57022ae09ea272

# `get_handoff_guide_input.json`

## Summary
- 人間が指定した target ID を受け取り、対応するエディター入力ハンドオフ・ガイド取得処理へ渡すための入力スキーマです。入力は空白でない単一の target ID に限定されます。

## Read this when
- target ID を指定してハンドオフ・ガイド取得を呼び出す入力契約を確認・変更するとき。

## Do not read this when
- ハンドオフ・ガイド本文の生成規則や取得結果の形式を確認するときは、対応する実装または result スキーマを直接読むべきです。

## hash
- ba99ecf430882cf3dcd443d0fa70e892ac1b45f060980faf7f53381f4104bc72

# `get_handoff_guide_result.json`

## Summary
- `editor_input_handoff` の get_handoff_guide 操作が返す結果の JSON Schema。成功時は対象に対応する handoff ガイド本文、失敗時は取得できなかった理由を表す。

## Read this when
- get_handoff_guide の結果契約を確認・変更するとき。
- 成功・失敗それぞれの返却形式を実装やテストから確認するとき。

## Do not read this when
- get_handoff_guide 以外の操作の結果形式を確認するとき。
- handoff ガイド本文の生成ロジックや対象選択の実装を直接調べるとき。

## hash
- cd2702db609493b0f02ee5273bea04cb843f841a35261e6ed36d43c8d28a35ef

# `guide.py`

## Summary
- 完全 prompt skeleton を受け取り、受信先への依頼作成方法・記入項目・参照上の注意を含む Markdown の handoff ガイド文面を構築する関数。生成物には受信先の prompt template をタグ付きで埋め込む。

## Read this when
- 受信先の editor input handoff ガイドの文面構築や、そのガイドに含める prompt template の扱いを確認したいとき
- handoff ガイドの使い方・記入の目安・完全 prompt skeleton の配置を調べるとき

## Do not read this when
- handoff 本文の項目、空欄検証、参照ファイル、送信元情報の注入を確認したいとき
- handoff target の lifecycle や MCP の入力・上書き処理を確認したいとき

## hash
- a27040792ca678e214a6c0c0b6cf9adc30029ce6da5b9ffa7df74f6a22beb3ba

# `overwrite_input.json`

## Summary
- エディタ入力引き渡しの上書き処理へ渡す JSON 入力の正本スキーマ。必須の依頼内容・背景・判断事項・未確定事項と、任意の oracle 参照を検証する入口。

## Read this when
- editor input handoff の上書き入力項目、必須条件、oracle 参照形式、追加プロパティ禁止の扱いを確認または変更するとき

## Do not read this when
- 検証済み入力から生成される Markdown 本文の構成や送信元情報の扱いを確認するときは、本文生成実装や対応する仕様を直接読む場合
- 実際の上書き処理の呼び出し、target の検証、ファイル書き込みの挙動だけを調べるとき

## hash
- 4f0053706addcf6b548b8030916909e4dfd772a613b61227eee0ef1c9df272d1
