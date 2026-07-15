# `apply`

## Summary
- `apply` サブコマンドの実装群。apply run の開始・中断・join、branch/worktree と state の管理、Codex による適用処理、結果レポート生成までを扱う。各ファイルは個別の処理責務を持つため、具体的な挙動を調べる際の入口になる。

## Read this when
- `cmoc apply` の fork・abandon・join の実行フローや cleanup 条件を確認したいとき。
- apply run の state、branch、worktree、process tracking、異常時復旧の挙動を調べたいとき。
- apply fork の結果レポートや変更差分の要約生成を確認したいとき。

## Do not read this when
- apply 以外のサブコマンドの実装を調べたいとき。
- apply の共通 state 操作、worktree 操作、git 操作だけを確認したいときは、対応する共通 runtime helper を直接読む。
- 具体的な prompt builder や report 文面など、単一の補助責務だけを調べる場合は、対象の専用実装へ直接進む。

## hash
- ebdfb1a05d2865ee25e401710f6808effb207d2d2abbca1dd99e757c687856a8

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
- session 系サブコマンドの実装パッケージ。session パッケージの初期化入口と、fork・join・abandon の各ライフサイクル処理を収める。
- session branch、home branch、state file、Git 操作、失敗時の rollback、join 時の conflict 解消と結果表示を扱う下位実装への入口。

## Read this when
- session の作成・参加・破棄の挙動や、session branch と state のライフサイクルを調べるとき。
- session join の merge conflict 検出・解消依頼・stage・commit・branch 削除を調べるとき。
- session 配下の実装構成や、パッケージ初期化処理の有無を確認するとき。

## Do not read this when
- 共通 CLI ルーティング、サブコマンド登録、状態モデル、Git の低レベル操作だけを調べるとき。
- session 以外のサブコマンドを調べるとき。
- join の conflict resolution builder など、session 実装内の特定処理だけを直接調べるときは、その定義元を読む方が適切。

## hash
- e9a707c2ffea5a14ea987c241ed5030cdac1bbcafe8c543cd8fbab935be5c367

# `tui.py`

## Summary
- `cmoc tui` サブコマンドの実行フローを担当する実装。利用者向けプロンプトの初期化・編集・読み込み、実行パラメータの解決、TUI 起動、関連する ignore 保証を扱う。TUI の起動処理やプロンプトからのパラメータ変換を調べる入口。

## Read this when
- `cmoc tui` の動作、エディタ選択、プロンプトテンプレート、TUI 起動前後の処理を変更・調査するとき
- 解決済みパラメータから `AgentCallParameter` を構築する処理や、TUI で許可されるファイルアクセスモードを確認するとき
- TUI サブコマンドのログ領域や `.cmoc` の ignore 保証を調査するとき

## Do not read this when
- TUI のパラメータ定義そのものや、TUI 起動パラメータの詳細仕様だけを調べるときは、対応する `acp.builder.tui` の実装を直接読む
- `cmoc tui` と無関係な CLI サブコマンド、一般的な設定読み込み、共有ランタイムの挙動だけを調べるとき

## hash
- 0e4aea977ac81ad59dc3b88e371aeedeca45632926cdf7cd1f6c6a418839e3b0
