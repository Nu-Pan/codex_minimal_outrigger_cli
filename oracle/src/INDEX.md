# `oracle`

## Summary
- oracle の設定、パス解決、標準定義、構造化文書生成を扱う共通実装への入口。複数の oracle 機能にまたがるモデルや文書生成の責務を確認し、該当する下位モジュールへ進むためのルーティング対象。
- agent call の prompt 構成、Structured Output、モデルや推論強度、ファイルアクセス、作業ディレクトリなどの定義を集約する領域。共通パラメータや論理列挙、feedback・indexing・oracle・realization・session・TUI・quota probe の呼び出し構築へ進む入口。
- feedback reporter から collector へ渡す入力契約を扱う領域。問題の分類・重要度・影響、人間対応の必要性、確信度、根拠、作業継続状態を構造化・検証する下位要素への入口。
- agent call 向け prompt の構成要素と統合順序、placeholder、エディタ入力の初期化、用途別 instruction の構成を扱う領域。共通規則をどの部品から組み立てるか調査する際の入口。

## Read this when
- cmoc の oracle 共通実装について、設定値、root placeholder、agent call のパスコンテキスト、agent 向け標準、または構造化 Markdown 文書生成の入口を確認・変更するとき。
- agent call の共通パラメータ、論理的なモデル種別、推論強度、ファイルアクセスモード、作業ディレクトリ、Structured Output、起動条件、実行権限の定義を確認・変更するとき。
- feedback reporter の入力形式や、検出した問題を人間向け feedback として構造化・検証する処理を調査・変更するとき。
- agent call に渡す prompt の部品、統合順序、依存関係、placeholder、エディタ入力初期テキスト、oracle・realization・routing・file access・feedback の共通規則を調査・変更するとき。

## Do not read this when
- 特定の CLI 機能、realization、oracle file、realization file、issue 状態などの具体的な挙動を確認するときは、該当する直接の実装・仕様を読む。
- 実際の agent call 実行処理や Codex CLI sandbox の正本仕様を確認するときは、実行処理・sandbox の定義を直接読む。
- collector 側の feedback 保存・集約・重複判定や、feedback の検出方法・継続判断だけを確認するときは、該当する直接の定義元を読む。
- 共通 prompt builder やパス解決の一般実装だけ、または個別 builder の実装だけを確認するときは、対応する下位モジュールを直接読む。
- 永続化設定の同期、doctor、列挙型の定義、標準値の個別利用箇所だけを確認するときは、それぞれの直接の定義元・利用元を読む。
- INDEX.md のルーティング情報だけを確認・変更するときは、この対象を読まない。

## hash
- dd231d0be5a5fff968def169cd82066b1aa67bd81366c859ffd169908c2eca29
