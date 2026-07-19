# `__init__.py`

## Summary
- oracle.acp_builder を acp.builder として公開する互換入口。既存の acp.builder.* 参照を維持し、canonical な basic モジュールを acp.builder.basic として利用可能にする。

## Read this when
- 既存の acp.builder.* 参照との互換性や、acp.builder.basic の公開経路を確認するとき
- acp.builder パッケージの __path__ 設定や oracle.acp_builder への委譲を変更するとき

## Do not read this when
- oracle.acp_builder の canonical な実装内容を確認したいとき
- acp.builder.* 参照の削除可否だけを判断するとき

## hash
- d6fdb57f4c932cedc07bf55090c3737b61b5ba34a5938f3126501984e040eaa5

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

# `oracle`

## Summary
- oracle command builder の realization package。oracle edit、investigation、review などの builder adapter 群への入口として機能する。
- 下位 package には、oracle edit の fork・launch_exec 経路、investigation の launch TUI adapter、review の finding 処理や canonical builder 委譲を含む。

## Read this when
- oracle command builder realization package の構成や、配下の builder adapter への入口を確認するとき。
- oracle edit、oracle investigation、oracle review の realization adapter の所在を判断するとき。

## Do not read this when
- oracle command builder の正本仕様や canonical builder 本体の実装詳細を確認するとき。
- builder adapter 以外の CLI、ACP、runtime path、具体的な編集・調査・レビュー処理を確認するとき。

## hash
- 3863319214972154659c695dafe70b7550ff4de51fccab7aff6cdb39cab699fb

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
- realization workload の builder adapter 群をまとめるパッケージ。realization apply と realization refactor の builder 連携実装への入口を提供する。
- apply 配下では apply 処理および fork 適用向け builder adapter、refactor 配下では fork 用の change summary parameter builder と file review parameter builder の公開入口を扱う。

## Read this when
- realization workload の builder adapter の責務や配置を確認・変更するとき。
- realization apply または realization refactor の fork 用 builder の公開入口・接続先を辿るとき。

## Do not read this when
- builder の共通処理や具体的な生成ロジックを直接確認・変更するとき。
- builder adapter 以外の realization workload や apply・refactor 処理を調査するとき。

## hash
- 6377b0e34b1a04f8b8b2462403fd218412cbb2fca391a75f4d8829a0640aece8

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
- oracle.acp_builder.session と互換性を保つ session package。既存の acp.builder.session.* import 経路と、join 配下の conflict resolution builder への委譲入口を扱う。

## Read this when
- acp.builder.session.* の互換 import 経路を維持・変更・削除するとき。
- oracle.acp_builder.session への移行や、互換 package を削除できる条件を確認するとき。
- session join の conflict resolution builder に関する互換経路を確認するとき。

## Do not read this when
- session の具体的な処理仕様や canonical 実装を確認したいとき。
- 互換 import の利用箇所や通常の公開 API を調査したいとき。

## hash
- f8abe886ee2d69de06c7edbe11929ce7fac0b3da0c3b4cd3cd86c173f2aa6cfd

# `tui`

## Summary
- TUI builder の互換 import 層。既存の `acp.builder.tui.*` 経路を維持するため、canonical builder の再公開と起動前準備を担う。各ファイルは互換性確認・削除判断や TUI 起動 parameter 構築の入口となる。

## Read this when
- 既存の `acp.builder.tui.*` import 互換性や互換層の削除可否を確認するとき。
- cmoc tui の起動 parameter 構築や editor input directory 準備を確認・変更するとき。
- TUI の resolve-parameter builder と FileAccessMode の再公開経路を確認するとき。

## Do not read this when
- TUI 実装本体の挙動や画面構成を確認したいとき。
- oracle 側の builder 本体や新規公開 API・import 経路を設計するとき。
- TUI 起動後の処理や TUI 以外の parameter builder を調べるとき。

## hash
- 41ec5786e69afcddd59bf54569d9584b03331498a4eca34f099cd6e0c16ae760
