# `apply`

## Summary
- この場所には現在サブコマンドの実装ソースがなく、現行の realization apply fork 処理は realization 系統にあります。

## Read this when
- apply の実装を探していて、現行の realization apply fork 処理の所在を確認したいとき。

## Do not read this when
- realization apply fork の処理を調べたり変更したりするときは、その実装を直接確認してください。
- run の join や abandon の処理を調べるときは、run 系統の実装を確認してください。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `doctor.py`

## Summary
- `cmoc doctor` の CLI 固有の入口です。共通の CLI 実行管理に接続し、doctor 前処理を明示的な単一ステップとして実行して、そのコマンド固有の結果を組み立てます。

## Read this when
- `cmoc doctor` の呼び出し単位の挙動や、前処理の明示実行・コマンド固有の結果を変更または確認するとき。

## Do not read this when
- doctor 前処理の修復内容や Git・index の扱いを調べるときは、共通前処理の実装を直接確認してください。
- 全サブコマンドに共通する実行ライフサイクルを調べるときは、共通 CLI 実行管理を確認してください。
- コマンドの登録や CLI 全体の構成を調べるときは、CLI のコマンド定義を確認してください。

## hash
- 1eb417245f2ab7964031bcace08e76c91beda19e6b7c26b38e163f2ec9977c3b

# `feedback`

## Summary
- Feedback observation を `cmoc feedback report` として処理し、issue の修復と自動 join を経て current report を publication するサブコマンド実装群です。
- report cut と候補処理、判定根拠の比較、publication 後の復旧が連携するため、サブコマンド全体の挙動を調べる入口になります。

## Read this when
- `cmoc feedback report` の入力固定、候補生成・集約、再検証、report publication の流れや結果を調べるとき。
- feedback issue の修復 wave、checkpoint、rollback、自動 join の制御を変更するとき。
- issue の再確認要否や、修復が同じ判定状態へ戻る場合の扱いを変更するとき。
- publication 後の cleanup・再開や、feedback run 固有の join／abandon 制約を調べるとき。

## Do not read this when
- raw feedback の収集や共通保存形式・artifact 検証だけを変更するときは、収集処理と共通 runtime の責務から確認してください。
- feedback_report 固有の制約や復旧が関係しない一般的な run の join／abandon や git lifecycle が対象なら、共通 run lifecycle の実装を直接確認してください。

## hash
- 168c1caef386191dc7f27066e4d357918e97d9c55d414ece27bd70c31a19be9d

# `indexing.py`

## Summary
- `cmoc indexing` の実行フローを組み立て、work-root の `oracle/doc` を対象に文書検索索引を同期します。
- 同期スコープの識別情報、同期結果、失敗状態を primary report に反映します。

## Read this when
- `cmoc indexing` の実行条件や、同期に渡すスコープ・設定を確認または変更するとき。
- 同期状態や結果が primary report にどう反映され、同期エラーがどう扱われるかを確認するとき。

## Do not read this when
- CLI 上のコマンド登録やヘルプ表示だけを確認するときは、CLI 宣言を直接確認してください。
- 索引の構築・保存・検索処理やスコープの共通定義を確認するときは、それぞれを担う共通検索処理やスコープ定義から確認してください。

## hash
- a3dae2674a00b244fdb950cb7c7548ce710dc62032e20dbf0951d3bf4cce86e3

# `oracle`

## Summary
- `cmoc oracle edit` と `cmoc oracle investigation` の実行フローをまとめる入口です。指示入力を受け付け、編集では Codex exec を2回順に実行し、調査では Codex TUI を起動します。
- 編集フローは main worktree 上の active な cmoc session branch を確認し、両フローで oracle 文書の検索範囲を使います。

## Read this when
- oracle コマンドの指示入力から exec／TUI 起動までの流れや、そのステップ・実行状態の管理を調べる、または変更する場合。
- 編集コマンドの起動条件や2回の exec 実行、調査コマンドの TUI 起動方法を変更する場合。

## Do not read this when
- agent に渡す prompt の内容や起動パラメータの構築を変更する場合。各コマンドの builder 実装を直接確認してください。
- 共通の prompt editor、文書検索範囲、CLI 実行基盤の挙動だけを変更する場合。それぞれの共通実装を直接確認してください。

## hash
- b775d0d47d85945c03e5fac73092facc10bce994117425dbcbd0e388a60395c1

# `realization`

## Summary
- `realization apply fork` と `realization refactor fork` の実行処理を担い、run の作成、変更の検査と commit、完了・中断・失敗の報告を管理する。
- apply は oracle の差分に沿った追従を行い、refactor は分類済みの oracle file と realization file を順に調査・修正して、未解決の所見も記録する。

