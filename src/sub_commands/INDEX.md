# `apply`

## Summary
- `apply` 系の各サブコマンド実装をまとめた入口。実行フロー全体を追うより、目的に応じて `fork` `join` `abandon` のどれを読むかを切り分けるために使う。
- 開始処理・中断後の整理・結果レポートのように、apply ライフサイクル上の責務ごとに分かれた実装を読むときの案内役になる。
- 共通の状態操作や個別サブコマンドの制御を直接読む前に、どの処理単位へ進むべきかを判断したいときの起点になる。

## Read this when
- `apply` 系サブコマンドのうち、どの実装ファイルを読むべきかを切り分けたいとき。
- apply の開始・中断・終了のどの段階を調べるべきかを先に判断したいとき。
- サブコマンド実装群の役割分担だけを確認してから、個別の実行本体へ進みたいとき。

## Do not read this when
- 特定のサブコマンドの引数、制御フロー、エラー処理を調べたいときは、対応する実装ファイルを直接読む。
- report 文面や差分要約など、結果表示の詳細だけを知りたいときは、レポート生成側の実装を読む。
- apply の共通 helper や state 管理だけを追いたいときは、この階層ではなく共通処理の実装へ進む。

## hash
- 89273baf1fe58b16b79eed879d6d6f3bd9c19ae7800bf9a2b99e6056373321b2

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
- `want` を書き出した oracle を、review oracle と同じ評価経路へ渡すための入口。評価対象の scope を受けて review 側の実行に委譲するので、oracle の評価フローを辿りたいときに読む。

## Read this when
- oracle の評価を review oracle と同じ経路で実行したいとき。
- scope を指定して、書き出した oracle を評価対象に乗せたいとき。

## Do not read this when
- oracle の実体を生成・修正したいだけのときは、直接その生成元や review 側の実装を読む。
- review の集約・レポート生成・対象列挙を知りたいだけなら、この薄い委譲層ではなく review 側の実装を読む。

## hash
- d2c72efffe412278a6207afbd665dfc79c3aba3444ba20b94bfddab2a5a70d70

# `indexing.py`

## Summary
- `cmoc indexing` サブコマンドを起動する入口。CLI 前提条件の検査、work root での INDEX 生成更新、更新差分の commit までをまとめて追いたいときに読む。

## Read this when
- `cmoc indexing` の起動条件や実行フローを確認したい。
- work root 側の `INDEX.md` 更新と commit が、どの順で・どの責務で行われるかを追いたい。
- indexing 実行前の安全条件検査を変更したい。

## Do not read this when
- `update_indexes` の具体的な更新ロジックや commit 内容そのものを見たい場合は、そこを実装する別ファイルを直接読む。
- 単に CLI 全体の共通起動処理を確認したいだけなら、より上位の subcommand 実装を先に読む。

## hash
- c37ac15e0f461975a999061ec892b3b8f00ae8e1b658187ec38ff3f0f2a2616c

# `review`

## Summary
- `review` 系サブコマンド群の入口となる package 境界と、`review oracle` コマンド本体の実行フローを案内する。ここでは境界確認だけを担う初期化モジュールと、セッション検証から隔離実行、結果集約、report 出力までを追う実行本体を分けて読む。

## Read this when
- `review` 系サブコマンド群がどこから始まり、どの実装へ進むべきかを確認したいとき。
- `review oracle` の実行手順、分岐、エラー終了、中断時の扱いを追いたいとき。
- review 対象の選定、worktree での隔離実行、report 出力の結び付き方を知りたいとき。

## Do not read this when
- `review` 系サブコマンド内の個別 helper の細部だけを見たいとき。
- 所見本文の描画や対象列挙など、`review oracle` の下位責務だけを直接確認したいとき。
- package 初期化時の import や公開シンボルの詳細だけを調べたいとき。

## hash
- fd59525ab0031b0d90dab28c37cac0f325e6f574f8e6a3e1e688f2b7e50d6916

# `review_index.py`

## Summary
- review 実行の最後に `INDEX.md` だけを commit し、review branch を session branch へ merge する処理を扱う。`INDEX.md` 以外の差分を拒否する制御や、merge 時の `INDEX.md` conflict 解決の境界を確認したいときに読む。

