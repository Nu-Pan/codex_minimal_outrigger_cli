# `apply`

## Summary
- 現在、apply サブコマンドの実装ファイルはありません。

## Read this when
- apply サブコマンドの実装が追加された後、その内容を確認するとき。

## Do not read this when
- apply 以外のサブコマンドを扱うとき。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `doctor.py`

## Summary
- `cmoc doctor` の CLI 入口を提供する。
- CLI runtime 経由で doctor preprocess を明示的に 1 ステップ実行する。
- 実行結果に現在の repo root を固有情報として返す。

## Read this when
- `cmoc doctor` のサブコマンド入口や、doctor preprocess の明示実行経路を確認するとき。
- doctor 実行時のステップ定義や terminal result に含まれる repo root 情報を確認するとき。

## Do not read this when
- doctor preprocess の具体的な処理内容や成果物を確認したいとき。
- CLI サブコマンド共通 runtime の実装や一般的な実行制御を確認したいとき。

## hash
- 1eb417245f2ab7964031bcace08e76c91beda19e6b7c26b38e163f2ec9977c3b

# `feedback`

## Summary
- feedback サブコマンドの実装入口。観測の集約・issue 判定・修復・publication・終了後の復旧を扱う配下実装への入口となる。

## Read this when
- feedback サブコマンドの処理全体を確認・変更するとき。
- 観測から report publication、remediation、run の finalization・recovery までの責務分担を把握するとき。

## Do not read this when
- feedback 以外のサブコマンドを扱うとき。
- feedback の個別処理だけを調べる場合は、判定・報告・修復・復旧を担当する配下対象を直接読むとき。
- 共通の run lifecycle、state、artifact、agent prompt の実装だけを調べるとき。

## hash
- 46b824ee861751bfa69426cb890c01880f3d4ef0f2ca14e1cb80e297f8e5629c

# `indexing.py`

## Summary
- work root の INDEX.md を更新する indexing CLI の実行入口を提供する。
- 実行前に cmoc 管理対象と clean worktree を確認し、排他ロック下で INDEX.md を更新・差分 commit し、結果を primary report に反映する。

## Read this when
- `cmoc indexing` の CLI 入口、実行前提条件、または indexing 処理全体の実行フローを確認するとき
- INDEX.md の更新、更新差分の commit、または indexing 実行結果の報告処理の呼び出し元を確認するとき

## Do not read this when
- INDEX.md の具体的な更新規則や探索・生成ロジックを確認したいときは、indexing 共通処理の対象を直接読む
- CLI 共通の実行制御や step 管理の仕様だけを確認したいときは、CLI runtime 共通処理の対象を直接読む
- worktree の clean 判定や cmoc 管理対象の検査実装だけを確認したいときは、対応する runtime 検査処理を直接読む

## hash
- 1b5fb1518b06f7acdfb54acdb2e8ab410c4772fa381bae42ed1af943e6209ce0

# `oracle`

## Summary
- oracle サブコマンド群をまとめる package 境界で、配下の oracle 実装へ進む入口。
- 編集系と調査系の oracle サブコマンド実装を含み、それぞれの実行入口や処理順序を確認する際の案内先。

## Read this when
- oracle サブコマンド群の構成や、編集・調査の実行入口を確認するとき。
- oracle サブコマンドの処理フローを調べる際に、個別実装へ進む前の package 境界を把握したいとき。

## Do not read this when
- `cmoc oracle edit` の具体的な prompt、起動パラメータ、入力・runtime など個別仕様を確認したいときは、編集サブコマンドの実装を直接読む。
- `cmoc oracle investigation` の具体的な起動パラメータや共通処理を確認したいときは、調査サブコマンドの実装または共通モジュールを直接読む。

## hash
- 456170d0023177b8d7c1f88de8f89137bcb75bb6fb6530543e9ea7dcdd0ba8cc

# `realization`

