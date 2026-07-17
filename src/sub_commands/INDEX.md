# `apply`

## Summary
- apply サブコマンド群の実装ディレクトリ。apply の abandon、fork、fork_report、join と、パッケージ入口を含み、実行ライフサイクル、cleanup、merge、レポート生成を確認するための入口。

## Read this when
- apply サブコマンドの実行制御、状態更新、worktree・branch・process の管理、cleanup 条件を調査または変更するとき。
- apply fork のレビュー・修正ループ、commit、収束判定、レポート生成を調査するとき。
- apply join の merge、force-resolve、想定外差分、conflict 処理、完了後の後始末を調査するとき。
- apply fork の完了・中断・失敗レポートの内容や変更差分の収集方法を調査するとき。

## Do not read this when
- apply 以外のサブコマンドだけを扱うとき。
- 共通の CLI runtime、session state、Git 操作、process lock などの一般実装だけを確認したいときは、対応する共通モジュールを直接読む。
- 具体的なサブコマンドの制御ロジックやレポート処理を読む必要がなく、パッケージの説明や import 時の挙動だけを確認したいときは、パッケージ入口を直接読む。

## hash
- d2dc9738d9c5b901b844d4b187faff2376b777411a9943dc5eb7dc1edb0e9a22

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
- `cmoc indexing` サブコマンドの実行入口。現在の work root を対象に、前提条件の検査、排他ロック下での INDEX.md 更新、更新差分の commit、更新件数の表示を行う。

## Read this when
- INDEX.md の maintenance 処理、`cmoc indexing` の CLI 実行条件、INDEX.md 更新の commit 処理を変更・調査するとき。

## Do not read this when
- 個別の INDEX.md エントリー内容や、インデックス生成ロジック自体を調べるとき。前者は対象の INDEX.md、後者は `commons.indexing` を直接読む。

## hash
- 1a10ace893665790d49691c5787a004cd8de79848adf472caa5099c64a4599b6

# `review`

## Summary
- review 系サブコマンド群をまとめる Python package。review oracle の CLI 実行ライフサイクルと、所見検出・対象列挙・INDEX 統合・レポート生成へ進むための入口を提供する。

## Read this when
- review 系サブコマンド群の package 境界や構成を確認したいとき。
- review oracle の実行ライフサイクルを調べるときは oracle.py を読む。
- 所見検出、oracle 対象列挙、INDEX 統合、レポート生成の具体的な処理を調べるときは、この階層内の各担当モジュールを読む。

## Do not read this when
- review oracle の具体的な所見検出ループだけを調べるとき。
- oracle 対象ファイルの列挙規則だけを調べるとき。
- review report の表示形式やファイル書き込みだけを調べるとき。
- review branch の INDEX 変更の commit・merge・conflict 解決だけを調べるとき。

## hash
- d0b68039591eb520040c7a01c7dcb12b6d27b65a6108ca7bdf6becb9892758fd

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
- レビュー対象 oracle file の finding 列挙・マージ・妥当性検証・採否判定を連続実行する中核ループ。進捗管理、中断時の部分結果保持、merge operation の検証と適用も担う。

## Read this when
- review oracle のループ制御、finding の enumerate/merge/validate/judge 処理を変更・調査するとき
- KeyboardInterrupt 時の部分結果や評価済みファイルの扱いを確認するとき
- finding merge operation の適用条件・ID 管理・意味的リトライを確認するとき

## Do not read this when
- review oracle の個別 agent call parameter 生成だけを変更・調査するとき
- review command のパス解決や CLI 入出力など、ループ本体以外を直接扱うとき
- review oracle と無関係なサブコマンドの実装を扱うとき

## hash
- d6b04ff683fc8b3f1d106f15426561f9dc2b2d3dbd406c492f7867bd21be3ab6

# `review_paths.py`

