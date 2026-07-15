# `apply`

## Summary
- `cmoc apply` 系のサブコマンド実装をまとめて案内する入口。各サブコマンドの実行本体、結果レポート、初期化時のパッケージ責務を、目的に応じて個別モジュールへ振り分ける。
- apply run の開始・破棄・完了後処理・レポート生成のどこを読むべきかを切り替えるための路線図であり、共通基盤や低レベルの branch/worktree 操作の入口ではない。

## Read this when
- `cmoc apply` のどのサブコマンド実装へ進むべきかを判断したいとき。
- apply run のライフサイクル、cleanup、state 更新、report 保存の責務境界を確認したいとき。
- パッケージ自体に初期化処理や再 export があるかを、実装詳細ではなく入口として確認したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、実行手順、エラー処理を調べたいときは、該当する各実装モジュールを直接読む。
- session state の定義や更新だけを見たいときは、apply 全体ではなく state 側の対象を読む。
- branch や worktree の一般操作、CLI 全体の共通実行基盤だけを見たいときは、このパッケージではなくより基礎の対象へ進む。

## hash
- 918837e11fd8c131df4a117ab1b9542815f1d4808a54bb24d7514aa6578143f8

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
- `cmoc indexing` の CLI 実行と、その前提確認・INDEX.md 更新・更新内容の commit までを一まとまりで扱う。`run_cli_subcommand` で実行される本体、work root を使うロック付き更新、前提検査の責務分担を確認したいときに読む。

## Read this when
- indexing サブコマンドの実行手順や、どの worktree を対象にするかを確認したい。
- INDEX.md の更新処理と、その更新差分を commit する流れを追いたい。
- 実行前に必要な worktree 安全条件や cmoc 依存条件を確認したい。

## Do not read this when
- INDEX.md の生成方針そのものを調べたいときは、更新対象の実体や indexing 実装側を読む。
- CLI の他サブコマンドや共通ランタイムの一般的な振る舞いを見たいときは、このファイルではなく対応するサブコマンドや runtime 側を読む。
- ロック実装や commit 生成の詳細な内部処理を追いたいときは、ここではなく該当する共通モジュールを読む。

## hash
- 1a10ace893665790d49691c5787a004cd8de79848adf472caa5099c64a4599b6

# `review`

## Summary
- review 系サブコマンドを束ねる小さな package の入口で、この階層が review 系機能群のまとまりであることを示す。実行ロジックや個別機能は持たず、下位の review 入口や周辺実装へ進む前の境界確認に使う。
- `review oracle` コマンドの全体制御を担う入口で、前提確認から隔離 worktree の生成・削除、review ループ起動、結果レポート出力までを一つにまとめる。実行順序や失敗時の振る舞い、worktree のライフサイクル、最終結果の集約を追うときの起点になる。

## Read this when
- review 系サブコマンド群の package 境界そのものを確認したいとき。
- この階層が review 系サブコマンド用の Python package として扱われる根拠を確認したいとき。
- `review oracle` の実行順序や失敗時の振る舞いを変えたいとき。
- session branch かどうかの判定、未コミット差分の拒否、interruption の扱いを確認したいとき。
- review 用 worktree のライフサイクルや、最終レポートに渡す実行結果の集約方法を見たいとき。

## Do not read this when
- review 系サブコマンドの具体的な CLI 挙動、引数、出力、制御フローを調べたいとき。
- review 系サブコマンド内の個別機能や実装詳細を調べたいとき。
- package 初期化時の import、副作用、公開シンボルを調べたいとき。ただし現在内容からはそのような責務は読み取れない。
- 個別の oracle 対象の列挙条件を見たいときは、対象選択側の実装を直接読む。
- index 差分の解決や merge の詳細を変えたいときは、review index 側の実装を読む。
- レポートの描画形式だけを変えたいときは、report 側の実装を読む。

## hash
- cedb335a71e46fbce3193691e06680ddf0495e5dc93bb83ca3c1bf537a0d8f6a

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
- `cmoc review oracle` の反復処理をまとめた実行ループ。新規所見の列挙、所見マージ、妥当性検証、採否判定、ユーザー中断時の部分結果保持を扱う。

## Read this when
- review oracle の周回順、dirty 判定、finding_id の扱い、中断時に残す結果、merge operation の適用ルールを確認したいとき。
- `cmoc review oracle` の loop 本体や、その途中で呼ばれる helper の責務境界を知りたいとき。

## Do not read this when
- サブコマンド全体の起動、引数解釈、レポート保存、出力整形を見たいとき。
- `codex exec` 呼び出し規約や個別 prompt の正本を確認したいとき。

## hash
- b2c5389138fd821d56cad5a577a5a618dd7fd3cf8e59a72004c5b9f66bba4bc9

# `review_paths.py`

## Summary
- `cmoc review oracle` のレポート用に、所見の `oracle_path` を絶対 path または oracle 配下の repository-relative key に正規化する。`{{oracle-root}}` の別名、root プレースホルダ、symlink を追わない扱いが関係する path 解決だけを見る。
- isolated worktree と main worktree の両方から来る path を同じ評価軸にそろえる必要があるときに読む。`worktree` / `root` の所属判定を伴う path 変換を、この module が責務として持つ。

