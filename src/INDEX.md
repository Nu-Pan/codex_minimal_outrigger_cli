# `acp`

## Summary
- `acp` 互換公開層の構成と、`oracle` 側の正本実装へ委譲する builder 入口を扱うディレクトリ。公開名の維持・削除や既存 import 経路からの移行を判断する際の上位入口となる。

## Read this when
- `acp` 互換入口の存廃、既存参照を `oracle` または実体モジュールへ切り替える導線を確認するとき
- `acp.builder` 配下の builder adapter の構成、canonical builder への委譲関係、realization からの接続先を探すとき

## Do not read this when
- 具体的な builder の prompt 仕様、入力検証、出力仕様、本体ロジックを調査・変更するときは対応する `oracle.acp_builder` 側を直接読む
- 互換入口ではなく `acp.*` の内部挙動や、利用側 CLI・realization の具体的な処理を調査するときは該当する下位対象・呼び出し元を直接読む

## hash
- 12591c9ca5725cc9729269a7d4b695f7e4672ea7af67e7f9c41037591fd1288f

# `basic`

## Summary
- `basic.*` の互換 import を維持するための realization 側公開入口。ACP 型、path model、構造化文書 API を正本実装から再公開し、個別実装や正本仕様は保持しない。各モジュールの公開経路・互換参照を確認するための下位入口である。

## Read this when
- `basic.*` の互換 import を維持・削除する判断をするとき。
- realization 側から ACP 型、path model、構造化文書 API がどの経路で公開されるかを確認するとき。
- 個別モジュールの再公開関係を調査するとき。

## Do not read this when
- ACP 型、path model、構造化文書 API の正本仕様や実装詳細を確認したいときは、各再公開元の oracle 側を直接読む。
- 個別 API の詳細や参照削除の影響だけを調べるときは、対象モジュールまたは参照箇所へ直接進む。
- `basic.*` と無関係な処理を調査・変更するとき。

## hash
- 292bc262556c427d8a4a7636a2c7e14127adfdea1c7d57f167e9bfa04d4ce5ea

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
- cmoc の共通 runtime 実装を集約するパッケージ。CLI 実行、Codex subprocess、設定、Git/worktree、状態管理、ログ、feedback、INDEX 更新、prompt 入力など、複数の実行経路で共有される補助機能への入口を提供する。
- 個別の runtime 機能を調査・変更するときは、対象機能に対応する各モジュールへ直接進む。パッケージ初期化ファイル自体は commons の入口確認時に読む。

## Read this when
- commons パッケージが提供する共通 runtime 機能の全体像や、対象機能に対応する実装モジュールの入口を確認するとき。
- CLI の実行 lifecycle、Codex 呼び出し、設定・パス・Git/worktree、session/run state、feedback、INDEX 更新、prompt editor など、複数機能にまたがる共通処理の担当モジュールを特定するとき。
- 次の対象を判断するため、個別モジュールの責務境界を一覧で確認する必要があるとき。

## Do not read this when
- 特定の runtime helper、CLI サブコマンド、Codex 実行経路、feedback 保存形式、または state schema の内部挙動だけを調べる場合は、対応する個別モジュールや正本仕様へ直接進む。
- commons と無関係なアプリケーション仕様、oracle、realization 実装だけを確認する場合。

## hash
- f5aed0a3e606ad32990fad02f3e8d9c94525e33b8ea5597c2dcc9c738a688311

# `config`

## Summary
- 設定モジュールの互換入口を提供するディレクトリ。`__init__.py` は `config.*` 参照を成立させ、`cmoc_config.py` は oracle 側の設定型を定義せず realization 側から再公開する。設定仕様の確認先ではない。

## Read this when
- 既存利用者の `config` または `config.cmoc_config` 参照を維持・確認するとき。
- 設定型の import 経路や互換入口の有無を調べるとき。

## Do not read this when
- 設定定義の内容や仕様そのものを確認するときは、oracle 側の設定定義を直接読む。
- 設定参照を新規に追加する実装判断では、利用側の参照経路を直接確認する。

## hash
- fbc828970884bf16f7e7e6174e3461888e3c4000d754454ba9794e1d2c99d6f2

# `main.py`

## Summary
- Typer を使った cmoc CLI のルート入口。トップレベルおよび session、oracle、realization、run、feedback 配下のサブコマンドを登録し、それぞれの実装関数へ処理を委譲する。
- Click/Typer の互換処理と CLI 引数解析エラーの cmoc 形式への変換を担い、通常実行と `_CMOC_COMPLETE` による自動補完 probe を分離する。
- CLI のコマンド構成、引数解析エラーの扱い、または console script からの起動経路を確認する際の入口であり、個別コマンドの挙動は各 `sub_commands` 実装を直接読む。

## Read this when
- cmoc の利用可能なトップレベル・サブコマンド構成を確認するとき
- Typer と Click の互換処理、CLI 引数解析エラーの表示・終了コード、または自動補完の起動経路を調査するとき
- console script が cmoc CLI をどのように起動するかを確認するとき

## Do not read this when
- 特定サブコマンドの業務処理や worktree 操作の詳細を調査するときは、対応する `sub_commands` の実装を直接読む
- oracle、realization、session などの仕様や外部挙動の正本を確認するときは、対応する oracle/specification を直接読む
- CLI とは無関係な共通ランタイムや個別機能の実装を調査するとき

## hash
- 8a443d75371da9adebc4b8b7dc79b17f5f85b50af38d34a7405727edb10de6e0

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
- `src/sub_commands` は cmoc の各 CLI サブコマンド実装を集約する上位ディレクトリで、doctor、feedback、indexing、oracle、realization、run、session、tui などの実行入口と、apply・review の未実装領域へのルーティングを提供する。サブコマンド単位の実行フローや配下パッケージの入口を確認する際の起点となる。

## Read this when
- cmoc の CLI サブコマンド実装の全体構成や、対象サブコマンドの実装入口を特定するとき
- 複数のサブコマンドにまたがる処理経路を調査し、doctor・feedback・indexing・oracle・realization・run・session・tui のいずれへ進むか判断するとき
- realization 配下で apply または refactor の workload 入口を探すとき

## Do not read this when
- 特定サブコマンドの詳細処理、正本仕様、共通 runtime、内部モジュールの実装だけを確認する場合は、対応する下位実装や仕様対象を直接読むとき
- INDEX.md の生成規則やルーティング内容自体を確認するとき
- apply または review の具体的な実装内容を確認するときは、実装追加後に対応する下位対象を直接読むとき

## hash
- 9d416c955ea46498a5b044b013f651ccd5b419cfcd52f708f243fcd882779585
