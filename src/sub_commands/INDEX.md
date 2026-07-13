# `apply`

## Summary
- `src/sub_commands/apply` 配下の `cmoc apply` 実装群への入口。各 subcommand の実行本体と、実行結果レポート生成の責務境界を確認したいときに使う。

## Read this when
- `cmoc apply` 系の実行フローや失敗時の状態遷移を追いたいとき。
- `abandon`・`fork`・`join` のどれが目的の処理かを切り分けて、該当実装へ進みたいとき。
- apply レポートの生成や保存条件を確認したいとき。

## Do not read this when
- 共通の Git runtime や session/state 基盤だけを確認したいときは、より下位の共通実装へ直接進む。
- `cmoc apply` 以外の subcommand の入出力や CLI 定義だけを見たいとき。
- 対象 subcommand がすでに分かっていて、その個別実装へ直接進めるとき。

## hash
- 3b1c668aa2a015c4fc50ad4b40711c4325069bcdc42379b387db9dc1b83e3677

# `doctor.py`

## Summary
- doctor サブコマンドの実処理として、CLI runtime の preprocess 実行経路へ処理を委譲する薄い入口。doctor 固有の処理内容はここでは持たず、明示的に doctor preprocess を起動する責務だけを持つ。

## Read this when
- doctor サブコマンドが呼ばれた時に、どの runtime preprocess 名へ委譲されるかを確認したいとき。
- doctor サブコマンドの実装入口と、runtime preprocess 実行処理との接続を変更または確認したいとき。

## Do not read this when
- preprocess command の実行方法、失敗時挙動、runtime 側の制御を調べたいときは、preprocess 実行を担う commons 側の実装を読む。
- doctor preprocess の中身や診断項目を調べたいときは、その preprocess 本体を読む。

## hash
- 13b0493ce99287b1643522676065d9b8d003da0fc0cc55a3423864c0541091a8

# `eval_oracle.py`

## Summary
- want を書き出した oracle 評価を、review oracle と同じ実装経路へ委譲する薄い入口。eval oracle 側に独自の評価処理を持たせず、評価本体は review oracle 実装に集約する。

## Read this when
- eval oracle サブコマンドがどの評価実装へ接続されるかを確認したいとき。
- want を書き出した oracle の評価経路と review oracle の評価経路が同一であることを確認したいとき。
- eval oracle 用の入口関数や委譲先を変更する必要があるとき。

## Do not read this when
- review oracle の評価処理本体、出力、検査内容を確認したいときは、委譲先の review oracle 実装を読む。
- oracle 評価の根拠となる正本仕様や working plan review の意図を確認したいときは、対応する oracle doc を読む。
- CLI の引数定義やサブコマンド登録を確認したいだけのときは、CLI 構成側の実装を読む。

## hash
- aa69d5ae36aec1c3d31050a5ce5880c23ecaa6c7edd6a3d605751ccaf75a2501

# `indexing.py`

## Summary
- `indexing` サブコマンドの実行入口をまとめる。CLI runtime 経由で事前検査を通し、work root に対する INDEX.md 更新とその commit を 1 本の処理としてつなぐ。
- この対象は、indexing 実行の開始条件と外形的な実行順序を知りたいときに読む。個々の index 更新ロジックやロック実装の詳細を追う場所ではない。

## Read this when
- `indexing` サブコマンドがどの前提条件を満たしたときに動くかを確認したい。
- 更新対象が current work root であること、更新後に差分を commit すること、出力される更新件数の要約を知りたい。
- CLI からの起動経路と、実処理本体・事前検査の分担を確認したい。

## Do not read this when
- INDEX.md の更新内容そのものや、更新アルゴリズムの詳細を知りたい場合は `commons.indexing` 側を見る。
- worktree の安全性チェックの中身だけを知りたい場合は、事前検査を定義している別の実装を見る。
- ロック機構や CLI runtime の共通処理を追いたい場合は、この対象ではなくそれぞれの共通実装を見る。

## hash
- ac15b45b7cb7a153e387d30a8cacf12ed7fb4fa6b1b4b4ce14763b3841eb8d88

