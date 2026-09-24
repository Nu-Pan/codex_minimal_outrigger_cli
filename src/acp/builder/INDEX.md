# `__init__.py`

## Summary
- `acp.builder` を `oracle.acp_builder` の互換 import 名前空間として整え、`basic` を同一モジュールとして再公開するパッケージ入口です。
- 個別 builder の処理は定義せず、ローカルの互換モジュールと oracle 側の submodule を同じ import 経路にまとめます。

## Read this when
- 既存の `acp.builder.*` import 経路を維持する理由や撤去条件、名前空間全体の探索・再公開を変更するとき。
- `acp.builder.basic` の参照同一性や oracle 側 submodule の利用可能性など、パッケージ共通の import 動作を追うとき。

## Do not read this when
- 特定 builder の機能や生成内容を確認・変更するときは、対応する `oracle.acp_builder` の実装を直接読む。
- 特定の旧 import 用 adapter の公開内容や互換挙動を確認・変更するときは、その個別 adapter を直接読む。

## hash
- 22b403da7bbad2f49a0a9a1b257c111160e9fe04c9e5918cdffbaa8f91fcfcfb

# `apply`

## Summary
- この領域には現在 builder の実装がなく、`cmoc realization apply fork` の prompt と起動パラメータは realization apply の builder とその正本に定義されています。

## Read this when
- builder 内で apply 関連実装の所在や、この領域に追跡対象の実装があるかを確認するとき。

## Do not read this when
- apply fork の prompt や commit 範囲の扱い、起動パラメータを確認・変更するときは、現行の realization apply builder とその正本を直接参照してください。

## hash
- 478f508acec80deb9c1a94b8057621e030919b5dbb1e3b7bc0927ec773be6a7b

# `common`

## Summary
- realization ACP builder で共有する、動的なプロンプト本文が Markdown の code fence を誤って閉じないようにする補正処理を担います。
- 現状はコンパイル済みコードのみで、保守対象のソース実装はありません。

## Read this when
- 動的な本文によって code fence が意図せず閉じる問題を調べ、残存する共有補正コードの挙動を確認するとき。

## Do not read this when
- プロンプトの文言や工程固有の構成だけを調べるとき。補正実装を編集するときは、管理対象のソース実装を探して直接読んでください。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `feedback`

## Summary
- feedback issue の同一性判断と remediation に使う builder parameter について、oracle 側の定義を `acp.builder` 配下から利用する互換 import 経路を提供する。
- 同一性判断用 builder と、正規化済み issue 1 件の確認・修正・検証用 builder が対象。実際の構築内容は oracle 側に定義されている。

## Read this when
- feedback observation と既存 issue 候補の同一性判断に使う builder の import 経路を確認・変更するとき。
- 正規化済み feedback issue の確認・修正・検証に使う builder の import 経路を確認・変更するとき。

## Do not read this when
- prompt の内容や parameter 構築、作業範囲など builder の実際の挙動を調べたり変更したりするとき。対応する oracle 側の定義を直接読む。
- session、indexing、apply など、feedback issue の同一性判断・remediation 用 builder に関係しない作業をするとき。

## hash
- 1529291db1b39121475004620e5b9bdf14e83d05abc08e4f8a0b4bbb4099ee9e

# `indexing`

## Summary
- 既存の `acp.builder.indexing.*` 参照を保つため、正本側の indexing 機能を公開する互換入口です。
- 目次エントリー生成用パラメータの実装は正本側へ委譲しています。

## Read this when
- 既存利用者向けの `acp.builder.indexing` 互換公開面を保守するとき。
- この互換参照が引き続き必要か、利用箇所を確認するとき。

## Do not read this when
- 目次エントリー生成の指示や起動パラメータを変更するときは、実装を担う正本側の builder を確認してください。
- 生成する目次エントリーの要件を調べるときは、目次機能のアプリケーション仕様を確認してください。

## hash
- 6699de11a8d3a0077b3875e46c010702c3e464b5be0a6809df05f24a3dc28744

# `oracle`

## Summary
- `cmoc oracle` の investigation TUI builder と edit exec builder について、既存の import 経路を保ちながら正本 builder の関数を再公開する realization adapter 群です。正本 builder の処理本体ではなく、互換 import の接点を確認する入口です。

