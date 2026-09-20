# `oracle`

## Summary
- cmocの正本ソースを構成するPython実装とJSONスキーマのルート。agent向け完全プロンプト、各種ポリシー、oracle/realizationの分類・ルーティング、ACP起動パラメータ、TUI・編集・調査・適用・競合解消・フィードバック処理、入力引き継ぎ、Markdown構造化レンダリング、パス・設定・文書参照モデルを提供する。
- prompt_builder は作業目的に応じた完全プロンプトと、oracle/realization、ファイルアクセス、ルーティング、フィードバック、編集入力引き継ぎ等の規定文を組み立てる入口。
- acp_builder は各cmocサブコマンドの agent 呼び出しパラメータを構築する入口で、実行対象・作業権限・作業ディレクトリ・構造化出力スキーマ・index preflight の組み合わせを定義する。
- other は構造化Markdown、パス解決、設定、文書参照など、プロンプト生成とACP構築で共有される基盤モデルを扱う。editor_input_handoff と feedback は、エディタ入力の本文生成およびフィードバック報告入力に関する正本データ構造を扱う。

## Read this when
- cmocがagentへ渡す完全プロンプトや、特定のポリシー文面がどの正本ソースから生成されるかを確認するとき。
- cmocサブコマンドのACP起動条件、ファイルアクセスモード、作業対象、実行時の補助プロンプト、構造化出力設定を確認するとき。
- oracle file と realization file の分類、ルーティング、INDEXエントリー生成、フィードバック処理の実装上の入口を探すとき。
- Markdown構造化文書のレンダリング、パス・リポジトリルート解決、設定・文書参照モデルなど、複数機能が共有する基盤を確認するとき。

## Do not read this when
- 単一サブコマンドの実装詳細だけを確認する場合は、該当する acp_builder 配下の個別モジュールへ直接進むべきである。
- agent向けポリシーの本文だけを確認する場合は、該当する prompt_builder/policy または prompt_builder/parts の個別モジュールを直接読むべきである。
- INDEXエントリー生成の出力形式や処理だけを確認する場合は、acp_builder/indexing の個別実装とスキーマを直接読むべきである。
- 共有Markdownレンダリングやパス解決の挙動だけを確認する場合は、other 配下の該当モジュールを直接読むべきである。

## hash
- 05a17c8e3332077ce1ef9515bd777ee2cd20ab201d7b7a079a5532d40ca1a54c
