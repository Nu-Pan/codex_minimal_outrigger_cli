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
- `feedback` 配下の builder adapter を、feedback issue の正規化・検証に関する処理を調べる際の入口として案内する。配下には同一性判断 builder と verification builder の互換 import 経路があり、実装仕様は対応する oracle 側を確認する。

## Read this when
- feedback issue の normalization または verification に関する builder adapter の構成を確認するとき
- feedback issue builder の互換 import 経路や、対応する oracle 実装への参照関係を確認するとき

## Do not read this when
- feedback 以外の builder adapter を調べるとき
- 正規化・検証の実装ロジック、入力検証、パラメータ生成、出力仕様を確認するときは、対応する oracle file を直接読む

## hash
- 08053b14ae66e2429f0bbd63341c153b782d94254b42351a90690a1191fc75fe

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
- oracle command builder の realization package。oracle command builder 関連の下位パッケージへ進むための入口。
- `cmoc oracle edit` の builder adapter。TUI 起動パラメータ生成、リポジトリ実パス解決、editor input directory 準備、oracle 側 builder 呼び出しの確認対象。
- `cmoc oracle investigation` の builder adapter。launch TUI 用パラメータ生成、完全な prompt の保存先準備、正本 builder への委譲経路を確認する入口。
- `cmoc oracle review` の builder adapter 群。旧 import 経路から canonical 実装へ委譲される構成や、finding 処理関連の adapter 入口を確認する対象。

## Read this when
- oracle command builder の realization package の責務や下位構成を確認するとき。
- `cmoc oracle edit` の builder adapter、TUI 起動パラメータ生成、editor input directory 準備、または oracle 側 builder 呼び出し経路を確認・変更するとき。
- `cmoc oracle investigation` の launch TUI 用パラメータ生成、prompt 保存先準備、正本 builder への委譲経路を確認するとき。
- `cmoc oracle review` の realization adapter、互換 import 経路、canonical 実装への委譲関係を確認するとき。

## Do not read this when
- oracle command builder 以外の処理を確認するとき。
- oracle edit の具体的な編集処理や CLI 全体の動作を確認するときは、対象の実装ファイルまたは上位の CLI 関連ファイルを直接読む。
- oracle 側の TUI builder の prompt 内容・本体ロジック、または oracle investigation 以外の builder や ACP 実装を確認するとき。
- oracle review の正本仕様、builder 以外の CLI 実装、finding 処理の具体的な入出力や処理内容を確認するときは、canonical 実装を直接読む。

## hash
- b459b1c949fc66afcec3cf74bc8d91b3618de6a429d7d4cf2729fb48ebe66c37

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
- realization workload の builder adapter を提供するパッケージ。apply と refactor の realization builder adapter へ進む入口となる。
- apply 系 realization builder adapter を収めるパッケージ。apply fork の launch_exec パラメータ builder adapter へ進む入口となる。
- refactor 系 realization builder adapter を収めるパッケージ。refactor fork の change summary と file review and fix の builder adapter へ進む入口となる。

## Read this when
- realization workload の builder adapter の構成や、apply・refactor 配下の builder adapter を確認・変更するとき。
- realization apply fork の launch_exec パラメータ builder adapter を確認するとき。
- realization refactor fork の change summary または file review and fix の builder adapter を確認するとき。

## Do not read this when
- realization workload 自体の処理や、builder adapter 以外の実装を確認するとき。
- apply・refactor 以外の realization builder を確認するとき。
- 各 builder が再公開する oracle 側の正本実装の詳細を直接確認するとき。

## hash
- 44137963fa26bebf3953bbafcd763985a810da6cf860b3f73ff5ac7e11e7f137

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
