# `__init__.py`

## Summary
- `oracle.acp_builder` を既存の `acp.builder` 互換入口として保つための初期化モジュール。正本側の `oracle.acp_builder` を探し、利用者が `acp.builder` 経由で参照しても同じ内容に到達できるよう `__path__` と `basic` の公開を調整する。

## Read this when
- `acp.builder.*` の参照互換を維持したいとき。
- `acp.builder` から `oracle.acp_builder` の正本モジュールへつなぐ入口の振る舞いを確認したいとき。
- 互換入口の削除条件や、どの公開面を残すかを判断したいとき。

## Do not read this when
- `oracle.acp_builder` 側の正本実装そのものを変更したいときは、そちらの配下を読む。
- `acp.builder` 配下の個別機能の実装を確認したいときは、この入口ではなく各サブモジュールを読む。
- `acp.builder` 以外の公開面や別名互換の方針を確認したいとき。

## hash
- 9bc5d41f21c981a29817fa108db0069000807957797ba986d13093db0973ea61

# `apply`

## Summary
- apply 系 agent call parameter builder のうち、既存 import 互換を担う領域。正本側 apply package への互換 import 経路と、apply fork 向け builder 群の薄い realization 入口をまとめて扱う。
- apply fork 向け builder では、repo root 解決、oracle builder import 準備、oracle 側生成結果から realization 側公開型への変換、旧来 import 互換 package 境界を確認する入口になる。

## Read this when
- apply 系 ACP builder の既存 import 互換を維持または削除できるか判断したいとき。
- apply fork の変更要約、ファイル単位所見列挙、所見適用に関する agent call parameter 構築経路を確認・変更したいとき。
- apply fork の realization 側 builder が oracle 側 builder をどう呼び出し、戻り値を realization 側公開型へ適合させるか確認したいとき。
- apply fork 用 ACP builder 共通の repo root 解決、oracle src import 準備、oracle parameter 受け渡し境界を確認したいとき。

## Do not read this when
- apply の具体的な処理内容、agent prompt、出力条件、parameter 生成内容の正本仕様や人間意図を確認したい場合は、対応する oracle 側 builder を読む。
- cmoc apply fork 全体の実行フロー、fork 作成、branch 操作、diff 生成、CLI 引数処理を調べたい場合は、上位の apply fork 実装や呼び出し元を読む。
- ACP parameter のデータ構造、公開型そのもの、汎用 git helper、path model を調べたいだけなら、それぞれの共通実装や型定義を読む。
- 新規機能の実装場所を探しているだけで、既存 import 互換や apply fork 向け ACP builder に関係しない。

## hash
- 2768622529fbcc60d514e387ab4731654edde265aeef4b6856a33d44fd97035d

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
- 正本側に集約された indexing index entry builder を、旧来の公開名前空間から参照し続けるための互換入口を収める。実処理や仕様本体ではなく、既存参照を成立させる薄い転送層と、その互換経路を残す理由・削除条件の確認入口として位置づけられる。

## Read this when
- 旧来の公開名前空間から正本側の indexing 実装へ到達する互換経路を確認したいとき。
- indexing index entry builder の import 経路互換性や、既存利用者向け参照を壊さないための薄い公開面を調べるとき。
- 互換入口を削除できるか判断するために、残存参照の有無や削除条件を確認したいとき。

## Do not read this when
- indexing の具体的な生成処理、探索処理、データ構造、入出力仕様を確認したいとき。実体を持つ正本側の実装を読む。
- builder 本体の実装、引数構築ロジック、新規機能追加、index entry 生成仕様そのものを調べたいとき。再公開先または実装側を読む。
- 単にパッケージ配下の通常モジュール構成や汎用的な import 規約を調べたいとき。

## hash
- 5ebe4d8f1b0167397eca53308c9fa3bff675bed78057d79508ec00483933f9c1

# `quota_probe.py`

## Summary
- `build_quota_availability_probe_parameter` を再利用する互換アダプタ。呼び出し側がこの公開関数を使っており、実体は正本側の quota probe 構築へ委譲されることだけを確認したいときに読む。

