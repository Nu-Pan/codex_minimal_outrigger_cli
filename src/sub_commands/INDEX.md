# `apply`

## Summary
- `cmoc apply` 配下の実行制御を読むための入口。ここでは個別サブコマンドの役割境界を見分け、必要なら各実行本体や補助レポート生成へ進む。
- `__init__.py` はサブコマンド実装パッケージの入口であり、初期化時の副作用や再 export の有無だけを確認したいときに使う。
- `abandon.py` は未 join の apply run を破棄して state を ready に戻す流れを扱い、停止・削除・状態更新の関係を確認したいときに読む。
- `fork.py` は apply fork のオーケストレーション本体で、前提確認から worktree 作成、所見適用、commit、state 更新、復旧条件までを追いたいときに読む。
- `fork_report.py` は apply fork の結果または失敗結果の Markdown レポート生成を担い、差分収集、要約、frontmatter、本文構成を確認したいときに読む。
- `join.py` は apply join の実行本体で、整合確認、想定外差分の判定、`--force-resolve` 復旧、merge、後始末の流れを確認したいときに読む。

## Read this when
- `cmoc apply` のサブコマンド実装のうち、どの責務がどのファイルにあるかを切り分けたいとき。
- パッケージ初期化、fork、join、abandon、fork report のどれを読むべきか迷っているとき。
- apply run の実行順序や終了時の state/report の流れを把握したいとき。

## Do not read this when
- 個別サブコマンドの引数定義や内部制御を詳しく追いたいときは、対応する実装ファイルへ直接進む。
- branch や worktree の一般的な操作だけを確認したいときは、共通 runtime 側を読む。
- apply 以外のサブコマンドや正本仕様そのものを探したいときは、この階層ではなくより直接の対象や oracle 側を読む。

## hash
- f33c287cdd84b1b07cdab63a4137dac4b2db039c610db90b82640a1570582678

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
- review oracle の実行ループをまとめる入口。所見の列挙、重複整理、反証と擁護の往復、採否判定、および merge 操作の検証と適用を一連の流れとして扱う。
- merge の構文検証や、検証失敗を semantic response failure として扱う境界も含むため、レビュー処理の制御フローやエラー扱いを確認したいときにここから入る。

## Read this when
- review oracle の処理順序や、列挙・マージ・検証・判定のどこで再試行や打ち切りが起きるかを確認したいとき。
- merge finding の操作仕様、target_id の重複禁止、未知 id の拒否など、所見統合のルールを確認したいとき。
- step callback にどの段階で通知するか、また review の進行ログをどう区切るかを追いたいとき。

## Do not read this when
- 個別の Codex パラメータ生成だけを見たいときは、各 `build_review_oracle_*_parameter` 側を直接読む。
- oracle file ごとの関連所見の抽出だけを確認したいときは、`finding_oracle_path` を扱う別モジュールを読む。
- レビュー全体の CLI 引数や設定値の定義だけが必要なら、呼び出し元のコマンド層を先に読む。

## hash
- 483350368294835c50169da6f3fe509592d07320314f339c266b4a484de9dcbf

# `review_paths.py`

## Summary
- review finding に含まれる oracle_path を、隔離 worktree 上で照合可能な実パスへ変換する補助処理を扱う。
- 空値・非文字列・未対応プレースホルダを None に落とし、絶対パス、<oracle-root> alias、path_model が解決できるプレースホルダ付きパスを区別して解決する。

## Read this when
- review finding の oracle_path を Path に変換する挙動を確認・変更したいとき。
- <oracle-root> alias や <work-root> などのプレースホルダ付きパスを、review 用の隔離 worktree 基準で扱う処理を調べるとき。
- finding 内の oracle_path が不正または未解決の場合に None になる境界を確認したいとき。

## Do not read this when
- 一般的な path keyword の定義や resolve_real_path の解決規則そのものを確認したいだけのときは、path_model 側を読む。
- review finding を生成する prompt や oracle_path の入力仕様を確認したいときは、finding 生成側の oracle 定義を読む。
- カレントディレクトリを一時変更する pushd の実装や副作用を調べたいだけのときは、runtime paths 側を読む。

## hash
- bf2334572baffb103819312c0414528aedfa5242943a0e4d60965d2541914102

# `review_report.py`

## Summary
- review oracle の実行結果を Markdown レポートとして保存・描画する処理を担う。
- 評価対象 oracle file の一覧、findings の採否・重大度別集計、frontmatter、表示用 path、最終 verdict 文言を組み立てる。
- review oracle の report 出力形式や findings 表示順、oracle path の表示変換を確認する入口となる。

## Read this when
- review oracle が生成する Markdown レポートの構成、frontmatter、見出し、表、verdict 文言を確認・変更したいとき。
- accepted/rejected findings や fatal/minor findings の分類、集計、表示順を追いたいとき。
- review oracle の出力で oracle file path がどのように相対表示されるかを確認したいとき。
- review oracle の途中失敗、対象 0 件、fatal/minor/ok の各結果が report 上でどう表現されるかを確認したいとき。

## Do not read this when
- review oracle の対象 oracle file をどう探索・選定するかを確認したいだけのとき。
- finding の生成、判定、採否決定そのもののロジックを確認したいとき。
- review oracle 以外の report 生成や、汎用的な report 保存先の規則だけを確認したいとき。

## hash
- 5a2499fad6f56637148a2a518aa7b69c30e6ea400a3a65e93a871335de8564b7

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
- session サブコマンド群の実装をまとめる階層で、個別コマンド本体と最小限のパッケージ入口だけを収める。session の起動・終了・統合の流れを追うときに、この階層から個別ファイルへ進む。
- `fork` は session branch の作成と session state 保存を扱い、`join` は session branch での merge と conflict 解消・状態更新・ブランチ削除を扱い、`abandon` は session branch の破棄と active session の終了処理を扱う。
- 各ファイルは session という同じ責務の中でも、開始、統合、終了で役割が分かれているため、処理の入口と状態遷移の種類で読む対象を切り分ける。

## Read this when
- session サブコマンド実装の境界や、どのコマンドがこの階層に属するかを確認したいとき。
- `session fork` の作成条件や state 保存、`session join` の merge と conflict 処理、`session abandon` の破棄フローを個別に追いたいとき。
- session 系コマンドの実行順序、branch 遷移、state 更新の責務分担を把握したいとき。

## Do not read this when
- 個別コマンドの詳細な引数、I/O、失敗条件まで追いたいときは、それぞれの実装ファイルを読む。
- session 以外の CLI ルーティングや共通基盤を調べたいときは、この階層ではなく上位や共通モジュールを読む。
- 単なるパッケージ初期化の有無だけを確認したいときは、`__init__.py` だけを見ればよい。

## hash
- 289ef3bd2bc9364307129f8d4edbc95e4bd52ba3d1ee3c3e7d9dbeca7a90fac6

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
