# `fork`

## Summary
- 適用処理を分岐環境で進める際に使う AI 呼び出しと、その構造化出力契約をまとめた領域。所見列挙、所見対応、変更要約など、レビューから修正依頼、作業結果の要約までのプロンプト生成と出力 schema への入口になる。
- oracle file と realization file の対応確認、realization file の要修正点抽出、検出済み所見をもとにした修正依頼、差分の人間向け要約といった、適用分岐処理内の AI エージェント連携仕様を確認するためのまとまり。

## Read this when
- 適用分岐処理で AI エージェントへ渡す role、goal、補助プロンプト、ファイルアクセス権限、モデル種別、reasoning effort、Structured Output schema の選択を確認または変更したいとき。
- oracle file と realization file を照合して、realization file の要修正点を列挙するレビュー呼び出しの仕様を追いたいとき。
- 列挙済みの所見を実装修正担当エージェントへ渡し、realization file を修正させる呼び出し条件を確認したいとき。
- 適用分岐処理の結果として、未加工の差分や主要な変更対象をもとに人間向けの変更要約を生成する仕様を確認したいとき。
- レビュー所見や変更要約を JSON の Structured Output として受け取るための契約を確認したいとき。

## Do not read this when
- 適用分岐処理のブランチ作成、ブランチ削除、差分取得、差分適用、レポート保存など、AI 呼び出し以外の制御フローを調べたいとき。
- AgentCallParameter、ModelClass、ReasoningEffort、FileAccessMode などの共通データ構造や enum の定義そのものを確認したいとき。
- 共通 prompt 部品のレンダリング、Markdown 化、path model、構造化ドキュメント処理など、複数機能にまたがる基盤実装を調べたいとき。
- 個別機能の正本仕様、realization standard、apply review standard の本文そのものを読みたいとき。
- 生成された所見や変更要約を CLI 表示、ログ、保存ファイル、レポート全体へどう組み込むかを調べたいとき。

## hash
- 94555cab0a65a828745156abf12cef61ee6ad8e44e6b2902504d24a4ee1b6f85