## Read this when
- `cmoc oracle investigation` の TUI builder について、互換 import やその呼び出し元を調べる・変更するとき。
- `cmoc oracle edit` の exec builder について、互換 import やその呼び出し元を調べる・変更するとき。

## Do not read this when
- builder の処理本体を調べる・変更するときは、正本 builder の実装を直接確認してください。
- 別の oracle コマンドの builder や、コマンドの振り分け処理を調べるときは、それぞれの担当箇所から確認してください。

## hash
- 2810fa78b0739f3864455e80717a1b762d7f0c9a0cf5ef71f9138eca71a1ee31

# `quota_probe.py`

## Summary
- 既存 runtime が使う quota availability probe の互換 API で、受け取った既存パラメーターの cwd を正本 builder へ渡します。

## Read this when
- quota probe の既存呼び出し口や、呼び出し元から cwd を引き継ぐ互換経路を調べる・変更する場合。

## Do not read this when
- probe の prompt や起動設定を調べる・変更する場合は、正本 builder の実装を直接確認してください。
- quota 回復の成功条件や待機・再開の判断を調べる場合は、その回復規則を定める仕様や runtime の処理を確認してください。

## hash
- ef2ca178df616e11ad6d6428a93aec32c490ee1f992d5f23e4033f63ba34410f

# `realization`

## Summary
- realization の apply/refactor 系 builder を従来の import 経路から公開する互換 adapter 群です。処理本体は oracle 側の builder に委譲します。
- apply は commit 範囲に基づく realization 反映処理の起動を、refactor は変更要約とファイル単位のレビュー・修正を扱います。

## Read this when
- realization の apply または refactor の builder adapter が担う範囲を確認・変更するとき。
- commit 範囲からの realization 反映、変更要約、またはファイル単位のレビュー・修正に対応する import 入口を調べるとき。

## Do not read this when
- builder が prompt や起動パラメータを実際に組み立てる方法を確認・変更するときは、oracle 側の対応する builder を直接読む。
- apply/refactor の CLI 実行や全体の処理順序を調べるときは、builder adapter ではなく実行を担う対象から確認する。

## hash
- b6b5442168a00f913a279c84098fbac73c406e61aa0172dcc352a7aa655ac1c2

# `review`

## Summary
- この場所にはレビュー処理を定義するソースや設定がなく、レビュー挙動を調べる実装の入口にはなりません。

## Read this when
- この場所にレビュー実装が置かれているか確認するとき。

## Do not read this when
- レビュー処理の挙動を理解または変更するときは、実装ソースと対応するテストを直接確認してください。

## hash
- b1818f8a7aa5b2f07cbd5c874c5e933a628678b56e0cf5f597975ca387544989

# `session`

## Summary
- 既存の session builder import 経路を維持する互換 package 群で、conflict 解消用 parameter builder の参照を正本実装へ中継する。

## Read this when
- 旧 session builder import の互換性や、この経路を維持する必要性を調べる・変更するとき。
- 旧 import 経路から conflict 解消用 parameter builder へつながる参照を確認するとき。

## Do not read this when
- conflict 解消用 prompt や起動 parameter の挙動を調べる・変更するときは、正本実装から始める。
- session join の merge 手順や conflict 解消後の処理を調べる・変更するときは、command 実装から始める。

## hash
- 8ac1297baa09ab5371a5d3fca45654e17e3211a70bd9f136e13a2b25ffa208e5

# `tui`

## Summary
- `cmoc tui` の起動パラメータ builder を、既存の realization 側 import 経路から利用できるようにする互換層。
- 公開名を oracle 側の builder に委譲し、パラメータ構築の処理本体は担わない。

## Read this when
- 既存の import 経路を維持・変更する必要性や、その利用箇所を調べるとき。
- builder の再エクスポートが利用側に与える影響を確認するとき。

## Do not read this when
- プロンプト内容や起動パラメータの構築挙動を変更・確認するときは、oracle 側の実装を直接読む。
- 入力編集から TUI 起動までの CLI フローを追うときは、サブコマンド本体を直接読む。

## hash
- 8b5e533d0629fa51629b23b240cec1b19c41b3772b23e0449961cf4be62f8082
