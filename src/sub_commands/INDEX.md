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
- feedback サブコマンドの実装群への入口。report の生成・検証・publication、remediation wave、run の recovery／cleanup を役割別に扱う。
- report cut を入力に observation の正規化・recurrence 集約・candidate verification・publication／incomplete 診断を行う report pipeline を扱う。
- issue 単位の remediation、seal・checkpoint・自動 join、merge 後の検証、publication recovery を含む feedback remediation の進行を扱う。
- publication 後の finalization journal に基づく cleanup／recovery、feedback run の明示 join／abandon、終了監査、report cut cleanup を扱う。

## Read this when
- feedback サブコマンドの実装を確認・変更するとき
- feedback report の report cut、observation 集約、candidate verification、publication または incomplete 診断を調査するとき
- feedback issue の remediation wave、seal、checkpoint、automatic join、merge 後検証、publication recovery を調査するとき
- feedback report publication 後の cleanup／recovery、明示 join／abandon の許可境界、終了監査や report cut cleanup を調査するとき

## Do not read this when
- feedback observation の受付・envelope 検証・raw store 保存だけを調査するとき
- normalize／remediate agent の parameter や Structured Output schema だけを確認するとき
- feedback state や run state の永続化 API、wave／join 管理、generation artifact の一般形式だけを調査するとき
- feedback 以外のサブコマンドや、feedback と無関係な report／Markdown／logging 処理を調査するとき

## hash
- ebb29b414db56d59cea8a40f10fe2277dbb922c11514471cd61962804d9b8261

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
- editing run の lifecycle サブコマンド実装と、旧 import path 互換 shim の入口。abandon・join の停止／統合／cleanup フローや、commons 側へ委譲された lifecycle・report 共通処理の所在を確認する際に読む。

## Read this when
- `cmoc run abandon` または `cmoc run join` の状態遷移、差分検査、merge、post-join、cleanup、rollback、report 保存を調査・変更するとき。
- 旧 `src.sub_commands.run.lifecycle`／report import path の互換性、commons 側への移行、shim の削除条件を確認するとき。
- editing run の lifecycle 実装の担当ファイルを特定し、abandon・join の具体処理または旧 import path の互換層から読み始めるとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。
- lifecycle・report の共通処理そのものや INDEX 生成規則、refactor state 同期規則、report 書式を確認する場合に、配下の専用実装を直接読めるとき。
- 旧 import path の互換性が関係せず、run の開始・通常実行・workload 固有編集など別の実装だけを確認するとき。

## hash
- 40e35fd9063663970e1add86290a2e56d6311a1d1e87a2233a7e472b14805f29

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
