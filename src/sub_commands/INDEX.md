# `apply`

## Summary
- apply 系サブコマンドの実行ライフサイクルを扱う実装群への入口。isolated worktree での適用開始、active run の破棄、完了・失敗結果の取り込み、report 生成、実行中 process の状態管理と停止確認をまとめて扱う。
- session branch と apply branch/worktree の対応、apply state の遷移、編集禁止対象の差分検出と復元、join 前後の想定外差分や cleanup など、apply run 全体にまたがる制御を調べる際の起点になる。
- 個別の処理は開始、破棄、取り込み、report、runtime 補助に分かれているため、apply のどの段階を確認するかを決めてから下位対象へ進むためのルーティング対象。

## Read this when
- apply run の開始から終了後の取り込みまたは破棄まで、apply 系サブコマンド全体の責務分担を把握したいとき。
- apply branch/worktree の作成・特定・削除、process id 管理、apply state の ready/active/completed/error 周辺の遷移をどこで扱うか探したいとき。
- 編集禁止対象の差分ロールバック、所見の適用、変更 commit、join 前の想定外差分検出、force resolve、report 出力など、apply run の段階別実装へ進む入口を選びたいとき。
- apply abandon、apply fork、apply join のいずれかに関する実行条件、失敗条件、CLI 出力、cleanup、warning の調査対象を切り分けたいとき。

## Do not read this when
- apply 以外のサブコマンド登録、CLI 全体の引数定義、共通 command dispatch を調べたいときは、上位のサブコマンド実装へ進む。
- session state や apply state の schema、session_id の生成、状態モデルそのものを確認したいときは、状態定義や session 管理側へ進む。
- git wrapper、worktree root、path model、CmocError、timestamp、report directory などの共通基盤だけを調べたいときは、共通 runtime や utility 側へ進む。
- Codex 呼び出し用 prompt、structured output、AgentCallParameter の組み立てだけを確認したいときは、apply 本体ではなく該当 builder 側へ進む。
- apply の外部挙動を検証するテスト観点や fixture を調べたいときは、対応するテスト領域へ進む。

## hash
- 56dfcc3494341c303562ef37109cc2cca66d512be10b3d73be3eb0edd7f934e0

# `indexing.py`

## Summary
- 現在の work root に対する INDEX.md maintenance サブコマンドと、その preflight 連携を実装する。
- INDEX.md 更新対象のディレクトリ・子要素の列挙、既存エントリーの再利用判定、Codex によるエントリー生成、Markdown へのレンダリング、更新差分の commit までを扱う。
- repository ごとの排他 lock、git ignored・binary・memo 除外、対象 hash による鮮度判定など、indexing 処理全体の制御ロジックの入口になる。

## Read this when
- cmoc indexing の CLI 実行、preflight での INDEX.md 最新化、または indexing commit の作成挙動を確認・変更したいとき。
- INDEX.md の生成対象に含めるファイルやディレクトリ、除外条件、対象 hash の計算、既存エントリー再利用の条件を調べたいとき。
- Structured Output から INDEX.md entry Markdown を作る処理、または Codex CLI に単一 entry 生成を依頼する経路を追いたいとき。

## Do not read this when
- INDEX.md entry のプロンプト内容や AgentCallParameter の構築仕様だけを調べたい場合は、builder 側の entry parameter 実装を読む。
- git コマンド実行、設定読み込み、binary 判定、git ignore 判定などの共通 runtime helper 自体の詳細を調べたい場合は、runtime 側の実装を読む。
- 生成済み INDEX.md の個別エントリー内容を確認したいだけの場合は、対象ディレクトリの INDEX.md を読む。

## hash
- 918f714139bfeb33ae4e0dfce726b7ad58062f9b91c4ff10b66c20dafd482715

# `init.py`

