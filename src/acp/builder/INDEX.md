# `__init__.py`

## Summary
- `acp.builder` への互換入口を提供する初期化処理。`oracle.acp_builder` を正本として参照しつつ、既存の `acp.builder.*` 呼び出しを成立させる役割を持つ。

## Read this when
- `acp.builder` 配下の公開名をどう解決するか確認したいとき。
- 既存利用者向けの互換性を維持しながら、`oracle.acp_builder` 側の実装を見せる必要があるとき。
- `basic` モジュールがどこから来るか、`acp.builder` のモジュール探索順を変える必要があるとき。

## Do not read this when
- `acp.builder.*` 以外の個別実装や機能の仕様を知りたいときは、対応する下位モジュールを読む。
- 互換入口ではなく、正本側の実装そのものを確認したいときは `oracle/acp_builder` 側を読む。
- `acp.builder` の公開面そのものを変えずに内部ロジックだけを追いたいときは、この入口ではなく対象の実体モジュールを読む。

## hash
- 848ff37eb14c8145806e0a19d2da20b284094ae0063abf6c9b7b80623ac29764

# `apply`

## Summary
- `acp.builder.apply` の既存 import 互換層と、`cmoc apply fork` の realization 側 builder を含む。fork builder は正本 builder への委譲、共通の repo root・oracle import 解決、レビュー・修正および変更要約用 parameter 構築の入口を担う。

## Read this when
- `acp.builder.apply` の import 互換経路や、`cmoc apply fork` の builder 委譲・共通 parameter 構築を確認または変更するとき。

## Do not read this when
- `cmoc apply fork` のループ制御、再投入、commit、state 遷移を調べるとき。
- レビュー・修正や変更要約の prompt・schema など正本仕様を確認するときは、正本側の apply 実装を直接読む。
- fork builder と無関係なサブコマンドや import 解決を変更するとき。

## hash
- 948fba5ad80aaea8fd392250eaed0b89e8ac00688150ddabee9004588f566efd

# `common`

## Summary
- 共通ビルダー処理を置くためのディレクトリだが、現在は対象本文となる通常ファイルを含まない。

## Read this when
- 共通ビルダー処理の置き場所を確認しており、この階層に本文ファイルが追加されているかを確かめる必要があるとき。

## Do not read this when
- 既存の共通ビルダー処理の実装詳細を探しているとき。現時点ではこの対象から読める本文がないため、より直接の実装ファイルまたは下位要素へ進む。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `indexing`

## Summary
- `acp.builder.indexing` の既存参照を保つための互換入口層。索引関連の正本実装へ到達するための名前空間維持が必要なときに読む。
- `acp.builder.indexing.index_entry` の再公開層。既存の利用経路を切らさずに正本側へつなぐ必要があるときに読む。

## Read this when
- 既存の `acp.builder.indexing.*` 参照を壊さずに索引関連機能へ進む必要がある。
- 互換入口として残すべきか、削除条件を判断したい。

## Do not read this when
- 索引関連の正本実装そのものを変更したい場合は、互換入口ではなく `oracle.acp_builder.indexing` 側を読む。
- この名前空間をもう参照しない前提で整理・削除したい場合は、互換維持ではなく利用側の参照先を確認する。

## hash
- e131b4693f423253e686c3d74b6f6a880be3d8227b2da0c4f95986b6e16fc6b1

# `quota_probe.py`

## Summary
- quota availability probe 用の互換入口。任意提供される oracle builder があればそれへ委譲し、未配布時は空 stdin・最小モデル・低推論 effort・読み取り専用の最小 probe を生成する。quota polling を利用する実装や、正本 builder の配布有無に関わる呼び出し経路の確認時に読む。

## Read this when
- quota availability probe の AgentCallParameter 生成経路を確認・変更するとき
- oracle builder が存在しない配布形態での互換 fallback や quota polling の挙動を確認するとき

## Do not read this when
- 正本の probe 仕様や canonical builder の内容を確認したいときは、先に oracle 側の対応文書・実装を読む
- quota probe と無関係な AgentCallParameter builder や CLI 処理を調べるとき

## hash
- f2e851afa17cb6748655efd734212191c964231c0d9bc6cfb608523dbeb99fd9

# `review`

## Summary
- review builder 周辺の互換 import 経路をまとめるディレクトリ。旧来の package 初期化と review oracle の互換層を入口として、canonical 実装への委譲、finding 処理、パラメータ生成、移行・削除可否を確認する。

## Read this when
- review builder 周辺の import 互換性や旧来の参照を調査するとき
- review oracle の互換経路、補正、canonical 実装への橋渡しを確認するとき
- 互換 package や shim の残存理由・削除条件を判断するとき

## Do not read this when
- レビュー finding の canonical な実処理や検証ロジックだけを確認したいとき
- 互換経路と無関係な builder、oracle path 処理、別サブコマンドの実装を調べるとき
- 新しいレビュー機能や利用者向け公開 API の仕様を確認したいとき

## hash
- 1e1407221a9ce3abcda4fd9dbd7690d10ed9bcaabd4f52fd1811038aaba0be99

# `session`

## Summary
- `acp.builder.session` 互換 package の入口。ここは本体実装ではなく、旧 `acp.builder.session.*` import を維持するための境界だけを案内する。配下の `join` は、session join の互換 import とその削除条件を確認したいときだけ進む。

## Read this when
- `acp.builder.session.*` の互換 import を維持する理由や、どこまで残すかを確認したいとき。
- `acp.builder.session` から `oracle.acp_builder.session` への移行可否を判断したいとき。
- 配下の `join` 互換 package を読むべきかを判断したいとき。

## Do not read this when
- session 実装の処理内容や内部構成を確認したいとき。
- 新規機能の公開入口や通常の公開 API を探しているとき。
- `acp.builder.session.join.conflict_resolution` の具体的な本体実装を確認したいとき。

## hash
- 3c402ed48a4677b3968a008f06a24d8ad06419aad25326ad38fd3d0f43f14139

# `tui`

## Summary
- `acp.builder.tui` の既存 import 互換を保つための薄い入口群で、TUI 起動・parameter 解決の転送先と、残すべき互換層かどうかを判断するときに読む。

## Read this when
- 既存の `acp.builder.tui.*` import を維持する必要があるか、置き換えや削除が可能かを確認したい。
- TUI 起動や parameter 解決の公開経路が、どの実体へ委譲されているかを追いたい。
- 互換 package として残っている理由や、どこまでが転送層でどこからが実体かを見分けたい。

## Do not read this when
- TUI の画面構成や挙動そのものを確認したい場合は、委譲先の実体を読む。
- 新しい公開 API や新規 import 経路を設計したいだけで、既存互換層の維持可否を見ない場合は読む必要がない。
- TUI 以外のコマンドや機能の入口を調べたい場合は対象外。

## hash
- 669cddd4070305d26edfbeb549909dedff34daf16e188730e91e7d3f60d6d84c