# `review`

## Summary
- `review` 系サブコマンド群の package 境界だけを示す最小の初期化モジュールで、具体的な処理や公開 API は持たない。
- `oracle.py` は `cmoc review oracle` の実行入口で、起動前提の確認から isolated review worktree の作成・削除、必要時の merge、所見レポート出力までの全体制御を担う。

## Read this when
- review 系サブコマンド群の package 境界そのものを確認したいとき。
- この階層が review 系サブコマンド用の Python package として扱われる根拠を確認したいとき。
- `cmoc review oracle` の実行フロー全体を確認したいとき。
- isolated review worktree の作成・削除、review branch の merge 条件、レポート出力までの制御を追いたいとき。
- review 実行の前提条件として、active session branch かどうか、git 未コミット差分がないかを確認したいとき。
- 対象 oracle の列挙や所見処理そのものではなく、それらをどう組み合わせて実行しているかを見たいとき。

## Do not read this when
- review 系サブコマンドの具体的な CLI 挙動、引数、出力、制御フローを調べたいとき。
- review 系サブコマンド内の個別機能や実装詳細を調べたいとき。
- package 初期化時の import、副作用、公開シンボルを調べたいとき。
- review 対象 oracle file の選定規則だけを知りたいとき。
- 所見の列挙・整理・擁護・反証の処理本体を追いたいとき。
- review branch の INDEX.md 反映や merge 失敗時の競合解決だけを確認したいとき。
- レポートの Markdown 形式や集計表示だけを確認したいとき。
- このサブコマンドの CLI 登録や引数定義だけを確認したいとき。

## hash
- 2aa5e427bc725a82d683da533801858fbf9f10adcb9dc77e5ed5d14d4f5c1a3c

# `review_index.py`

## Summary
- review 用 worktree/branch に生じた差分を INDEX.md のみに制限し、必要な INDEX.md 変更だけを commit する処理を扱う。
- review branch を session branch へ merge し、競合が INDEX.md だけの場合に ours 側採用または削除で自動解決して merge commit を完了させる処理を扱う。
- git status、diff、merge、checkout、rm、commit を通じて review oracle indexing の差分検査・確定・取り込みを行う入口である。

## Read this when
- review oracle が作った差分に INDEX.md 以外が混ざった場合のエラー条件や確認方法を調べるとき。
- review worktree 上の INDEX.md 変更を commit する条件、commit しない条件、戻り値を確認するとき。
- base commit 以降の review branch 差分が INDEX.md だけであることを検査する処理を確認するとき。
- review branch の merge 失敗時に、INDEX.md 競合だけを自動解決する挙動を変更・確認するとき。
- review oracle indexing と review branch merge の git コマンド呼び出し順や失敗時の CmocError を追うとき。

## Do not read this when
- INDEX.md エントリー本文の生成規則や preflight indexing 全体の仕様を確認したいだけの場合は、対応する oracle doc を読む。
- git コマンド実行ラッパー、HEAD commit 取得、status path 収集の共通処理そのものを変更したい場合は、それらの runtime/helper 側を読む。
- review oracle のプロンプト、分離 worktree の作成、または subcommand 全体の制御フローを調べたい場合は、上位の review command 実装を読む。
- INDEX.md 以外の通常ファイル差分を merge・解決する汎用的な仕組みを探している場合は、この対象ではない。

## hash
- 500e71a4ff36cb5a35cbc12a4bb56b76f82c137800554580654c20e984e4fc66

# `review_loop.py`

## Summary
- `cmoc review oracle` の所見処理本体を扱う。新規所見の列挙、所見の統合、反証と擁護による再検証、採否判定、merge operation の妥当性検証と適用をまとめて読む入口である。
- 対象は review 実行の全体制御ではなく、所見リストの反復処理と `finding_id` を中心にした状態遷移である。レビュー対象 oracle の選定や最終レポート生成とは責務が分かれている。