## Summary
- リポジトリを cmoc が扱える初期状態へ同期する init サブコマンドの実装。repo root の `.cmoc` ignore と設定同期を行い、必要な初期コミットを作成しつつ、実行前から存在した利用者の staged 差分と `.gitignore` の作業ツリー・index 状態を復元する。
- ログ作成前に `.cmoc` ignore を保証するための事前処理と、その副作用を通常の復元対象から識別する一時状態管理を含む。
- 成功時に利用者へ表示する Markdown 形式の結果文を組み立てる。

## Read this when
- init サブコマンドが repo root に対してどの初期化処理を行うか確認・変更したいとき。
- 初期化時の `.gitignore`、`.cmoc`、設定同期、初期コミット作成の扱いを確認したいとき。
- init 実行前から staged だった利用者差分を初期化コミットへ混ぜない制御や、実行後に staged 差分を戻す処理を確認したいとき。
- ログ作成前に `.cmoc` ignore を保証する事前処理と、そのときの `.gitignore` 状態保持・失敗時破棄を確認したいとき。
- init 成功時の stdout 表示内容を変更・検証したいとき。

## Do not read this when
- 他サブコマンドの通常実行ラッパーやログ保存の共通挙動だけを調べたいときは、CLI サブコマンド実行基盤を扱う共通実装を読む。
- repo root の特定方法、git 実行 wrapper、設定同期、`.cmoc` ignore の具体的な実装だけを調べたいときは、それらを提供する runtime 側の実装を読む。
- init 以外のサブコマンドの利用者向け挙動、出力、状態更新を調べたいときは、該当するサブコマンド実装を読む。
- テストで期待される init の外部挙動だけを確認したいときは、対応するテストを読む。

## hash
- f6cfac0c12fdaaa4d2af3187ac858030cdd5c8c77ab1be9f544af785191ef79a

# `review.py`

## Summary
- active session branch 上の oracle を isolated review worktree でレビューするサブコマンド実装の入口を扱う。
- scope 検証、session branch と worktree 状態の前提確認、review 用 branch/worktree の作成と後始末、対象 oracle file の列挙、Codex 実行ループ、INDEX 変更の commit/merge、review report 出力までの orchestration を担う。
- レビュー対象の列挙、レビュー実行ループ、report 描画、merge conflict 解決などの詳細処理は下位 helper module に委譲し、この対象はそれらを CLI コマンドとして接続する位置づけにある。

## Read this when
- oracle review サブコマンドの実行順序、前提条件、失敗時 report 出力、または一時 review worktree と一時 branch のライフサイクルを確認したいとき。
- review scope の受け付け条件や、active session branch・clean worktree・cmoc ignore 確保などの preflight がどこで行われるかを追うとき。
- oracle review の処理全体で、対象列挙、Codex review loop、INDEX 変更 commit、review branch merge、report 書き込みがどの順でつながるかを把握したいとき。
- CLI 層から review 関連 helper へ渡される主要な値、特に session state、config、review worktree、review branch、fork/join commit、findings の流れを確認したいとき。

## Do not read this when
- oracle file の列挙条件や scope ごとの対象選択の詳細だけを確認したい場合は、対象列挙を担当する helper を読む。
- Codex に渡す review prompt、review loop の反復制御、finding の merge operation 適用の詳細だけを確認したい場合は、review loop 側の helper を読む。
- review report の表示形式、finding section の描画、report file の書き込み内容だけを変更したい場合は、report 生成を担当する helper を読む。
- review branch の merge、INDEX 変更 commit、conflict 解決、worktree status path の扱いだけを調べたい場合は、review index 操作を担当する helper を読む。
- 通常の indexing preflight の中身や、Codex 実行・git worktree 作成・branch 削除など runtime 共通処理の実装詳細を確認したい場合は、それぞれの共通 helper を直接読む。

## hash
- 683f45afe7813f49a04b82cb6d1ba48c5faf9f4a588193292002d1d82a68fc2d

# `review_index.py`

## Summary
- oracle review 用 worktree で生成された INDEX.md 差分の commit と、review branch から session branch への merge を扱う。
- INDEX.md 以外の差分検出、porcelain status の path 抽出、INDEX.md だけが conflict した場合に session 側採用で解決する処理をまとめている。

