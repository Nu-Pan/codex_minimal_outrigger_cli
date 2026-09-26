# `acp`

## Summary
- `oracle.acp_builder` の機能を `acp.builder.*` 経由で使うための互換 import 層です。canonical package の `basic` と検索パスを公開し、各種 builder を再公開します。
- `quota_probe` は既存 API の引数から cwd を取り出して canonical builder に渡します。

## Read this when
- 既存の `acp.builder.*` import の解決、互換 adapter の保守、追加や削除を調べるとき。

## Do not read this when
- builder が組み立てる parameter の内容や動作を変更するときは、対応する `oracle.acp_builder` の実装を直接確認してください。
- どの command がこれらを呼び出すか、または command 自体の動作を調べるときは、import 元の command 側から確認してください。

## hash
- f53ee6777f891da19115922f44b5ae6ae51c69df977b395fb33f77b038ef286c

# `basic`

## Summary
- 正本側の ACP 型、パスモデル、構造化文書ノードを再実装せずに再公開し、従来の `basic` 名前空間の import 互換性を保つ入口です。文書描画では旧来の入力形式を正本 renderer に渡す変換も担います。

## Read this when
- 従来の `basic.*` 経由の import を維持・移行・削除する場合や、互換層の公開名を確認する場合。
- 互換層に依存する実行時利用箇所を追い、移行や削除が可能か調べる場合。

## Do not read this when
- ACP 型、パス解決、構造化文書モデルや描画の正本挙動・仕様を変更または調査する場合は、正本実装や仕様へ直接進んでください。この層はそれらの定義を持たず、名前の再公開と旧入力形式の変換を担います。
- 従来の import 互換性に関係しない新しい処理を実装する場合は、対象となる正本 API を直接確認してください。

## hash
- fba8b1754e82c009f9cbef23688c4e14663036989629fee696f1fedddf4b8d8f

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
- 複数のコマンド経路で共有する実行基盤をまとめ、CLI の終端処理、ログとレポート、パスと設定、Codex の起動・回復などを扱う。
- Git と worktree、session と editing run の状態遷移・結合・後処理、doctor と refactor の同期を支える。
- feedback の受理・保存・状態管理、oracle 文書検索、editor input handoff、Windows 通知などの共通処理を含む。
- 文書検索には、固定資材を検証して Node 推論へ渡す境界と、その Node worker も含む。

## Read this when
- 複数のコマンドから使われる実行ライフサイクルや設定・パス処理の変更箇所を探すとき。
- Codex subprocess の起動条件、出力処理、回復、TUI 記録など、呼び出し境界の挙動を追うとき。
- Git/worktree、session・editing run、doctor の状態遷移や後処理を調べるとき。
- feedback の受理から保存・状態管理まで、または文書検索や editor input handoff の共通 transport を調べるとき。

## Do not read this when
- 個別サブコマンドの利用者向け手順や固有の実行順序だけを調べるときは、そのコマンドの実装へ進む。
- 意図された挙動や受け入れ条件を確認するときは、実装補助ではなく正本の oracle 仕様を読む。
- Node 文書検索 worker の内部実装や依存関係だけを変更・調査するときは、worker のサブディレクトリへ直接進む。

## hash
- e8d4fdc2d684b532bee776e872727735fdbb0558f33784237b8ade153f1f2284

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
- Typer による CLI のコマンド構成と各処理への接続、および起動時の Click/Typer 互換処理を担う。
- CLI 引数解析エラーの cmoc 形式への変換や、補完 probe の実行境界も定義する。

## Read this when
- コマンドや option の追加・削除・階層変更、引数解析時のエラー処理、補完 probe の挙動を変更するとき。
- Click/Typer の help 表示や metavar の互換性、CLI の起動方法を調べるとき。

## Do not read this when
- 個別コマンドが呼び出された後の処理を変更するときは、そのコマンドの実装を直接確認する。
- 共通エラーレポートの生成内容を変更するときは、エラー描画を担う共通実装を直接確認する。

## hash
- 152356060879923b4fdaa428fe03ce05434e993db66c94dbc2cd0660a39f76f1

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
- 個別 CLI サブコマンドの処理本体をまとめ、doctor preprocess、文書検索索引の同期、Codex TUI の起動を扱う。
- oracle の編集・調査、realization の apply・refactor、session と editing run の lifecycle、feedback の報告・修復・判定履歴・publication 後の復旧を扱う。共通 runtime や各種 helper の実装ではなく、コマンド固有の処理を担う。

## Read this when
- doctor preprocess、文書検索索引の同期、または依頼文から TUI を起動する CLI 処理を変更するとき。
- oracle、realization、session、run、feedback のコマンド固有の処理や状態遷移を変更するとき。
- コマンド処理から共通 runtime や補助機能をどう呼び出すか確認するとき。

## Do not read this when
- コマンドの登録、引数解析、または処理本体への振り分けだけを変更するときは、CLI の入口を確認する。
- 特定の処理群の変更だと分かっている場合は、その下位の処理群から確認する。共通 runtime、検索、prompt 構築などの機能自体を変更するときは、その実装を直接確認する。

## hash
- 9aab087dd91f9645802cd0084a8565e2fb34f083432839325f85a1667eb5ba82
