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
