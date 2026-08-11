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
- feedback サブコマンドの実装領域。feedback サブコマンド共通の入口と、観測データから issue candidate を検証・集約し、report artifact と current pointer を再開可能な transaction として publication する report 処理を扱う。

## Read this when
- feedback サブコマンドの挙動、処理順序、状態遷移、再開動作を確認・変更するとき
- feedback observation から issue candidate への変換、normalization、recurrence 集約、verification を調べるとき
- feedback generation、Markdown report、current pointer の publication、interruption、cleanup を調べるとき

## Do not read this when
- feedback observation の書き込みや共通 state/store のデータ形式だけを調べるとき
- normalize/verify 用 agent prompt や Structured Output schema の契約だけを確認するとき
- feedback 以外のサブコマンドを扱うとき

## hash
- a05c1144474e800bc478bccd588060aec29026db9c4d9c9b1a864b16060b3609

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
- oracle 系サブコマンドを構成する実装群をまとめる package の境界であり、oracle の編集・調査・レビューに関する CLI 実行、レビュー制御、対象選定、パス解決、レポート生成などの下位実装へ進む入口です。

## Read this when
- oracle 系サブコマンドの構成や、編集・調査・レビュー機能の実装入口を確認するとき。
- oracle review の実行制御、対象選定、パス解決、結果出力といった関連実装の所在を把握するとき。

## Do not read this when
- 特定の oracle サブコマンドの詳細な実行フローを確認するときは、該当する個別実装を直接読んでください。
- oracle 編集・調査・レビューの契約やプロンプト内容そのものを確認するときは、対応する oracle 仕様を直接読んでください。

## hash
- f3d7d78e2a812543dabb7c6810b328632f4c00f2ae58601de7c6708264582b08

# `realization`

## Summary
- realization workload サブコマンドを構成するパッケージで、サブコマンドの入口、apply 処理、リファクタリング処理へのルーティングを担う。配下の各実装を確認するための上位入口。

## Read this when
- realization workload サブコマンド全体の構成や、apply・リファクタリング処理のどちらを確認すべきか判断するとき。
- realization サブコマンドの実装領域を調査または変更するとき。

## Do not read this when
- realization workload に関係しないサブコマンドを確認するとき。
- apply の実行ライフサイクルだけを調査する場合は apply の対象へ、リファクタリングの実行フローだけを調査する場合は refactor の対象へ直接進む。

## hash
- 52de2b20ad84777810fb00969bf4d07b114bd3f917c4de29c9748ed61871551f

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
- editing run の共通 lifecycle サブコマンドと、旧 import path を維持する互換 shim をまとめるパッケージ。`abandon` と `join` の停止・終了・cleanup 処理、および共通 lifecycle/report 実装への入口を提供する。

## Read this when
- `cmoc run abandon` または `cmoc run join` の lifecycle、process 停止、差分検査、merge、report、resource cleanup を調査・変更するとき。
- editing run 関連の旧 import path と canonical な共通実装の対応関係を確認するとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。
- 共通 lifecycle や report の実装詳細だけを確認する場合は、canonical な commons 側の実装を直接読む。
- 特定の run 処理の詳細を調べる場合は、このパッケージ入口ではなく該当する実装ファイルを直接読む。

## hash
- 29cc74a42dc1ea81641da803919b7bd2c6516f4871db1c58377724e48f0ad7cf

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
