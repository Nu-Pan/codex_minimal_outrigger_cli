# `acp`

## Summary
- 既存の acp 系 import を正本の oracle builder 群へつなぐ互換層です。一部の builder は既存の公開名や引数に合わせて薄く適合させます。

## Read this when
- 既存の acp 系 import の解決や移行、互換 adapter の振る舞いを調べるとき。

## Do not read this when
- builder の正本の仕様や実装を調べるときは、oracle 側の builder を直接確認してください。
- 特定の下位領域の adapter だけを調べるときは、その領域の資料から確認を始めてください。

## hash
- cbe163f474a70a0051f83c7d31c161fb76f2b478066c2ad91794d80d27d50353

# `basic`

## Summary
- 既存の `basic.*` 参照を保つ互換 import 層。ACP 型、構造化文書 API、パスモデルを正本側から再公開し、構造化文書の旧 list 入力も canonical renderer に渡す。

## Read this when
- `basic.*` 経由の import、公開名、または構造化文書の旧入力形式との互換性を調べたり変更したりするとき。

## Do not read this when
- 正本側の型や実装の振る舞いだけを変更し、`basic.*` の互換 import や公開名に関係しない場合は、正本側の該当実装から読む。

## hash
- e66d85791589dac1aca9c82c3aeba73b5416451d343c2feb68cbe202afe895a9

# `cmoc_runtime.py`

## Summary
- 平坦な runtime import path を共通 runtime API へ委譲する互換 shim で、公開面を共通側の公開 API に合わせ、既存の利用箇所が責務別モジュールへ移行するまで維持されます。

## Read this when
- 従来の import path の互換性、公開パッケージへの収録、またはその互換層を削除できる移行条件を調べるとき。

## Do not read this when
- 共通 runtime API の個別機能の実装や挙動を調べたり変更したりするときは、委譲先の共通 API や該当する責務別モジュールを直接確認してください。

## hash
- 43fb961149b599635a1abdceb8611969195b689f50ec716e0231e113d978fded

# `commons`

## Summary
- 複数のサブコマンドで共有する runtime 処理を担い、Codex の起動と回復、CLI の終端処理やログ・レポート、設定・Git・session/run 状態、INDEX と doctor の lifecycle、feedback の受付・保存、入力 handoff と通知を扱う。
- 個別コマンドの手順ではなく、呼び出し元をまたいで共有される実行境界や状態管理を追うときの入口。

## Read this when
- 複数のコマンドに共通する Codex 実行、CLI 終端処理、設定・パス・Git、session/run 状態、INDEX 更新や doctor の振る舞いを変更するとき。
- feedback の共通受付・保存・状態管理、実行ログやレポート、入力 handoff、通知の共有処理を変更するとき。

## Do not read this when
- 特定のサブコマンド固有の手順や workload だけを追うときは、そのコマンドの実装から読む。
- 正本仕様の要件を確認または変更するだけのときは、該当する仕様から読む。

## hash
- 820e33f42f46cd39459adf16e0b8329c75a08072782af5651f65766ed58885af

# `config`

## Summary
- `config.*` の既存 import を保つ互換入口で、設定型を正本の定義から再公開する。
- 設定型の定義や設定の読み書き処理ではなく、互換 import の維持・確認に使う。

## Read this when
- 既存の `config.*` import との互換性を確認・変更・削除するとき。

## Do not read this when
- 設定型の項目や既定値を変更するときは、正本の設定定義を確認するとき。
- 設定の読み込み、保存、JSON 変換の挙動を調べるときは、runtime config の実装を確認するとき。

## hash
- 8571722dab57a84f72fd99845c9e5c092cb64b05d9f5ac72e976209acca14524

# `main.py`

## Summary
- CLI の command tree と起動時の共通処理をまとめ、各コマンドを実処理へ接続する入口。
- Typer/Click の互換処理、補完 probe、引数解析エラーの変換も担う。

## Read this when
- コマンドの登録や階層、CLI の起動方法を変更・調査するとき。
- 補完 probe、引数解析エラー、help 表示の互換処理など、複数コマンドに共通する挙動を調べるとき。

## Do not read this when
- 特定コマンドの処理内容を変更・調査するときは、そのコマンドの実装へ進む。
- コマンドの期待仕様を確認するときは、該当する oracle 仕様へ進む。

## hash
- 9779ae11e83145b4d1e6f180791ff3855507369621957c37448f8d4a6caed407

# `oracle.py`

## Summary
- `src` 単独起動時に正本側の `oracle` パッケージを解決する薄い橋渡しで、正本モジュールの実装自体は担いません。

## Read this when
- `src` だけで起動した場合の `oracle.*` import 解決や、その橋渡しを調べる・変更する場合。

## Do not read this when
- 正本側 `oracle.*` モジュールの機能や内部実装を調べる場合は、そのモジュールを直接読んでください。
- `oracle.*` の import 解決に関係しない CLI 起動やコマンド処理が対象の場合は、該当する起動点やコマンド実装から読んでください。

## hash
- e476648f073484004b64741d40d6d373fab223e001be01ac8051f9c5ab15e095

# `sub_commands`

## Summary
- cmoc の各サブコマンドを CLI runtime に接続し、コマンド固有の処理と状態遷移を実装する層。
- 診断・索引更新・TUI 起動、oracle 編集・調査、realization の適用・リファクタリング、session と editing run の管理、feedback observation の処理と report 公開を扱う。
- 入力収集、Codex 呼び出し、変更検査、state・report 更新、回復と cleanup の流れをコマンド単位で追う入口。

## Read this when
- サブコマンドの実行時の振る舞い、前提条件、エラー処理、結果報告の流れを変更または調査するとき。
- session や editing run の作成・統合・破棄が、worktree や state にどう作用するか確認するとき。
- feedback observation の取り込みから判定・修復・report 公開、または中断後の回復までを追うとき。
- oracle や realization を扱うコマンドが、対話入力・agent 呼び出し・変更検査をどう組み立てるか調べるとき。

## Do not read this when
- CLI コマンドの登録、引数、ディスパッチ経路だけを変更・確認するときは、CLI command tree の入口を読む。
- 特定のサブコマンド群の局所的な実装だけが対象なら、この階層全体ではなく対応する下位項目から読む。
- 複数コマンドで共有する Git・state・run lifecycle・indexing の処理を変更するときは、その共通処理の実装を直接読む。
- agent に渡す prompt の構築や、コマンドの意図を定める正本仕様を調べるときは、それぞれの builder または oracle 仕様を読む。

## hash
- b8de349368fadbb1699708a754fc7ce7ffb655dd6e533d27fcd74a1051e340f3