## Read this when
- review の隔離 worktree で発生した差分を commit する条件や、review branch を session branch に取り込む条件を確認したい。
- merge conflict が `INDEX.md` だけのときに自動解決してよいか、どの差分を許容しないかを確認したい。

## Do not read this when
- review 対象の列挙や report の描画を追いたい場合は、対象選択・レポート側の文書を読む。
- review 実行全体のフローや CLI 入り口を追いたいだけなら、subcommand 全体の本文を先に読む。

## hash
- 114fcb70e72c2d3d48d04ca130852a6142148c4f61ea9504529d356f7666dc93

# `review_loop.py`

## Summary
- `cmoc review oracle` の実行ループ本体を扱う。所見の列挙・マージ・検証・採否判定の周回制御、ユーザー中断時の部分結果保持、merge 操作の適用と検証をここで追う。

## Read this when
- `cmoc review oracle` の処理順、反復回数の打ち切り条件、ダーティフラグの更新、所見 ID の付与や継続条件を確認したいとき。
- 中断時にどこまでを確定済み結果として残すか、また `KeyboardInterrupt` をどのようにレビュー継続可能な形へ変換するかを確認したいとき。
- merge 操作の妥当性検証や、所見リストへの適用ルールを確認したいとき。

## Do not read this when
- レビュー対象 oracle の選び方や `--scope` の意味だけを知りたいときは、対象選定とパス解決を扱う別のファイルを読むべき。
- レビュー結果の Markdown レポート体裁や集計表示だけを確認したいときは、レポート生成側を読むべき。
- Codex 呼び出し用の個別 prompt 仕様だけを確認したいときは、oracle 側の parameter builder 定義を読むべき。
- review 以外の apply や session 系のサブコマンド挙動を確認したいとき。

## hash
- 966ffb4be92050ae8cc33c95618720cffd6e93f46e824c12696fd37c2121d881

# `review_paths.py`

## Summary
- review 系サブコマンドで使う oracle path の解決と key 化をまとめた入口。finding の `oracle_path` を絶対 path に直し、report や対象照合で同一 oracle file を識別するための正規化を担う。

## Read this when
- `review oracle` の finding から参照先を復元したいとき
- symlink を追跡しない path 正規化や、review 対象の同一性判定を確認したいとき
- review report や finding 照合で oracle file の表示・集計ずれを追いたいとき

## Do not read this when
- review の実行手順、ループ制御、レポート本文の構成を変えたいときは、より上位の review orchestration/report 側を読む
- 対象 oracle file の列挙条件そのものを見たいときは、対象列挙モジュールを読む
- 単なる表示文言や Markdown の体裁だけを調整したいときは、このファイルではなく report 生成側を読む

## hash
- 739dd10ce6e0bfa7b45ee39c2bdef0b4d7cbc791d144480e58fdd77fffeb478c

# `review_report.py`

## Summary
- レビュー oracle report を Markdown と YAML frontmatter で組み立てて保存する処理があるため、`review oracle` の出力形式、見出し構成、所見の並び順、集計値、保存先決定を確認したいときに読む。
- 所見の抽出・分類・表示整形・最終 verdict 判定がこの対象の責務なので、レビュー結果の見え方を変える変更や、レポート生成ロジックの修正時に読む。
- `sub_commands/review_paths.py` のようなパス解決や、レビュー実行そのものの探索・収集ロジックを追う目的ではなく、レポート文面と保存処理だけを見たいときに読む。

## Read this when
- `review oracle` のレポート本文、frontmatter、集計値、所見の表示順を変える可能性があるとき。
- レビュー結果の保存先やファイル名の決め方を確認したいとき。
- 所見が accept/reject、fatal/minor でどう分かれて表示されるかを確認したいとき。

## Do not read this when
- レビュー対象 oracle file の選定方法やパス抽出の詳細を追いたいだけなら、関連する path 解決側を先に読む。
- レビュー処理の実行手順や収集ロジック、対象探索の本体を変えたいだけなら、この対象ではなくレビュー実行側を読む。
- Markdown 報告の見た目ではなく、レビュー判定ルールそのものを変えたいときは、判定元の仕様やロジック側を読む。

## hash
- f0d2ffa1af56e99015b8f2f1f604e601dc583464a2d831353edcc5405c8d8800

# `review_targets.py`

