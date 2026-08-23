# `doc`

## Summary
- `oracle/doc` 配下の正本文書群を、cmoc の共通仕様・設計検討・開発ルール・アプリケーション仕様へ案内する最上位の入口です。`app_spec`、`branch_model.md`、`considered_alternative`、`dev_rule` から、対象の仕様・用語・不採用案・開発手順に応じた下位文書を選びます。

## Read this when
- cmoc の正本仕様・設計資料・開発ルールを横断して探すとき
- アプリケーション共通仕様、branch／commit／worktree のモデル、不採用となった設計案、Python・CLI・環境・テストの開発規約の参照先を判断するとき
- 対象文書が複数の仕様領域にまたがり、まず適切な下位ディレクトリまたは文書を選ぶ必要があるとき

## Do not read this when
- 対象の個別仕様書や開発ルール文書が明らかな場合は、その文書を直接読むとき
- 特定機能の実装、prompt、Structured Output schema、テスト実行手順など、既に対象が明確な下位内容だけを確認したいとき
- `oracle/doc` 配下の文書と無関係な realization、実装ファイル、既存の INDEX.md の内容を確認するとき

## hash
- ed14661f8a936ff7b45ee16838fea19ff16b0e64c4072e348dfc9a5bed13a512

# `src`

## Summary
- oracle 関連の agent call 構築機能を、目的別 builder、feedback 契約、共通モデル、prompt 構築部品に分けて案内する上位ルーティング対象。agent call の起動条件、アクセス制約、パス解決、prompt 構成を調べる際の入口となる。
- acp_builder は、モデル種別・推論強度・ファイルアクセスモード・cwd などの AgentCallParameter を基盤に、feedback、indexing、oracle、quota probe、realization、session、TUI の目的別 agent call を構築する下位モジュール群への入口。
- feedback は、agent の observation を人間向け feedback issue として扱うための入力契約と、issue の同一性判断・現在状態の検証に関する定義への入口。
- other は、cmoc 設定、agent call 単位の root placeholder とパス解決、構造化文書ノードおよび GFM レンダリングを扱う共通モデルへの入口。
- prompt_builder は、完全 prompt、editor 初期入力、prompt 部品、file access・routing・oracle・realization・feedback などの policy を構築し、objective、placeholder、static／dynamic part を統合する機能への入口。

## Read this when
- oracle 配下の agent call 構築機能の全体配置や、目的別 builder への進み方を確認するとき
- AgentCallParameter の共通項目、モデルやアクセスモード、agent call cwd の扱いを調べるとき
- cmoc 設定、root placeholder、パス解決、構造化 Markdown 文書の共通実装を確認するとき
- agent call 用 prompt の構成、policy の選択、editor 初期入力、placeholder 統合を調べるとき
- feedback observation と issue の同一性・現在性検証に関する入力契約の入口を探すとき

## Do not read this when
- 特定の agent call の prompt 文面、起動パラメータ、Structured Output schema の具体的な定義だけを確認したいときは、該当する acp_builder 下位対象を直接読む
- 共通設定、パス解決、構造化文書の具体的な型や関数だけを確認したいときは、other の定義元を直接読む
- 特定 policy の文面や適用条件だけを確認したいときは、prompt_builder/policy の該当対象を直接読む
- feedback の保存・集約・重複判定の実行処理や、agent call の実行制御を確認したいときは、対応する利用側実装を直接読む
- oracle file や realization file 自体の仕様・実装を確認したいときは、それぞれの正本対象を直接読む

## hash
- 355e8b768bde8e52183463c20358c52dc60d2e2b92d67db80e9d35a481b41127
