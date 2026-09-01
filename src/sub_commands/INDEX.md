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
- `cmoc doctor` サブコマンドの実行入口。CLI ランタイム経由で doctor preprocess を明示的に実行し、処理結果に repo_root を含める。
- doctor サブコマンドの実行手順や preprocess 呼び出し、TerminalResult の固有情報を確認・変更するときの入口。実行基盤そのものや preprocess の仕様・実装を確認する場合は、参照先のランタイムまたは preprocess 文書へ進む。

## Read this when
- doctor サブコマンドの実行フロー、doctor preprocess の起動、または doctor 固有の TerminalResult を調べるとき。
- `cmoc doctor` の CLI 接続や、doctor preprocess を明示的に実行する責務を変更するとき。

## Do not read this when
- doctor preprocess の詳細仕様や処理内容だけを確認したいとき。
- CLI ランタイム共通の実行制御や、doctor 以外のサブコマンドの挙動を確認するとき。

## hash
- f3c8753693352207cc3092f5d4ea63ab9c38554a03bfaa451bcce6c7a1ebb851

# `feedback`

## Summary
- feedback サブコマンド実装の入口。feedback 関連の CLI 処理を確認・変更するときに参照する。
- 固定済み report cut を起点に、feedback report の検証、checkpoint 管理、issue・machine 集約、candidate 検証、正常 publication、incomplete 診断を処理する。feedback report の実行経路や状態遷移を調べる際の中心的な実装対象である。

## Read this when
- feedback サブコマンドの実装や CLI 入口を確認・変更するとき。
- feedback report の report cut 固定、再開・中断・失敗処理、cleanup、checkpoint、writer lock、current pointer の挙動を調べるとき。
- feedback observation の検証結果を用いた normalization、verification、candidate 集約、正常 publication、incomplete 診断の処理を調べるとき。
- feedback state と feedback report の仕様に対する実装対応を確認するとき。

## Do not read this when
- feedback report 以外のサブコマンドを扱うとき。
- feedback observation の入力形式や raw store の保存処理だけを調べるときは、観測入力と保存を直接定義する対象を先に読む。
- issue normalization・verification 用の agent prompt や Structured Output schema だけを調べるときは、それぞれの builder・schema を直接読む。
- report の Markdown 表示形式だけを確認するときは、report rendering を仕様化する対象を先に読む。

## hash
- 247bd90db7c4b0a6ae3200d51a272f144142be3e05b33c1e8f81a1ead4a0263c

# `indexing.py`

## Summary
- CLI の indexing サブコマンドを実行するランタイム入口。実行前に worktree の安全条件を検査し、排他制御下で INDEX.md の更新・差分 commit・実行結果の primary report 反映までを統括する。indexing CLI の実行フローや、更新・commit の責務を確認する際の入口となる。

## Read this when
- indexing サブコマンドの実行手順、安全条件、排他制御、INDEX.md 更新または commit 処理を変更・調査するとき
- indexing 実行結果として更新件数、commit ID、更新対象一覧がどのように報告されるか確認するとき

## Do not read this when
- INDEX.md の生成規則や個別ファイルの内容を確認するだけで、indexing CLI の実行フローを扱わないとき
- CLI 共通実行基盤や INDEX.md 更新処理そのものの詳細を直接確認する必要があり、それぞれの実装対象へ進めるとき

## hash
- 5b254b536c60d465922e7592e423030a458acf28d2899bef100dd4163d6f7c26

# `oracle`

## Summary
- oracle 系サブコマンドの package 境界を示し、oracle サブコマンド群への入口となる。
- `cmoc oracle edit` の入力収集、起動前提の検証、本命 oracle 編集 agent call と仕様削減 agent call の実行フローを担う。
- `cmoc oracle investigation` の調査指示入力、完全プロンプト構築、Codex TUI 起動までの read-only 実行フローを担う。
- 編集関連の実装ファイルを含まない空のディレクトリで、現時点の下位要素へのルーティング先はない。

## Read this when
- oracle 系サブコマンドの package 構成や入口を確認するとき。
- `cmoc oracle edit` の CLI フロー、入力編集、本命・仕様削減 agent call の起動条件や実行順序を確認するとき。
- `cmoc oracle investigation` の CLI フロー、調査指示編集、プロンプト構築、Codex TUI 起動を確認するとき。
- このディレクトリに編集関連ファイルが追加されたか確認するとき。

## Do not read this when
- 個別 oracle サブコマンドの prompt 契約や仕様そのものを確認したいとき。
- prompt editor の共通入出力処理だけを確認したいとき。
- oracle edit の agent 起動パラメータ構築だけを確認したいとき。
- oracle investigation の TUI 起動パラメータや共通 runtime の詳細だけを確認したいとき。
- oracle サブコマンドの実装を調査するときに、空の編集ディレクトリだけを確認しようとしているとき。