## Read this when
- quota availability probe の引数生成経路をたどりたいとき
- この公開関数がどこへ委譲するか、また遅延 import を含む互換維持の理由を確認したいとき

## Do not read this when
- canonical な prompt や call settings の正本を確認したいときは、`<work-root>/oracle/src/oracle/acp_builder/quota_probe.py` を読む
- quota probe 以外の ACP builder 群の分岐や実装方針を追いたいときは、より直接の実装側を読む

## hash
- 3f7514ef51853e259d4a0bd798493cc4a16259f271db9ab7157db55bbf2d9520

# `review`

## Summary
- review builder 配下で、旧 import 経路を維持する互換 package 初期化と review oracle 向け互換 adapter 群を束ねる階層。
- 実処理は主に canonical oracle path や oracle src 側へ委譲され、この階層は移行中 caller との互換性、削除条件、正本 builder 由来 prompt の限定補正境界を確認する入口になる。

## Read this when
- review builder 周辺の旧 import 互換性や、古い acp.builder.review 系参照を削除できるか確認する。
- review oracle の旧 import 経路から canonical oracle path への移行状況、互換 shim の再 export 対象、または削除可否を確認する。
- merge finding や validate finding advocate の agent call parameter について、正本 builder 取得後に realization 側で補正される範囲と削除条件を確認する。

## Do not read this when
- review builder の実処理、変換ロジック、finding enumeration、judgment、challenger validation の parameter 構築を調べたい場合は、より直接の実装先を読む。
- review oracle の正本仕様や正本 prompt の内容そのものを確認したい場合は、oracle 側の該当本文を読む。
- review oracle 以外の builder、agent call parameter 全般、path model、INDEX.md エントリー生成、または一般的な oracle file 定義を調べたい場合。

## hash
- 8c0170ecf4d16e76f4eabb38112c44d157461f19eb65650a549149278abf7611

# `session`

## Summary
- session builder 配下の旧 acp.builder 系 import path 互換を扱う領域。session 本体の挙動ではなく、既存参照を canonical oracle 実装または互換入口へ中継する薄い公開面維持層をまとめる。

## Read this when
- acp.builder.session.* の旧 import path 互換がどの入口や canonical 実装へつながるかを確認したいとき。
- session builder 配下の互換 package や再公開モジュールを残す理由、公開面維持、削除条件を調べたいとき。
- session join builder の旧公開元や互換経路を追跡しているとき。

## Do not read this when
- session 実装の具体的な挙動、制御フロー、builder 呼び出し順を確認したいとき。
- conflict resolution parameter builder など canonical oracle 実装側の内容や仕様根拠を確認したいとき。
- 互換 import の実際の利用箇所や、利用者向け公開面から参照がなくなったかを判断したいとき。
- 新規機能の入口や通常の公開 API を探しているとき。

## hash
- d636121a29a1f6f7a6d22e0e3a8ad6b3f97e18b5065aec22c899dbab39d5d021

# `tui`

## Summary
- TUI 起動・resolve parameter builder について、旧 `acp.builder.tui.*` import surface を維持するための realization 側互換層を扱うディレクトリ。
- oracle 側 canonical builder を呼び出しまたは再公開しつつ、TUI runtime で必要な最小の補助処理や既存公開名の維持を担う。

## Read this when
- 既存 import 経路 `acp.builder.tui.*` の互換維持、公開名、削除可否を確認するとき。
- TUI 起動用または resolve 用の parameter builder を realization 側から利用する入口を確認するとき。
- oracle 側 builder と realization 側互換 wrapper の関係、または TUI 起動前に保証される runtime 側 directory の責務を確認するとき。

## Do not read this when
- AgentCallParameter や TUI parameter builder の正本仕様を確認したい場合は、oracle 側の canonical builder を読む。
- TUI 画面構成、CLI サブコマンド全体、runtime path 全般、logs directory 構成を調べたい場合は、それぞれを扱う対象を読む。
- 新しい公開 API や新規 import 経路を設計したいだけで、既存互換 import surface の維持や移行に関係しない場合。

## hash
- 6d462fda219bbdc61a8fa9fb6b8d497d66e925f893607def2c4864a23c271fb6
