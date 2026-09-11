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
- cmoc の共通 runtime helper 群をまとめる commons パッケージ。CLI、Codex 実行、設定、Git、ログ、パス、状態、feedback、report など横断的な実行基盤を確認・変更するときの入口。
- INDEX.md の検査・生成・鮮度確認・復元・commit を含む indexing lifecycle の実装と、Codex 実行前 preflight の連携を確認できる。
- editor input handoff、feedback reporter、primary report、run lifecycle など、複数の実行経路で共有される境界処理を担当する。

## Read this when
- cmoc の複数コマンドにまたがる runtime API、実行結果、例外、ログ、パス、設定、Git、state の共通処理を調べるとき
- Codex exec／TUI の起動、retry、preflight、Structured Output、process tracking、通知連携を確認するとき
- INDEX 更新、feedback の受理・保存・公開、editor input handoff、primary report、editing run の共通 lifecycle を追うとき

## Do not read this when
- 特定のサブコマンド固有の業務処理や利用者向け仕様だけを確認したいとき
- 個別 runtime module の内部実装、schema、protocol、state model、report 定義など、より直接の対象が明確なとき
- commons と無関係な UI、外部サービス、または個別テストの期待値だけを調べるとき

## hash
- 8af7338dec5ef1ac9945d68a4e82f39f9bed0536e85b5076be4d18d9c5019bcf

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
- cmoc の各サブコマンドにおける CLI 入口と、feedback・oracle・realization・run・session の実装 package への上位ルーティングを提供する。
- doctor、indexing、tui の直接実装と、サブコマンド固有処理を担う配下 package の入口を扱う。

## Read this when
- サブコマンドの CLI 入口を横断して確認するとき。
- doctor preprocess の明示実行、INDEX.md の更新・commit、または依頼文編集から Codex TUI 起動までの入口を調べるとき。
- feedback、oracle、realization、run、session の各サブコマンド群から個別実装へ進む先を判断するとき。

## Do not read this when
- 特定サブコマンドの判定・報告・修復・復旧などの詳細処理を確認したい場合は、feedback 配下の担当実装を直接読むとき。
- oracle の編集・調査、realization の apply・refactor、run の lifecycle、session の fork・join・abandon など個別処理の詳細だけを調べるときは、対応する下位対象を直接読むとき。
- 共通 CLI runtime、prompt editor、indexing 共通処理、または TUI 起動パラメータの仕様だけを確認するときは、参照される共通実装を直接読むとき。

## hash
- 60f844e1c51754322b2d2d6aea9bc87c6eaa1e98d46611027cfdb05326552010
