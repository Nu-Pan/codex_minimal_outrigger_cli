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

# `feedback`

## Summary
- feedback normalization 用の builder adapter をまとめるディレクトリ。feedback builder の公開入口と、対応する oracle 実装へのルーティングを担う。

## Read this when
- feedback issue の正規化パラメータ builder の公開入口や参照先を確認するとき。
- feedback builder 経由で正規化処理を利用する箇所を調査するとき。

## Do not read this when
- feedback normalization 以外の builder 実装を調べるとき。
- 正規化 builder の具体的な実装や仕様を確認するときは、対応する oracle file を直接読む。

## hash
- e07cc95b5d6752cc55467387169ba8d8b4b61e0eb4f5f73f66071a7ed17e3e1b

# `indexing`

## Summary
- acp.builder.indexing 名前空間を既存の参照点として維持し、正本側の index 関連実装へ委譲する互換入口を提供するディレクトリ。名前空間の互換維持と、対象本文を組み込む AgentCallParameter 生成を扱う。

## Read this when
- 既存の acp.builder.indexing 参照を壊さずに index 関連機能へ到達させる必要があるとき。
- index_entry の正本 builder への委譲や、対象本文をプロンプトへ埋め込む際のコードフェンス保護を確認・変更するとき。

## Do not read this when
- index 関連の正本実装やプロンプト構築仕様そのものを変更・確認するときは、正本側の対応ファイルを直接読む。
- この互換名前空間を廃止・整理する場合は、まず利用側の参照先と互換維持の要否を確認する。

## hash
- 07317faa574f6c7bf9fbe3c1147a482510b656f8e8645c62791424988aa92c1e

# `oracle`

## Summary
- oracle command builder の realization package。`cmoc oracle` 配下の各 command builder adapter への入口をまとめ、正本 builder への委譲経路や TUI 起動パラメータ生成を扱う。
- oracle edit、oracle investigation、oracle review の用途別 adapter が下位要素として配置されている。

## Read this when
- oracle command builder realization package の責務や構成を確認するとき。
- `cmoc oracle edit`、`cmoc oracle investigation`、`cmoc oracle review` の builder adapter への入口を選ぶとき。
- 各 command の TUI 起動パラメータ生成、正本 builder への委譲、review finding 関連処理の経路を調べるとき。

## Do not read this when
- oracle 側の canonical builder の仕様、prompt 本文、モデル設定を直接確認したいとき。
- oracle command builder 以外の CLI、ACP、実行時処理を調べるとき。
- 特定 command の具体的な実装詳細を確認する場合は、該当する下位 adapter を直接読むとき。

## hash
- 18463836dc75b25542916f55c623ac06e143062987b60b6ecef88fe360837c5f

# `quota_probe.py`

## Summary
- quota availability probe の互換 builder。利用可能な正本 builder を委譲先として解決し、optional oracle builder がない配布形態では、最小モデル・低推論・読み取り専用・空 stdin の quota polling 用パラメータを生成する。

## Read this when
- quota availability probe の呼び出し経路、正本 builder への委譲、または oracle builder 未配布時の互換 fallback を確認するとき。

## Do not read this when
- quota probe の正本仕様や canonical builder の詳細を確認したいとき。oracle 側の該当実装・仕様を直接読むこと。
- quota polling 以外の ACP builder や一般的な AgentCallParameter の仕様を確認するとき。各担当領域の直接の実装・仕様へ進むこと。

## hash
- 6de081322a7c345a77160cd3f575b27f994fe305aea137e57709bc44fde31ab3

# `realization`

## Summary
- realization の各処理（apply・refactor）における builder adapter を収めるパッケージ。処理別 builder 接続点や fork 用 adapter の入口として、下位の builder 実装を辿る起点となる。

## Read this when
- realization apply または refactor の builder adapter の責務・配置・接続を確認または変更するとき。
- apply fork や refactor fork における builder adapter の連携箇所を調査するとき。

## Do not read this when
- builder の共通処理、正本 builder の仕様、prompt fence 共通処理を直接確認または変更するとき。
- realization apply・refactor の処理本体や builder adapter の詳細実装を直接調査するとき。

## hash
- fc9a68f6e5f27c8919d8df67a03008e24d0d9a45ec0c1d88428e2b2b21ceace6

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
- 既存の `acp.builder.session.*` import 互換性を維持するための session package。初期化入口と、canonical な session join 競合解決実装への互換アダプターを含む。
- session join の互換 import 経路、競合解決 parameter のラッパー、競合 path の prompt 埋め込み、code block fence 保護を確認するための入口。

## Read this when
- 既存の `acp.builder.session.*` import 経路や互換 package の公開面を調査・変更するとき。
- session join の競合解決互換ラッパーや canonical 実装との対応関係を確認するとき。
- 互換 package を削除または oracle 側実装へ移行できる条件を検討するとき。

## Do not read this when
- session join の具体的な処理内容や canonical な競合解決仕様を確認したいとき。
- session 実装の通常の挙動や構成要素、新規機能の入口を調査するとき。
- 互換 import の利用箇所や利用者向け API から参照が残っているかを確認したいとき。

## hash
- 7db33cfd6e9f321d2d2a5d79c5f69777fe5ac95f0ba1cd67f0d3d4df2a7aee6f

# `tui`

## Summary
- TUI 起動 builder の既存 import 経路を維持する互換 package。実装本体への入口ではなく、不要になった場合に削除を検討する対象。
- TUI 起動 parameter builder を既存の互換 import 経路から再公開するモジュール。実体は oracle 側の TUI 起動定義にあり、利用箇所からその定義へ進む入口。

## Read this when
- TUI 起動 builder の既存 import 経路や互換性を確認するとき
- 互換 import の解決先や、その経路を削除・変更できるか判断するとき

## Do not read this when
- TUI 起動 parameter の生成ロジックや起動処理そのものを調査・変更するとき
- TUI 以外の ACP builder、共通 parameter builder 仕様、または互換性に関係しない処理を扱うとき

## hash
- 8b5e533d0629fa51629b23b240cec1b19c41b3772b23e0449961cf4be62f8082
