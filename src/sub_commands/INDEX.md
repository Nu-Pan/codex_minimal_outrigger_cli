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
- oracle 系サブコマンドの実装をまとめるディレクトリ。oracle の編集・調査・レビューの各 CLI 実行経路と、それらを支えるレビュー対象列挙、パス解決、レポート生成、INDEX 差分処理などへの入口となる。

## Read this when
- oracle 系サブコマンドの構成や、編集・調査・レビュー機能の実装箇所を確認するとき。
- oracle review の対象列挙、パス解決、レビュー結果の出力、INDEX.md の commit・merge 処理を調査するとき。

## Do not read this when
- 個別サブコマンドの詳細な実行フローを確認する場合は、該当する実装ファイルへ直接進む。
- oracle の調査・編集契約やプロンプト内容そのものを確認する場合は、対応する oracle 仕様を直接読む。
- 共通のプロンプト入力処理や TUI 起動パラメータの詳細だけを確認する場合は、対応する共通モジュールまたは専用実装へ進む。

## hash
- ced40e35b79d0ff61c3e19d460573df1c397c904796c2a60cf129c08bf28647a

# `realization`

## Summary
- realization workload サブコマンド全体のパッケージ入口。配下の apply や refactor など、realization に関する個別 workload の実装へ進む起点となる。

## Read this when
- realization workload サブコマンドの実装構成や、apply・refactor など配下の処理を確認するとき。
- realization 配下の workload を横断して、どの個別実装を読むべきか判断するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。
- apply または refactor の具体的な実行 lifecycle や状態管理を確認する場合は、対応する個別実装へ直接進むとき。

## hash
- 9755f41edc34313f6424146666e7267651d9b1978e880bc0993ab6fcc9844c25

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
- session サブコマンドの実装パッケージ。session の各ライフサイクル処理を確認・変更する際の入口であり、開始・継続・完了・破棄に相当する個別処理へ進むためのルーティングを担う。

## Read this when
- session サブコマンドの実装構成や、fork・join・abandon の各処理の入口を確認するとき。
- session の branch・state を扱うライフサイクル処理を確認・変更するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- 特定の session 処理の詳細を確認する場合は、該当する個別サブコマンド実装を直接読む。
- session state の一般定義や共通 runtime の仕様だけを確認する場合は、それぞれの正本仕様・共通実装を直接読む。

## hash
- eca8a6509002c96e29d6832c8753e099c704b3a21f6823212b83ce7d5dc542ad

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
