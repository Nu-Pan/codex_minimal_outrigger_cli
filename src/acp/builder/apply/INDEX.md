# `fork`

## Summary
- `cmoc apply fork` の作業を AI エージェントへ委譲するための呼び出しパラメータと、その結果を受け取る Structured Output schema をまとめた領域。
- 適用ブランチ上の差分要約、ファイル単位の所見列挙、検出済み所見に対応する realization file 修正依頼という、fork 適用処理の周辺タスク用 prompt 構築を扱う。
- 実際の Git 操作や fork 適用の制御フローではなく、各サブタスクに与える role、goal、参照標準、ファイルアクセス権限、モデル指定、出力 schema の入口として位置づく。

## Read this when
- `cmoc apply fork` が変更要約、所見列挙、所見対応作業をどのような AI 呼び出し条件で実行するか確認・変更したいとき。
- 適用ブランチの差分や所見リストを prompt に埋め込む形式、参照させる標準、読み書き権限、モデルクラス、推論努力の指定を調整したいとき。
- 作業レポート用の変更要約や、実装レビュー所見リストの Structured Output schema を確認したいとき。
- fork 適用処理の下流で使う、ファイル単位調査、要修正点報告、修正作業依頼の境界を把握したいとき。

## Do not read this when
- `cmoc apply fork` の CLI 引数解析、サブコマンド登録、実行順序、ブランチ操作、git コマンド実行そのものを調べたいとき。
- 差分や所見を統合して実際に適用する制御フロー、または適用結果を保存・反映する処理を確認したいとき。
- oracle standard、realization standard、apply review standard、path 解決、AgentCallParameter、完全 prompt 生成などの共通部品そのものを調べたいとき。
- 個別の変更対象ファイルの内容、テスト、ルーティング文書など、所見対応後の具体的な realization file を直接確認すれば足りるとき。

## hash
- 94555cab0a65a828745156abf12cef61ee6ad8e44e6b2902504d24a4ee1b6f85
