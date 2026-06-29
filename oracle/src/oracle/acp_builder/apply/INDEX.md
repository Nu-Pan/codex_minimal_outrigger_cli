# `fork`

## Summary
- `cmoc apply fork` に関係する agent call parameter と Structured Output schema の正本仕様断片をまとめる領域。
- 差分要約、ファイル単位の所見列挙、検出所見への対応といった apply fork 用 AI 呼び出しの prompt、file access profile、モデル設定、出力契約への入口になる。

## Read this when
- `cmoc apply fork` で差分要約、実装レビュー所見の列挙、または所見対応を行う agent call の正本仕様断片を確認したいとき。
- apply fork 系の prompt、role、goal、file access profile、Structured Output schema、モデル種別、reasoning effort の対応関係を調べたいとき。
- fork 適用後の作業レポートやレビュー結果について、人間向け要約・所見リスト・修正担当 agent への入力形式を固定したいとき。

## Do not read this when
- `cmoc apply fork` の git 操作、branch 操作、fork 作成・適用・分岐制御など、実行フロー本体を確認したいとき。
- 個別ファイルの patch 内容、diff 生成手順、または realization file を実際に修正する実装本体を探しているとき。
- 汎用的な prompt 構築、path placeholder 解決、file access profile の共通実装、または apply fork 以外のサブコマンド用 agent call parameter を確認したいとき。

## hash
- 0c35da1bb0e5418d2227930e1dbd0bb1f718e657874b812669f509b974ad8eb0
