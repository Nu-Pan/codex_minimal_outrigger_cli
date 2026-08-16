# `oracle`

## Summary
- cmoc の agent 呼び出し定義と、その prompt・設定・構造化出力・パス・ポリシーを構成する実装群のルート。agent call の共通パラメータは acp_builder、prompt の合成は prompt_builder、設定・パス・ポリシー・Markdown 構造は other、feedback 入力契約は feedback から確認する。
- acp_builder ではモデルクラス、推論強度、ファイルアクセスモード、作業ディレクトリ、Structured Output、用途別の起動パラメータを扱う。
- prompt_builder では担当概要・完了条件、共通ポリシー、ファイルアクセス規定、routing、placeholder、エディタ入力文面を統合して完全 prompt を構築する。
- other では cmoc 設定、agent call の worktree・repository root 解決、ポリシー合成、構造化 Markdown レンダリングを扱う。
- feedback では agent が人間対応を要する問題を報告するための入力スキーマを扱う。

## Read this when
- agent call の共通パラメータ、モデル・推論設定、ファイルアクセス、作業ディレクトリ、Structured Output の構成を確認するとき
- 用途別の agent call builder や acp_builder 配下の oracle・realization・session・tui・indexing の入口を探すとき
- 完全 prompt の構成順序、注入される共通規定、placeholder、editor handoff、routing の扱いを確認するとき
- cmoc 設定、root placeholder と worktree の解決、PolicyCollection の合成、Markdown レンダリングを確認するとき
- feedback reporter の入力項目と問題報告契約を確認するとき

## Do not read this when
- 実際の CLI サブコマンドの実行制御や agent call の実行処理だけを確認するとき
- 個別の oracle file・realization file の正本仕様や、session の Git 操作だけを確認するとき
- 特定の prompt policy の具体的な要求や禁止事項だけを確認するときは、prompt_builder/parts 配下の定義を直接読む
- 保存済み feedback の収集・集約・重複判定だけを確認するとき
- Codex CLI sandbox の正本仕様やその他の外部規定を確認するときは、指定された oracle 文書を直接読む

## hash
- 0f2eea0a33165d7d43a10746f402a0f2b549ad421eab956319863e06004254ea
