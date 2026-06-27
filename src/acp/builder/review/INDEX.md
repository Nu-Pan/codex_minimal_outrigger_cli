# `oracle`

## Summary
- `cmoc eval-oracle` の oracle review における所見処理を扱う領域。新規所見の列挙、所見の妥当性を支持・否定する理由の収集、所見の採否判定、複数所見の整理に使う AI 呼び出しパラメータ構築と Structured Output 契約への入口になる。
- レビュー対象の正本仕様断片、既知所見、既知理由、所見リストをどのように prompt へ渡し、oracle file を根拠にしたレビュー結果だけを返させるかを確認するための下位要素をまとめている。
- 所見の生成・検証・判定・統合という review oracle の各段階について、prompt の役割、読み取り権限、モデル・推論設定、対応する出力契約を追うためのルーティング単位である。

## Read this when
- `cmoc eval-oracle` の oracle review で、所見を列挙・検証・採否判定・整理する各 AI 呼び出しの入口を探しているとき。
- oracle file を根拠にしたレビュー所見について、既知情報との重複を避けて新規の所見や理由だけを返させる prompt 制御を確認したいとき。
- レビュー所見を人間へ提示するかどうかの判定、または判定理由に支持側・反対側の観点をどう反映するかを確認したいとき。
- 複数の oracle review 所見について、重複・矛盾・過剰な細分化を解消する編集操作の出力契約や prompt 構築を確認したいとき。
- review oracle 系の Structured Output 契約と、それを参照するエージェント呼び出しパラメータの対応関係を確認したいとき。

## Do not read this when
- oracle file や realization file の基本定義、所有責任、配置ルールを確認したいだけのとき。
- レビュー基準となる正本仕様断片そのものや、個別の oracle file 本文を読みたいとき。
- `cmoc eval-oracle` 以外のサブコマンドの prompt 構築、AI 呼び出しパラメータ、出力契約を扱うとき。
- prompt 部品の共通組み立て、markdown rendering、パス解決、基本データ型など、review oracle 固有ではない基盤処理を変更したいとき。
- 生成済みの所見や編集操作を実際に保存・表示・通知・適用する後段処理を探しているとき。
- INDEX.md エントリーの一般的な記述方針や、ルーティング文書そのものの標準を確認したいとき。

## hash
- a145efedba88847f4bd0acf7077469c9bfb6158fc6f286e028f982c864fa4d81
