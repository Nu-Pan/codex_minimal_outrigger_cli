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
- `review oracle` の Markdown レポート生成をまとめた実装で、保存先解決・frontmatter・verdict・所見一覧の描画を扱う。`<work-root>/oracle/doc/app_spec/sub_command/review_oracle.md` の表示順や項目を合わせたいときに読む。

## Read this when
- `review oracle` の出力本文や frontmatter を変えるとき
- 所見の集計、採否別の並び、oracle file ごとの件数表示を確認したいとき
- レポート保存先やファイル名の生成方法を追いたいとき

## Do not read this when
- `review oracle` 以外のサブコマンド仕様を見たいときは、各サブコマンドの実装へ進む
- レビューワークフロー全体の判定ロジックを見たいだけなら、所見収集や判定の元実装を先に読む
- `review oracle` の対象抽出だけを確認したいときは、レポート描画より対象列挙側を先に読む

## hash
- 800f474d769496f9704ff2ef650edf863cd1179a408dbfe75309b5f760bd3eb1

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
- `session` 系サブコマンド実装をまとめた階層で、`fork`・`join`・`abandon` の各実行本体を分けて収める。ここは個別操作の入口を選ぶための案内であり、実処理そのものは各モジュールで扱う。
- `__init__.py` はこの階層をパッケージとして成立させる最小初期化で、公開 API や挙動は持たない。`fork.py` は session 作成時の branch/state 生成と衝突回避・rollback を扱い、`join.py` は merge と conflict 解消を含む終了処理を扱い、`abandon.py` は home branch への復帰後に session を破棄する流れを扱う。

## Read this when
- session 系サブコマンド全体の構成を見て、どの実装モジュールへ進むべきかを判断したいとき。
- session の開始・統合・破棄のいずれかで、branch 遷移や state 更新の責務分担を先に把握したいとき。
- この階層にパッケージ初期化以外の共通処理があるか、または個別サブコマンドがどの責務で分かれているかを確認したいとき。

## Do not read this when
- CLI の共通起動や subcommand 登録の全体像を知りたいときは、より上位の共通実行層を読む。
- 個別の session 操作の条件、失敗時挙動、出力、branch/state 変更を知りたいときは、対応する実装モジュールを直接読む。
- session 以外のサブコマンド実装を追いたいときは、この階層ではなく別の sub_commands 配下を見る。

## hash
- 9fd5546b65dc716d41bd7cdcdd3ce1dc40a0e29d68dc6354c65e401cf560f759

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
