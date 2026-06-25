# `fork`

## Summary
- `cmoc apply fork` の補助的な AI エージェント呼び出しと、その構造化出力契約を扱う領域。変更要約、ファイル単位の要修正所見列挙、所見対応作業のためのプロンプト構築と schema がまとまっている。
- 適用・分岐処理そのものではなく、作業レポートやレビュー所見、所見対応エージェントへの入力をどのように組み立てるかを確認する入口になる。

## Read this when
- `cmoc apply fork` で差分要約、所見列挙、所見対応作業を AI エージェントへ依頼する際の prompt、モデル種別、reasoning effort、ファイルアクセス権限、Structured Output schema の対応を確認・変更したいとき。
- apply fork のレビュー結果や変更要約を、カテゴリ単位またはファイル単位の構造化データとしてどの粒度で返すかを確認したいとき。
- oracle file や realization file を起点にした要修正点調査、または所見リストを使った realization file 修正依頼のプロンプト構成を追いたいとき。
- 作業レポート用に git diff や所見 JSON がどのように補助入力としてエージェント prompt へ埋め込まれるかを確認したいとき。

## Do not read this when
- `cmoc apply fork` 全体の CLI 引数処理、fork 作成・削除、git 操作、対象ファイル一覧の作成、複数呼び出しの統合など、サブコマンド本体の制御フローを調べたいとき。
- 個々の差分を検出するアルゴリズム、変更をカテゴリへ分類する実処理、または実際のファイル修正ロジックを確認したいとき。
- 共通の prompt 部品、Markdown レンダリング、パス解決 helper、AI 呼び出し基盤そのものの実装を確認したいとき。
- apply fork 以外のサブコマンドの prompt、schema、エージェント設定を調べたいとき。

## hash
- d38cd804b314e18a5f023f0c20960742dc3f039536ec53b5f7daf6fd61647bb2
