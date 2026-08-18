# `doc`

## Summary
- cmoc の正本文書を、アプリケーション仕様と開発ルールの領域に分けて案内する入口。CLI や session/run などの挙動仕様は app_spec、実装・環境・テストの規約は dev_rule へ進む。

## Read this when
- cmoc の正本仕様、開発ルール、実装規約、テスト要件の所在を横断的に確認するとき
- 対象文書が app_spec と dev_rule のどちらに属するか判断するとき

## Do not read this when
- アプリケーション挙動の具体的な仕様が明確で、app_spec 配下の個別文書へ直接進めるとき
- 実装配置、開発環境、テスト要件、テスト実行手順のいずれかが明確で、dev_rule 配下の個別文書へ直接進めるとき
- considered_alternative、branch_model など特定領域の資料だけを調査するとき

## hash
- 6a3131cafc07825e70191d23065036a1e688919b452850fff55aa111ca8c0229

# `src`

## Summary
- cmoc の oracle 実装をまとめるルート。agent call パラメータの構築、用途別の oracle・realization・session・feedback・TUI・indexing 定義、prompt の構築、パス・設定・構造化 Markdown の共通モデルを扱う。目的別の実装を探すときは、まずこの階層から `oracle/acp_builder`、`oracle/prompt_builder`、`oracle/other`、`oracle/feedback` へ進む。

## Read this when
- AI エージェント呼び出しのパラメータや用途別の起動定義を調査・変更するとき
- 完全 prompt、prompt policy、placeholder、エディタ入力文面の構築を調査・変更するとき
- agent call 間で共有する設定、パス解決、構造化 Markdown のモデルやレンダリングを調査・変更するとき
- oracle・realization・session・feedback・TUI・indexing の実装入口を確認するとき

## Do not read this when
- 正本仕様や利用規約そのものを確認したいとき
- 実際の CLI サブコマンドの処理フローや agent call の実行機構を確認したいとき
- 特定の agent call、prompt policy、共通モデルの実装が特定できているとき
- feedback の報告入力データだけを確認したいとき

## hash
- eb66bed724bc51cebf174087887abaf6b0cf95b77d42c0df5713d328473682c5