## Read this when
- review worktree の INDEX.md 変更だけを commit する条件、INDEX.md 以外の差分をエラーにする制御、または status parsing を確認・変更したいとき。
- review branch merge の失敗時に INDEX.md conflict だけを自動解決する挙動、merge 後 commit の取得、手動解決へ回す条件を調べたいとき。

## Do not read this when
- review oracle 全体の一時 worktree 作成・削除順序や active session 制約を確認したいときは、`review.py` を読む。
- oracle file の対象列挙、finding loop、または report rendering を確認したいときは、それぞれ `review_targets.py`、`review_loop.py`、`review_report.py` を読む。
- git command 実行 wrapper や worktree 操作 helper 自体の実装を調べたいときは、runtime 側を読む。

## hash
- 42f2f7a768474b5b07e47ec55750ce65ea6bba3439c7cd667355dc5c6ca6efa9

# `review_loop.py`

## Summary
- review oracle の finding 収集、重複整理、検証、判定を Codex 実行ループとして組み立てるサブコマンド内部処理を扱う。
- oracle 断片ごとの finding 列挙結果を既存 finding と突き合わせ、merge operation を適用し、advocate/challenger による検証理由を蓄積したうえで judge 結果を finding に反映する。
- finding 内の oracle_path を実パスへ解決し、特定 oracle 断片に関連する finding だけを抽出する補助処理も担う。

## Read this when
- review oracle の列挙、merge、validate、judge の実行順序や反復終了条件を確認・変更したいとき。
- Codex に渡す review oracle 用 parameter builder の呼び出し方、purpose、cwd、root、config の受け渡しを追いたいとき。
- finding の初期フィールド、finding_id の採番、merge/delete/replace 操作の適用結果を確認・変更したいとき。
- finding の oracle_path が絶対パス、worktree 相対パス、パスキーワード付き表記からどう解決されるかを調べたいとき。

## Do not read this when
- review oracle のプロンプトや Structured Output parameter の内容そのものを確認したいだけなら、builder 側を読む。
- review oracle の反復回数など設定値の定義や読み込みを確認したいだけなら、config 側を読む。
- 通常のレビュー対象ファイル探索、作業ツリー作成、CLI 引数処理など、review oracle loop の外側のサブコマンド制御を調べたい場合は、呼び出し元を読む。
- oracle file や realization file の正本上の意味・編集責務を確認したい場合は、仕様側を読む。

## hash
- fc53ad61245cfefd472c00b98d52710dbb36a95e94af1044426cce8da5006269

# `review_report.py`

## Summary
- oracle review 結果を Markdown + YAML frontmatter の report として描画し、report directory へ書き出す処理を扱う。
- verdict 判定、frontmatter fields、評価対象 oracle file の表、fatal/minor finding section、path 表示整形をまとめている。

## Read this when
- review report の出力 path、frontmatter 項目、result/verdict の判定条件、または fatal/minor finding の表示形式を確認・変更したいとき。
- oracle path の表示整形、finding section の Markdown 文面、エラー時 report の描画を調べたいとき。

## Do not read this when
- review oracle の実行順序、一時 branch/worktree、対象 oracle file の列挙、finding loop、INDEX.md merge を確認したいときは、それぞれ該当する review 系 module を読む。
- 生成済み report の個別内容だけを読みたいときは、report 出力先の生成物を直接読む。

## hash
- 5a4bc1bc25bc2c3390133302a704cfab266f75d5d961859b561a4a82777866ee

# `review_targets.py`

## Summary
- oracle review の対象 oracle file を scope 別に列挙する処理を扱う。
- full scope では全 oracle file、session scope では session 開始 commit から変更された oracle file のうち、INDEX.md、git ignored、binary file を除外した対象を返す。

