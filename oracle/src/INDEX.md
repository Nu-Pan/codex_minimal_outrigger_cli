# `oracle`

## Summary
- cmoc の設定値、Git worktree と root placeholder の解決、構造化文書の Markdown レンダリングを扱う共通基盤への入口。
- agent call の prompt、policy、ファイルアクセス規定、oracle／realization の扱い、routing、editor input を組み立てる責務を担う。
- 用途別 agent call に渡す prompt、cwd、Structured Output schema、アクセスモード、preflight などの起動パラメータを構築する。
- oracle review、oracle investigation／edit、realization apply／refactor、feedback、session join、TUI、indexing、quota probe などの個別 agent call 定義への入口を提供する。
- エディタ入力上書き、feedback reporter 入力、oracle review 所見、各種 Structured Output の契約を定義する下位要素を含む。

## Read this when
- cmoc の設定モデル、agent call の cwd と worktree、root placeholder の解決、または構造化文書の生成規則を確認・変更するとき。
- agent call の prompt 構成、policy の適用、ファイルアクセス制約、routing、oracle／realization の扱い、editor input の初期文面を調査・変更するとき。
- 特定の cmoc 操作に対応する agent call の起動パラメータ、Structured Output schema、アクセスモード、preflight、または用途別 prompt を確認するとき。
- oracle review の所見列挙・統合・検証・判定、feedback の検証・正規化、realization の編集、session conflict 解消などの個別処理の入口を探すとき。
- エディタ入力上書きや feedback reporter など、外部ツールに渡す入力契約を確認するとき。

## Do not read this when
- 実際の Codex CLI 実行、サブコマンドの引数解析、agent call の実行後処理だけを確認したいときは、対応する実行本体を直接読む。
- 特定の agent call の詳細な prompt 文面、出力項目・型・形式、個別 oracle／realization の仕様を確認したいときは、対応する下位ファイルを直接読む。
- 設定値の具体的な既定値、パス解決の個別変換規則、Markdown ノードの詳細なレンダリング挙動を確認したいときは、該当する共通基盤ファイルを直接読む。
- feedback の保存・集約・重複判定や、問題を検出して継続可否を判断するロジックだけを確認したいときは、collector または対応する処理本体を直接読む。

## hash
- 33e10657bd5d9d30de8c498a08ffb513a616dd60197eaaaa3d6c7cb3b2c38236
