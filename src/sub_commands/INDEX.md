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
- feedback サブコマンドの実装領域。観測データからの report 生成、検証、checkpoint 管理、publication、診断、状態遷移および成果物の cleanup を扱う。feedback の処理全体を確認・変更する際の入口となる。

## Read this when
- feedback サブコマンドの全体フローや状態遷移を確認・変更するとき。
- report cut の固定・再開、candidate 集約、normalization／verification、report publication、current pointer、失敗時の診断や cleanup を扱うとき。

## Do not read this when
- feedback 以外のサブコマンドを扱うとき。
- feedback の正本スキーマや個別 helper の仕様・実装だけを調べるときは、対応する oracle file または直接の対象へ進む。

## hash
- e131bb8ea9f9f25768166e1c178e6f7debf6da68ce6c9b7133a00cfbe51237f3

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
- oracle 系サブコマンドの実装をまとめる package 境界。oracle の編集・調査・レビューに関する各サブコマンド実装と、レビューの対象選定・実行ループ・パス処理・レポート・INDEX 差分統合を下位要素として扱う。

## Read this when
- oracle 系サブコマンドの構成や、編集・調査・レビュー機能の実装入口を確認するとき。
- oracle review の実行 lifecycle、対象範囲、反復処理、パス解決、レポート生成、INDEX 差分統合のどこを読むべきか判断するとき。

## Do not read this when
- 個別サブコマンドの詳細な実行フローを確認する場合は、対応する実装ファイルへ直接進む。
- oracle review の finding 生成・検証・判定、対象パス、レポート、INDEX merge の詳細だけを確認する場合は、それぞれの担当実装へ直接進む。
- oracle 編集・調査のプロンプト契約や共通入力処理の詳細だけを確認する場合は、参照される oracle 仕様または共通モジュールへ直接進む。

## hash
- 297a302fb336ee090d323f3982e535c62e4fdd74ce49d4f35580beb093595862

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口。配下の apply および refactor の実装へ進むための起点となる。
- apply は apply workload の実行フロー、agent 実行後の差分検査、run 状態更新、rollback、fork report 保存を扱う。
- refactor は refactor fork の lifecycle、対象選択、変更検証、state 更新、INDEX 同期、完了・中断・エラー処理を扱う。

## Read this when
- realization workload サブコマンドの実装や構成を確認するとき。
- apply workload の実行フロー、run 状態遷移、差分検査、失敗時処理を調査・変更するときは apply へ進む。
- refactor fork の実行 lifecycle、対象選択、完了条件、変更検証、状態更新を調査するときは refactor へ進む。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。
- apply agent のプロンプト生成や差分適用仕様だけを確認するときは、より直接該当する agent 実装へ進む。
- editing run 共通 lifecycle、INDEX 生成機能、run isolation、interruption などの一般仕様だけを確認するときは、対応する共通実装・正本仕様へ直接進む。

## hash
- 917f590ce1df8dd1598a6dd7c53f92907aa03aa2ec281c003c780563f21d72a1

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
- 編集 run の共通 lifecycle サブコマンドと、その実装・互換 shim へのルーティング入口。active run の停止・統合・cleanup、共通 lifecycle helper、report writer の責務を確認するために読む。
- active editing run を状態に応じて停止し、process、worktree、branch、state、tracking を cleanup する abandon 処理。停止失敗や cleanup 未完了時の資源保持、lifecycle report の生成も扱う。
- active run の差分を検査して session branch へ merge し、INDEX.md conflict の再生成、post-join hook、refactor state 同期、report 保存、失敗時 rollback、cleanup を行う join lifecycle。
- 共通 editing run lifecycle 実装を旧 import path から再公開する互換 shim。共通処理そのものではなく、旧参照との互換性や canonical 実装への移行を確認するときに読む。
- 共通 run report writer を旧 import path から再公開する互換 shim。lifecycle report または fork report の参照互換性を確認するときに読む。

## Read this when
- editing run の停止、統合、失敗復旧、cleanup、process tracking、state 同期、lifecycle report の挙動を調査または変更するとき
- run join における想定外差分、force-resolve、INDEX.md 限定 conflict 処理、post-join hook、refactor state 同期を確認するとき
- 旧 import path の lifecycle helper または report writer の互換性を確認するとき

## Do not read this when
- editing run 以外のサブコマンドを扱うとき
- 特定の共通 helper、Git 操作、state 管理、report writer の canonical 実装詳細だけを確認するときは、それぞれの commons 側実装を直接読む
- run の workload 固有処理や CLI 一般起動処理だけを調査するとき

## hash
- e2d8137bb96c1def3e634c2c07b2f4a61f95b3a1aede98383871042558d0b68c

# `session`

## Summary
- session サブコマンドの実装パッケージ。session のライフサイクル処理を確認・変更する際の入口となり、個別処理は abandon、fork、join の各実装へ振り分ける。

## Read this when
- session サブコマンド全体の実装構成を確認するとき。
- session の作成、参加、放棄などのライフサイクル処理を調査・変更するとき。
- session 配下の個別サブコマンド実装へ進む入口を判断するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- abandon、fork、join のいずれか一つの具体的な挙動だけを確認する場合は、該当する個別実装を直接読むとき。

## hash
- 14871b5571e1d1bfa949219d406af407fb411afd8187752103edcca1a3036516

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
