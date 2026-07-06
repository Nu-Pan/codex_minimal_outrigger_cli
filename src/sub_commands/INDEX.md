# `apply`

## Summary
- apply 系サブコマンドの実行本体をまとめる実装ディレクトリ。apply run の開始、破棄、join、レポート生成など、apply state・worktree・branch・process・差分検査を伴う制御を扱う。
- apply fork の対象ファイル選定、Codex 呼び出し、収束判定、失敗時復旧、apply join の conflict 処理や cleanup など、apply workflow の主要な状態遷移を追う入口になる。

## Read this when
- apply サブコマンドの実行条件、状態遷移、branch/worktree/process 管理、cleanup、警告出力を確認または変更したいとき。
- apply fork が調査対象ファイルをどう決め、finding 列挙・適用・再キュー・commit・report 生成をどう制御するかを調べるとき。
- apply join の差分分類、force-resolve、merge conflict、INDEX.md conflict の自動解決、join 後の状態更新や後片付けを扱うとき。
- apply abandon による未 join apply run の破棄、実行中 process 停止、apply worktree・branch・process id の削除条件を確認したいとき。
- apply fork の成功・失敗レポート、frontmatter、本文構成、変更要約、未収束時表示などを変更したいとき。

## Do not read this when
- apply 以外のサブコマンド、CLI 全体の Typer 登録、外側のコマンドルーティングだけを調べたいとき。
- worktree 検索、git wrapper、状態ファイル読み書き、oracle file 判定、path model などの共通 runtime API 自体を変更したいとき。
- Codex に渡す prompt、parameter schema、finding 列挙・適用・変更要約の builder 詳細だけを確認したいとき。
- oracle file や realization file の定義、INDEX.md 生成規則、path model の正本仕様を確認したいとき。
- 具体的な apply workflow の制御ではなく、パッケージ説明や import 時副作用の有無だけを確認したいとき。

## hash
- 9ed4fc11fa0bcc0f2d99496dd75fab85283e82bf5aec8b66dd75b5631ac8a908

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
- cmoc の indexing サブコマンド実行入口を定義し、CLI runtime 経由で現在の work root に対する INDEX.md maintenance を起動する実装を扱う。
- indexing 実行前の preflight、安全条件の検査、index 更新の排他実行、更新結果の commit、CLI 向けの更新件数出力までを結びつける薄い orchestration 層である。
- INDEX.md の生成・更新ロジックそのものではなく、既存の indexing 共通処理をサブコマンドとして呼び出すための接続点として読む。

## Read this when
- cmoc indexing サブコマンドの実行フロー、CLI runtime への渡し方、command 名や argv、work root runtime の指定を確認・変更したいとき。
- indexing 実行前に clean worktree や cmoc ignore 条件をどこで検査しているかを確認したいとき。
- INDEX.md maintenance がどの root に対して lock 付きで実行され、更新後にどのように commit と件数出力へ進むかを追いたいとき。
- indexing サブコマンドが Codex exec 実行関数や indexing 共通処理へどのように依存しているかを確認したいとき。

## Do not read this when
- INDEX.md の内容生成、差分検出、更新対象探索、commit 処理、lock 実装などの詳細ロジックを調べたいときは、ここではなく indexing 共通処理側を読む。
- work root の定義、CLI runtime の一般的な実行規約、clean worktree 判定、cmoc ignore 判定の詳細を調べたいときは、それぞれの runtime helper 側を読む。
- Typer app へのサブコマンド登録やトップレベル CLI 配線を確認したいだけなら、CLI entrypoint や subcommand 登録側を読む。
- oracle 上の indexing サブコマンド仕様そのものを確認したいときは、実装ではなく対応する oracle doc を読む。

## hash
- 300dd7538efb7a60cb06753149ee3b7f779bd687acbf6cc8a567083f8e6fa0a8

# `review`

## Summary
- review 系サブコマンド群の実装を置く package。package 境界だけを示す初期化モジュールと、review oracle サブコマンドの実行入口・全体制御を担う module を含む。
- review oracle workflow では、active session branch と clean worktree の検証、isolated review worktree の作成、oracle 対象列挙、review loop 実行、INDEX 変更の commit/merge、作業用 worktree/branch の後始末、review report 出力を接続する。

## Read this when
- review 系サブコマンド群の package 境界や、この階層が review 系サブコマンド用 Python package として扱われる根拠を確認したいとき。
- review oracle サブコマンドの実行順序、前提条件、作業用 branch/worktree のライフサイクル、失敗時 report 出力を確認したいとき。
- oracle review workflow が下位 module を呼び出す流れや、INDEX 変更の commit/merge と report 作成のタイミングを追いたいとき。
- 未コミット差分がある場合や active session branch 以外での実行を拒否する制御を確認したいとき。

## Do not read this when
- review oracle の個別処理だけを確認したいときは、対象列挙、review loop、review report、INDEX 操作を担う下位 module を直接読む。
- review 系サブコマンドの具体的な CLI 挙動、引数、出力、制御フローのうち、この階層の実行入口以外に閉じた詳細を調べたいとき。
- package 初期化時の import、副作用、公開シンボルを調べたいとき。ただし現在内容からはそのような責務は読み取れない。

## hash
- 5eb0e18b30d330973e0e2740952884fec3b20ec52f89beb14128d849de33d21a

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
- review oracle の finding 抽出、統合、検証、判定を Codex 呼び出しで反復実行する制御ロジックを扱う。
- finding list に対する merge/delete/replace 操作の検証と適用、および semantic retry 失敗時のエラー化を担う。

