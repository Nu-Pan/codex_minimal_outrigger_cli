# `acp`

## Summary
- `acp` 互換入口と `acp.builder` 配下の互換入口群を扱う。旧来の import 経路を維持しつつ、`oracle` 側の正本実装や各機能の実体へ到達するための境界を提供する。

## Read this when
- `acp` または `acp.builder` の公開名・互換 import 経路・委譲先を確認したいとき。
- 互換入口の維持、整理、削除可否を判断するとき。
- apply、indexing、review、session、TUI、quota probe などの入口から対応する実体へ進みたいとき。

## Do not read this when
- 特定機能の正本仕様や本体実装だけを確認したいときは、対応する `oracle.acp_builder` 側または委譲先の実体を直接読む。
- `acp.*` の内部挙動そのものを変更したいときは、対象の実体モジュールを直接読む。

## hash
- 42d30cc28f71c611205d0e05abb41a5cf21bca2db9041834b4f593295855d276

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
- cmoc の実行時に複数モジュールから共有される runtime helper 群をまとめる領域。CLI 実行ライフサイクル、Codex 起動、設定、Git・worktree、パス、ログ、状態、エラー、Ollama、INDEX 更新などの共通機能への入口を提供し、個別機能の詳細は下位モジュールへ案内する。

## Read this when
- cmoc の複数モジュールで共有される runtime helper の配置や公開 API の入口を確認したいとき。
- CLI 実行、Codex 呼び出し、設定、Git・worktree、パス、ログ、状態管理などの共通処理について、担当モジュールを特定したいとき。
- INDEX.md 更新や doctor・Ollama など、横断的な実行時機能の実装箇所を探すとき。

## Do not read this when
- 特定の helper の実装詳細、入出力、失敗時挙動を確認したいとき。該当する下位モジュールを直接読む。
- CLI サブコマンド固有の業務処理やテスト固有の処理を調べたいとき。各責務を直接担う対象へ進む。
- runtime helper の正本仕様や利用者向け出力仕様を確認したいとき。対応する oracle 文書を読む。

## hash
- 04ea997d5f468254fe26fc9568aa15ba2db115bac413917165036f988ddd3e6c

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
- cmoc の Typer CLI アプリケーション本体。トップレベルおよび session、apply、review 配下のサブコマンドを定義し、各処理実装へ振り分ける。
- CLI 引数解析エラーを cmoc 共通のエラーレポートへ変換し、補完処理や終了コードも制御する。
- CLI option の scope enum と console script からの起動入口も扱う。

## Read this when
- cmoc のコマンド名、サブコマンド、option、scope の定義を確認するとき
- CLI 引数解析エラーの変換やアプリケーション起動処理を変更・調査するとき
- doctor、tui、indexing、eval-oracle、session、apply、review の CLI 接続先を確認するとき

## Do not read this when
- 個別サブコマンドの処理内容や内部状態遷移を調査するときは、各サブコマンド実装を直接読む
- エラー内容の正本仕様を確認するときは、参照されている error_handling の oracle file を読む
- CLI ルーティングと無関係な共通ランタイムや個別機能の実装を調査するとき

## hash
- f1b5909218e631af903858d2cb1bcd9ece673fae06127d35f2622169e8431015

# `oracle.py`

## Summary
- `src` から `oracle.*` を import したときに、正本側の実装群へ解決させるための境界を見る入口。`oracle` 名前空間の参照先を切り替える仕組みだけを扱い、個別の oracle 実装内容を追う前段として読む。

## Read this when
- `src` 経由の import で正本側 `oracle.*` が見つからない、または参照先の切り替え方法を確認したいとき。
- `oracle` 名前空間を packaged realization ではなく正本ソースへ向ける必要があるかを判断したいとき。

## Do not read this when
- `oracle.*` 配下の個別機能や実装内容を知りたいときは、ここではなく正本側の該当モジュールを読む。
- 通常のアプリ機能や CLI の挙動を追いたいだけなら、この import 解決の仕組みは読まなくてよい。

## hash
- 7ef36bb425d49e4907bce740821b18302da678a21b33bf887d9fd94c111929a5

# `sub_commands`

## Summary
- サブコマンド実装をまとめるディレクトリ。apply、review、session などの実行入口と個別処理、INDEX 更新、TUI・doctor の起動処理を下位要素への入口として提供する。

## Read this when
- サブコマンド全体の構成や、対象となるサブコマンド実装の入口を確認したいとき。
- apply、review、session、TUI、doctor、indexing などのサブコマンドの実行制御や責務分担を調査・変更するとき。
- 特定のサブコマンドについて、配下の個別モジュールへ進む前に実装の所在を把握したいとき。

## Do not read this when
- 共通 CLI runtime、設定、Git 操作、session state、process lock などの共通実装だけを調べたいとき。
- 特定のサブコマンドの詳細な制御ロジック、パス処理、レポート生成、対象列挙を調べる場合は、この階層の案内を経由せず担当モジュールを直接読むとき。
- サブコマンド実装と無関係な oracle、テスト、ドキュメントだけを扱うとき。

## hash
- 2d812820441b93872001052d66a5cfad4b30e1dbd794758999d261a7d3b29747
