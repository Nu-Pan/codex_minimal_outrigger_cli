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
- `doctor` サブコマンドの CLI 実行入口。doctor preprocess を明示的に実行し、実行ステップを表示したうえで repo_root を terminal result の詳細として返す。doctor コマンドの処理経路や preprocess 呼び出し、結果詳細の扱いを確認するときに読む。

## Read this when
- doctor サブコマンドの実行フローを変更・確認するとき
- doctor preprocess の明示実行方法や CLI ランタイムへの委譲を確認するとき
- doctor の terminal result に含まれる repo_root の由来を確認するとき

## Do not read this when
- doctor preprocess 自体の仕様や実装を確認する場合は、参照コメントが示す preprocess の仕様対象を直接読むとき
- doctor 以外のサブコマンドの処理を確認するとき
- CLI ランタイム共通処理の仕様だけを確認する場合

## hash
- 1891afa5229702961b641eebcc2aba8eacf0dd3a0e747225c5b766683628419f

# `feedback`

## Summary
- feedback サブコマンドの実装をまとめたディレクトリ。feedback 関連の処理を確認・変更するときの入口で、report cut の状態機械と publication・診断・再開処理を扱う下位実装へ進むために読む。

## Read this when
- feedback サブコマンドの挙動や実装を確認・変更するとき。
- `cmoc feedback report` の publication、incomplete 診断、中断・再開、checkpoint、cleanup、current pointer 切替を追跡するとき。
- feedback observation の validation、issue 集約、verification、report 出力の連携を調査するとき。

## Do not read this when
- feedback 以外のサブコマンドを扱うとき。
- feedback observation の一般的な envelope・raw store 仕様だけを確認するとき。
- 共通の feedback state、artifact 操作、lock、pointer 実装だけを確認するとき。
- issue normalization・verification agent の prompt や Structured Output schemaだけを確認するとき。
- 通常の Markdown report 描画だけを確認するとき。

## hash
- d7e59a4f0776547b55aff1fdec8a490a5b2fc6ea52d7e1509923aa49f32d771b

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
- 対象ディレクトリは、oracle 系サブコマンドの CLI 実装群への入口です。編集、調査、レビューの各サブコマンドと、レビュー対象列挙・実行ループ・レポート・パス処理などの専用実装へ進むための構成を扱います。

## Read this when
- oracle 系サブコマンドの CLI 実行フローや package 構成の入口を確認するとき。
- oracle edit、investigation、review のいずれかを調査・変更するとき。
- oracle review の対象選定、実行ループ、パス解決、レポート、INDEX 差分処理の担当箇所を特定するとき。

## Do not read this when
- 個別サブコマンドの prompt 契約や agent 起動パラメータなど、下位実装の詳細だけを確認したいとき。
- 共通 runtime、prompt editor、ACP builder など、oracle ディレクトリ外の共通実装を直接調査する場合。

## hash
- 1e3431e73d3697064b92ee41aaea48abeaa37f6510ba7b6a01200054e525e158

# `realization`

## Summary
- realization workload サブコマンドの実装をまとめるパッケージ階層。apply による成果物適用処理と、refactor によるリファクタリング処理への入口を提供する。

## Read this when
- realization workload サブコマンド全体の構成や、apply・refactor のどちらへ進むべきかを確認するとき。
- realization の workload 実装に関するサブコマンドの責務分担を調査するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。
- apply の実行ライフサイクルや fork report 保存の詳細だけを確認するときは apply 配下を直接読む。
- realization のリファクタリング処理の詳細だけを確認するときは refactor 配下を直接読む。

## hash
- 526e7d8b4cb8e735ee28786b035ac0d2826943dfc6781fb4eb6f015d6e8336f5

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
- editing run の共通 lifecycle サブコマンドをまとめるパッケージの入口。run の abandon・join と、旧 import path から再公開される lifecycle・report の移行状況を確認する際に読む。
- run の通常作成・編集処理の入口ではなく、配下の各実装へ進む前に、editing run の cleanup、統合、互換 shim の構成を把握するためのルーティング対象。

## Read this when
- editing run の lifecycle サブコマンド全体の構成や、abandon・join・互換 shim の担当範囲を確認するとき
- run の cleanup、merge、rollback、state・report 更新を含む lifecycle 挙動の調査先を判断するとき
- 旧 import path から commons 側の canonical 実装への移行状況や、互換 shim の削除可否を確認するとき

## Do not read this when
- run の具体的な作成・編集処理や、editing run 以外のサブコマンドを調べるとき
- 特定の abandon・join 処理、共通 lifecycle 実装、report writer の詳細を確認するときは、配下または commons 側の該当実装を直接読む
- 一般的な Git 操作、state・process tracking・report API、INDEX.md 生成規則そのものを調べるとき

## hash
- 3dd64c8b8d1611f19b565e707bc75e5fa80d998008bdc017d821e3564989462a

# `session`

## Summary
- session サブコマンドの実装パッケージ。session の fork、join、abandon に関する CLI 実行経路、branch 操作、session state 更新、失敗時の rollback や conflict 処理を確認するための入口。

## Read this when
- session サブコマンドの実装や構成を確認・変更するとき
- session の fork、join、abandon のライフサイクル処理を確認するとき
- session branch、home branch、session state の連携や、失敗時の復元処理を調査するとき

## Do not read this when
- session 以外のサブコマンドを扱うとき
- session state のデータ構造や共通 runtime API の仕様だけを確認するとき
- CLI 共通処理、Git branch 操作、Codex 実行や prompt 生成の共通規則だけを確認するとき

## hash
- 81d8e78b3feff700eed035b62266b8cb05c28182f2ca53c12b66c879af5d29bd

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
