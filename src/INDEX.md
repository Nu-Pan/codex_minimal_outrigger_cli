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
- cmoc の CLI 実行を支える共通 runtime 実装を集約するディレクトリです。Codex の exec/TUI 起動、設定・パス・プロセス管理、ログ・結果・primary report、feedback、editor input handoff、INDEX/doctor、editing run の state と lifecycle を横断する基盤処理を扱います。

## Read this when
- 複数のサブコマンドにまたがる runtime の責務分担や、Codex 実行から結果記録・run 管理までの共通フローを調べるとき。
- 個別の実装に入る前に、対象機能が CLI lifecycle、Codex 境界、report/log、feedback、INDEX、または editing run のどの共通処理に属するか確認するとき。

## Do not read this when
- 特定の機能の実装箇所が明確なときは、このディレクトリ全体ではなく該当する `runtime_*.py` または `indexing.py` を直接読んでください。
- oracle 仕様の意味や要求を確認したいときは、ここではなく対応する `oracle` 配下の仕様を読んでください。

## hash
- d091aec2288b6ae87881364fe11b6902a426440086cd09774112ac57a0965fe9

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
- CLI の個別サブコマンド実装をまとめる入口で、doctor・tui・indexing と、session・run・feedback・oracle・realization の各サブコマンド群を扱う。
- session は session branch の作成・参加・破棄、run は editing run の共通 lifecycle、feedback は報告・判定・修復・復旧、oracle は oracle の編集・調査、realization は apply/refactor workload の実装へ進むための下位入口である。

## Read this when
- cmoc のサブコマンド全体から、どの機能群の実装を確認・変更すべきか判断するとき。
- doctor・tui・indexing の直接処理、または session・run・feedback・oracle・realization のサブコマンド群への入口を確認するとき。

## Do not read this when
- 特定のサブコマンドの詳細な処理フローや引数・状態遷移を確認する場合は、該当する下位ファイルを直接読む。
- サブコマンド共通でない基盤処理や、oracle・realization の正本仕様を確認する場合は、このディレクトリではなく対応する実装・仕様を直接読む。

## hash
- 0227d566b83c7cef8c3c9a07493a4ffdcf672baba4f37324c7d0829b2737fcbf
