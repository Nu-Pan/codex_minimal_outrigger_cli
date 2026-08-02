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
- oracle command builder の realization adapter 群をまとめたパッケージ。`cmoc oracle edit`、`investigation`、`review` 各コマンドの起動パラメータ生成や builder adapter への入口を提供する。
- 下位項目では、コマンド別の TUI 起動処理、AgentCallParameter 生成、finding 関連レビュー処理などの実装領域へ進める。

## Read this when
- oracle command builder の realization package の責務や下位構成を確認するとき。
- `cmoc oracle edit`、`investigation`、`review` の builder adapter の入口や呼び出し経路を調査・変更するとき。
- 各 oracle command の下位 builder 実装へ進む対象を選ぶとき。

## Do not read this when
- oracle command の正本仕様や canonical builder の prompt 本文を確認したいとき。
- builder adapter 以外の CLI、TUI、共通パス解決処理を調査するとき。
- 特定コマンドの具体的な実装詳細を確認したいときは、対応する下位項目を直接読む。

## hash
- 884ba366cb3af7b4c8a69c6b405ad80d04a1e72822eb20ebc4d3f178b1680658

# `quota_probe.py`

## Summary
- quota availability probe の互換入口。canonical な oracle builder が利用可能な場合は委譲し、未配布時は最小構成の読み取り専用 probe パラメータを生成する。

## Read this when
- quota availability probe の builder 呼び出し経路、oracle builder への委譲、または optional distribution 向け fallback を確認・変更するとき。

## Do not read this when
- canonical な quota probe の正本仕様や builder 自体の実装を確認したいとき。oracle 側の quota probe 定義を直接読むこと。

## hash
- 53cb131c3313e1f5578fcb289b0afa963a2ba5e0a184345ede301eb26faf67fd

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
- session 関連の互換 import 経路を提供する realization package。session 初期化と join 配下の canonical 実装への接続・旧 import 維持を扱う下位要素への入口。

## Read this when
- acp.builder.session.* の互換 import 経路や公開面を確認・変更するとき。
- session join に関する互換経路や、競合解決パラメータ生成への接続を確認するとき。

## Do not read this when
- session の具体的な実装挙動や構成要素を確認したい場合。
- canonical 実装そのものや、互換 package の参照元を調査する場合。

## hash
- e7357a6d7de42b0fb8253544f1d8069f2495ebe105125df1b044135c21268d74

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
