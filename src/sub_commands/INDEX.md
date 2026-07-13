# `apply`

## Summary
- `cmoc apply` 系のサブコマンド実装をまとめる領域で、開始・終了・実行結果の記録をそれぞれ別の実装に分けて読む入口。
- `__init__.py` はパッケージの役割確認だけに使い、`abandon.py` は実行中の apply run の破棄、`fork.py` は 1 回分の apply 実行制御、`fork_report.py` は fork の結果レポート生成、`join.py` は apply join の整合確認とマージ処理を担う。
- この階層は apply フロー全体を横断して読む必要があるときに使い、個別の subcommand の制御やレポート、cleanup の責務境界を切り分けるための案内に向く。

## Read this when
- apply 系サブコマンドの全体像から、どの責務がどのファイルにあるかを見分けたいとき。
- 破棄・開始・レポート・結合のうち、特定の apply フローに関わる実行本体や状態遷移を確認したいとき。
- パッケージ説明だけを確認したいときや、どの実装ファイルへ進むべきかを最初に絞り込みたいとき。

## Do not read this when
- apply 以外の subcommand の仕様や実装を調べたいとき。
- 共通 runtime 操作、branch/worktree 基盤、state 読み書きの詳細だけが目的で、この階層の個別制御を読む必要がないとき。
- 個別コマンドの引数定義やエラー処理を直接追うなら、該当する下位実装へ進んだ方がよいとき。

## hash
- c084231ddcd3f355de782a413d5132dc96c0d020b8b2a4a43378fd587b5a5061

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
- `__init__.py` は review 系サブコマンド群の package 境界だけを示す最小の初期化モジュールです。ここでは具体的な CLI 動作や公開 API は追わず、この階層を review 系の Python package として扱う根拠を確認したいときに読む対象です。
- `oracle.py` は review oracle の実行入口です。isolated review worktree の作成と削除、対象 oracle の選択、review branch の merge 条件、所見収集と report 出力までの流れを追いたいときに読む対象です。

## Read this when
- review 系サブコマンド群の package 境界そのものを確認したいとき。
- この階層が review 系サブコマンド用の Python package として扱われる根拠を確認したいとき。
- review oracle の実行フローを確認したいとき。
- review worktree の作成・削除、review branch の merge 条件、所見レポートの出力経路を確認したいとき。
- review 対象の oracle ファイル列挙、scope に応じた対象選択、レビュー処理ループ、失敗時のレポート生成を追いたいとき。

## Do not read this when
- review 系サブコマンドの具体的な CLI 挙動、引数、出力、制御フローを調べたいとき。
- review 系サブコマンド内の個別機能や実装詳細を調べたいとき。
- package 初期化時の import、副作用、公開シンボルを調べたいとき。ただし現在内容からはその責務は読み取れません。
- 通常の subcommand 実行基盤や汎用 runtime 操作だけを追いたいとき。
- oracle 対象の列挙規則やレビュー index の衝突解決だけを確認したいとき。

## hash
- 9c33838b8459397caba6c5f972c9d55f9980ac457c8c8101bc3161d760c9a7bb

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
- `cmoc review oracle` の所見処理ループ本体を扱う。新規所見の列挙、所見マージ、妥当性検証、採用判定の順序と、各段階でのダーティフラグ更新やリトライ条件を確認したいときに読む。
- 所見マージの編集操作を所見リストへ適用する検証ロジックもここにある。`finding_id` の再利用禁止、delete/replace/merge の許容条件、merge 段階の意味的リトライ方針を確認したいときに読む。

## Read this when
- `cmoc review oracle` が所見をどう反復処理するか、どの段階で次の周回へ進むかを確認したいとき。
- 新規所見の追加、重複所見の統合、challenge/advocate による再検証、judge による verdict 付与の流れを追いたいとき。
- merge finding の操作仕様や、無効な edit operation をどう扱うかを確認したいとき。

## Do not read this when
- レビュー対象 oracle file の列挙条件や scope 判定だけを知りたいときは、対象選定側を読む。
- 最終レポートの Markdown 形式や frontmatter の項目を知りたいときは、レポート生成側を読む。
- 個別 agent call の prompt 正本そのものを確認したいときは、対応する oracle src の builder を読む。

## hash
- 9d31c1efd3694568048a7c0e419fec8fcdcf0befe5c23b7445105f983e73238c

# `review_paths.py`

## Summary
- `finding` に入った `oracle_path` を、symlink を追跡しない絶対 path と repository-relative key に変換する補助をまとめたモジュール。レビュー用の oracle パス解決とキー正規化を扱うときに読む。
- `<oracle-root>` の別名や `<...>` 形式の root 参照を解釈し、レビュー対象の oracle file を worktree 基準で比較できるようにする。

## Read this when
- `finding` に含まれる oracle の参照先を、実際のファイル path として解決したいとき。
- review 結果の集約で、worktree が違っても同じ oracle file を同一 key として扱いたいとき。
- `<oracle-root>` や他の root プレースホルダから始まる path を受け取る処理を追加・修正するとき。

## Do not read this when
- review レポート本文の構成や採点基準だけを変えたいとき。
- 一般的な path 正規化だけを直したいとき。
- oracle_path 以外の finding 項目の解釈や列挙ロジックを変更したいとき。

## hash
- 81ea9ace374c686536c1de93839f2dd8b921e2c6e6f68f5038fd070dec4862bf

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
- `src/sub_commands/session` 配下の session サブコマンド実装への入口。各コマンド個別の制御ロジックや session 状態の扱いを確認するときに、この階層から下位モジュールへ進む。

## Read this when
- session 系サブコマンドの個別実装を読む前に、この階層が session 用のまとまりか確認したいとき。
- session サブコマンドの共通の入口として、どの操作がこの階層に属するかを把握したいとき。

## Do not read this when
- 個別の session サブコマンドの処理、引数、入出力、状態操作を調べたいとき。その場合は下位の実装モジュールを読む。
- 共通 CLI ルーティングや session 以外のサブコマンド実装を調べたいとき。

## hash
- 915f8cd24174802a4183466abe107fa2049067ea27746018e971115fb6debdfe

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
