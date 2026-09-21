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

# `get_initial_guide_input.json`

## Summary
- 人間が明示した引き渡し先の target ID を指定して、editor input handoff の初期ガイド取得を依頼するための入力スキーマ。handoff 本文を上書きする入力ではなく、初期文面の取得処理への入口。

## Read this when
- editor input handoff の初期ガイド取得処理で、呼び出し側が指定する引き渡し先を確認・変更するとき。
- handoff の上書き入力ではなく、初期ガイド取得用の入力形式を確認するとき。

## Do not read this when
- editor input handoff の本文生成や送信元情報の構築を確認したいときは body.py を直接読む。
- handoff 本文を構成して上書きする入力形式を確認したいときは overwrite_input.json を読む。
- 初期ガイド取得の結果形式を確認したいときは get_initial_guide_result.json を読む。

## hash
- 974d4321449ff50132781f72dfec8e889680b57b93d34960d2a3f9baabdafeec

# `get_initial_guide_result.json`

## Summary
- エディタ入力ハンドオフの初期ガイド取得結果を定義する JSON Schema。取得成功時の初期文面、または取得失敗時の理由を表現する。

## Read this when
- 初期ガイド取得処理の返却形式を確認・変更するとき
- 初期文面が取得できた場合と取得できない場合の結果構造を確認するとき

## Do not read this when
- 初期ガイド取得の入力形式を確認するときは get_initial_guide_input.json を読む
- 初期ガイド取得の処理ロジックを確認・変更するときは body.py を直接読む
- 初期ガイド以外のエディタ入力ハンドオフ結果を扱うとき

## hash
- 7a2f649247b8325d0987fc463601abef5d779f372be90771252880bb726daaff

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