## Read this when
- review oracle の finding enumerate/merge/validate/judge の実行順序、反復条件、dirty 管理を確認・変更したいとき。
- finding merge の Structured Output operation の許容条件、finding_id の採番、重複・未知 ID・不正 kind の扱いを確認・変更したいとき。
- review oracle loop が Codex 実行パラメータ builder、設定値、log root、worktree、oracle path とどう連携するかを追いたいとき。

## Do not read this when
- review 対象の oracle file 一覧作成や finding から oracle path を取り出す処理だけを確認したいときは、より直接その責務の対象を読む。
- Codex 実行パラメータのプロンプト内容や Structured Output schema 自体を確認したいときは、各 builder 側を読む。
- review oracle 以外の review workflow、CLI 引数、設定定義を確認したいだけのときは、それぞれの責務を持つ対象を読む。

## hash
- e905f9cf7705c92dbd8fbbdd55db0080f23e60a8bc26b5a4ca8987880fc5b237

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
- review oracle の実行結果を Markdown レポートとして保存・描画する処理を担う。評価対象 oracle、採否・重要度別の finding、処理結果、関連 commit 情報をレポート本文と frontmatter にまとめる。
- finding の oracle path 表示、重要度別セクション描画、エラー・対象なし・fatal・minor・ok の verdict 文言決定もこの対象の責務に含まれる。

## Read this when
- review oracle のレポート保存先、ファイル名生成、Markdown 構成、frontmatter 内容、verdict 文言を確認または変更したいとき。
- finding の accept/reject や fatal/minor の分類がレポート上でどう集計・表示されるかを確認したいとき。
- oracle path をレポート内でどのような相対表示にするか、root 外や oracle 配下の path 表示規則を確認したいとき。

## Do not read this when
- review oracle がどの oracle file を対象に選ぶか、finding をどう生成・判定するかを調べたいだけのとき。
- reports directory や timestamp など、レポート共通の保存場所・時刻生成の基盤処理を確認したいとき。
- review oracle 以外のサブコマンドの出力やレポート形式を調べたいとき。

## hash
- 87d7bf56e0f59687e42dd834adfed00993792180ac41fc86a4b4670b86a21372

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
- session 系サブコマンド実装をまとめるディレクトリ。package 初期化に加え、session branch の作成、home branch への join、merge しない破棄など、session lifecycle の具体的な CLI 処理へ進む入口となる。
- 各サブコマンドは CLI runtime、git 操作、session state、worktree 条件、利用者向け出力や失敗時復旧を扱うが、共通 helper や正本仕様そのものはこの階層の主責務ではない。

## Read this when
- session 系サブコマンドの実装ファイルを探し、fork、join、abandon のどれを読むべきか判断したいとき。
- session branch の作成、home branch への merge 完了、merge しない破棄など、session lifecycle の外部挙動や状態更新を確認または変更したいとき。
- session 操作での事前条件、clean worktree 要求、branch/state の確認、成功時出力、失敗時エラーや rollback 方針の実装入口を探すとき。
- session join の merge conflict 自動解消や、conflict 解消後の差分検査、marker 残存判定、merge commit 完了処理を調べたいとき。

## Do not read this when
- session 以外のサブコマンド、共通 CLI ルーティング、サブコマンド登録の実装を調べたいとき。
- git 実行 wrapper、CLI runtime、worktree 検査、branch 判定、state file schema、path model などの共通実装そのものを確認したいとき。
- session 系サブコマンドの正本仕様断片を確認したいとき。その場合は対応する oracle doc を読む。
- 個別サブコマンドがすでに特定できており、その処理だけを詳しく確認したいとき。その場合は該当する実装モジュールを直接読む。

## hash
- a4c55dddea5656ceda9a0db4e06f5c0d783a2cba9c5e0b4df1666b59de815c53

# `tui.py`

## Summary
- 対話的な依頼文編集から実行パラメータ解決、Codex TUI 起動までをつなぐ `cmoc tui` の実装を担う。
- TUI 用ログ領域への元 prompt 作成、利用可能なエディタ選択、HTML コメント除去、解決済み JSON からの起動パラメータ構築、TUI で許可される file access mode の検証を扱う。
- CLI runtime から現在の repository/context を取得して TUI 本体処理へ渡し、ログ作成前に必要な `.cmoc` ignore を保証する入口でもある。

## Read this when
- `cmoc tui` の実行フロー、エディタ起動、prompt ファイル作成、TUI 起動前の parameter 解決を変更したいとき。
- TUI サブコマンドで利用する file access mode、role・summary・goal・各標準フラグの既定値や resolved JSON の読み取り方を確認したいとき。
- TUI 実行時のログ保存先、元 prompt と完成 prompt の扱い、`.cmoc` ignore 保証の挙動を調べたいとき。
- TUI 起動前の Codex exec 呼び出しと TUI 起動呼び出しの引数、cwd、purpose、config の渡し方を確認したいとき。

## Do not read this when
- TUI 用 prompt の標準文面や agent call parameter の最終的な本文構築そのものを確認したいだけなら、TUI 起動パラメータを組み立てる builder 側を読む。
- resolved JSON を生成するためのプロンプトや schema、TUI で指定可能な解決項目を確認したいだけなら、parameter resolve の builder 側を読む。
- CLI runtime 共通の subcommand 実行、config 読み込み、log path、repository root 判定、Codex 実行 wrapper の詳細を調べたいだけなら、runtime 共通処理を読む。
- TUI 以外のサブコマンドの挙動や CLI 全体の command routing を調べたい場合は、そのサブコマンドまたは CLI entrypoint を読む。

## hash
- ec33c67348f84c67cb37c97936f7d21ff0b8f53fe546f3169c70732bb149c750
