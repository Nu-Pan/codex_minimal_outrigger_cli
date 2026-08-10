# `apply`

## Summary
- 現在、apply サブコマンドの実装ファイルはありません。

## Read this when
- apply サブコマンドの実装が追加された後、その内容を確認するとき。

## Do not read this when
- apply 以外のサブコマンドを扱うとき。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `doctor.py`

## Summary
- `cmoc doctor` サブコマンドの実装。CLI ランタイム経由で doctor preprocess を 1 ステップ実行し、完了後に repo_root を表示する。doctor コマンドの実行経路と preprocess 呼び出しの入口として扱う。

## Read this when
- doctor サブコマンドの実装や実行手順を変更・調査するとき
- doctor preprocess の呼び出し位置、実行ステップ、表示内容を確認するとき

## Do not read this when
- doctor preprocess 自体の仕様や処理内容を確認したいときは、参照される oracle/doc/app_spec/doctor_preprocess.md を直接読む
- CLI ランタイム共通処理の仕様や実装だけを確認したいとき

## hash
- 48cc149773f0620f64d4650bed55bdb7b42dada088e55d312892186978176836

# `feedback`

## Summary
- feedback サブコマンドの実装領域。feedback の CLI 入口と、raw observation から report の検証・集約・生成・公開・cleanup までの active-state publication pipeline を扱う。
- feedback report の処理順序、再開可能な report cut、checkpoint、writer lock、candidate 集約、normalization/verification、current pointer 公開の挙動を確認・変更するときの入口。

## Read this when
- feedback サブコマンドの挙動や実装を確認・変更するとき。
- feedback observation から issue candidate や machine aggregate を作る処理、deduplication、30 日 recurrence threshold を調査するとき。
- normalization・verification、report artifact の生成、publication、失敗・中断・cleanup 状態の遷移を調査するとき。

## Do not read this when
- feedback observation の envelope や active state の永続化形式そのものを確認する場合は、参照される runtime feedback state/store の実装を直接読む。
- normalization・verification の agent prompt や Structured Output schema の正本を確認する場合は、対応する builder と oracle schema を直接読む。
- CLI の一般的な実行基盤、session/run state、ログ機構の共通仕様を確認する場合は、各共通モジュールを読む。
- publication 後の Markdown report 表示だけを確認する場合は、report の生成処理または実際の出力 artifact を直接読む。

## hash
- 7758528ba1cd0299f38f05abd815c88f5d344d9d6737c8e542419859e3891553

# `indexing.py`

## Summary
- `cmoc indexing` サブコマンドの CLI 実行入口。worktree の安全条件を確認し、ロック下で INDEX.md の更新と差分 commit を実行する。

## Read this when
- `cmoc indexing` の実行フロー、worktree 前提条件、インデックス更新・commit 処理を変更または調査するとき。

## Do not read this when
- インデックス更新の具体的な処理や commit の実装自体を調査するときは、`commons.indexing` の実装を直接読む。
- 他のサブコマンドの CLI 実行フローだけを調査するとき。

## hash
- 648fe512e7039f2060fbe5969945f9992a0b8b3697e92d2cbbf949083d8804ce

# `oracle`

## Summary
- oracle 系サブコマンドの実装をまとめる package で、oracle の編集・調査・レビューを行う CLI の入口と関連する処理を扱う。
- 編集・調査サブコマンドの起動処理に加え、レビュー対象の列挙、review loop、パス解決、INDEX 差分の merge、レポート生成までが下位要素に分割されている。各機能の詳細を確認する際の入口となる。

## Read this when
- oracle サブコマンド群の構成、共通する責務の分担、または個別サブコマンドへの入口を確認するとき。
- oracle review の実行管理から対象列挙、判定ループ、INDEX merge、レポート生成までの関連実装をたどるとき。

## Do not read this when
- 特定のサブコマンドの実行フローやレビュー補助処理の詳細だけを確認する場合は、該当する下位実装を直接読む。
- oracle 編集・調査・レビューの契約やプロンプト内容そのものを確認する場合は、参照される oracle 仕様を直接読む。

## hash
- 5f7d625641883143b44ef90c1b87b3958c79739eb1af1d0a2f022b19382d09f9

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口。apply workload と refactor fork の実装、およびそれぞれのCLI実行フローへ案内する。

