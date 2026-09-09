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
- `cmoc doctor` の CLI 入口を提供する。
- CLI runtime 経由で doctor preprocess を明示的に 1 ステップ実行する。
- 実行結果に現在の repo root を固有情報として返す。

## Read this when
- `cmoc doctor` のサブコマンド入口や、doctor preprocess の明示実行経路を確認するとき。
- doctor 実行時のステップ定義や terminal result に含まれる repo root 情報を確認するとき。

## Do not read this when
- doctor preprocess の具体的な処理内容や成果物を確認したいとき。
- CLI サブコマンド共通 runtime の実装や一般的な実行制御を確認したいとき。

## hash
- 1eb417245f2ab7964031bcace08e76c91beda19e6b7c26b38e163f2ec9977c3b

# `feedback`

## Summary
- feedback サブコマンドの実装を構成するモジュール群への入口。判定根拠の構築、report の検証・publication、remediation の実行、publication 後の recovery を扱う。

## Read this when
- feedback サブコマンドの処理全体の責務分担や実装入口を確認・変更するとき。
- 判定状態、report cut と publication、issue remediation、finalization・cleanup のいずれかを調べるとき。

## Do not read this when
- feedback 以外のサブコマンドを扱うとき。
- feedback の候補分類・結果分類などの正本仕様だけを確認するとき。
- 個別の処理対象が decision、report、remediation、recovery のいずれかに明確に限定されているときは、該当モジュールを直接読む。

## hash
- a351b30e6a1aaf278df5835b678ba71fe1c975a2ad41a223ab180f1ad361717c

# `indexing.py`

## Summary
- work root の INDEX.md を更新する indexing CLI の実行入口を提供する。
- 実行前に cmoc 管理対象と clean worktree を確認し、排他ロック下で INDEX.md を更新・差分 commit し、結果を primary report に反映する。

## Read this when
- `cmoc indexing` の CLI 入口、実行前提条件、または indexing 処理全体の実行フローを確認するとき
- INDEX.md の更新、更新差分の commit、または indexing 実行結果の報告処理の呼び出し元を確認するとき

## Do not read this when
- INDEX.md の具体的な更新規則や探索・生成ロジックを確認したいときは、indexing 共通処理の対象を直接読む
- CLI 共通の実行制御や step 管理の仕様だけを確認したいときは、CLI runtime 共通処理の対象を直接読む
- worktree の clean 判定や cmoc 管理対象の検査実装だけを確認したいときは、対応する runtime 検査処理を直接読む

## hash
- 1b5fb1518b06f7acdfb54acdb2e8ab410c4772fa381bae42ed1af943e6209ce0

# `oracle`

## Summary
- oracle 系サブコマンドの package 境界を示し、oracle サブコマンド群への入口となる。
- `cmoc oracle edit` の入力収集、起動前提の検証、本命 oracle 編集 agent call と仕様削減 agent call の実行フローを担う。
- `cmoc oracle investigation` の調査指示入力、完全プロンプト構築、Codex TUI 起動までの read-only 実行フローを担う。
- 編集関連の実装ファイルを含まない空のディレクトリで、現時点の下位要素へのルーティング先はない。

## Read this when
- oracle 系サブコマンドの package 構成や入口を確認するとき。
- `cmoc oracle edit` の CLI フロー、入力編集、本命・仕様削減 agent call の起動条件や実行順序を確認するとき。
- `cmoc oracle investigation` の CLI フロー、調査指示編集、プロンプト構築、Codex TUI 起動を確認するとき。
- このディレクトリに編集関連ファイルが追加されたか確認するとき。

## Do not read this when
- 個別 oracle サブコマンドの prompt 契約や仕様そのものを確認したいとき。
- prompt editor の共通入出力処理だけを確認したいとき。
- oracle edit の agent 起動パラメータ構築だけを確認したいとき。
- oracle investigation の TUI 起動パラメータや共通 runtime の詳細だけを確認したいとき。
- oracle サブコマンドの実装を調査するときに、空の編集ディレクトリだけを確認しようとしているとき。

## hash
- ed0e9b8fea43533d9ad7c042135f4f82804bdc36036c330a8498b11afa88fc9a

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口。
- apply workload の実行入口と、editing run の作成、oracle 差分範囲の固定、追従 agent 実行、変更検査・commit、run 状態記録への入口。
- refactor fork の lifecycle、進捗、unresolved findings、完了判定、変更・commit・INDEX 更新の検証、中断・エラー時の cleanup と report 保存への入口。

## Read this when
- realization workload サブコマンドの構成や実装を確認するとき。
- realization apply workload の実行手順、差分の始点、agent 実行後の変更検査・commit、joinable/error run の状態遷移を確認するとき。
- realization refactor fork の lifecycle、進捗、完了判定、検証境界、cleanup、report 保存を確認するとき。

## Do not read this when
- realization apply・refactor 以外の処理を確認するとき。
- apply workload の agent 起動パラメータだけを確認したいとき。
- editing run の共通 lifecycle、run の join・abandon、refactor state の基本形式を確認したいとき。
- INDEX.md 生成の一般仕様や利用者向け CLI 仕様だけを確認したいとき。

## hash
- 7863e2ae464f696f8c773550be032b394c7f18036877703b399cc1b482dfb7e2

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
- editing run サブコマンドのライフサイクル処理への入口。active run の停止・join・cleanup と、旧 import path から共通処理へ移行する互換 shim の位置づけを確認できる。

## Read this when
- editing run の停止、join、cleanup、state 遷移、report 保存、worktree・branch・process tracking の扱いを調査・変更するとき。
- editing run 共通 lifecycle の旧 import path 互換性や canonical 実装への委譲関係を確認するとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。
- workload 固有の編集処理や、INDEX 生成規則、refactor state 同期規則、lifecycle report の書式など、配下または専用実装を直接確認すべきとき。

## hash
- cc257375e5b5fa0539aaac28d349f9b8fa34413c57877e0338f5d5063d9e404f

# `session`

## Summary
- session サブコマンドの実装パッケージであり、session のライフサイクル処理を確認する際の入口となる。
- session fork・join・abandon の各処理へ進むための下位実装の入口を提供する。

## Read this when
- session サブコマンドの実装構成やライフサイクル処理の入口を確認・変更するとき。
- session fork、join、または abandon の具体的な実行経路を調べるとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- SessionState の共通仕様、Git 操作の共通実装、または conflict resolution builder の詳細だけを確認したいとき。

## hash
- 2dbb14ef2fe555aa592c813a6dc6bea2bcd1a551c6e9140931e69cf339dca804

# `tui.py`

## Summary
- 利用者の依頼文を編集し、完全なプロンプトと TUI 起動パラメータを構築して Codex TUI を実行する `tui` サブコマンドの本体処理。
- プロンプト入力の準備から収集・確定、実行前のインデックス作成準備、repository context と設定を用いた TUI 起動までを担う入口。

## Read this when
- `cmoc tui` の実行経路や、利用者入力から Codex TUI 起動までの流れを調査・変更するとき。
- TUI 起動時の context・設定の受け渡しや、起動前の共通 CLI 処理を確認するとき。

## Do not read this when
- TUI 起動パラメータの詳細だけを調査・変更する場合は、パラメータ構築担当の対象を直接読むとき。
- プロンプト編集入力の予約・編集・収集・確定の仕様だけを確認する場合は、プロンプト入力担当の対象を直接読むとき。
- CLI 共通実行基盤や設定ロードの一般仕様だけを確認する場合は、それぞれの担当対象を直接読むとき。

## hash
- 40d49f1a34914cf741647d5b3151e153ee8b1f25767665901565d7443e01b08a