## Read this when
- `realization apply fork` が oracle 差分を処理し、変更を run の成果物として公開する流れを調べるとき。
- `realization refactor fork` の対象巡回、所見の追跡、処理単位の確定、中断時の扱いを調べるとき。

## Do not read this when
- refactor の対象分類、state schema、対象選択規則だけを調べる場合は、共有 refactor runtime を直接読む。
- agent 向け指示や structured output の組み立てだけを調べる場合は、builder 側へ進む。
- CLI のコマンド登録だけを調べる場合や、全コマンド共通の run lifecycle・report 処理だけを調べる場合は、それぞれの入口・共通 runtime を直接読む。

## hash
- 47fa22b3e075f343e7ab769c1d95c4cdc9184eeba113ebd4667da63f94dfc01b

# `review`

## Summary
- 現状、レビュー関連の実装ソースはなく、無視対象のコンパイル済みキャッシュだけが残っています。現行 CLI のレビュー機能の実装入口としては扱えません。

## Read this when
- このディレクトリにレビュー実装が存在するか、残存キャッシュの状態を確認するとき。

## Do not read this when
- 現行 CLI のコマンド構成や oracle edit・investigation の挙動を調べるときは、CLI 定義とそれらの実装を直接確認してください。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `run`

## Summary
- 既存の editing run を join して差分を統合する処理と、abandon して process・worktree・branch を cleanup する処理を扱う。merge 後の状態・report 更新や失敗時の復旧を変更するときの入口。
- 共通 lifecycle・report helper の旧 import 経路を保つ shim も含む。共通 helper の本体ではなく、この package からの互換 export を変更するときに参照する。

## Read this when
- active run の join・abandon、merge 失敗時の rollback、cleanup の再試行、状態や report の確定方法を変更するとき。
- run lifecycle・report helper の互換 export を変更するとき。

## Do not read this when
- workload ごとの新規 run 開始や準備の流れだけを変更するときは、その workload の開始処理を直接読む。
- 共通 lifecycle・report helper の実装や feedback 固有の recovery ルールだけを変更するときは、それぞれの共通 helper または feedback recovery の実装を直接読む。

## hash
- 02e252fa9d14209ce0fee2cfc66f30aad209c9c8082f8d13a2e823dd5620af21

# `session`

## Summary
- session branch と state のライフサイクルを扱い、現在の local branch からの fork、home branch への join、取り込まずに終了する abandon の処理をまとめる。
- session 全体の作成・統合・終了を調べる入口であり、個々の編集 run の処理とは責務が異なる。

## Read this when
- session fork の作成条件、branch と state の保存、失敗時の rollback を確認・変更するとき。
- session join の merge、競合解消の呼び出し、state 更新、branch cleanup の流れを確認・変更するとき。
- session abandon の cleanup や、失敗後に session を復元する処理を確認・変更するとき。

## Do not read this when
- CLI のコマンド登録や利用者に見える入口だけを確認するときは、その登録を担う箇所へ進む。
- 編集 run の開始・実行・join・abandon が対象なら、run のライフサイクル実装へ進む。
- join が呼び出す競合解消 agent の入力組み立てだけが対象なら、その専用 builder の実装へ進む。

## hash
- 2c60b7680bab50a72dfcfa7d2440583572fc8ecd56fb34c7f91d91968bfa38a0

# `tui.py`

## Summary
- `cmoc tui` の CLI 実行フローを調整し、実行前処理、実行段階、リポジトリと worktree の設定読み込みをまとめる。
- 依頼文の編集用入力とプロンプト骨格を準備し、編集後の依頼文から起動パラメータを構築して Codex TUI に渡す。

## Read this when
- `cmoc tui` の実行順序や、入力編集からパラメータ構築、Codex TUI 起動までの連携を変更するとき。
- このコマンド固有の実行前処理、検索範囲、設定選択、実行ステップを調べるとき。

## Do not read this when
- 入力ファイルの予約、編集、検証、保存の共通動作を変更するときは、共有プロンプト入力の担当を読む。
- TUI 用プロンプトの内容や起動パラメータの組み立てを変更するときは、TUI 起動パラメータの担当を読む。
- Codex TUI プロセスの起動方法を変更するときは、TUI 実行ランタイムの担当を読む。
- 別の CLI コマンドの処理を調べるときは、そのコマンドの担当から読む。

## hash
- 173e64179de97c117feb5c3e14dc6413a00d6ed9934883c544228cca674c1c00