## Read this when
- realization workload サブコマンドの実装構成や入口を確認するとき。
- realization apply の実行、差分検査、run lifecycle、成果物commit、fork report、異常時処理を調査するとき。
- realization refactor fork の対象選択、agent呼び出し、変更・状態検証、finding追跡、完了判定、cleanup、report生成を調査するとき。

## Do not read this when
- realization apply や realization refactor 以外の処理を扱うとき。
- apply fork の実行パラメータ構築だけを確認するときは、対応するlaunch parameter builderを直接読む。
- refactor agent promptやchange summaryの入力形式だけを確認するときは、対応するbuilder実装を直接読む。
- 編集runの共通ライフサイクル、git変更分類、process tracking、report書式などの一般実装だけを確認するときは、インポート先の共通runtimeモジュールを直接読む。
- 正本仕様そのものを確認するときは、対応するoracle docを直接読む。

## hash
- de21ea428f2f02cf3349981ad06b9033e9d85844bf7e51a2648e48b4de04f751

# `review`

## Summary
- review サブコマンドの realization 実装を配置するディレクトリ。現在は実装本文がなく、レビュー処理の具体的な入口として参照できる下位要素はない。

## Read this when
- review サブコマンドの実装ファイルを追加・変更する場所を確認するとき。

## Do not read this when
- oracle review の処理内容や仕様を調べるときは、対応する oracle 実装・仕様文書を直接読む。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `run`

## Summary
- editing run の共通 lifecycle サブコマンドをまとめるパッケージ。active run の破棄・統合、共通ライフサイクル処理、run report writer への入口を提供する。
- abandon.py は active editing run の停止、関連プロセス・worktree・branch・state の cleanup、ライフサイクルレポート出力を扱う。
- join.py は active editing run の merge、conflict 解決、post-join 処理、state 同期、report 保存、rollback、cleanup を扱う。
- lifecycle.py と report.py は、それぞれ共通 lifecycle 実装と report writer の旧 import path を維持する互換 shim である。

## Read this when
- editing run の abandon または join の実行条件、状態遷移、merge・cleanup・rollback を調査・変更するとき。
- run worktree、branch、state、process tracking、lifecycle report、post-join 処理の連携を追跡するとき。
- editing run 共通 helper や report writer の旧 import path との互換性を確認するとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。
- 特定の共通 lifecycle や report writer の実装詳細だけを確認する場合は、canonical な commons 側の実装を直接読む。
- workload 固有の編集処理や、一般的な Git runtime helper の仕様だけを確認する場合。

## hash
- b9be04f44dd594a3090de6e402b3418a738e1dac102b9ac48826ba41754aa7e9

# `session`

## Summary
- session サブコマンドの実装パッケージ。session の各ライフサイクル処理を確認する際の入口となる。
- session の abandon、fork、join における branch 操作、state 更新、競合解消、失敗時の復旧を扱う。

## Read this when
- session サブコマンドの実装や構成を確認・変更するとき。
- session の作成、離脱、統合、branch・state のライフサイクルを調査するとき。
- session join の merge conflict 解消や検証処理を確認するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- session の共通 state データ構造、runtime Git 処理、Codex 実行規則だけを確認したいときは、それぞれの共通実装や定義を直接読む。

## hash
- 8a0dfef628903e21e7fae720cdfc2150168e3c41e5d0776d9d80ec9fd63a111d

# `tui.py`

## Summary
- `cmoc tui` サブコマンドの実行入口と本体処理を担う。プロンプト編集用入力を準備・収集・確定し、固定パラメータで Codex TUI を起動する。

## Read this when
- `cmoc tui` の起動フロー、プロンプト編集、Codex TUI 起動処理を変更または調査するとき。
- TUI 実行前の indexing preflight、ログ前チェック、サブコマンド進捗管理の連携を確認するとき。

## Do not read this when
- TUI 起動パラメータの構築仕様だけを確認する場合は、パラメータ builder の実装を直接読む。
- プロンプト入力・保存・確定の詳細仕様だけを確認する場合は、prompt editor input 関連の実装または参照された正本仕様を直接読む。
- Codex TUI 自体の実行実装や共通 CLI ランタイムの挙動だけを確認する場合は、各ランタイム実装を直接読む。

## hash
- c544eb81e5f42cc514f3b4ffc390709325ed6cdb0cdd79ec833f4beff51e1ffa
