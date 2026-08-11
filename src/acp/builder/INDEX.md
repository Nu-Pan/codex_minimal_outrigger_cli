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
- feedback issue の正規化・検証に関する builder adapter をまとめるパッケージ。既存の import 経路から利用する互換層として、配下の builder 関数を参照する入口となる。

## Read this when
- feedback issue の normalization または verification に関する builder adapter の構成を確認するとき
- feedback issue 用 builder の公開 import 経路や、配下の normalize・verify adapter を追跡するとき

## Do not read this when
- feedback 以外の builder adapter を調べるとき
- builder の正本仕様や prompt 構築・起動パラメータの詳細を確認するときは、対応する oracle file を直接読む

## hash
- 08053b14ae66e2429f0bbd63341c153b782d94254b42351a90690a1191fc75fe

# `indexing`

## Summary
- 旧来の `acp.builder.indexing` 参照を維持する互換入口をまとめた層。正本実装を持たず、index 関連の builder へ既存の名前空間から到達するための下位要素を案内する。

## Read this when
- `acp.builder.indexing` から正本の index 関連機能へ進む互換経路や、旧参照の維持・削除可否を確認するとき。

## Do not read this when
- index 関連の正本実装や prompt 受け渡し仕様を変更・確認するときは、`oracle.acp_builder.indexing` 側を直接読む。
- インデックスエントリーの routing 規則や生成内容だけを確認し、互換入口を扱わないとき。

## hash
- 1c8da24f240805f39c5f79ce1ca72634f5148162f3d7ab5dfb1f822f685347df

# `oracle`

## Summary
- oracle command builder の realization package。oracle command builder 関連の各 builder adapter への入口として、oracle edit・investigation・review の実装領域を案内する。
- oracle edit は TUI 起動パラメータ生成、editor input directory の準備、oracle 側 builder 呼び出しを扱う。
- oracle investigation は launch TUI 用パラメータ生成、完全な prompt の保存先準備、正本 builder への委譲を扱う。
- oracle review は finding の列挙・統合・判定・妥当性検証用 canonical builder の再公開と、動的 prompt section の code fence 保護を扱う。

## Read this when
- oracle command builder の realization adapter の責務や構成を確認するとき。
- oracle edit、oracle investigation、oracle review の builder adapter への入口を探すとき。
- 各下位パッケージの TUI 起動パラメータ生成、正本 builder への委譲、または review finding 処理の実装へ進むとき。

## Do not read this when
- oracle 側 builder の正本仕様、prompt 内容、または本体ロジックを確認したいとき。
- oracle edit・investigation・review と無関係な builder、ACP、CLI 実装を調べるとき。
- 具体的な編集処理や review の個別 adapter 実装を確認したいときは、対応する下位パッケージを直接読む。

## hash
- 7fddd72a119b2bba3e406da45c8c366cada1b6427df197ed1b171d9e5e68364e

# `quota_probe.py`

## Summary
- 互換配布向けの quota availability probe builder。正本 builder が利用可能なら動的に委譲し、未配布時は最小の読み取り専用 probe パラメータを生成する。quota polling 用の呼び出し設定へ進む入口。

## Read this when
- quota availability probe の呼び出しパラメータ生成、正本 builder への委譲、または optional oracle builder 未同梱時の互換 fallback を確認・変更するとき。

## Do not read this when
- canonical な quota probe 仕様や builder 本体を確認したいときは、正本側の builder と oracle 仕様を直接読む。一般的な ACP パラメータ生成や他の probe の挙動を調べるときは、それぞれの実装へ進む。

## hash
- 621d28401b116690ded1c277f87c7f6e123798cd6d17286d1187c4d9d587e5be

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