## Summary
- review 用 oracle の列挙条件を決める入口。`full` か session scope かで対象集合が変わるため、どの oracle file をレビュー対象に含めるかを判断したいときに読む。
- 全 oracle file の走査と、review fork 時点から session 開始時点までに変化した oracle file の抽出を行う。review 対象の選定ロジックを確認したいときにこのファイルを読む。

## Read this when
- review の対象 oracle file をどう決めているかを知りたい。
- session scope の review で、なぜ変更差分だけが対象になるのかを確認したい。
- oracle file の列挙方法そのものを調べたいが、個別の review 実装や表示処理ではなく対象選定の入口を見たい。

## Do not read this when
- review 対象の具体的な表示や実行処理を追いたい場合は、対象選定の後段の実装を読む。
- oracle file の定義や判定基準そのものを知りたい場合は、oracle 側の仕様断片を読む。
- review 対象の全体設計やコマンド構成を知りたいだけなら、このファイルではなく上位のコマンド定義を読む。

## hash
- 76065333206f76110f8fd22ca0b12ba596c4ac579c061039705d0b7ce83a8516

# `session`

## Summary
- `__init__.py`: session 系サブコマンド実装のパッケージ境界を示す最小初期化モジュール。下位の session 実装へ進む入口として扱う。
- `abandon.py`: `cmoc session abandon` の破棄フローを扱う。active session の終了、home branch への復帰、session branch の削除、失敗時の巻き戻しが主題。
- `fork.py`: `cmoc session fork` の作成フローを扱う。現在の branch を home branch として session branch を作り、state 保存と失敗時の rollback まで含む。
- `join.py`: `cmoc session join` の実行オーケストレーションを扱う。session branch を home branch に merge し、状態更新、branch 削除、conflict 時の切り替えまで追う。

## Read this when
- `__init__.py`: session パッケージの境界や、この階層に初期化処理があるかだけを確認したいとき。
- `abandon.py`: session の破棄手順、rollback、再実行可能性、利用者向け出力を変えたいとき。
- `fork.py`: session 作成条件、既存 active session の扱い、session-id 生成、state 保存、失敗時 cleanup を確認したいとき。
- `join.py`: session join の実行順序、merge conflict の扱い、状態更新、branch 削除条件を確認したいとき。

## Do not read this when
- `__init__.py`: 個別の session サブコマンドの処理を知りたいときは、各実装モジュールを読む。
- `abandon.py`: session の作成・参加・継続を見たいときは、該当サブコマンド側を読む。
- `fork.py`: CLI 引数定義やサブコマンド配線だけを見たいときは、上位の CLI 入口を読む。
- `join.py`: 状態スキーマや conflict 解消用の引数生成だけを知りたいときは、より直接の定義側を読む。

## hash
- 1cd11f46c5f0bd63e9f38725f2d43815ae216a4cc0defdc2099af8f423f00073

# `tui.py`

## Summary
- `cmoc tui` の実行本体。利用者が編集する元プロンプトの作成、エディタ起動、実行パラメータ解決、Codex TUI 起動までの一連の流れを扱う。
- TUI 起動前に使うテンプレート文面、編集後プロンプトの読み取り、利用可能なエディタ選択、TUI 用の `AgentCallParameter` 生成をまとめている。
- `cmoc tui` 実行時に `.cmoc` の ignore 条件を保証する処理も含む。

## Read this when
- `cmoc tui` の起動手順や、編集された元プロンプトがどのように最終 TUI 呼び出しへ渡るかを追いたいとき。
- TUI 用の初期プロンプト文面、エディタ選択条件、実行パラメータの解決方針を変えたいとき。
- TUI 実行前に必要なログ領域・ignore 条件・保存先の扱いを確認したいとき。

## Do not read this when
- Codex の TUI 起動時に渡す個別フィールドの定義や生成元だけを追いたいときは、`acp.builder.tui` 側を先に読むべきとき。
- `cmoc tui` 以外のサブコマンドのルーティングや共通実行基盤を見たいだけのとき。
- CLI 引数定義やサブコマンド登録だけを確認したいときは、より上位の実行入口を読むべきとき。

## hash
- 19e2a3688db71a103e4ea6207ce44e0435f7e1d1f266fc4f65afbfc6bc3f6a08
