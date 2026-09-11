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
- cmoc の共有 runtime 実装を集約する commons パッケージ。CLI、Codex 実行、設定、Git、ログ、パス、状態、feedback、report、run lifecycle など、複数の実行経路から利用される共通境界への入口。

## Read this when
- 複数のサブコマンドや実行経路にまたがる runtime 機能の入口・公開 API・共通 lifecycle を確認するとき
- Codex 実行、INDEX 更新、feedback、設定、Git、state、report、run 管理などの共通実装の所在を調べるとき
- 特定の runtime helper を読む前に、commons 配下で担当モジュールを選ぶとき

## Do not read this when
- 特定の runtime helper の内部挙動が明確で、その個別実装を直接確認すれば足りるとき
- 利用者向け仕様や個別 CLI の業務フローなど、commons の共通実装に関係しない内容を確認するとき

## hash
- 8a48e24964f735f1b42748c0ac3f4b7740cdee4378a99f4c5c6f4c2c37036d3f

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
- src/sub_commands 配下のサブコマンド実装と関連パッケージへの入口を提供する。
- apply は現時点で実装がなく、将来追加された実装を確認するための空の境界である。
- doctor.py は doctor CLI の入口、preprocess の明示実行、repo root を含む実行結果を扱う。
- feedback は観測判定、修復、report publication、cleanup・recovery の処理経路を扱う。
- indexing.py は前提条件確認、排他下での INDEX.md 更新と差分 commit、結果報告までの indexing CLI フローを扱う。
- oracle は編集系・調査系 oracle サブコマンドの package 境界として個別実装へ案内する。
- realization は apply と refactor の workload 実装へ進む上位入口である。
- review は realization 配下の review 実装を置く境界だが、現時点で具体的な実装はない。
- run は editing run の abandon・join、停止・統合・cleanup・report・状態遷移、旧 import path の互換 shim を扱う入口である。
- session は session の fork・join・abandon、branch・state 操作、統合・破棄・rollback・cleanup を横断する入口である。
- tui.py は依頼文の編集から完全プロンプトと起動パラメータを構築し、Codex TUI を実行する入口である。

## Read this when
- src/sub_commands 配下のサブコマンド実装の構成や、各処理領域への入口を確認するとき。
- doctor の CLI 入口、preprocess の明示実行、実行結果の repo root 情報を確認するとき。
- feedback の判定・修復・report publication・run 状態遷移・cleanup/recovery を横断して調べるとき。
- INDEX.md 更新の前提条件、排他実行、差分 commit、primary report 反映を確認するとき。
- oracle サブコマンドの編集・調査系実装への案内が必要なとき。
- realization 配下の apply／refactor workload の構成や入口を確認するとき。
- review realization の実装配置場所を確認するとき。
- editing run の abandon／join と共通 lifecycle の入口を探すとき。
- session の fork／join／abandon を横断して追跡するとき。
- cmoc tui のプロンプト編集、起動パラメータ構築、Codex TUI 起動経路を確認するとき。

## Do not read this when
- apply が追加される前に、apply サブコマンドの具体的な処理内容を確認したいとき。
- 対象が別のサブコマンドで、該当する下位実装や共通 runtime が直接の確認先になるとき。
- doctor preprocess の具体的処理や CLI 共通 runtime だけを調べるとき。
- feedback の共通 run lifecycle、永続 artifact 形式、観測受付の詳細だけを調べるとき。
- indexing の具体的な更新規則・探索生成ロジック、CLI runtime、worktree 検査実装だけを調べるとき。
- oracle edit／investigation の個別 prompt、起動パラメータ、共通処理を調べるとき。
- realization apply／refactor の具体的 lifecycle や実装詳細だけを調べるとき。
- oracle review の処理内容や仕様を調べるとき。
- 共通 lifecycle の canonical 実装、workload 固有処理、run 作成や通常編集だけを調べるとき。
- 共通 CLI 実行基盤、Git 操作、state 永続化の一般仕様だけを調べるとき。
- TUI parameter builder、prompt editor input、共通 runtime の仕様だけを調べるとき。

## hash
- deb721ebf5c95173cb0930a28d16a7a968267419e7513e69de485d68a80780a1