## Read this when
- 所見がどの順序で列挙・マージ・検証・判定されるかを確認したいとき。
- merge finding の edit operation を所見リストへどう適用し、どの条件で `ValueError` や `CmocError` にするかを確認したいとき。
- `finding_id` の再利用禁止、dirty 判定、semantic retry の扱いを変更・確認したいとき。

## Do not read this when
- review 対象 oracle file の選定条件だけを知りたいときは `review_targets` を読む。
- `cmoc review oracle` の起動前提、隔離 worktree の作成・削除、branch merge、レポート保存までの全体制御を追いたいときは `oracle.py` を読む。
- finding の oracle_path 解決や path 正規化だけを確認したいときは `review_paths.py` を読む。
- レポート本文の Markdown 形式や集計順序だけを知りたいときは `review_report.py` を読む。

## hash
- 1a9502524bec53e191e887bd16e5e0d850cbaf2dc8b4947c411de7e014da5ea2

# `review_paths.py`

## Summary
- レビュー結果で見つかった oracle の path を、symlink を追わない絶対 path や oracle 配下の repository-relative key に正規化するための変換関数を置く。isolated worktree 上の評価と main worktree 起点の finding を同じ oracle の所属判定へ揃える役割が中心で、境界外の path は無視する。

## Read this when
- finding に含まれる oracle_path の正規化方法を確認したいとき.
- main worktree と isolated worktree をまたぐ oracle file の所属判定や key 化の挙動を変えたいとき.
- oracle 配下の path を report 評価用にどう解釈するかを調べたいとき.

## Do not read this when
- レビュー対象の oracle 側の仕様本文を確認したいだけなら、対応する oracle doc/src を読むべきで、この file は読まない.
- oracle 以外の realization path 変換や一般的な path 操作を探しているなら、より直接の実装を読むべきで、この file は読まない.
- finding 生成やレビュー判定ロジックそのものを追いたいだけなら、変換後の利用先を読むべきで、この file は読まない.

## hash
- c7a2397ddcdf2ab7cd9fa1f3de046e53590e4c3bb75128456f73fdcdcd38a660

# `review_report.py`

## Summary
- review oracle レポートの Markdown 生成を担う。`write_review_oracle_report` は保存先ディレクトリを作って、`render_review_oracle_report` の出力を timestamp 名の report ファイルとして書き込む入口である。
- この対象は、review oracle の出力形式、前提条件、判定文言、frontmatter、oracle file ごとの集計表、finding の並び順や見せ方を確認したいときに読む。
- 補助関数は、finding の severity/verdict ごとの振り分け、結果判定、frontmatter の整形、finding セクションの描画、oracle file 表示名の正規化をまとめて扱う。

## Read this when
- review oracle のレポート本文や frontmatter の項目を変更したいとき。
- finding の集計方法、accept/reject の扱い、fatal/minor の見せ方を確認したいとき。
- oracle file の表示名や、レポート内での path 集計キーの扱いを変えたいとき。
- レポートの保存先・ファイル名・生成タイミングを確認したいとき。

## Do not read this when
- review oracle の検出ロジックや finding 生成ロジックだけを追いたいときは、finding を作る側のサブコマンドや review paths 側を先に読む。
- report の保存先ディレクトリの共通ルールだけを知りたいときは、`reports_dir` や timestamp を定義している共通モジュールを読む。
- このファイルは report の描画専用なので、レビュー対象 oracle の探索・判定・実行制御を確認したいだけなら直接読む必要はない。

## hash
- d496499d4a070109c3738c1b6cdef8368f6a7523e3fae59de2e4dfa94be613ca

# `review_targets.py`

## Summary
- review oracle の対象となる oracle file を、指定 scope と session 状態に基づいて列挙する実装。full scope では全 oracle file、session scope では session 開始 commit から review fork commit までに変更された oracle file だけを返す。
- oracle file 判定と git diff 結果を組み合わせ、review 対象候補の全件列挙と scope による絞り込みの入口になる。

## Read this when
- review oracle がどの oracle file を対象にするかを確認・変更したいとき。
- full scope と session scope の対象範囲の違い、または session 開始 commit が無い場合の挙動を確認したいとき。
- oracle ツリー内のファイルから review 対象候補を列挙する条件を確認したいとき。

