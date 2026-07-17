# `acp`

## Summary
- `acp` 互換の公開入口と ACP builder 群を扱う。互換 import 経路を維持しながら、apply、review、session、TUI、indexing、quota probe などの下位 builder へ進むための入口となる。

## Read this when
- `acp` 公開名や互換 import 経路の存廃を判断するとき。
- ACP builder の構成や、対象機能に対応する下位 builder の入口を確認するとき。

## Do not read this when
- 特定 builder の具体的な処理や canonical な仕様だけを確認したいとき。
- 互換入口ではなく、個別の builder 実装や内部挙動を直接変更・調査したいとき。

## hash
- 3d90c81e3e3d3fe0dde392931009adf26ab57acf4a73344cf8072a768dcc68fa

# `basic`

## Summary
- `basic.*` の互換 import を維持する公開入口群。ACP 型、path model、構造化文書 API を実体定義から再公開し、`basic` 側に実装や正本仕様を複製しない。

## Read this when
- `basic.*` 経由の公開名や互換 import の維持・廃止を判断するとき。
- ACP 型、path model、構造化文書 API の realization 側での再公開関係を確認するとき。

## Do not read this when
- 各 API の正本仕様や実装本体を確認したいときは、対応する oracle 側を直接読む。
- `basic.*` の公開面や互換 import に関係しない処理を調査・変更するとき。

## hash
- 6427f271674f13de9f39976c4fe0d10226ad4c7573c6fa05a58ee5db32f274b7

# `cmoc_runtime.py`

## Summary
- `commons.cmoc_runtime` の公開名を互換的に再公開する薄い import shim。pyproject が `cmoc_runtime` を公開し、ツリー内の呼び出し元がこのパスを直接 import している間の移行入口。

## Read this when
- `cmoc_runtime` の互換 import path、公開名、または runtime module への移行状況を確認するとき。

## Do not read this when
- runtime の実装や責務別 module の詳細を確認するときは、`commons.cmoc_runtime` または該当する runtime module を直接読む。
- 互換 path の移行完了後は、この shim を読む必要はない。

## hash
- ce0901465f229760c4bd1f4c5ce3f4a035bb53bf6aee04de082b5843cff3ff17

# `commons`

## Summary
- cmoc の共通 runtime helper をまとめる commons パッケージ。CLI 実行、Codex、設定、Git、パス、ログ、状態、Ollama、INDEX 更新などの実装入口を提供し、配下の個別 runtime モジュールへ進むためのディレクトリ。

## Read this when
- 複数の共通 runtime 機能にまたがる実装箇所や、commons 配下のモジュール構成を確認するとき
- CLI 実行、Codex 起動、設定、Git、パス、ログ、状態管理などの共通処理の入口を探すとき

## Do not read this when
- 特定の runtime 機能の実装詳細を調べるときは、commons 配下の対応する個別モジュールを直接読む
- CLI サブコマンド固有の処理や利用者向け仕様だけを確認するときは、該当する command 実装または oracle 文書を直接読む

## hash
- b9d4cdeffaa0a1218b27310a1192f3f26ebcf3c091e7c58f2d146aab31c9a951

# `config`

## Summary
- `config.*` 参照を既存利用者向けに維持するための互換入口群。ここでは設定の実体を持たず、正本の oracle src を再公開する経路だけを確認する。
- `config.cmoc_config` から Cmoc 設定型を再公開する入口。設定定義そのものではなく、既存の公開参照を壊さないための接続点として読む。

## Read this when
- `config` からの import 経路を維持・確認したいとき。
- `config.cmoc_config` 経由で Cmoc 系の設定型を参照したいとき。
- 設定の正本を変更せず、互換入口の有無だけを確認したいとき。

## Do not read this when
- 設定仕様そのものを確認したいときは、正本側の oracle src を読む。
- `config.*` 以外の公開面や新規設定追加を扱いたいとき。
- 設定定義の項目意味や保存仕様を調べたいとき。

## hash
- c121a67917bdcc7850097d1a5fc153afb19f375da55ada79794c9c5739b22514

# `main.py`

## Summary
- Typer を用いた cmoc CLI のアプリケーション定義と起動入口。共通エラー変換、トップレベル command、session/apply/oracle のサブコマンド、各実装関数への接続、scope option を扱う。下位サブコマンドの CLI 入口や全体の command 構成を確認する際の起点となる。

## Read this when
- cmoc のトップレベル command、サブコマンド構成、CLI option、Typer/Click のエラー処理を変更・調査するとき
- console script またはモジュール実行時の CLI 起動経路を確認するとき

## Do not read this when
- 特定サブコマンドの処理本体や branch 操作、doctor、TUI、indexing の詳細な挙動を調査するときは、対応する sub_commands 配下の実装を直接読む

## hash
- 9b7a3a4c03d63245486277dfc1529a5fb4d3762221561d93d68eba46846c93cc

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
- cmoc の各サブコマンド実装を収めるディレクトリ。apply、doctor、indexing、review、session、tui などの CLI 実行入口と、review 系の対象列挙・ループ・レポート・パス処理を扱う下位実装への入口となる。

## Read this when
- サブコマンドの CLI 実装や構成を確認・変更するとき。
- apply、doctor、indexing、review、session、tui の実行フローや、review 関連の対象列挙・finding 処理・レポート・INDEX 更新を調査するとき。

## Do not read this when
- 共通 runtime、Git、worktree、Codex 実行基盤など、サブコマンド横断の実装だけを扱うとき。
- 特定サブコマンド内の詳細処理だけを変更・調査するときは、対応する下位実装を直接読む。

## hash
- e834b9003a731b0e9e2df6d552f13c80c596d8438922bfbc47bc2462d610a19e
