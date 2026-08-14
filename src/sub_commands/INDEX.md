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
- oracle 系サブコマンドの実装を収める package。edit、investigation、review の CLI 入口と、review の対象列挙・所見処理・パス解決・レポート・INDEX 差分統合を扱う。各サブコマンドの実行フローを確認した後、詳細処理は対応する下位モジュールへ進む。
- edit.py は `cmoc oracle edit` の入力予約、完全プロンプト確定、main worktree と active session branch の検証、Codex TUI 起動を統括する。
- investigation.py は `cmoc oracle investigation` の調査指示入力、完全プロンプト確定、設定読込、Codex TUI 起動を統括する。
- review.py は `cmoc oracle review` の isolated worktree lifecycle を統括し、review 対象作成、review loop、INDEX 差分の merge、中断・失敗時の cleanup と report 生成を扱う。
- review_index.py は review worktree の変更を INDEX.md に限定して検査・commit し、review branch の merge、INDEX.md 競合解決、merge 失敗後の復旧を扱う。
- review_loop.py は oracle review の finding 列挙、重複 finding の merge、challenger・advocate による反復検証、judge による採否判定、finding merge operation の適用を扱う。中断時の部分進捗も呼び出し元へ返す。
- review_paths.py は finding の oracle_path を解決し、main repository と isolated worktree の境界を考慮した repository-relative key を生成する。symlink は追跡しない。
- review_report.py は oracle review の Markdown report と YAML frontmatter を生成・保存し、verdict、評価対象、finding の分類・表示順を決める。
- review_targets.py は review scope に応じて oracle review 対象を列挙する。full scope では全 oracle file、session scope では session fork commit から review fork commit までに変更された oracle file を返す。

## Read this when
- oracle サブコマンドの CLI 入口、入力から TUI 起動までの実行経路を確認・変更するとき。
- oracle review の isolated run、worktree・branch lifecycle、中断・失敗時の cleanup、report 生成を確認するとき。
- oracle review の finding 列挙・統合・検証・判定、対象ファイル選定、パス正規化、report 出力、INDEX 差分 merge のいずれかを調査・変更するとき。

## Do not read this when
- oracle サブコマンドの利用者向け契約や実行仕様そのものを確認するときは、対応する正本仕様を直接読む。
- TUI の起動パラメータ、プロンプト入力管理、共通 runtime、個別 review agent の prompt や Structured Output schema の詳細だけを確認するときは、各 import 先の実装を直接読む。
- oracle review と無関係な一般 CLI や別サブコマンドの処理を調査するとき。

## hash
- 53ea6c375bf3bf031b94d62d7c7d48aca6adaeda60fd90a00a2d4f851a369798

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
- `cmoc tui` サブコマンドの CLI 実行入口と本体処理を定義する。インデックス前処理、プロンプト編集入力の予約・収集・確定、固定パラメータによる Codex TUI 起動を扱う。TUI サブコマンドの起動フローや、現在の repository/work context からの実行経路を確認するときの入口。

## Read this when
- `cmoc tui` の CLI runtime、起動手順、ステップ数、ログ前処理を変更または確認するとき。
- オリジナルプロンプトを編集して完全な起動プロンプトを確定し、Codex TUI を呼び出す処理を追跡するとき。
- repository の現在コンテキストから設定を読み込み、TUI 実行へ渡す経路を確認するとき。

## Do not read this when
- TUI 起動パラメータの具体的な構築規則だけを確認する場合は、TUI parameter builder を直接読む。
- プロンプト編集入力の保存・入力検証・ルート除外の仕様だけを確認する場合は、prompt editor 関連モジュールまたは正本仕様を直接読む。
- Codex TUI 自体の実行実装や共通 CLI サブコマンドの汎用制御だけを確認する場合は、呼び出される runtime モジュールを直接読む。

## hash
- 1dbb1c380550c5e0e896083956f1c7d480a83c3cc50b4d24946fab436b41aeac
