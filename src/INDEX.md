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
- commons 配下で共有される runtime の実装入口。CLI・Codex 実行、設定、Git、ログ、パス、状態、結果、feedback、report、run lifecycle、editor input handoff など、複数の実行経路が利用する共通処理を扱う。
- 実行前後の lifecycle、subprocess 境界、Structured Output 検証、quota／capacity 対応、エラー変換、診断ログ、primary report、Windows 通知など、上位実行経路を横断する制御の入口。
- feedback の受付・保存・publication、session／run state、refactor state、worktree／process tracking、INDEX 更新、editor input handoff の IPC など、永続 state と安全な境界管理を確認するための下位実装への入口。

## Read this when
- 複数の CLI・Codex・TUI 実行経路で共有される runtime API、共通 lifecycle、結果型、エラー処理、ログ、パス、設定、Git、state の実装を確認・変更するとき。
- Codex subprocess の起動、Structured Output の検証、capacity／quota の retry、call log、TUI 通知、editor input handoff など、実行境界を調査するとき。
- feedback observation の受付・保存・publication、primary report、editing run、refactor、INDEX 更新など、複数モジュールにまたがる共通の永続化・復旧・cleanup を追うとき。
- 特定の共通責務を担当する runtime サブモジュールの入口を特定し、その実装へ進む必要があるとき。

## Do not read this when
- 特定の CLI サブコマンドの業務処理や利用者向け仕様だけを確認したいときは、該当するサブコマンド実装または正本仕様を直接読む。
- 特定の runtime helper、schema、error 型、report 定義、feedback payload、IPC protocol の詳細だけを調べるときは、commons 配下の対応する個別対象を直接読む。
- INDEX.md の利用者向けルーティング規則や Codex 実行・editing run・feedback report の正本仕様そのものを確認するときは、対応する仕様文書を直接読む。

## hash
- c0d2eb771276afadf6cb5aebd31b314b232db3ebc2e400aee1c29fd31907403b

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
- cmoc の各サブコマンド実装を配置する package 境界であり、apply・doctor・feedback・indexing・oracle・realization・review・run・session・tui の実装入口を提供する。
- サブコマンド全体の構成を把握し、目的のサブコマンド実装へ進むための上位ルーティング先となる。

## Read this when
- cmoc のサブコマンド実装の配置や全体構成を確認するとき。
- 特定のサブコマンド実装を調査する前に、対応する実装入口を選ぶとき。
- 新しいサブコマンド実装の追加先や、既存サブコマンドの package 境界を確認するとき。

## Do not read this when
- 特定サブコマンドの具体的な処理、prompt 契約、共通 runtime、ライフサイクルなどを確認したいときは、対応する下位実装を直接読む。
- サブコマンド以外の共通処理や仕様を調査するとき。

## hash
- 1581b401631326b6fb49c6d4b053c8510331fbb5c5d0bd8761ab90b1ade4f3bc
