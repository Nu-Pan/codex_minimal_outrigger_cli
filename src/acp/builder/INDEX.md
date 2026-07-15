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
- `oracle.acp_builder.quota_probe` が配布されない環境でも quota availability probe を成立させる互換入口を扱う。正本 builder への委譲と、未配布時に返す最小 probe の分岐を確認したいときに読む。
- `AgentCallParameter` を受けて probe 用パラメータへ変換する責務を持つ。呼び出し元の cwd を維持しつつ、代替経路の存在条件やフォールバック内容を見たいときに読む。

## Read this when
- quota availability probe の互換動作や fallback の有無を確認したい。
- optional な oracle 側 builder が無い配布形態でも動くべきかを判断したい。
- probe の既定値が最小構成になっている理由を知りたい。

## Do not read this when
- quota probe の本来の仕様や Codex 呼び出し規約そのものを確認したい場合は、正本側の builder か oracle/doc/app_spec/codex_exec_rule.md を読む。
- acp builder 全体の別機能を探しているだけなら、この互換入口ではなく該当 builder を直接読む。

## hash
- 102d844da2e0449cf34e4eb8c6dc71fd44068a7d8df835340a7b349dad321a42

# `review`

## Summary
- `__init__.py` は review builder 系の互換 import だけを支える入口。旧 `acp.builder.review` 参照を残す必要があるか、あるいは互換層を削除できるかを判断するときに読む。
- `oracle` は review builder の互換 shim と正本 oracle への橋渡しをまとめた入口。旧 import 経路の維持可否と、review finding の生成・判定・擁護・反証のどの入口に進むべきかを切り分けるときに読む。

## Read this when
- `__init__.py` の互換 import を確認する。
- `__init__.py` を含む review builder 周辺の古い参照を削除できるか判断する。
- `oracle` 配下で旧い import 経路の互換維持条件や削除可否を確認する。
- `oracle` 配下で review finding の所見生成、判定、擁護、反証のどの入口に進むべきか切り分ける。
- `oracle` 配下の symlink 経由の path 表示や既知の互換修正の位置を確認する。

## Do not read this when
- `__init__.py` で review builder の実処理や変換ロジックを調べたい。
- `__init__.py` で新しい公開 API や利用者向け機能の仕様を確認したい。
- `__init__.py` と無関係な builder 実装を変更したい。
- `oracle` で新しい review 機能全体の設計や、oracle 以外の builder 群を探したい。
- `oracle` で互換 shim ではなく正本の review oracle 本体だけを直接追いたい。
- `oracle` 配下の薄い入口ではなく、実装本体の詳細ロジックを確認したい。

## hash
- dcb356d75e263d93bc452e01a1ba25f2a2d653e27cda46185b96b1a1e25f3077

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
