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
- cmoc の共通 runtime 境界を構成し、CLI の終端処理、Codex exec/TUI、設定、Git、パス、ログ、結果、エラーを横断して利用する基盤。
- INDEX.md の検査・生成・鮮度確認・書き込み・復元、doctor の修復、editing run の lifecycle と worktree/process cleanup を扱う実行管理の入口。
- prompt editor handoff、feedback collector/reporter・durable store・report state、primary report、refactor state など、各機能の安全な IPC・永続化・状態管理を担う下位 runtime 群への入口。

## Read this when
- 複数の CLI 実行経路で共有される runtime API、実行 lifecycle、状態管理、ログ、結果、エラー処理の責務を横断して確認するとき。
- Codex 実行前後の preflight、subprocess、Structured Output、retry、TUI、editor handoff、feedback、report、Git/worktree の連携境界を調査するとき。
- INDEX 更新、doctor 修復、editing run、session state、feedback state など、複数の下位機能にまたがる整合性や復旧処理の入口を探すとき。

## Do not read this when
- 特定の機能の仕様や個別実装だけを確認したい場合は、対象となる runtime モジュールまたは対応する正本仕様を直接読むとき。
- CLI サブコマンド固有の業務処理、設定モデル、feedback schema、editor handoff protocol など、共通 runtime の横断入口を必要としない調査を行うとき。
- 単一の結果型、低レベルの Git/path 操作、個別の report 描画や保存処理だけを確認する場合。

## hash
- 9f0cbb04a3b9f259451331ee24daea364c347779cee7701c8ed2d31ef2400b5a

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
- cmoc の CLI コマンドツリーを構成し、doctor・tui・indexing・feedback report と session／oracle／realization／run 配下の各コマンドを実装関数へ接続する起動入口。
- Typer と Click の互換境界および CLI 引数解析エラーの cmoc 形式への変換を、このファイルで一元的に扱う。

## Read this when
- cmoc の公開 CLI コマンド構成、サブコマンドの登録、console script の起動経路を確認するとき。
- Typer／Click の版差による help 互換性や、通常実行・補完 probe・引数解析エラーの境界を調査するとき。

## Do not read this when
- 個別コマンドの業務処理や session／oracle／realization／run の詳細動作を確認したいときは、接続先の sub_commands 実装または対応する app_spec を直接読む。
- INDEX.md の更新処理そのものや feedback observation の収集・報告仕様を確認したいときは、indexing／feedback の実装・正本仕様を直接読む。

## hash
- 31b3b57d02930d07729a3c68dc9072f718b7ccdc19fa4a18c399c6f4ba33cf6f

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
- 対象ディレクトリは、CLI サブコマンドの実装をサブコマンド単位で配置する上位パッケージで、doctor・feedback・indexing・oracle・realization・run・session・tui など個別の実行入口へ進むためのルーティング起点です。
- apply や review のように現時点で実装本文がない領域も含め、サブコマンド実装の追加・構成確認時に同階層の対象を振り分ける役割を担います。

## Read this when
- CLI サブコマンド全体の構成を確認するとき。
- 特定のサブコマンド実装へ進む入口や、サブコマンド間の配置・責務分担を判断するとき。
- サブコマンド実装の追加先や、realization・oracle・run など配下の階層構成を確認するとき。

## Do not read this when
- 特定サブコマンドの具体的な処理、入力、状態遷移、runtime 呼び出しを確認・変更するときは、対応するサブコマンド実装を直接読む。
- CLI 共通 runtime や INDEX.md の更新規則など、サブコマンド配置を越えた共通処理だけを調べるときは、対応する共通実装・仕様を直接読む。
- サブコマンド以外のディレクトリや機能を扱うとき。

## hash
- 2110f03c4c5f906941cc783b5ebdbe50a6e33d185134e816267312da6fcc32be