## Read this when
- review レポートに出す oracle file の path 表示を変えたい。
- 所見データの `oracle_path` が、絶対 path・`{{oracle-root}}` 付き path・root プレースホルダ付き path のどれで来ても同じ形にしたい。
- symlink を踏まない path 正規化や、main worktree と isolated worktree の境界判定を調整したい。

## Do not read this when
- `cmoc review oracle` の所見列挙・マージ・検証・判定の手順を変えたいだけなら、より上流のレビュー手順定義を読む。
- oracle file のレビュー基準そのものを変えたいなら、この path 変換ではなく `review_oracle` 側を読む。
- `RootPathPlaceHolder` や `resolve_real_path` の一般的な実装を確認したいだけなら、この module ではなくそれらの定義箇所を読む。

## hash
- 64d912c294cf5559590fc131006b59474f97885375f456e5050ff1a2e38d80f9

# `review_report.py`

## Summary
- `review oracle` の Markdown レポートを組み立てて保存する入口。レポート本体の描画、frontmatter の値決定、所見の並び順の整形をまとめて扱う。
- 所見の集計や oracle file 表示名の整形など、レポート表示に直結する補助処理も含む。

## Read this when
- レビュー結果を timestamp 名の report file として保存する処理を変えたいとき。
- frontmatter に載るメタデータ、Verdict 文面、所見一覧の見せ方を確認したいとき。
- oracle file ごとの所見件数の数え方や、表示上の path 正規化を追いたいとき。

## Do not read this when
- レビュー対象 oracle の探索や判定ロジックそのものを変えたいときは、レビュー実行側や所見生成側を先に読む。
- report の保存先ディレクトリ設計や共通の reports 取り回しだけを見たいときは、`cmoc_runtime` 側を先に読む。
- 所見の path 解決や key 化の細部だけが目的なら、`sub_commands.review_paths` を直接読む。

## hash
- 2c5c131fddb39b1b4b98ffe2606898f1a183b48b10b371d0ddd1a87f6daefd56

# `review_targets.py`

## Summary
- `review oracle` の対象 oracle file をどう選ぶかを確認したいときの入口。`full` では全 oracle file を、`session` では session 開始時点から review fork までに変化した oracle file を対象にするため、対象集合の切り分けだけを先に判断したい場合に読む。
- review 実行本体やレポート生成ではなく、レビュー対象の列挙条件とスコープ差分の決め方を追うときに使う。

## Read this when
- review の対象 oracle file がどの条件で選ばれるかを知りたいとき。
- `session` スコープで変更差分だけが対象になる理由を確認したいとき。
- oracle file の全件列挙と、レビュー開始時点のスナップショット差分抽出の入口だけを見たいとき。

## Do not read this when
- レビュー手順の反復制御、所見のマージ、検証、採否判定を追いたいときは、実行ループ側を読む。
- レビュー結果の Markdown レポート体裁や集計を見たいときは、レポート生成側を読む。
- oracle file の定義やレビュー基準そのものを確認したいときは、oracle 側の仕様断片を読む。

## hash
- 5ec510cfdccdb608eb26afaabebb8e9075b417b1a87c3300026bf06703324b02

# `session`

## Summary
- `cmoc session` 系サブコマンド群の入口になる階層です。各サブコマンドの実処理、実行条件、状態更新、branch 操作を個別に追いたいときにここから下位モジュールへ進みます。

## Read this when
- `cmoc session` 配下のどのサブコマンド実装に進むべきかを確認したいとき。
- session 系サブコマンドの境界だけを先に把握して、個別実装を読む前に対象を絞りたいとき。

## Do not read this when
- 個別サブコマンドの処理内容を知りたいときは、`abandon.py`、`fork.py`、`join.py` などの該当モジュールを直接読む。
- 共通 CLI ルーティングや session 以外のサブコマンドを確認したいときは、この階層ではなく上位の共通実装を読む。

## hash
- 6c939256135e482c589e3b6c8d300fa48b6055b7d08987e685a6afda7c3224c3

# `tui.py`

## Summary
- `cmoc tui` の対話起動フローを担う。初期プロンプトの作成、エディタ起動、解決済みパラメータの組み立て、Codex TUI 起動までの接続点を読むときに入る。
- 補助関数群は、editor 選択、テンプレートの整形、解決パラメータの既定値補完、TUI 用 `AgentCallParameter` の生成、`.cmoc` の事前保証を分担する。

## Read this when
- `cmoc tui` の入出力や起動順、どの段階で何を編集・解決・起動するかを確認したいとき。
- TUI 用の依頼文テンプレート、既定の role / summary / goal、ファイルアクセスモードの扱い、追加の読込対象を確認したいとき。
- `.cmoc` の ignore 保証や、ログ領域に作る原稿ファイルの扱いを確認したいとき。

## Do not read this when
- `cmoc` の他サブコマンドの実行制御を見たいときは、それぞれのサブコマンド実装へ進む。
- Codex 側の実際の TUI 描画やプロンプト文面の詳細を知りたいだけなら、ここではなく参照先の正本仕様を読む。
- 一般的な設定読み込みやロギング基盤の詳細だけを追いたいときは、このファイルではなく対応する共通基盤を読む。

## hash
- 4d4dd202a1d1e85e987b296d875b6a53087d812c311e9a62aec9a3a1a3075695