## Do not read this when
- review 結果の表示形式、診断内容、プロンプト内容を確認したいとき。
- oracle file かどうかの共通判定そのものを確認したいとき。
- session 状態の保存・復元や review fork commit の作成処理を確認したいとき。

## hash
- 6348e3e7183b868e00c08b13eb27e550cf440e14e718b53dcc3599c73657aaca

# `session`

## Summary
- `__init__.py` は session 系サブコマンド実装を収める最小のパッケージ初期化モジュールです。具体処理や公開 API は持たず、この階層がサブコマンド実装の入口かだけを確認したいときに読む対象です。
- `abandon.py` は `cmoc session abandon` の実行本体です。session branch を home branch へ戻してから破棄し、state を abandoned に更新する流れと、cleanup 失敗時の rollback を確認したいときに読む対象です。
- `fork.py` は `cmoc session fork` の実行本体です。現在の local branch から session branch と session state を新規作成し、衝突回避、worktree の clean 確認、失敗時 rollback を含めて確認したいときに読む対象です。
- `join.py` は `cmoc session join` の実行本体です。session branch から home branch へ merge し、必要なら conflict 解消を依頼し、state 更新・branch 削除・結果表示までの制御を確認したいときに読む対象です。

## Read this when
- `__init__.py` は、session 系サブコマンドのパッケージ境界や、パッケージ自体に初期化処理があるかを確認したいときに読む。
- `abandon.py` は、`session abandon` の実行条件、branch 遷移、state 更新、cleanup 失敗時の rollback 方針を確認したいときに読む。
- `fork.py` は、`session fork` の作成手順、事前条件、失敗時 rollback、表示結果を確認したいときに読む。
- `join.py` は、`session join` の実行条件、失敗条件、出力内容、状態遷移、merge conflict の扱いを確認したいときに読む。

## Do not read this when
- `__init__.py` は、個別の session サブコマンドの処理、引数、入出力、状態操作を調べたいときには読まない。
- `abandon.py` は、`session abandon` の CLI 入口だけ知りたいときや、join / fork など別の session 操作を追いたいときには読まない。
- `fork.py` は、`session fork` の CLI runtime 起動や共通前処理だけを見たいとき、または join / abandon を追いたいときには読まない。
- `join.py` は、`session join` の CLI 入口だけを知りたいとき、session 全体の一覧や fork / abandon を追いたいとき、一般的な git 操作や共通実装だけを知りたいときには読まない。

## hash
- bf4e9c66b73f369a31fc7b827e7d5b4c0f08980a1092b78933a4d5a2731a43c8

# `tui.py`

## Summary
- `cmoc tui` の実行本体をまとめた入口。利用者が編集する元プロンプトの作成、エディタ起動、実行パラメータ解決、Codex TUI 起動までを一連で扱う。
- TUI で使う editor 選択、元プロンプトの読み取り、解決済み JSON からの `AgentCallParameter` 構築、`.cmoc` の ignore 保証もこの対象に含まれる。

## Read this when
- `cmoc tui` の起動手順、入力プロンプトの扱い、起動前後のログやパラメータ解決の流れを確認したいとき。
- TUI 用の実行パラメータや、使用可能な file access mode の判定を変えたいとき。
- エディタ選択や、編集後プロンプトの読み取り方法を直したいとき。
- TUI 実行時に `.cmoc` をログ作成前に ignore へ入れる必要があるかを確認したいとき。

## Do not read this when
- `cmoc tui` 以外のサブコマンドのルーティングや実行フローを見たいとき。
- プロンプト本文そのものの正本仕様を確認したいときは、ここではなく参照先の oracle doc を読むべきとき。
- Codex の TUI 起動に渡す個別フィールドの定義や生成元を追いたいだけなら、`acp.builder.tui` 側を先に読むべきとき。

## hash
- 7f2454216d463ad190e4a3c166c26cd93c530744aefeeecd86a7d2607b839a6b
