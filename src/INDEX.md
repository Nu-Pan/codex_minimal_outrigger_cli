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
- commons 配下で共有される cmoc runtime API と実行時 helper 群への入口。
- CLI、Codex 実行、設定、Git、ログ、パス、状態、feedback、report、editor handoff など、複数の実行経路にまたがる共通基盤を扱う。

## Read this when
- 複数の実行経路から利用される runtime API や共通 helper の責務を確認するとき。
- commons 配下で対象となる個別 runtime module を選び、実装確認の入口を判断するとき。
- Codex 実行、設定、Git、ログ、パス、状態、feedback、report、editor handoff の共通処理を横断して調べるとき。

## Do not read this when
- 特定の runtime module の内部挙動や個別データ構造だけを確認する場合。
- CLI サブコマンド固有の業務処理や正本仕様、schema 本文、テスト固有の期待値だけを確認する場合。

## hash
- 0a6321f486fad5f65ed0cd70f351bf2ae0ba8805c92eff53e61d9ea1605d3bdf

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
- サブコマンド実装をまとめるディレクトリ入口。doctor、feedback、indexing、oracle、realization、review、run、session、tui など、各サブコマンドの実行入口や配下の処理へ進むための上位ルーティング対象。
- apply は現時点で実装ファイルがなく、将来 apply サブコマンドの実装が追加された場合に確認する対象。
- doctor は `cmoc doctor` の CLI 入口と、doctor preprocess を CLI runtime 経由で明示的に 1 ステップ実行する処理を扱う。
- feedback は判定根拠の固定・差分検出、remediation から publication、report 集約・公開、publication 後の recovery までを扱うモジュール群への入口。
- indexing は work root の INDEX.md 更新、実行前提条件の検査、排他ロック、差分 commit、primary report 反映を行う CLI 入口。
- oracle は編集系・調査系を含む oracle サブコマンド群の package 境界で、個別の実行入口や処理フローへ進むための対象。
- realization は realization 配下の workload 実装をまとめ、apply と refactor の処理入口へ振り分けるディレクトリ。
- review は review サブコマンドの realization 実装を配置するディレクトリだが、現時点で具体的な実装本文はない。
- run は editing run の abandon・join に関する停止、統合、cleanup、report、状態遷移、および旧 import path の互換 shim を扱う実装群への入口。
- session は session の fork・join・abandon に関する実行条件、状態遷移、branch 操作、失敗時 rollback を扱う実装パッケージ。
- tui は依頼文の編集から完全プロンプト・起動パラメータの構築、Codex TUI の実行までを担う tui サブコマンド本体。

## Read this when
- src/sub_commands 配下のサブコマンド構成を把握し、個別の実装対象へ進む入口を判断するとき。
- doctor、feedback、indexing、oracle、realization、review、run、session、tui のいずれかの CLI 入口または実装群を調査・変更するとき。
- apply または review の実装追加先を確認するとき。

## Do not read this when
- 特定サブコマンドの具体的な処理詳細だけを確認したい場合は、対応する下位実装を直接読むとき。
- CLI runtime 共通処理、repository・work root 解決、共通 artifact や canonical JSON など、サブコマンド固有ではない処理だけを調べるとき。
- src/sub_commands 配下のサブコマンドを扱わないとき。

## hash
- d8ae54525d971b3f36638cdb3085808dc7fdbf5b60a1ce55c65ef16919497ada