## Summary
- `realization` サブコマンド配下の workload 実装をまとめるディレクトリ入口。apply と refactor の各処理へ進むための上位ルーティング対象。

## Read this when
- realization サブコマンドの workload 構成や、apply／refactor の処理入口を確認するとき。
- realization 配下で apply または refactor の workload 実装を調査・変更するとき。

## Do not read this when
- realization サブコマンド以外の処理を扱うとき。
- apply または refactor の具体的な lifecycle・実装詳細だけを確認したい場合は、対応する下位対象を直接読む。

## hash
- 485bfb2542457396c18017597ca6537502902f62230f1c638da651edbaddf10d

# `review`

## Summary
- review サブコマンドの realization 実装を配置するディレクトリ。現在は実装本文がなく、レビュー処理の具体的な入口として参照できる下位要素はない。

## Read this when
- review サブコマンドの実装ファイルを追加・変更する場所を確認するとき。

## Do not read this when
- oracle review の処理内容や仕様を調べるときは、対応する oracle 実装・仕様文書を直接読む。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `run`

## Summary
- 日本語の技術文書として、対象ディレクトリにある editing run のライフサイクル関連実装への入口。abandon・join の停止／統合／cleanup と、旧 import path の互換 shim を含む配下を、run lifecycle の共通処理やサブコマンド固有処理の調査時に振り分ける。

## Read this when
- editing run の停止・統合・cleanup・report・状態遷移など、複数の run lifecycle 実装を横断して確認するとき。
- `cmoc run abandon` または `cmoc run join` の処理入口を探すとき。
- 旧 import path の lifecycle／report 互換性を確認するとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。
- 共通 lifecycle の canonical 実装や workload 固有の merge・差分処理など、配下の特定実装を直接確認すべきとき。
- run 作成・通常編集・差分生成など、abandon／join のライフサイクル範囲に直接関係しない処理だけを調べるとき。

## hash
- b692c0592ebbf0f3b0b5fd155b8143d42f7edb6c6653a1301d983d594801c52c

# `session`

## Summary
- session サブコマンドの各実行処理をまとめた実装パッケージ。session の fork・join・abandon を調べる際の入口となる。

## Read this when
- session サブコマンドの fork・join・abandon の実装、実行条件、状態遷移、branch の作成・merge・削除、失敗時の rollback を確認・変更するとき。
- session lifecycle の処理を横断して、個別サブコマンドの実装へ進む入口を探すとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- SessionState のデータ形式や共通 CLI 実行基盤など、session サブコマンド個別処理ではなく共通仕様を直接確認したいとき。

## hash
- 89bf0eb4e153eff8d5e63bc4b85e0397a541efcf3443452c57179100b082497e

# `tui.py`

## Summary
- 利用者の依頼文を編集し、TUI 起動用の完全プロンプトとパラメータを構築して Codex TUI を実行する `tui` サブコマンドの本体処理。
- 現在の repository と設定を取得し、プロンプト入力の予約・編集・収集・確定を経て、AI Agent TUI の起動へ進む入口。

## Read this when
- `cmoc tui` の CLI 実行経路、プロンプト編集フロー、TUI 起動パラメータの構築、または Codex TUI の起動処理を確認・変更するとき。
- TUI サブコマンドが現在の repository 状態や設定をどのように読み込み、入力編集から起動までを接続しているかを調べるとき。

## Do not read this when
- TUI 起動パラメータの内容や構築規則そのものを確認したいときは、参照される TUI parameter builder を直接読む。
- プロンプト編集の予約・入力収集・確定の仕様を確認したいときは、prompt editor input の担当実装を直接読む。
- 共通 CLI 実行制御、設定読み込み、repository・work root の解決の仕様を確認したいときは、それぞれの runtime 実装を直接読む。

## hash
- b935bdedceb7574ad8a75f38c8fb3dc4750ea131140116b8658328016ddc18ac
