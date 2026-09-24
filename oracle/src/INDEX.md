# `oracle`

## Summary
- cmocのagent呼び出しに用いる正本コード群。ACP呼び出しパラメータ、プロンプト、パスモデル、フィードバック入力、editor input handoffの構築を扱う。
- `acp_builder` は各サブコマンド向けのagent呼び出しパラメータとStructured Output schemaを定義する入口。
- `prompt_builder` は作業規定・ポリシー・目的・プレースホルダを統合したagent向け完全promptを構築する。
- `other` は構造化Markdown、パス解決、文書参照、cmoc設定など複数機能から共有される基盤モデルを提供する。
- `editor_input_handoff` と `feedback` は、TUIから渡す入力本文およびフィードバック報告入力の正本形式を構築・定義する。

## Read this when
- cmocのサブコマンドがどのagent呼び出しパラメータ、prompt、schemaを使うかを横断的に確認したいとき。
- promptの規定・ポリシー・placeholderの組み立て方を確認したいとき。
- agent callで共有されるGit worktreeのパス解決や構造化Markdown表現を確認したいとき。
- editor input handoffやfeedbackの入力形式・本文生成の責務を確認したいとき。

## Do not read this when
- 特定のサブコマンドのagent呼び出し仕様だけを調べる場合は、`acp_builder`配下の対応する個別ファイルを直接読む。
- 特定のpromptポリシーだけを確認する場合は、`prompt_builder/policy`配下の該当ファイルを直接読む。
- 共有基盤の単一モデルや単一schemaの詳細だけが必要な場合は、`other`または各機能ディレクトリ内の対象ファイルを直接読む。

## hash
- c4144b145b29a23e5750abb4b61f5ae421732faaa4db817d5cb4038083c2467d