## Summary
- oracle ファイルのパスを安全に解決し、評価対象のリポジトリ相対キーへ変換する補助関数群。絶対パス、oracle-root エイリアス、既知のルートプレースホルダーを扱い、シンボリックリンクを追跡しない正規化を行う。

## Read this when
- oracle_path の解決や oracle file のリポジトリ相対キー化を変更・確認するとき
- main worktree と cmoc 管理下の isolated worktree のパス境界を確認するとき

## Do not read this when
- review report の生成ロジックや oracle 内容そのものを確認したいとき
- パス解決・oracle キー変換に関係しないサブコマンド処理を変更するとき

## hash
- 64d912c294cf5559590fc131006b59474f97885375f456e5050ff1a2e38d80f9

# `review_report.py`

## Summary
- review oracle の実行結果を Markdown レポートとして保存・描画するモジュール。レポートの保存先、YAML frontmatter、Verdict、評価対象 oracle 一覧、Fatal/Minor 所見の表示を扱う。

## Read this when
- review oracle のレポート形式、判定結果、所見の分類・表示順、評価対象 oracle の一覧を変更または確認するとき
- review oracle 実行後に生成されるレポートの保存処理やパス表示を変更するとき

## Do not read this when
- review oracle の対象 oracle file の選定・評価ロジック自体を変更または確認するとき
- 他のサブコマンドのレポート形式や、レビュー以外の永続化処理を扱うとき

## hash
- fc68feb20231a9c0576da203d66683c72b8b4b67eec4b70d57e3fdd7f98b9c72

# `review_targets.py`

## Summary
- review oracle の scope に応じてレビュー対象の oracle file を列挙する。full scope では oracle ツリー全体を対象にし、session scope ではセッション開始コミットから review fork commit までに変更された oracle file に限定する。

## Read this when
- review oracle の対象ファイル列挙処理を変更・確認するとき
- full scope と session scope の対象範囲やコミット差分の扱いを確認するとき

## Do not read this when
- oracle file の内容やレビュー実行そのものを変更・確認するとき
- review 対象列挙と無関係なサブコマンドの処理を変更・確認するとき

## hash
- 5ec510cfdccdb608eb26afaabebb8e9075b417b1a87c3300026bf06703324b02

# `session`

## Summary
- session 系サブコマンドの実装パッケージ。session の fork、join、abandon と、パッケージ初期化モジュールを下位要素として収める入口。

## Read this when
- session サブコマンド全体の構成や、fork・join・abandon のどの実装へ進むべきかを確認したいとき。
- session branch、session state、merge、破棄処理のいずれかを調査・変更するとき。

## Do not read this when
- 共通 CLI ルーティングや session 以外のサブコマンドを調べるとき。
- 特定の session サブコマンドの詳細な挙動だけを調べるとき。その場合は対応する下位実装を直接読む。

## hash
- 2ddc936b16739248793392ee38e5ae623a8c4422f180d881c9019185f1e1f834

# `tui.py`

## Summary
- `cmoc tui` サブコマンドの実行フローと補助処理を担う実装ファイル。利用者向けプロンプトの初期化・編集・読み込み、実行パラメータの解決、Codex TUI の起動、TUI 用ファイルアクセスモードの検証を扱う。TUI サブコマンドの挙動変更や関連するパラメータ構築・エディタ選択・ignore 保証を調べる際の入口。

## Read this when
- `cmoc tui` の起動処理、プロンプト編集、TUI 起動パラメータ、ファイルアクセスモード検証を変更または調査するとき
- TUI 実行前の `.cmoc` ignore 保証やエディタ選択・終了エラーの挙動を確認するとき

## Do not read this when
- TUI 以外のサブコマンドの実装を調べるとき
- 共通 CLI ランタイム、設定、ログ、パラメータビルダー自体の詳細を直接調べるときは、それらの定義元を読む

## hash
- 66edc6a24c58eeba12a447d3a68e8c7bdada3c440e6ff9fd788f8ae5daff1a84
