# `__init__.py`

## Summary
- サブコマンド実装パッケージの入口として、パッケージの役割を短い docstring で示すだけの対象。
- 具体的な処理、公開 API、import 副作用、設定値は持たないため、実装詳細への入口ではなく、パッケージ単位の責務確認に限って使う。

## Read this when
- サブコマンド実装パッケージそのものに、パッケージ説明や初期化時の処理があるかを確認したいとき。
- パッケージ import 時に実行される処理や再 export が存在しないことを本文で確認したいとき。

## Do not read this when
- 具体的なサブコマンドの引数定義、実行処理、入出力、エラー処理を調べたいとき。
- 実装変更やテスト追加のために、実際の制御ロジックを読む必要があるとき。
- パッケージ説明の文言確認以外が目的で、同階層または下位の具体的な実装対象へ直接進めるとき。

## hash
- e5354bb58c94a87f51093db4681c6f341202c07abf4b77772fb37b788f40b7b1

# `abandon.py`

## Summary
- `cmoc apply abandon` の実行本体です。未 join の apply run を安全に破棄し、apply state を ready に戻すための判定、停止、worktree/branch 削除、state 更新、結果表示をまとめています。
- このファイルは、apply abandon の実行順序や安全条件を確認したいときに読む対象です。CLI の手続き全体を把握したい場合の入口になります。

## Read this when
- `cmoc apply abandon` がどの条件で実行可能か、何を削除し、どの state を戻すかを確認したい。
- apply run の破棄処理で、process 停止・branch/worktree 削除・state 初期化のつながりを追いたい。
- apply branch 上と session branch 上で挙動がどう分かれるかを確認したい。

## Do not read this when
- apply run の状態定義そのものを知りたい場合は、state 定義側を読む。
- worktree や branch の一般的な操作方法だけを知りたい場合は、共通 runtime や branch 操作の実装を読む。
- CLI の他の apply サブコマンドの仕様を知りたい場合は、それぞれのサブコマンド実装を読む。

## hash
- 628d23721070460f8552708ef4fce3582fa12871a65b0daa76867126b610fd4f

# `fork.py`

## Summary
- `apply fork` の実行制御をまとめる入口。session branch の前提確認、apply worktree 作成、所見列挙と適用、commit、state 更新、最終レポート出力までを追うときに読む。
- 同じ領域の補助実装として、対象ファイル候補の正規化・重複排除・列挙範囲決定・commit subject 生成・前回 join 後の merge commit 解決も含む。
- 所見列挙そのものや適用処理の詳細は別モジュールに委ねており、このファイルは apply loop の orchestration と失敗時復旧条件の把握に向く。

## Read this when
- `apply fork` の開始条件、進行ステップ、終了時の state/report の流れを確認したいとき。
- 調査対象ファイルの選び方、oracle と realization の扱い分け、重複除去、再調査の条件を確認したいとき。
- apply loop の中で commit を作る条件や、前回の join 以降の差分をどう再開するかを追いたいとき。

## Do not read this when
- 所見の抽出ロジックや Codex への具体的な問い合わせ内容だけを知りたいときは、所見列挙側の実装を見る。
- 所見の適用方法や Codex 実行パラメータの生成だけを知りたいときは、適用側の実装を見る。
- report の書式や永続 state の定義全体だけを知りたいときは、それぞれの責務に対応する別ファイルを見る。

## hash
- b8887dc1c4f44cb2cbe02c292709cae00945e4a4611e0f529277c6458eb68f6b

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を Markdown レポートとして保存する処理を担う。
- apply worktree 上の fork 起点以降の管理対象差分と未追跡ファイル差分を集め、Codex による変更要約または機械的な fallback 要約をレポートへ含める。
- 収束状態、所見数推移、apply branch や fork commit などの作業文脈を YAML frontmatter と本文に描画する。

## Read this when
- apply fork の作業レポート生成、失敗時レポート生成、保存先、frontmatter、本文構成を確認または変更したいとき。
- apply fork の変更内容要約がどの git diff 範囲、未追跡ファイル、fallback 条件から作られるかを確認したいとき。
- 未収束時の警告文、所見数推移、変更なし表示など、apply fork レポート上の利用者向け文言を扱うとき。

## Do not read this when
- apply fork のループ制御、所見列挙、作業ブランチ作成や worktree 管理そのものを確認したいだけのとき。
- Codex に渡す変更要約用パラメータの schema や prompt の詳細を確認したいとき。
- apply fork 以外のサブコマンドのレポート生成や git 差分取得を扱うとき。

## hash
- 690ca1ebff01a6a1ac9195d36ffc86e75bd1813b5048748f25df508d82db8524

# `join.py`

## Summary
- apply join の実行本体を扱う。session branch / apply branch の整合確認、想定外差分の判定、`--force-resolve` 時の復旧、`git merge`、状態更新、後始末までを一連の流れとしてまとめている。
- apply join の結果レポート生成と、想定外差分の分類・復元・rename 元追跡・INDEX.md だけの conflict 解消もここに含まれる。
- branch や worktree の一般的な runtime 操作は別モジュールに寄せ、このファイルは join 固有の制御と判定に読む。

## Read this when
- apply join の CLI 挙動、成功時の cleanup、失敗時メッセージや report 出力を変えたいとき。
- session branch と apply branch のどちらを対象にするか、どの差分を許可・禁止するか、`--force-resolve` で何を戻すかを確認したいとき。
- merge conflict の扱い、rename を含む想定外差分の分類、結果レポートの内容を追いたいとき。

## Do not read this when
- apply branch を作る・開始する・終了するなど join 以外の apply フローを追いたいときは、より直接の subcommand 実装を読む。
- branch/worktree の基礎操作だけを確認したいときは、このファイルより `cmoc_runtime` や `commons.runtime_apply` を先に読む。
- 単に `INDEX.md` や oracle 側の正本仕様を探しているだけなら、この実装ではなく oracle 文書を読む。

## hash
- f041901b929c362452351cfc4db5c1a6e3a959ad6026c20ca7bd42d70cea0519