## hash
- ed0e9b8fea43533d9ad7c042135f4f82804bdc36036c330a8498b11afa88fc9a

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口であり、配下の apply workload と refactor 処理へ進むためのディレクトリ。
- apply 配下では realization apply の workload、特に fork 実行のライフサイクルや run state、差分検証、commit/rollback、report、cleanup を扱う。
- refactor 配下では realization file の refactor fork における対象選択、state・INDEX 初期化、agent 委譲、変更検証、commit/rollback、完了判定、report 保存を扱う。

## Read this when
- realization workload サブコマンドの実装構成や入口を確認するとき。
- realization apply workload、特に cmoc realization apply fork の処理順序や成功・失敗時の動作を確認・変更するとき。
- realization refactor、特に cmoc realization refactor fork の lifecycle、対象選択、state 管理、変更検証、完了判定を確認・変更するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。
- realization apply や refactor の仕様、共通 runtime、共通 editing run、一般的な run join・abandon の契約を確認するとき。
- fork 以外の realization apply サブコマンド固有処理、個別 realization file の agent prompt、変更概要生成の Structured Output や prompt、INDEX 更新の一般仕様だけを確認するとき。

## hash
- 16f438305634d5f5e7f1d84e4467b142603b3f7b61da6250278c7a6daaad750f

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
- editing run サブコマンドの共通 lifecycle 実装と、関連する abandon・join・旧 import path 互換 shim の入口。active run の停止、merge、cleanup、state・report 更新などの実装経路を確認する際に、配下の該当ファイルへ進むために読む。

## Read this when
- editing run サブコマンドの共通 lifecycle や配下の実装を横断して確認するとき。
- run abandon の停止、cleanup、state 更新、失敗時の再試行可能状態を調べるとき。
- run join の merge 前後処理、INDEX 再生成、rollback、report 保存、cleanup を調べるとき。
- 旧 import path の互換 shim と canonical 実装への委譲関係を確認するとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。
- run の正本仕様や状態遷移を確認するときは、対応する app_spec・lifecycle 仕様を直接読む。
- workload 固有の編集・apply・refactor 処理を確認するときは、対応する workload 固有の実装を直接読む。
- 共通 runtime helper や report writer の具体的な挙動を確認するときは、canonical 実装を直接読む。
- 旧 import path との互換性が関係しない場合は、lifecycle.py や report.py の shim を読む必要はない。

## hash
- bf31b65cdb0353a73a14c0edd0e7dd69845bdd50bbe2cdc0aa876f71b4105f2b

# `session`

## Summary
- session サブコマンドの実装パッケージで、session の各ライフサイクル操作を確認する際の入口。`abandon`、`fork`、`join` の CLI 実装を扱い、branch 操作、session state 更新、失敗時の復旧、merge conflict 解消などの個別処理へ進める。

## Read this when
- session サブコマンドの実装や構成を確認・変更するとき
- session の abandon、fork、join における branch 操作、state 更新、rollback、merge conflict 処理を調べるとき

## Do not read this when
- session 以外のサブコマンドを扱うとき
- session state の正本仕様、一般的な Git branch 操作、CLI 共通処理、state 永続化など、配下の個別実装より対応する仕様書や共通機能の対象を直接読むべきとき

## hash
- 028294677a2cec33fe38538e3f03d84e144e7676317ae304fe2cd37957e58026

# `tui.py`

## Summary
- `cmoc tui` サブコマンドの実行入口。indexing preflight と入力編集前の検査を有効にし、現在のリポジトリ状態から TUI 起動処理へ接続する。
- 完全プロンプトの skeleton を構築し、利用者が編集したオリジナルプロンプトを収集・確定して、TUI 起動パラメータと現在の設定を用いて Codex TUI を起動する。

## Read this when
- `cmoc tui` の CLI 実行経路や、現在の repository/worktree context からの起動方法を確認するとき
- プロンプト編集入力、完全プロンプトの構築、TUI 起動処理がどの順序で連携するかを確認するとき

## Do not read this when
- TUI 起動パラメータの詳細な構築仕様を確認したいときは `build_tui_launch_tui_parameter` の実装または正本仕様を直接読むとき
- プロンプト編集用の予約・収集・確定処理の詳細を確認したいときは `commons.prompt_editor_input` を直接読むとき
- 一般的な CLI サブコマンドの実行制御や結果処理を確認したいときは `cmoc_runtime` を直接読むとき

## hash
- f1bd5b17ca50cb086ffade1c5b37da290a1b11719bd28de5ce570d1dc2804701