## Read this when
- review 対象となる oracle file の列挙条件、session scope と full scope の違い、または INDEX.md・binary・git ignored file の除外条件を確認・変更したいとき。
- session 開始 commit から oracle 配下の変更 path を取得し、列挙済み oracle file と照合する処理を調べたいとき。

## Do not read this when
- review oracle 全体の実行順序、一時 worktree、finding loop、INDEX.md merge、report rendering を確認したいときは、それぞれ該当する review 系 module を読む。
- binary 判定、git ignored 判定、git diff wrapper 自体の実装を調べたいときは、runtime 側を読む。

## hash
- f42029951fa3338498710cca446b7ee6dbf8f87039fc10726d2cecc385a0c05c

# `session`

## Summary
- session 系サブコマンドの実装をまとめる領域。通常 branch から session branch を作成する処理、active session branch を home branch へ取り込む処理、merge せず破棄する処理を扱う。
- 各サブコマンドは実行前条件、worktree の clean 確認、cmoc ignore の保証、branch 切り替え、session state 更新、利用者向け出力、共通 CLI 実行 wrapper への接続を担う。
- join では merge conflict 発生時に Codex CLI へ解消を依頼し、残存 conflict marker や unmerged path の検査から merge commit まで進める補助処理も含む。

## Read this when
- session fork、session join、session abandon の実行条件、状態遷移、branch 操作、利用者向け出力を確認または変更したいとき。
- 通常 branch から session branch を作成する流れ、active session を home branch へ merge する流れ、または merge せず破棄する流れの実装入口を探すとき。
- session 系サブコマンドが共通 CLI 実行 wrapper、indexing preflight、git 実行 helper、session state 読み書き helper をどの順序で呼び出すかを追いたいとき。
- session join の conflict 解消依頼、解消後の検査、merge commit までの制御を確認したいとき。

## Do not read this when
- session 以外のサブコマンド、CLI 全体のコマンド登録、Typer app 構成を調べたいとき。
- session state の schema、state file path 算出、branch 判定、worktree clean 判定、git 実行、timestamp 生成など共通 runtime helper の内部実装を知りたいだけのとき。
- apply、review、indexing など session 操作以外の業務処理を調べたいとき。
- Codex CLI に渡す conflict 解消依頼パラメータの構築仕様そのものを確認したいとき。

## hash
- 466ff6de3251f18b083d7100e33214824fbab69ca3268efc0094e57e67b94cac

# `tui.py`

## Summary
- 利用者が編集した依頼文を起点に、TUI 用の実行パラメータ解決、完全 prompt の生成・保存、Codex TUI 起動までをつなぐサブコマンド実装。
- 依頼文テンプレートの作成、エディタ選択・起動、HTML コメント除去、解決済み JSON からの AgentCallParameter 構築、Markdown 見出しの StructDoc 変換を扱う。

## Read this when
- 対話的に依頼文を編集して Codex TUI を起動する処理の流れを確認・変更したいとき。
- TUI 起動時の file access mode、model class、reasoning effort、完全 prompt 生成、structured output schema の扱いを確認したいとき。
- 利用可能なエディタの選択順、エディタ異常終了時のエラー、依頼文テンプレートや保存先 log 領域の扱いを変更したいとき。
- TUI 向けパラメータ解決結果の JSON から値や真偽値を取り出す規則、または Markdown 見出しを構造化 prompt に変換する規則を確認したいとき。

## Do not read this when
- 通常の非対話 CLI 実行、Codex exec の低レベル実行、または TUI 以外のサブコマンド起動処理だけを調べたいとき。
- TUI パラメータ解決用 prompt の具体的な schema や選択肢定義そのものを調べたいときは、その解決パラメータを構築する側を読む。
- 完全 prompt の共通フォーマットや StructDoc の markdown レンダリング仕様を調べたいときは、prompt 構築・構造化文書レンダリング側を読む。
- INDEX 生成の preflight 処理そのものを調べたいときは、indexing の preflight 実装を読む。

## hash
- da24e922e6a1930a64a5667c2c3867e90de41524c59de1c97005abece970b630
