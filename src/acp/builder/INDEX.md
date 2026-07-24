# `__init__.py`

## Summary
- oracle.acp_builder を acp.builder として公開する互換入口。canonical な oracle 実装を参照し、既存の acp.builder.* 参照を維持するためのパッケージ初期化と basic モジュールの公開を担う。

## Read this when
- acp.builder パッケージの互換性や公開入口を調査するとき
- acp.builder.basic の import 経路、oracle 実装との接続、既存参照の削除条件を確認するとき

## Do not read this when
- oracle.acp_builder の canonical 実装そのものを変更・調査するときは、oracle 側の対象を直接読む
- acp.builder.* の利用箇所や利用者向け公開面を調査するときは、各参照元を直接読む

## hash
- 22b403da7bbad2f49a0a9a1b257c111160e9fe04c9e5918cdffbaa8f91fcfcfb

# `apply`

## Summary
- 現時点では INDEX.md・AGENTS.md 以外のファイルや下位要素がなく、具体的な実装責務は確認できない。

## Read this when
- このディレクトリに新しいファイルや下位要素が追加され、その責務を確認する必要があるとき。

## Do not read this when
- このディレクトリ以外の apply 処理や fork 機能の実装を調べるとき。

## hash
- 478f508acec80deb9c1a94b8057621e030919b5dbb1e3b7bc0927ec773be6a7b

# `common`

## Summary
- ACP builder 間で共有する Markdown code fence 補正処理を提供するディレクトリ。動的本文に含まれるバッククォート列やセクション終了マーカーを考慮し、prompt 内の対象セクションを安全に囲むための処理が入口となる。

## Read this when
- ACP builder の prompt 生成で、動的本文に code fence やセクション終了マーカーが含まれる場合の補正処理を変更・調査するとき。
- prompt の code block 境界検出、終了マーカーの選択、fence 長の決定ロジックを確認するとき。

## Do not read this when
- ACP builder の個別 prompt 構成や正本の prompt 仕様だけを確認したいとき。
- code fence 補正を直接利用しない他領域の ACP 実装を変更するとき。

## hash
- f50a062f030f1209abf7382a0abe3809fa71f747b2405107c3879bff97d3bb70

# `indexing`

## Summary
- `acp.builder.indexing` を既存参照向けの互換入口として提供する層。正本実装への再公開と、index エントリー生成時の対象本文のコードフェンス保護を扱う。

## Read this when
- 既存の `acp.builder.indexing` 参照を維持・変更するとき
- index エントリー生成用 builder の互換ラッパーや prompt 境界を調査するとき

## Do not read this when
- 正本の index 関連実装や builder の仕様を変更・調査するとき
- 互換入口を廃止・整理し、利用側の参照先を確認するとき

## hash
- 7b4f30d341127e87b90fba42a33c5a83c98a69f61b5ab4678cc062e32593b5a4

# `oracle`

## Summary
- oracle command builder realization のパッケージ群。`oracle edit`、`oracle investigation`、`oracle review` の各 builder adapter を入口として、TUI 起動パラメータ、AgentCallParameter、finding 処理、canonical builder 委譲、互換補正などを扱う。

## Read this when
- oracle command builder realization の構成や各サブパッケージの責務を確認するとき
- `cmoc oracle edit` の TUI 起動パラメータ生成入口を調査・変更するとき
- `cmoc oracle investigation` の builder adapter、リポジトリ解決、editor input 準備、launch TUI 用 parameter 生成を調査・変更するとき
- `cmoc oracle review` の finding 処理、検証用 parameter builder、canonical builder との委譲、path・prompt 補正、互換経路を調査・変更するとき

## Do not read this when
- oracle builder の正本仕様や具体的な prompt 定義を確認するとき
- builder adapter の個別実装詳細を確認するときは、対象サブパッケージ内の実装ファイルを直接読む
- oracle command builder 以外の ACP builder、TUI 実装、共通パス解決処理を調査するとき

