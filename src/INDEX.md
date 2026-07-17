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
- cmoc 共通 runtime helper 群をまとめる commons パッケージ。CLI 実行、Codex、設定、Git、パス、ログ、状態、Ollama、INDEX 更新などの横断的な実装入口を提供する。個別の共通 runtime 機能や公開 API の構成を確認するときに、配下の担当モジュールへ進むための入口。

## Read this when
- 複数の cmoc 共通 runtime 機能にまたがる処理や import 境界を調査・変更するとき
- CLI、Codex、設定、Git、パス、ログ、状態、Ollama、INDEX 更新などの共通実装の担当モジュールを探すとき
- commons 配下の個別モジュール間の責務分担や公開 API を確認するとき

## Do not read this when
- 特定のサブコマンド固有の業務処理や CLI 引数だけを調査するとき
- 正本仕様を確認したいときは、対応する oracle 文書を直接読むとき
- 対象となる個別 runtime helper が明確な場合は、このディレクトリ全体ではなく担当モジュールを直接読むとき

## hash
- f1fd96d41aeff23444bc9a9e4f03e36452e07479221e6f020cff8fc4275b57cc

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
- Typer ベースの cmoc CLI のルート定義。共通エラー変換、トップレベルコマンド、session/apply/review のサブコマンド、console script の起動入口を扱う。CLI コマンドの追加・変更、引数や option の定義、コマンド実装への接続を調べる際の入口。

## Read this when
- cmoc の CLI コマンド一覧、サブコマンド階層、option の既定値や列挙値を確認するとき
- Typer・Click の引数解析エラー処理や CLI 起動方法を変更するとき
- CLI 入口から各サブコマンド実装への接続を追うとき

## Do not read this when
- 特定サブコマンドの処理内容や業務ロジックだけを調べるときは、対応する sub_commands 配下の実装を直接読む
- oracle のエラー処理・usage・サブコマンド仕様そのものを確認するときは、参照コメントに示された oracle file を読む

## hash
- 81225c8de9d313ba42585b37881ac6abea55daa56d41186a024931538e368802

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
- CLI サブコマンドの実装領域。session／apply の fork・join・abandon、review oracle の実行・対象列挙・評価ループ・レポート・INDEX commit、indexing・doctor・eval_oracle・tui の実行入口と補助処理を扱う。各サブパッケージおよび個別モジュールへの入口。

## Read this when
- サブコマンドの実行フロー、状態遷移、worktree／branch 操作、Codex 実行、レポート生成、INDEX 更新の実装を確認・変更するとき。
- session または apply のライフサイクル、review oracle の対象選定・finding 評価・merge、TUI や preprocess の CLI 入口を調査するとき。

## Do not read this when
- 共通 CLI runtime、Git／state／process tracking、indexing 共通処理、Codex parameter builder などの共通実装だけを調査するときは、対応する定義元を直接読む。
- 特定サブコマンド内の prompt／parameter、レポート描画、対象列挙など単一機能だけを調査するときは、該当する個別実装を直接読む。

## hash
- 6c0a0b17389a1d2816e579bf27c3dccb379a7d4006b53b0c6f3c7d639767615e
