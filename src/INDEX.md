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
- cmoc の共通 runtime helper をまとめる commons パッケージ。CLI、Codex 実行、設定、Git、ログ、パス、状態、feedback、report、run lifecycle など、複数の実行経路から共有される処理への入口です。

## Read this when
- 共通 runtime API の公開窓口や commons パッケージの構成を確認するとき
- CLI・Codex・設定・Git・状態・feedback・report・run 管理などの共有実装を変更または調査するとき
- 複数のサブコマンドにまたがる実行 lifecycle、外部プロセス境界、永続 state、成果物管理の責務を確認するとき

## Do not read this when
- 特定の helper の内部挙動だけを確認したいときは、該当する個別 runtime module を直接読む
- 利用者向けの正本仕様、個別サブコマンドの業務処理、または個別 schema の内容だけを確認したいとき
- commons の共通処理を利用しない機能や、テスト固有の期待値だけを調べるとき

## hash
- 92a6715b519d87ad58d5e968e5a0e00757e947fe9435221021614e68c2dc22e3

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
- apply サブコマンドの実装配置先。現在は実装がなく、将来の apply 実装への入口。
- `cmoc doctor` の CLI 入口。doctor preprocess の明示実行と repo root を含む結果生成を担う。
- feedback サブコマンドの入口。観測の report 化、判定、issue 修復、publication 後の recovery へ振り分ける。
- INDEX.md 更新を行う indexing CLI の入口。前提検査、排他下での更新、差分 commit、結果報告を担う。
- oracle 系サブコマンドの入口。oracle edit と oracle investigation の入力処理、検証、agent または TUI 起動を担う。
- realization workload の入口。apply workload と refactor fork の lifecycle、agent 実行、変更検査、commit、状態記録を扱う。
- review サブコマンドの実装配置先。現在は具体的な実装がなく、追加実装への配置上の入口。
- editing run の共通 lifecycle 実装への入口。run abandon・join の停止、統合、cleanup、report、互換 shim を扱う。
- session サブコマンドの入口。session fork・join・abandon の lifecycle 処理へ進むための起点。
- 利用者入力から完全なプロンプトと TUI 起動パラメータを構築し、Codex TUI を実行する tui サブコマンド本体。

## Read this when
- apply サブコマンドの実装が追加され、その処理内容や配置を確認するとき。
- `cmoc doctor` の入口、doctor preprocess の明示実行、実行結果の repo root 情報を確認するとき。
- feedback の全体構成を確認し、観測、判定、修復、publication 後 recovery の調査先を判断するとき。
- `cmoc indexing` の実行前提、INDEX.md 更新、差分 commit、結果報告の呼び出し元を確認するとき。
- oracle 系サブコマンドの構成、oracle edit の agent call、または oracle investigation の TUI 起動フローを確認するとき。
- realization apply・refactor の実行手順、run 状態遷移、完了判定、変更検査、cleanup、report 保存を確認するとき。
- review サブコマンドの実装ファイルを追加・変更する場所を確認するとき。
- editing run の停止、統合、cleanup、report、状態遷移、または `cmoc run abandon`・`cmoc run join` の入口を確認するとき。
- session サブコマンドの構成、または session fork・join・abandon の実行経路を確認するとき。
- `cmoc tui` の入力収集、プロンプト構築、indexing 準備、context・設定の受け渡し、TUI 起動経路を確認するとき。

## Do not read this when
- apply 以外のサブコマンドを扱うとき。
- doctor preprocess の具体的な処理内容や成果物を調べるとき。
- CLI 共通 runtime や一般的な実行制御を調べるとき。
- feedback 内の特定処理の実装詳細が明確で、対応する下位モジュールを直接読めるとき。
- INDEX.md の更新規則や探索・生成ロジックを調べるとき。
- oracle 個別サブコマンドの prompt 契約や、共通 prompt editor・TUI runtime の詳細だけを調べるとき。
- apply workload の agent 起動パラメータだけ、または editing run の共通 lifecycle だけを調べるとき。
- review の具体的な処理内容や oracle review の仕様を調べるとき。
- run の canonical lifecycle、workload 固有の merge・差分処理、run 作成や通常編集だけを調べるとき。
- SessionState、Git 操作共通実装、conflict resolution builder の詳細だけを調べるとき。
- TUI 起動パラメータ、prompt editor、CLI 共通 runtime、設定ロードの詳細だけを調べるとき。

## hash
- 20c73fc92d6098ed124c44136844e4baa845f8adb2993fda18139d242116a965
