# `oracle`

## Summary
- AIコーディングエージェント呼び出しの共通パラメータ定義と、用途別の agent call 構築実装を扱うディレクトリ。indexing、oracle、quota probe、realization、session、TUI の prompt、起動条件、アクセスモード、作業ディレクトリ、Structured Output 契約へ進む入口となる。

## Read this when
- AgentCallParameter の共通契約、モデル、推論強度、ファイルアクセス、prompt、Structured Output schema、cwd、preflight 設定を確認するとき
- INDEX.md エントリー生成、oracle の用途別 agent call、Codex CLI quota probe、realization の追従・refactor、session join の conflict 解消、cmoc tui の起動設定を調査・変更するとき
- 用途別 agent call の prompt、起動条件、権限、出力契約の入口を特定するとき

## Do not read this when
- 既存 INDEX.md のルーティング内容だけを確認したいとき
- モデル名やバックエンド固有の解決処理、共通 prompt 生成、path model、構造化文書などの共通仕様だけを確認したいときは、それぞれの定義元を直接読む
- realization の通常の implementation・test・ancillary、session join の通常処理、TUI の画面表示や対話操作など、個別の実行処理を確認したいとき
- 具体的な issue 内容、report cut reference、raw log、個別のレビュー対象や所見判定など、用途別定義の範囲外のデータや処理を調べるとき

## hash
- a0544ce5c363655c3a63456caacd1176875e6959e7617aa5324a35401af1d839
