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
- ACP builder の動的 Markdown section を対象に、内側の backtick によって外側の code fence が誤閉鎖しないよう、canonical renderer で本文を正規化して fence 長を補正する共通処理。単一 section と review prompt 内の連続 section の実体位置特定を扱う。

## Read this when
- ACP builder の prompt 生成で、動的 section の code fence 保護や section 実体位置の特定を変更・調査するとき。

## Do not read this when
- 固定的な prompt 定義や builder 固有の section 内容だけを変更するとき。Markdown code fence の補正処理を直接扱わない場合。

## hash
- 6d72aa648c1db3dbe426fc72a1ec7b985a823e2671fa93055518cf3142638cea

# `indexing`

## Summary
- `acp.builder.indexing` 名前空間を既存利用者向けの互換入口として維持し、index 関連の正本実装へ到達するための薄いラッパー群。名前空間の互換維持が必要な場合の入口であり、正本実装そのものは扱わない。
- INDEX.md エントリー生成用の parameter とコードフェンス保護を再利用し、oracle 側 builder の機能を互換 API として公開する。既存参照の維持や互換処理を確認する際に読む対象。

## Read this when
- `acp.builder.indexing.*` という既存参照を維持したまま index 関連機能を変更・確認するとき。
- INDEX.md エントリー生成時のコードフェンス保護や oracle builder parameter の互換公開を調査するとき。
- 正本実装への互換入口の配置や参照維持の要否を判断するとき。

## Do not read this when
- INDEX.md エントリー生成の正本仕様や本体実装を確認・変更したいときは、oracle 側の対応実装を直接読む。
- index 関連のルーティング内容だけを確認したいとき。
- 互換入口を廃止・整理したいときは、この層ではなく利用側の参照先と削除条件を確認する。

## hash
- 37cee89e49545fd3915d9485ed1550137c59694ab48dee8b411c4688574b40a6

# `oracle`

## Summary
- oracle command builder の realization package。`cmoc oracle edit`、`investigation`、`review` 向け builder adapter の入口と配置領域をまとめる。
- edit は TUI 起動パラメータ生成、investigation は AgentCallParameter 生成・リポジトリ解決・editor input 準備、review は finding 関連 builder と prompt fence 保護・oracle path 補正を扱う。
- 各サブパッケージの具体的な実装や、正本 builder の仕様を確認するための下位入口となる。

## Read this when
- oracle command builder realization package の構成や責務を確認するとき
- `cmoc oracle edit`、`cmoc oracle investigation`、または `cmoc oracle review` の builder adapter の入口を探すとき
- investigation の起動パラメータ生成や editor input ディレクトリ準備の呼び出し経路を確認するとき
- review の finding 処理、prompt fence 保護、symlink 使用時の oracle path 補正を調査するとき

## Do not read this when
- 各 builder adapter の具体的な実装詳細を確認したいときは、該当サブパッケージ内の実装を直接読む
- canonical builder の正本仕様や prompt 本文を確認したいとき
- oracle command builder 以外の処理、CLI 実装、TUI 実装、共通パス解決だけを調査するとき

## hash
- b15278f90286bcb53b7b837ff3788e5671322e47082dabbef1ce2afe6dc0c4cf

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
- realization workload の builder adapter パッケージ。apply と refactor の builder 接続実装へ進む入口で、各処理の adapter 配下を案内する。

## Read this when
- realization workload の builder adapter の責務や構成を確認・変更するとき
- realization apply または realization refactor の builder 接続実装を辿るとき

## Do not read this when
- builder の共通処理や realization workload 自体の内容を直接確認・変更するとき
- apply または refactor の個別処理の実装詳細を直接調査するとき

## hash
- fef61b156f03d1ee3eff168d5115acfd08a91bee8e8529ebc94e4aff2e73ebc9

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
- `acp.builder.session` の互換 package 群を収めるディレクトリ。`oracle.acp_builder.session` との互換性を保ち、既存の import 経路を維持するための初期化・委譲入口を提供する。
- `join` 配下では、session join の競合解消パラメータ生成を canonical 実装へ委譲し、競合 path の prompt 埋め込み時の code fence 保護も扱う。

## Read this when
- `acp.builder.session.*` の import 互換性や互換 package の構成を確認するとき。
- session join の競合 path prompt 生成、または oracle 実装への移行・互換 package 削除条件を確認するとき。

## Do not read this when
- session 実装の具体的な挙動や構成要素を確認したいとき。
- canonical な session join 実装の仕様・本体を確認したいとき。
- 新規機能の入口や通常の公開 API を探しているとき。

## hash
- c5f0b718785064c435caf9962ec3862ee71d03d51e42fa397e4be1c4b0c0c6f5

# `tui`

## Summary
- TUI 向けの agent call parameter builder を旧 import 経路から利用するための互換アダプター群。起動用 builder と resolve-parameter builder を再公開し、正本 builder の結果を TUI の契約に合わせて変換する。

## Read this when
- TUI 起動時の parameter 生成や Structured Output schema path の扱いを確認・変更するとき。
- TUI の resolve-parameter builder、互換 import 経路、プロンプト内コードフェンス保護を確認・変更するとき。
- 既存の acp.builder.tui.* import と oracle.acp_builder.tui 互換層の削除可否を確認するとき。

## Do not read this when
- TUI 実装本体の挙動や画面構成を確認したいとき。
- canonical builder の仕様や実装を確認・変更するとき。
- 新しい公開 API や新規 import 経路を設計するとき。

## hash
- 5cae55527a9d5a3694f74db600627569ee745a36affcaff094f3c1a495c934e1
