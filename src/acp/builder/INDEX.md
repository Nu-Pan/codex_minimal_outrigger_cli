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
- ACP builder で共有する Markdown code fence の補正処理を提供する。動的な section 本文内のバッククォート列に応じて外側 fence を調整し、Markdown code block が途中で閉じないようにする。canonical rendering 後の code block 本文取得も扱う。

## Read this when
- ACP builder の prompt 生成で、動的本文を含む Markdown code block の fence 補正を変更・調査するとき
- section heading、終了 marker、info string、section body に基づく補正対象の探索や置換処理を確認するとき
- Markdown rendering の normalization や struct_doc 連携を確認するとき

## Do not read this when
- 個別 prompt の内容や正本の prompt 仕様を確認するとき
- Markdown code fence 補正と無関係な ACP builder 機能、CLI 挙動、一般的な Markdown 処理を調査するとき

## hash
- 91e56654c60ea2e30e699706e914facc1a2a66fe556c98213383f2974a3d3dee

# `indexing`

## Summary
- `acp.builder.indexing` を既存参照向けの互換入口として提供する層。名前空間は正本実装への到達点を維持し、`index_entry.py` は正本 builder を再公開しつつ、対象本文中のコードフェンスを prompt 内で保護する。

## Read this when
- `acp.builder.indexing.*` の既存参照を維持・移行する必要があるとき。
- index entry builder の互換ラッパー、正本実装の再公開、または prompt 内のコードフェンス保護を調査・変更するとき。

## Do not read this when
- index 関連の正本実装や parameter 構築内容を変更・確認するときは、`oracle.acp_builder.indexing` 側を直接読む。
- この互換入口を削除・整理するときは、まず利用側の参照先と互換維持の要否を確認する。
- index entry 生成と無関係な ACP builder や一般的な prompt 処理を調査するとき。

## hash
- 304258abfed8bce7fcc86a1480d1f4253634cd0ef88d3c3443da69ea8b654713

# `oracle`

## Summary
- oracle command builder の realization adapter 群をまとめるディレクトリ。oracle edit、investigation、review 向けの builder 入口と、各種 AgentCallParameter・TUI 起動パラメータ生成への導線を提供する。

## Read this when
- oracle command builder の realization adapter の構成や、edit・investigation・review builder の入口を確認するとき
- oracle investigation の起動準備や、oracle review の builder・互換経路・prompt 埋め込み処理へ進むとき

## Do not read this when
- canonical builder の正本仕様や prompt 本文を確認したいとき
- builder adapter 以外の CLI 実装、TUI 実装、または共通パス解決処理だけを調査するとき

## hash
- f4a89e1b23e4206396587fa4bb5b96fd9d63f337d5401ffc13f24e81fa96300f

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
- realization workload を builder に適応する adapter 群。apply と refactor の builder 連携実装への入口で、各処理の fork 用 adapter を下位要素として含む。

## Read this when
- realization workload の builder adapter の責務や実装入口を確認・変更するとき。
- realization apply または realization refactor の fork 処理で、builder 接続や parameter・prompt 生成を調査するとき。

## Do not read this when
- builder の共通処理や正本 builder の仕様・実装を直接確認するとき。
- apply や refactor の処理本体、builder adapter 以外の実装を調査するとき。

## hash
- dd4d54b809f769edf6dc38155aee0e327e295ecaeb688abf622a8d82f0884d19

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
- `acp.builder.session` の旧来 import 経路を維持する互換用 package。`oracle.acp_builder.session` の canonical 実装へ接続する初期化・互換入口を提供する。

## Read this when
- `acp.builder.session.*` の import 互換性や旧来の公開経路を確認するとき。
- session join の互換入口や、canonical 実装との対応関係を確認するとき。

## Do not read this when
- session の具体的な処理仕様や canonical 実装の挙動を確認したいとき。
- 互換 import の利用箇所や、互換 package を削除できる条件を調査したいとき。

## hash
- f10f062b0a846084dc1e828f0e1ce69b87f0925c508b6d96f8368cd3f469a547

# `tui`

## Summary
- TUI 関連の互換 import 経路を提供する薄い builder package。既存の `acp.builder.tui.*` 参照を維持し、canonical な oracle 側実装を再公開する入口として機能する。
- 起動 parameter builder と resolve-parameter builder の互換アダプターを含む。resolve-parameter では入力プロンプト内のコードフェンスを保護した `AgentCallParameter` を返す。

## Read this when
- 既存の TUI builder import 経路や互換性を確認・変更するとき。
- TUI 起動 parameter builder または resolve-parameter builder の公開入口を調査するとき。
- 互換 package を削除できる条件や、canonical builder との責務分担を確認するとき。

## Do not read this when
- TUI の画面構成や実装本体の挙動を調査するとき。
- canonical builder の仕様や生成ロジックを確認するときは、oracle 側の実装を直接読む。
- 新しい公開 API や新規 import 経路を設計するとき。

## hash
- 801321d9f63ed206ef16d23682e512d09bcea697d6428f92eebb693b2d4048df
