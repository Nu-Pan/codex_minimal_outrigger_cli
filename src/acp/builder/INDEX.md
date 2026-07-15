# `__init__.py`

## Summary
- `acp.builder` を既存利用者に対する互換入口として読むための導線。正本の `oracle.acp_builder` を優先しつつ、`acp.builder.*` 参照を成立させるための役割と、どの公開面を維持しているかを確認したいときに読む。

## Read this when
- `acp.builder` を import したときに、正本の oracle 実装へどう接続しているかを確認したい。
- `acp.builder.basic` などの既存参照がなぜ動くのか、互換層の責務と削除条件を知りたい。
- oracle 側のモジュールを正本のまま使いながら、local wrapper がどこまで互換性を担保するかを追いたい。

## Do not read this when
- `acp.builder` の実装本体や新規機能の仕様を知りたい場合は、正本側の `oracle.acp_builder` を読む。
- 互換入口ではなく、`acp.builder.*` への依存をなくす作業をしている場合は、ここより利用箇所の整理を先に見る。
- パッケージ内部の詳細なモジュール設計や実装ロジックを確認したいだけなら、この互換ラッパではなく対象モジュール本体を読む。

## hash
- 509b6204eeeca3f085e3e26ff0c52971deabd980ea82d9d6ec634b9638cda306

# `apply`

## Summary
- `cmoc apply` 系の互換公開面をまとめて案内する入口。実処理本体ではなく、既存 import を壊さずに正本側の apply 実装へ進むためのルーティングに使う。
- `fork` 系の builder 入口と、その下で正本実装へ委譲する薄い層を含む。fork 固有の前処理や委譲先を追うときに読む。

## Read this when
- `acp.builder.apply` 配下のどの入口に進むべきか判断したいとき。
- 旧来の `cmoc apply fork` 系 import を維持しつつ、正本側へ進む経路を確認したいとき。
- fork 系 builder の前処理や委譲先を探していて、まず読む対象を絞りたいとき。

## Do not read this when
- 新しい apply 実装の正本を探したいときは、互換層ではなく `oracle/src/oracle/acp_builder/apply` 側を見る。
- この配下に実処理や仕様本体がある前提で読むべきではない。
- `cmoc apply fork` 以外のサブコマンドや別系統の公開面を追いたいとき。

## hash
- 80f80d8c070654b3303ea873951068eae266dd150f704255560d46d2ab9cd13f

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
- `quota availability probe` の互換入口。正本 builder への委譲と、配布物に正本 builder が含まれない場合の最小 probe への退避を確認したいときに読む。
- quota 確認を成立させるための後方互換だけを担当するため、正本側の probe builder の仕様や、quota polling 全体の実行制御を追う目的ではここを起点にしない。

## Read this when
- `quota availability probe` が正本 builder に委譲されるか、未配布時にどの最小 probe に落ちるかを確認したいとき。
- 配布形態ごとの互換動作を確認し、正本 builder の有無で呼び出し先を切り替える入口だけを見たいとき。

## Do not read this when
- 正本の `quota_probe` 生成仕様そのものを確認したいときは、互換入口ではなく正本側の builder を読む。
- quota polling の待機・再試行・復帰制御全体を追いたいときは、ここではなく実行制御側を読む。

## hash
- f9d221b3230b6f08444a7fc20c332d0daeef3afa8494a7fd067e99948770a81c

# `review`

## Summary
- `acp.builder.review` の互換 import 層。旧来の参照を壊さないための薄い package 初期化と、review oracle 互換エントリをまとめて案内する。
- 互換 import を維持するだけの層と、`acp.builder.review.oracle.*` から正本 oracle 実装へ進む入口を切り分けるために読む。

## Read this when
- 旧来の `acp.builder.review` 系 import の互換性や削除可否を確認したいとき。
- `acp.builder.review.oracle.*` の参照を整理して、どの呼び出し元を正本 oracle 実装へ移すべきか判断したいとき。
- この package が残されている理由や、互換層を外せる条件だけを確認したいとき.

## Do not read this when
- review oracle の実処理や変換ロジックそのものを確認したいとき。
- 新しい公開 API や利用者向け機能の仕様を追いたいとき。
- 互換 import ではなく、正本の oracle 実装仕様を直接読みたいとき。

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
