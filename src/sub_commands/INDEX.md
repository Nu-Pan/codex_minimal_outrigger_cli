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
- feedback サブコマンドの実装をまとめたディレクトリ。report cut を起点に、raw observation の固定・検証、issue 正規化、machine observation 集約、candidate verification、正常 publication／incomplete 診断までの feedback report 処理を追跡・変更するときの入口。
- publication pipeline の writer lock、checkpoint、current pointer、generation artifact、cleanup、中断・失敗状態を扱う実装と、その配下の report 処理へ進むための入口を提供する。

## Read this when
- feedback サブコマンドの挙動、処理順序、再開可能な report cut、publication、incomplete 診断、cleanup を確認・変更するとき
- feedback report の issue candidate 正規化、machine recurrence 集約、verification、active generation 更新を調査するとき
- report cut manifest、checkpoint、current pointer、generation artifact の整合性や中断時の状態遷移を確認するとき
- feedback サブコマンド配下の実装の責務分担や、report 処理の詳細入口を確認するとき

## Do not read this when
- feedback state の永続形式や report cut／generation の共通 helper 契約だけを確認したいときは、対応する共通 helper を直接読む
- raw observation の保存、canonical JSON、secret masking、path 制約だけを確認したいときは、feedback store の実装を直接読む
- normalization／verification agent の prompt builder や Structured Output schema だけを確認したいときは、対応する builder／schema を直接読む
- feedback report の正本仕様や interruption 契約だけを確認したいときは、対応する仕様書を直接読む
- feedback 以外のサブコマンドを扱うとき

## hash
- 02d17cd0bb5710dc0394527b1524d11102df0ccdadd5f27cdaab6acf367462de

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
- oracle 系サブコマンドの実装をまとめる package。oracle の編集・調査・レビューに関する CLI 実行入口と、レビュー対象の列挙、実行 loop、パス解決、INDEX 差分処理、レポート生成の下位実装への入口を提供する。

## Read this when
- oracle サブコマンド群の構成や、各サブコマンド実装・レビュー関連モジュールへの入口を確認するとき。
- oracle の編集、調査、レビューの CLI 実行フローを横断して調べるとき。

## Do not read this when
- 特定の oracle サブコマンドの詳細な実行処理を確認する場合は、対応する個別実装を直接読む。
- oracle の仕様やプロンプト契約そのものを確認する場合は、参照される oracle 仕様を直接読む。
- 共通入力処理、TUI 起動パラメータ、レビュー loop、INDEX merge、レポート形式など単一の責務だけを調べる場合は、対応する下位モジュールを直接読む。

## hash
- 591a4f6d4908c9ce98815bd2deee760a75273e200444f5ea066327dd965d35c1

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口で、配下の apply と refactor の処理へ進むための起点。apply workload の実行フローや refactor fork のライフサイクルを確認する際に対象を選ぶ。

## Read this when
- realization workload サブコマンドの実装構成や入口を確認するとき。
- apply workload または realization refactor の処理を調査・変更するとき。

## Do not read this when
- realization に関係しない処理を確認するとき。
- 共通ライフサイクル、CLI 契約、INDEX 更新規則など、より直接対応する共通実装や正本仕様を確認するとき。

## hash
- 69e98a3c5cc5c69a34276cc6e1e7368b204ef4f49af540303b1de06d598a2773

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
- session サブコマンド群の実装をまとめたパッケージ。session の fork・join・abandon 各ライフサイクル処理を確認する際の入口となる。
- fork は session branch と state の作成、join は home branch への merge と session branch の後処理、abandon は session の中止と状態・branch の cleanup を担当する。

## Read this when
- session サブコマンドの実装構成や、fork・join・abandon のライフサイクル処理を確認・変更するとき。
- session branch、state 更新、merge、cleanup の責務分担を把握する必要があるとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- session state のデータ構造や CLI 共通 runtime の仕様だけを確認するときは、それぞれの共通実装を直接読む。

## hash
- 1b1611b1ea2d8279a73a3618517b9350f41d554703ee4341f2ef485077c7e30c

# `tui.py`

## Summary
- `cmoc tui` サブコマンドの実行入口。インデックス前処理とログ前チェックを行い、現在のリポジトリ状態から設定を読み込んで、プロンプト編集、完全プロンプト確定、Codex TUI 起動までの処理を束ねる。TUI 起動フロー全体の責務や、サブコマンド実行時の固定手順を確認するときの入口となる。

## Read this when
- `cmoc tui` サブコマンドの実装や起動経路を調べるとき。
- プロンプト編集後に Codex TUI を起動する処理の流れを確認するとき。
- TUI 実行時のインデックス前処理、ログ前チェック、設定読み込みの接続点を確認するとき。

## Do not read this when
- プロンプト入力の予約・収集・確定処理の詳細だけを調べるときは、対応するプロンプト編集ヘルパーを直接読む。
- TUI 起動パラメータの構築仕様だけを調べるときは、TUI 起動パラメータの builder を直接読む。
- 他の CLI サブコマンドの実装を調べるとき。

## hash
- cacb2eae3a201d06057dd49a7879e0f55a6d8ec151e0568fda9487924961cb2d
