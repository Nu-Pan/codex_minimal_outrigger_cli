# `acp`

## Summary
- acp 互換公開入口を扱い、既存の acp.* 参照を oracle.* または実体モジュールへ移行する際の上位入口となる。
- oracle.acp_builder を acp.builder として公開する互換入口で、目的別 builder adapter と canonical 実装への導線を提供する。

## Read this when
- acp という公開名や acp.builder.* の互換 import 経路を維持・削除・移行できる条件を判断するとき。
- acp.builder 配下の構成や、feedback・indexing・oracle・realization・session・tui など目的別 builder adapter への入口を確認するとき。

## Do not read this when
- acp 配下の具体的な実装仕様や内部挙動を確認・変更するときは、対応する下位対象または oracle の canonical 実装を直接読む。
- builder 共通処理の詳細を調査するときは common などの共通処理対象を直接読む。
- 互換入口ではなく acp.builder の利用箇所や利用者向け公開面を調査するときは、各参照元を直接読む。

## hash
- cbe163f474a70a0051f83c7d31c161fb76f2b478066c2ad91794d80d27d50353

# `basic`

## Summary
- `basic.*` の旧公開 import を維持する互換名前空間。ACP 型、path model、構造化文書 API は正本を複製せず、既存実装の再公開または委譲によって利用者向け入口を提供する。

## Read this when
- `basic.*` の互換参照を維持・削除する条件や、利用者向け API の移行先を判断するとき。
- ACP 型、path model、構造化文書の旧 API 入口を確認し、正本実装への委譲関係を追跡するとき。

## Do not read this when
- ACP 型、path model、構造化文書の正本仕様・実装詳細を確認したいときは、各再公開元を直接読む。
- 個別モジュールの具体的な公開内容や利用箇所だけを調べるときは、`basic` 全体ではなく該当モジュールまたは参照元を直接読む。

## hash
- e66d85791589dac1aca9c82c3aeba73b5416451d343c2feb68cbe202afe895a9

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
- cmoc の共通 runtime 層。CLI サブコマンドの実行 lifecycle、設定・状態・パス管理、Git/worktree 操作、ログ・レポート・feedback、Codex exec/TUI 起動、editor input handoff、INDEX 更新など、複数の実行経路が共有する基盤処理を提供する。
- 個別サブコマンドの業務処理ではなく、実行境界・永続 state・外部プロセス・成果物記録を横断して扱う共通 API とデータモデルの入口。

## Read this when
- 複数の CLI サブコマンドに共通する実行 lifecycle、Codex 呼び出し、Git/worktree 管理、ログ・レポート、feedback、state 永続化の挙動を調べるとき。
- 共通 runtime API や結果モデルの責務・連携関係を確認したいとき。

## Do not read this when
- 特定サブコマンド固有の業務フローや正本仕様を確認したいときは、そのサブコマンドの実装または oracle 文書を直接読んでください。
- 個別の共通機能の詳細を調べる場合は、このディレクトリ全体ではなく該当する runtime モジュールを直接読んでください。

## hash
- d5cce425edadea97b1502f53ea11350e60a2935e8e8fd348b4cc07da4b92d559

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
- cmoc の Typer/Click CLI ツリーと起動入口を定義する。トップレベルおよび session、oracle、realization、run、feedback 配下の各コマンドを、対応するサブコマンド実装へ接続する。
- Click/Typer の互換性補正、補完 probe の扱い、CLI 引数解析エラーの cmoc 形式への変換など、CLI 起動時の境界処理を担う。

## Read this when
- cmoc の CLI コマンド追加・変更や、コマンド階層とサブコマンド実装の接続先を確認するとき。
- Typer/Click の版差による help 表示、補完、引数解析エラー、終了コードの挙動を調査・変更するとき。
- console script からの起動経路や、feedback report の遅延ロードを確認するとき。

## Do not read this when
- 個別コマンドの業務処理や、各サブコマンド実装の詳細を変更・調査するときは、対応する sub_commands 配下を直接読む。
- oracle、realization、session、run などの内部ワークフロー仕様だけを確認したいときは、対応する正本仕様や実装を直接読む。
- INDEX.md の生成規則や一般的なエラー処理仕様だけを確認したいときは、該当する仕様文書を直接読む。

## hash
- 9779ae11e83145b4d1e6f180791ff3855507369621957c37448f8d4a6caed407

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
- CLI のサブコマンド実装をまとめる入口で、doctor・tui・indexing と、oracle・realization・run・session・feedback の各サブコマンド群を扱う。
- 各サブコマンド群は、ライフサイクル操作、フィードバック報告・修復、セッション管理、oracle 操作など、コマンド単位の処理と状態遷移を実装する。

## Read this when
- CLI サブコマンドの一覧、構成、担当領域を把握したいとき。
- 特定のサブコマンドを追加・変更し、その実装の配置先や関連する処理群を確認するとき。

## Do not read this when
- 特定サブコマンドの詳細な挙動だけを確認したい場合は、配下の該当ファイルまたはサブディレクトリを直接読む。
- CLI 全体の起動処理や共通ランタイム、引数解析の仕様だけを確認したい場合は、親階層や共通実装を直接読む。

## hash
- 6a34f7867b3168ad4d0f1da9f4ee2f9f46b0593951cd7e27916c7e29d31da349
