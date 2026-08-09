# `oracle`

## Summary
- cmoc の oracle src にあるエージェント呼び出し構築実装のルート。共通パラメータ、prompt 構築、Structured Output schema、および TUI・indexing・feedback・oracle review・realization・session join 向けの呼び出し定義を扱う。
- 共通モデル、構造化文書、パス解決、規範モデルは基盤領域に、prompt の共通構造は prompt 構築領域に、用途別の呼び出し条件と schema は acp_builder 配下の各用途領域に分かれている。

## Read this when
- AI コーディングエージェントのモデル、推論強度、ファイルアクセス、作業ディレクトリ、Structured Output などの呼び出し契約を調査するとき。
- cmoc の TUI、indexing、feedback、oracle、realization、session join のいずれかに対応する prompt や agent call parameter の構築箇所を特定するとき。
- 共通 prompt builder、基盤モデル、または用途別 builder のどこから調査を始めるか判断するとき。

## Do not read this when
- 実際の cmoc サブコマンドの実行フローや agent call の起動処理を調査するときは、呼び出し側または実行基盤を直接読む。
- prompt の共通構造や静的な規範部品だけを確認したいときは、prompt 構築領域または対応する部品へ直接進む。
- 個別の schema、基盤モデル、正本仕様、realization 実装、または feedback 保存処理の詳細だけを確認したいときは、対応する直接の対象を読む。

## hash
- 6760e918ada732a1e1d9cf64b41d3fab5b71e3eb778de547385306f5fef00264
