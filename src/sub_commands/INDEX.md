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
- feedback サブコマンドの実装を集約する入口。サブコマンドの起動定義と、観測の集約から検証、checkpoint 再開、generation／Markdown／current pointer の publication、incomplete 診断、cleanup までの report pipeline を扱う。feedback サブコマンドの処理全体を確認・変更するときに読む。

## Read this when
- feedback サブコマンドの挙動や実装を確認・変更するとき
- feedback observation から issue candidate や machine aggregate を構築し、verification と report publication までの処理を調査するとき
- checkpoint 再開、中断時の状態更新、incomplete 診断、publication や cleanup の扱いを確認するとき

## Do not read this when
- feedback state の正本データ契約や状態遷移を確認するとき
- feedback report の利用条件や外部仕様を確認するとき
- normalization・verification の個別契約、共通 runtime state・store・logging・publication artifact の実装を直接確認するとき

## hash
- a4855ff6a0d145df272c92a3ad332349adb3119c0a25dc07cf191c1b8caa2686

# `indexing.py`

## Summary
- `cmoc indexing` サブコマンドの実行入口と本体を定義する。CLI 実行前の worktree 条件を検査し、ロック下で INDEX.md の更新と差分 commit を行うため、インデクシング処理の開始条件・実行手順・commit 動作を確認するときの入口となる。

## Read this when
- `cmoc indexing` の CLI 実行フロー、前提条件、worktree ロック、INDEX.md 更新、または更新結果の commit を調べるとき。

## Do not read this when
- INDEX.md の具体的なルーティング内容や生成規則を調べるとき。
- インデックス更新の内部処理を調べるときは `commons.indexing` を直接読む方が適切。
- CLI 共通の実行制御や worktree 検査の実装を調べるときは `cmoc_runtime` を直接読む方が適切。

## hash
- b6ca80b2815cc79bb34fdd9c72a3df659eaaea8b5bae9a5d3d1835a51d0aebd5

# `oracle`

## Summary
- oracle 系サブコマンドの実装をまとめる package。oracle edit、investigation、review と、それらの対象列挙・review loop・レポート・path 解決などの下位実装への入口を提供する。

## Read this when
- oracle サブコマンド群の構成や、各サブコマンドの実行入口を確認するとき
- oracle review の対象選定、実行 loop、レポート生成、INDEX 限定 merge など関連実装の所在を判断するとき

## Do not read this when
- 個別サブコマンドの詳細な実行制御を確認する場合は、該当する実装ファイルを直接読むとき
- oracle 文書の仕様、共通 prompt editor、agent 起動パラメータなど、別の正本仕様・共通実装が主対象のとき

## hash
- 9baebefb222289ac9bc7816f2986faa60aac56d0f8a115cef4a37294b9e1c84c

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口です。apply と refactor の各 workload 実装へ進むための上位ルーティング対象で、サブコマンド全体の構成や workload の選択を確認するときに読みます。

## Read this when
- realization サブコマンドの実装構成や、apply・refactor workload の入口を確認するとき。
- realization 配下で対象 workload が未特定のまま調査を開始するとき。

## Do not read this when
- apply workload の実行フローや fork lifecycle の詳細を確認する場合は apply へ直接進むとき。
- refactor workload の実行フローや対象ファイル処理の詳細を確認する場合は refactor へ直接進むとき。
- realization workload に関係しない処理を確認するとき。

## hash
- 59b55777e72514952e508c1806fd0f41a1b6a5c4e581adb2a54a4e262187b4e7

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
- editing run の共通 lifecycle サブコマンドをまとめるパッケージの入口。関連する run サブコマンドの共通処理を確認する際に読む。
- abandon は active editing run の停止・破棄と、worktree・branch・state・process tracking の cleanup lifecycle を扱う。
- join は active run の検証、branch merge、INDEX 再生成、state 同期、report、cleanup、および失敗時の rollback・再試行可能性を扱う。
- lifecycle と report は、それぞれ commons 側の canonical 実装を旧 import path から再公開する互換 shim である。

## Read this when
- editing run サブコマンドの共通 lifecycle や、その配下の実装を調査・変更するとき。
- cmoc run abandon の停止・破棄処理、cleanup 順序、worktree・branch の削除挙動を確認するとき。
- cmoc run join の merge、post-join、state 同期、report、cleanup、失敗時 rollback を確認するとき。
- 旧 import path による lifecycle 操作または run report writer の互換性を確認するとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。
- run の具体的な処理や workload 固有の処理を確認する場合は、この入口ではなく配下の該当実装を直接読むとき。
- worktree・branch・process 操作や共通 lifecycle・report writer の canonical 実装詳細を確認する場合は、インポート先の commons 側を直接読むとき。

## hash
- 6a97207376f4a7fe194c37979921e51cf211a75ae66be26b6557889056d3a921

# `session`

## Summary
- session サブコマンドの実装パッケージ。session のライフサイクル処理や構成を確認する際の入口で、個別の fork・join・abandon 実装へ進むためのルーティング対象。

## Read this when
- session サブコマンドの実装構成やライフサイクル処理を確認・変更するとき。
- session の fork、join、abandon など個別処理の実装を調査する前に、パッケージ全体の入口を把握するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- CLI 共通ランナー、Git 操作、session state の一般仕様など、共通実装や正本仕様を直接確認することが目的のとき。

## hash
- 7f1cfedbc25bb55290f8b96f0d1468ffe3ee6f86d17b244fa883e0d1ccd9d943

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
