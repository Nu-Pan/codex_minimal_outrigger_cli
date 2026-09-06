# `acp`

## Summary
- acp 互換の公開入口を扱い、既存の acp.* 参照を oracle.* または実体モジュールへ移行する際の入口となる。
- acp.builder 配下の builder adapter と共通処理をまとめ、oracle 実装への互換入口、処理種別ごとの adapter、共有プロンプト整形、indexing への入口を提供する。

## Read this when
- acp という公開名の存続・削除や、既存参照を oracle 側の実体へ切り替える導線を判断するときは __init__.py を読む。
- acp.builder の全体構成、処理種別ごとの builder adapter の入口、共有プロンプト整形や index-entry 生成の配置を確認するときは builder を読む。

## Do not read this when
- acp 配下の具体的な実装仕様や移行先の詳細だけを確認したい場合は、対応する実体モジュールを直接読む。
- 特定 builder の入力制約・生成結果、acp.builder の利用箇所、正本仕様や実装そのものを確認したい場合は、この階層の入口ではなく対象の下位要素や参照元を直接読む。

## hash
- c39cd6b24e8a598b8b78eb8acddb1ed600865b536a16aabbfd39d2696e960214

# `basic`

## Summary
- `basic.*` の互換 import 公開面をまとめた realization 側の入口。ACP 型、path model、構造化文書 API の旧参照から、各互換モジュールまたは再公開元の正本へ進むための下位要素入口を提供する。

## Read this when
- `basic` 名前空間に残る互換 API の範囲や、旧 import から移行先を確認したいとき。
- ACP、path model、構造化文書の互換入口を横断して、個別モジュールを読むべきか判断するとき。

## Do not read this when
- 個別 API の実装、再公開内容、型定義、描画仕様を確認したいときは、`basic.acp`、`basic.path_model`、`basic.struct_doc`、またはそれぞれの正本実装を直接読む。
- 正本仕様そのものや、`basic` 名前空間と無関係な処理を調べるとき。

## hash
- ea7ec701e546985b90dda735f067c250cdd2609d2464948e58591d98ccf40fd2

# `cmoc_runtime.py`

## Summary
- 互換 import path から共通 runtime API を再公開する入口。公開名は共通 runtime の限定された公開面に従い、runtime と型チェッカーへ同じ互換名を伝える。

## Read this when
- 既存の互換 import path を利用する呼び出し元、または共通 runtime API の再公開・移行状況を確認するとき。

## Do not read this when
- 共通 runtime の実装内容や個別 API の責務を確認したいときは、直接 commons.cmoc_runtime を読む。
- 互換 import path の移行完了後に削除可否だけを判断するときは、移行対象の責務別 runtime module と pyproject の公開設定を直接確認する。

## hash
- 43fb961149b599635a1abdceb8611969195b689f50ec716e0231e113d978fded

# `commons`

## Summary
- cmoc の共通 runtime helper を集約する commons パッケージ。CLI、Codex 実行、設定、Git、ログ、パス、結果、状態、feedback など、複数の実行経路で共有する runtime 機能への入口を提供する。

## Read this when
- 複数の実行経路で共有される runtime 機能の配置や公開 API の入口を確認するとき
- CLI、Codex 実行、設定、Git、ログ、パス、結果、状態、feedback などの共通 helper を横断して利用・変更するとき
- 対象となる個別 runtime helper を特定し、その実装へ進む入口を確認するとき

## Do not read this when
- 特定の runtime helper の内部実装や個別挙動を直接確認したいとき
- 特定サブコマンドの業務処理や個別仕様だけを確認したいとき
- INDEX.md の生成規則や利用者向けルーティング仕様だけを確認したいとき

## hash
- 852a52b5c7e2f1b59af62bec4fc5f522b2b4d0abae2c315719316fb2f06f2883

# `config`

## Summary
- config.* 参照を維持するための互換入口。
- oracle 側の cmoc 設定型を realization 側の config.cmoc_config から再公開する経路への入口。

## Read this when
- config からの import 互換性を確認するとき。
- realization 側の config.cmoc_config における設定型の再公開経路を確認するとき。

## Do not read this when
- 設定型の定義や設定値の仕様そのものを確認したいとき。
- config.cmoc_config の参照経路を新規追加・変更する実装判断を行うとき。

## hash
- 8571722dab57a84f72fd99845c9e5c092cb64b05d9f5ac72e976209acca14524

# `main.py`

## Summary
- cmoc CLI のトップレベル入口と session／oracle／realization／run／feedback のコマンドツリーを定義する。
- Typer の起動境界で Click 8.2 の help 互換性を補正し、通常の引数解析エラーを cmoc のエラーレポートへ変換する。
- CLI 補完 probe では通常コマンドを実行せず、明示した completion marker を Click に渡す。

## Read this when
- cmoc の利用可能なコマンド階層や、各コマンドがどのサブコマンド実装へ委譲されるかを確認するとき。
- Typer／Click の互換処理、引数解析エラーの終了コード付き報告、または補完時の副作用防止を確認するとき。
- console script から cmoc CLI を起動する入口を確認するとき。

## Do not read this when
- 個別コマンドの実処理、oracle／realization のワークフロー、session／run のブランチ操作の詳細を確認したいとき。
- INDEX.md 更新、TUI 起動、feedback report の生成規則そのものを確認したいときは、対応する委譲先の実装または仕様を直接読む。

## hash
- cebff8c904ea04e4cf0994e553ef7082dece329269c6fbfaf592dc1bdb36db12

# `oracle.py`

## Summary
- `src` 起動時に正本側 `oracle.*` パッケージを解決するための互換用 package shim。`oracle/src/oracle` をパッケージパスとして再公開し、正本ソースが存在しない場合は `ModuleNotFoundError` を送出する。

## Read this when
- `src` だけを起動した際の `oracle.*` パッケージ解決や互換 import の挙動を確認するとき。

## Do not read this when
- 正本側 `oracle.*` の実装内容を確認するときは、直接 `oracle/src/oracle` 配下を読む。
- `src` の通常の CLI 実装や、package shim と無関係な import 経路を調査するとき。

## hash
- e476648f073484004b64741d40d6d373fab223e001be01ac8051f9c5ab15e095

# `sub_commands`

## Summary
- cmoc の各サブコマンド実装パッケージへの入口。doctor、feedback、indexing、oracle、realization、review、run、session、tui の責務別実装へ進むための上位ルーティングを提供する。
- サブコマンド単位で、CLI 入口、report・remediation、INDEX 更新、oracle 操作、realization workload、run・session lifecycle、TUI 起動などの処理を扱う。
- apply と review は現時点で実装本文がなく、将来のサブコマンド実装配置先として位置づけられている。

## Read this when
- cmoc のサブコマンド実装の構成や、目的のサブコマンドに対応する実装パッケージを確認するとき。
- doctor、feedback、indexing、oracle、realization、review、run、session、tui のいずれかの CLI 入口またはサブコマンド固有処理を調査・変更するとき。
- apply または review の実装追加後に、その配置先を確認するとき。

## Do not read this when
- 特定サブコマンドの具体的な処理内容、共通 runtime、prompt 契約、INDEX 生成規則などを直接調査する場合は、対応する下位実装または共通処理の対象へ進むとき。
- サブコマンドに属さない oracle 仕様、共通 lifecycle API、永続化形式、一般的な Markdown・logging 処理だけを確認するとき。

## hash
- a2c81712426dd36496f5d5d963e6b0950f2063c34dc7e076af29b7c171a58e05
