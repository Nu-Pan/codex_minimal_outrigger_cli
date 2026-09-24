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
- コマンド間で共有する cmoc runtime 基盤で、サブコマンドの開始・終了、設定と状態、Codex 実行、Git・worktree、編集 run、INDEX 更新と doctor 修復、feedback、報告・ログなどを担う。
- 共通 API と責務別の runtime 境界をまとめているため、複数コマンドに関わる共有動作や、これらの境界をまたぐ変更の入口となる。

## Read this when
- 複数のサブコマンドに共通する runtime の挙動を追う、または共通境界にまたがる変更を行うとき。
- Codex 実行、Git・worktree と編集 run、feedback、INDEX 更新・doctor 修復の間で状態や終了処理がどう連携するか調べるとき。

## Do not read this when
- 単一コマンド固有の動作だけを調べる場合は、そのコマンド側から始め、共有 runtime が関わる箇所だけを確認する。
- 設定や挙動の正本を確認する場合は、共有実装ではなく該当する正本へ直接進む。
- 変更対象の共有責務がすでに分かっている場合は、パッケージ全体ではなくその責務の実装から読む。

## hash
- aade47cd64a36f4243bc56866db4c4f0ec0d3fe1376cdc9a187aaedf857f31c1

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
- doctor・tui・indexing と oracle、session、run、realization、feedback の各サブコマンド固有の実行処理を担う。
- 実行前提の確認から agent 起動、成果の検査、状態・報告の更新、中断回復、merge、cleanup までを制御し、共通 runtime や parameter builder を利用する。
- CLI の登録・引数解釈ではなく、呼び出されたコマンドの処理本体を調べる入口。

## Read this when
- 対象コマンド固有の実行手順、事前条件、状態遷移、失敗時の処理を調べる・変更する。
- feedback report の観測処理、修復、publication と最終処理の流れを追う。
- session/run の join・abandon や realization の fork が連携する処理を調べる。

## Do not read this when
- CLI のコマンド登録、構文、オプション、起動時の互換処理を調べる場合は、CLI の入口を直接読む。
- Git 操作、プロセス追跡、状態管理、indexing など複数コマンドで共有する挙動を調べる場合は、共通 runtime の実装を直接読む。
- agent に渡す指示文や parameter の内容、または正本仕様を確認する場合は、対応する builder や oracle の仕様を直接読む。

## hash
- 23dd540833356ed991b93ee0866a813892301840802bef26cb23e96883d3ca1b
