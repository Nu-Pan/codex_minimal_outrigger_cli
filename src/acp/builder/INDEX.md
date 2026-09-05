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
- ACP builder 間で共有する、プロンプト内の Markdown code fence を補正する処理の配置先。
- レビュー用セクションを検出し、構造化ドキュメントとして再描画した本文に含まれるバッククォートと外側の code fence が衝突しないよう調整する。
- 個別の builder 機能ではなく、複数の builder から共通利用されるプロンプト整形処理を確認するときの入口。

## Read this when
- ACP builder のプロンプト生成で Markdown code fence の保護や再描画が必要なとき
- レビュー用セクションの位置検出、セクション単位の code fence 補正、構造化ドキュメントの Markdown 化を調査するとき
- 個別 builder の処理ではなく、builder 共通のプロンプト整形ロジックを確認するとき

## Do not read this when
- 特定の oracle、realization、session、feedback などの個別 builder の責務や入出力を調査するとき
- プロンプト整形を利用する呼び出し元の業務ロジックを確認するとき
- 正本となる構造化ドキュメント描画処理そのものを調査するときは、その正本実装を直接読む

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `feedback`

## Summary
- feedback builder adapter 群の公開入口。issue の同一性判断と remediation 用の oracle builder へ進むための上位入口。
- 構造化 observation と既存候補を比較し、feedback issue が既存か新規かだけを判断する builder の互換 import 経路。
- 正規化済み feedback issue の存在確認、realization 修正、検証、結果分類を行う remediation builder の互換 import 経路。

## Read this when
- feedback builder adapter の公開範囲や、normalization と remediation の下位入口を確認するとき
- feedback issue の同一性判断 builder を呼び出す import 経路を確認するとき
- 正規化済み issue の remediation builder を呼び出す import 経路や、修正・検証処理への入口を確認するとき

## Do not read this when
- issue の同一性判断基準、入力制約、Structured Output 後条件などの実装仕様を確認したいときは対応する oracle の normalize_issue 実装を直接読む
- issue remediation の修正対象、結果分類、差分記録、検証規則などの実装仕様を確認したいときは対応する oracle の remediate_issue 実装を直接読む
- feedback issue 以外の builder や、builder adapter と無関係な一般処理を調べるとき

## hash
- 1529291db1b39121475004620e5b9bdf14e83d05abc08e4f8a0b4bbb4099ee9e

# `indexing`

## Summary
- `acp.builder.indexing` 名前空間から `oracle.acp_builder.indexing` の正本実装へ到達するための互換入口を扱う。`__init__.py` は名前空間の互換参照を、`index_entry.py` は index-entry パラメータ生成機能の再公開を担う。

## Read this when
- 既存の `acp.builder.indexing` 参照を維持する必要がある。
- 互換入口の配置、公開内容、または削除条件を確認したい。
- index-entry 生成機能を旧参照経由で利用する箇所を調査する。

## Do not read this when
- index 関連機能の正本実装や実装詳細を変更・確認したい場合は、`oracle.acp_builder.indexing` を直接読む。
- 互換入口を整理・削除する場合に、利用側の参照状況を確認する必要がない。

## hash
- 6699de11a8d3a0077b3875e46c010702c3e464b5be0a6809df05f24a3dc28744

# `oracle`

## Summary
- oracle command builder の realization package。oracle command builder 関連のパッケージ入口として機能する。

## Read this when
- oracle command builder の realization package の責務や構成を確認するとき。
- oracle edit または oracle investigation の builder adapter へ進む入口を確認するとき。

## Do not read this when
- oracle command builder 以外の処理を確認するとき。
- oracle edit の具体的な編集処理や CLI 全体の挙動を確認するときは、実装ファイルまたは上位の CLI 関連ファイルを直接読む。
- oracle investigation の具体的な調査処理や正本 builder の仕様・挙動を確認するときは、oracle 側の実装を直接読む。

## hash
- 58c688dd7c1093d31b2606ce40f37a3ab07a5ffb88e26aa47c77e1f3045fa02c

# `quota_probe.py`

## Summary
- quota availability probe の canonical builder への互換入口。既存 caller 向けの公開関数を提供し、probe 用の cwd を正本 builder に渡す。

## Read this when
- 既存の acp.builder.quota_probe 参照を維持・変更する必要があるとき。
- quota availability probe の builder 呼び出し経路や互換 API を確認するとき。

## Do not read this when
- canonical な probe builder の実装詳細を確認したいときは、正本の oracle 側実装を直接読む。
- quota availability probe と無関係な agent call parameter の処理を確認するとき。

## hash
- ef2ca178df616e11ad6d6428a93aec32c490ee1f992d5f23e4033f63ba34410f

# `realization`

## Summary
- realization workload を builder に適応する adapter 群を収めるディレクトリ。apply と refactor の処理別 builder adapter へ進む入口であり、配下の個別 adapter の詳細確認にも利用する。

## Read this when
- realization workload と builder の接続構成を確認・変更するとき
- realization の apply または refactor に関する builder adapter の入口を探すとき
- 配下の処理別 adapter や fork 用 adapter を辿るとき

## Do not read this when
- builder の共通処理や realization workload 自体を直接確認・変更するとき
- apply または refactor 以外の処理を調査するとき
- 個別 adapter の詳細実装を直接確認したいときは、対応する配下の対象へ進むとき

## hash
- b6b5442168a00f913a279c84098fbac73c406e61aa0172dcc352a7aa655ac1c2

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
- 既存の acp.builder.session.* import との互換性を維持するための package 群。session join の conflict resolution は canonical 実装へ委譲され、通常の session 実装そのものではなく互換参照の入口を提供する。

## Read this when
- 既存の acp.builder.session.* import を維持する理由を確認するとき。
- session join の conflict resolution が canonical 実装へ委譲される関係や、互換 package を削除・移行できる条件を調査するとき。

## Do not read this when
- session 実装の仕様、挙動、構成要素を確認したいとき。
- 新規機能の入口や通常の公開 API を探しているとき。
- 互換 import の具体的な利用箇所を調べたいときは、参照元を直接検索する。

## hash
- 8ac1297baa09ab5371a5d3fca45654e17e3211a70bd9f136e13a2b25ffa208e5

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
