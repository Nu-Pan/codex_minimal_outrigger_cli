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
- feedback サブコマンド実装の入口。feedback 関連の CLI 処理を確認・変更するときに参照する。
- 固定済み report cut を起点に、feedback report の検証、checkpoint 管理、issue・machine 集約、candidate 検証、正常 publication、incomplete 診断を処理する。feedback report の実行経路や状態遷移を調べる際の中心的な実装対象である。

## Read this when
- feedback サブコマンドの実装や CLI 入口を確認・変更するとき。
- feedback report の report cut 固定、再開・中断・失敗処理、cleanup、checkpoint、writer lock、current pointer の挙動を調べるとき。
- feedback observation の検証結果を用いた normalization、verification、candidate 集約、正常 publication、incomplete 診断の処理を調べるとき。
- feedback state と feedback report の仕様に対する実装対応を確認するとき。

## Do not read this when
- feedback report 以外のサブコマンドを扱うとき。
- feedback observation の入力形式や raw store の保存処理だけを調べるときは、観測入力と保存を直接定義する対象を先に読む。
- issue normalization・verification 用の agent prompt や Structured Output schema だけを調べるときは、それぞれの builder・schema を直接読む。
- report の Markdown 表示形式だけを確認するときは、report rendering を仕様化する対象を先に読む。

## hash
- 247bd90db7c4b0a6ae3200d51a272f144142be3e05b33c1e8f81a1ead4a0263c

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
- realization workload サブコマンドのパッケージ入口で、配下の apply workload と refactor 処理へ進むための上位エントリー。
- apply workload と refactor fork の実装を、それぞれの処理構成・ライフサイクル・状態管理・報告処理の確認対象として案内する。

## Read this when
- realization workload サブコマンドの構成や実装入口を確認するとき。
- realization apply workload、特に apply fork の処理順序・状態遷移・差分適用・commit/rollback・report・cleanup を調査するとき。
- realization refactor、特に refactor fork の対象選択・調査修正・進捗状態・完了判定・commit・report・割り込み処理を調査するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。
- realization apply の仕様や共通 editing run の契約を確認するときは、対応する oracle/specification または共通 runtime 実装を直接読む。
- fork 以外の apply サブコマンド固有処理、単一 realization file のレビュー・修正、変更概要の分類・要約、refactor state の一般的な同期・保存・対象選択だけを確認するときは、対応する下位実装を直接読む。

## hash
- 49b9177f9507abc46a43ebf91a65f855cddc3e4b3d3634245926a02571ad9ef5

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
- editing run サブコマンドの共通 lifecycle 実装と、関連する abandon・join・旧 import path 互換 shim の入口。active run の停止、merge、cleanup、state・report 更新などの実装経路を確認する際に、配下の該当ファイルへ進むために読む。

## Read this when
- editing run サブコマンドの共通 lifecycle や配下の実装を横断して確認するとき。
- run abandon の停止、cleanup、state 更新、失敗時の再試行可能状態を調べるとき。
- run join の merge 前後処理、INDEX 再生成、rollback、report 保存、cleanup を調べるとき。
- 旧 import path の互換 shim と canonical 実装への委譲関係を確認するとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。
- run の正本仕様や状態遷移を確認するときは、対応する app_spec・lifecycle 仕様を直接読む。
- workload 固有の編集・apply・refactor 処理を確認するときは、対応する workload 固有の実装を直接読む。
- 共通 runtime helper や report writer の具体的な挙動を確認するときは、canonical 実装を直接読む。
- 旧 import path との互換性が関係しない場合は、lifecycle.py や report.py の shim を読む必要はない。

## hash
- bf31b65cdb0353a73a14c0edd0e7dd69845bdd50bbe2cdc0aa876f71b4105f2b

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