## hash
- bb280a914bfec6a466bc9cdff9cb69b6b8d5fdcf45ea0aa832d8500b650fd349

# `quota_probe.py`

## Summary
- オプションの正本 quota probe builder を呼び出す互換入口。正本 builder が配布されていない場合は、最小モデル・低推論・読み取り専用・空 stdin の probe parameter を生成するフォールバックを提供する。

## Read this when
- quota availability probe の parameter builder の呼び出し経路や、正本 builder 不在時の互換 fallback を確認・変更するとき。

## Do not read this when
- quota probe の正本仕様や canonical builder 自体を確認したいときは、oracle 側の quota probe 定義を直接読む。
- quota polling と無関係な ACP builder や一般的な agent call parameter の仕様を扱うとき。

## hash
- bd4ece6e70b550295d32513160360390ee1574d55e7d89eff3b0237a8da32ec0

# `realization`

## Summary
- realization workload を builder に適応するための adapter 群。realization の apply と refactor に関する builder 連携実装への入口。

## Read this when
- realization workload の builder adapter を確認・変更するとき。
- realization apply または refactor の builder 連携、関連する prompt 生成や agent call parameter 生成経路を調査するとき。

## Do not read this when
- builder の共通処理や realization workload 自体の実装を直接確認・変更するとき。
- oracle 側の正本仕様や prompt 本文、builder adapter 以外の apply・refactor 処理を確認するとき。

## hash
- c57218292a9d3126558589fd11c39955da3c3544685878a877da5bca83bb6c7c

# `review`

## Summary
- review builder の finding 判定・検証・列挙・マージに関する Python 実行時キャッシュを含むディレクトリです。対応する実装の実行痕跡を確認する入口ですが、正本仕様や編集対象の実装ではありません。

## Read this when
- review builder の finding 関連処理について、生成済み Python キャッシュの存在や内容を調査するとき。

## Do not read this when
- 正本仕様を確認するとき。
- 実装やテストを変更・レビューするとき。

## hash
- b1818f8a7aa5b2f07cbd5c874c5e933a628678b56e0cf5f597975ca387544989

# `session`

## Summary
- oracle.acp_builder.session との互換性を保つための package 群。既存の acp.builder.session.* import 経路を維持し、canonical 実装への互換入口を提供する。
- session 本体の互換初期化と、join における競合解決関連の互換 import 経路を扱う。

## Read this when
- acp.builder.session.* の import 互換性や公開面を確認するとき。
- session join の競合解決パラメータ生成や prompt 内の競合 path 処理について、旧来の import 経路から調査するとき。
- oracle.acp_builder.session 参照への移行や、互換 package を削除できる条件を確認するとき。

## Do not read this when
- session の canonical な実装内容や具体的な挙動を確認したいとき。
- 新規機能の入口や通常の公開 API を探しているとき。
- session join と無関係な builder 処理を調査するとき。

## hash
- ee79651acdf3f8b095b9fbd2c05579c47bf26bc5810a20d6bfb70f9d8f192b8c

# `tui`

## Summary
- 既存の `acp.builder.tui.*` import との互換性を維持するための TUI builder adapter package。`oracle.acp_builder.tui` の正本実装を再公開・呼び出しし、TUI 起動 parameter と resolve-parameter builder の互換入口を提供する。

## Read this when
- 既存の `acp.builder.tui.*` import 経路の互換性や削除可否を確認するとき。
- TUI 起動 parameter builder または resolve-parameter builder の互換 adapter と公開名を調査・変更するとき。
- resolve-parameter adapter における prompt のコードフェンス保護処理を確認するとき。

## Do not read this when
- TUI 実装本体の挙動や画面構成を確認したいとき。
- canonical builder の仕様・具体的な生成ロジックを確認したいとき。
- TUI と無関係な builder、prompt 生成、ACP parameter 処理を調査するとき。
- 新しい公開 API や新規 import 経路を設計するとき。

## hash
- dde6940495ab123f6aa961d878adcf222c619fe6a2845e840ca34809659ca7d5
