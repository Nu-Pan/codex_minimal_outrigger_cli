# `oracle`

## Summary
- `acp_builder` は agent call のモデル、推論強度、ファイルアクセス、prompt、Structured Output schema、作業ディレクトリなどの起動パラメータを定義し、oracle・realization・session・TUI など用途別の起動定義へ分岐する入口です。
- `feedback` は agent が検出した問題を構造化して報告する入力契約を定義し、問題分類・重要度・影響・原因・根拠・作業継続状態の形式を確認する入口です。
- `other` は cmoc の設定モデル、Codex CLI 設定、agent call の作業ルート解決、パスプレースホルダー、構造化文書の Markdown 化を扱う共通基盤です。設定・パス・文書レンダリングの挙動を確認するときに進みます。
- `prompt_builder` は agent call に渡す完全 prompt とエディタ初期入力を構築し、placeholder、oracle／realization の基本説明、ファイルアクセスや routing などの policy を組み合わせる領域です。prompt の構成や個別 policy の実装を追跡する入口になります。

## Read this when
- agent call の起動パラメータや用途別 builder を確認・変更するとき
- agent feedback の入力形式や検証契約を確認するとき
- cmoc の設定値、パス解決、placeholder、構造化文書のレンダリングを確認するとき
- agent に渡す prompt の構成、policy、placeholder、エディタ入力を確認・変更するとき

## Do not read this when
- oracle や realization の正本仕様、またはそれらの操作結果そのものを確認したいとき
- 通常の CLI 呼び出し処理や agent 実行制御の実装を確認したいとき
- collector による feedback の保存・集約・重複判定を確認したいとき
- 個別の下位 builder、policy、schema の詳細だけを確認したいときは、対応する下位対象を直接読むとき

## hash
- 98ced5e948e480a895cd588a7785199368a444d64bcabdd2012f45d0fe9e9f17
