# `oracle`

## Summary
- AI コーディングエージェント呼び出しのパラメータ構築定義をまとめた領域。共通契約と、indexing・feedback・realization・session・tui・oracle 向けの処理別設定を扱う下位要素への入口。
- feedback reporter から collector へ渡す問題報告の入力契約を扱う領域。分類・重要度・影響、人間対応の必要性、根拠、確信度、作業継続状態に関する定義を確認する入口。
- 設定モデル、パスコンテキストと root placeholder 解決、構造化 Markdown 生成など、cmoc の共通基盤モデルと文書生成ヘルパーをまとめた領域。
- agent 向け完全 prompt の構築実装をまとめた領域。summary・goal、共通 policy、oracle／realization の説明、補助部品、placeholder を統合する処理と、その下位の共有部品・policy への入口。

## Read this when
- 特定の cmoc 処理が構築する agent call パラメータ、完全 prompt、モデル・推論設定、ファイルアクセス、Structured Output、cwd、indexing preflight を調査・変更するときは acp_builder を読む。
- feedback reporter の入力形式や、検出した問題を人間向け feedback として構造化・検証する処理を確認するときは feedback を読む。
- cmoc の設定モデル、パス表記・root 解決、または構造化 Markdown 文書生成の共通実装を調査・変更するときは other を読む。
- agent call に渡す完全 prompt の構成、policy の注入条件・順序、共通説明、placeholder、エディタ入力の扱いを調査・変更するときは prompt_builder を読む。

## Do not read this when
- agent call の実行制御や終了結果の処理を調査するときは、acp_builder ではなく呼び出し側または実行処理を直接読む。
- collector 側の保存・集約・重複判定、または feedback の検出方法や継続判断だけを確認するときは、feedback ではなく該当する collector・判定処理を直接読む。
- 個別 CLI 機能、oracle review の具体的処理、設定ファイルの実内容、特定機能固有の prompt・仕様を確認するときは other ではなく直接の実装・仕様を読む。
- 個別 policy や共有 prompt 部品の本文だけを確認するときは prompt_builder 全体ではなく policy または parts 配下を直接読む。
- StructDoc・StructBlock、FileAccessMode、agent call の path context、利用側 CLI 実装、INDEX.md 自体を確認するときは prompt_builder ではなくそれぞれの定義元・利用側を直接読む。

## hash
- a25981db1d9de844c467f6f2335b195124d8b61b7ab378567d4c9942a4e2bd87
