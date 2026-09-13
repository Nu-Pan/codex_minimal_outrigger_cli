# `doctor.md`

## Summary
- `cmoc doctor` コマンドの仕様への入口。doctor preprocess の明示的な呼び出し、引数・事前条件・実行手順、および全終了経路で保存する primary report の要件を扱う。

## Read this when
- `cmoc doctor` の呼び出し方法、実行前提、処理委譲先、または doctor 実行結果の primary report 要件を確認するとき。

## Do not read this when
- doctor preprocess 自体の検証・修復内容を確認したいときは、正本である doctor preprocess の仕様を直接読む。
- `cmoc doctor` 以外のサブコマンドの仕様や、primary report の一般的な仕組みだけを確認したいとき。

## hash
- e004c75b5a42802cdae0ddd2d023d7ccf4b5fcc7f7065f6ee33a285dd6ad1330

# `editing_run.md`

## Summary
- 編集 run を開始する workload、同時実行制約、共通開始・終了処理、join／abandon の検証・差分検査・cleanup、および report と terminal result の共通仕様を定める。

## Read this when
- realization apply／refactor または feedback report の編集 run lifecycle を実装・変更・調査するとき
- cmoc run join／abandon の事前条件、merge、post-join、状態遷移、差分扱い、cleanup を確認するとき
- editing run の report や terminal result に必要な共通情報と終了経路を確認するとき

## Do not read this when
- run の隔離資源や session／run state の正本定義だけを確認したいとき
- realization apply、realization refactor、feedback report の workload 固有処理だけを確認したいとき
- oracle edit、read-only investigation、session lifecycle、または conflict 解消の仕様を確認するとき

## hash
- ba9914a84f850ac36212be33adf25c274aed5767c3045eddb7ab0c0989c78339

# `feedback_report.md`

## Summary
- `cmoc feedback report` の開始・再開条件、intake wave、issue 単位の remediation、差分検証・commit、auto join、publication、recovery、interruption、error、および report・終了コードの正本仕様を扱う。
- feedback observation を issue identity に正規化し、安全な realization 修正を行って自動 join する処理全体の入口であり、feedback report の実行動作や失敗時の state 保持を確認するための対象。

## Read this when
- `cmoc feedback report` の CLI 契約、事前条件、run 開始・再開、または session との隔離境界を確認するとき。
- raw observation の validation、machine・agent observation の normalization、issue remediation call、Structured Output、差分受理、issue commit、rollback の仕様を確認するとき。
- intake wave の自然完了条件、auto join、join 後検査、publication、incomplete、user interruption、error recovery の扱いを確認するとき。
- 正常・診断・中断・エラー時の report 保存内容、表示対象、および終了コードを確認するとき。

## Do not read this when
- raw observation の収集方法、結果分類、feedback state の schema や report cut の詳細そのものを確認したい場合は、本文が参照する各正本仕様を直接読む。
- normalize issue や remediate issue の prompt、workload 固有パラメータ、Structured Output schema の詳細を確認したい場合は、本文が指定する builder と schema を直接読む。
- branch model、run isolation、編集 run 共通仕様、差分検証、割り込みなどの一般規則だけを確認したい場合は、本文が参照する共通仕様を直接読む。
- feedback report の処理全体ではなく、個別の observation 収集・state 管理・agent call 実装・report 出力実装だけを調べる場合。

## hash
- e0d8c7ffcf1eb59c94285b7e2e5b938ee4bf966681324ede8196f394f5bc6df7

# `indexing.md`

## Summary
- `cmoc indexing` の実行契約と、全終了経路で保存するインデクシング実行要約を定義する仕様。
- 作業ツリーの変更確認から doctor preprocess、明示的なインデクシング実行、primary report 保存までの入口。

## Read this when
- `cmoc indexing` の実行条件や実行手順を確認したいとき。
- インデクシング実行の成功・失敗時に必要な報告内容と保存責務を確認したいとき。

## Do not read this when
- インデクシング処理の詳細仕様を確認したいとき。
- 特定の実行結果や診断ログを確認したいとき。

## hash
- 8a2acc19195064829931578f12875ea420efb5ab64e1889c6c68e9ebfbad5381

# `oracle_edit.md`

## Summary
- `cmoc oracle edit` の目的、引数、ユーザー指示からの prompt 構築、本命・仕様削減 agent call の実行順序と編集境界を定める。
- doctor preprocess、indexing preflight、起動前条件、失敗時処理、primary report、ログ、通知、終了状態および差分の扱いを確認するための入口。

## Read this when
- `cmoc oracle edit` の実行可否や実行順序を確認するとき。
- oracle file の編集を agent に委譲する処理、仕様削減 call、report・ログ・terminal result の扱いを変更または調査するとき。
- 他の workload と異なり、run lifecycle、worktree 操作、自動 commit、終了後 indexing を行わない境界を確認するとき。

## Do not read this when
- oracle file の内容そのものや oracle file を扱う判断基準を確認したい場合は、参照先の oracle 関連仕様を直接読むとき。
- prompt editor input、codex exec の共通規則、doctor preprocess、indexing、console・通知の詳細だけを確認したい場合は、それぞれの正本仕様を直接読むとき。
- 実装の具体的な起動処理や builder の詳細だけを確認したい場合は、指定された実装ファイルを直接読むとき。

## hash
- 97a58e3280ca0c36a137af24e1a1ab623bb16d5db612c172de14728b8f2eb16c

# `oracle_investigation.md`

## Summary
- oracle file に関するユーザーの調査指示を受け取り、doctor preprocess と prompt editor input lifecycle を経て Codex CLI の TUI を起動するサブコマンド。oracle file を根拠とする調査結果を日本語中心でユーザーへ回答する。

## Read this when
- oracle file の内容や扱いを調査したいとき
- oracle file に関する調査指示の入力から Codex CLI TUI 起動までの流れを確認したいとき
- このサブコマンドの調査境界、TUI 起動パラメータ委譲、調査結果とファイル変更の扱いを確認したいとき

## Do not read this when
- oracle file の判断基準そのものを確認したいときは oracle_and_realization.md を読む
- エディタ入力 handoff の共通仕様を確認したいときは editor_input_handoff.md を読む
- TUI 用 Codex CLI の共通起動仕様を確認したいときは tui.md を読む
- インデクシングの実行条件や処理対象を確認したいときは indexing.md を読む
- 正確な TUI prompt 文面や workload 固有の起動パラメータを確認したいときは対応する builder 実装を直接読む

## hash
- 6fe48095b50246d79a48318c59aefa145b94ecc7f9110a9e1832c97f03d6a4fd

# `realization_apply.md`

## Summary
- realization apply の fork workload における目的、追従対象差分、agent call、成果物 report、join 後 hook、終了条件を定義する仕様。realization file への oracle 変更反映処理の入口。

## Read this when
- realization apply の fork が、どの commit 範囲の oracle 変更を対象にするか確認したいとき。
- 追従 agent の呼び出し回数・cwd・変更可能な file の境界や、fork 後の検査・commit・report 保存を確認したいとき。
- apply run の join 後に比較始点 commit が更新される条件、またはエラー時の扱いを確認したいとき。

## Do not read this when
- realization apply の fork 以外の編集 run の共通 lifecycle を確認したいときは、編集 run 共通仕様を直接読むべき。
- oracle file と realization file の適合性そのものの判定基準を確認したいときは、oracle と realization の適合性を定義する仕様を直接読むべき。
- 実装上の prompt、builder 引数、起動パラメータの具体的な構築方法を確認したいときは、指定された launch_exec.py を直接読むべき。

## hash
- 7d6be11e3ab32fcad457ee0a93ece1eefcf33a7ab8688998e820ea044682366b

# `realization_refactor.md`

## Summary
- realization refactor fork の目的、refactor state 同期、current fork の unresolved target 管理、処理単位と loop、完了・中断・エラー、report 生成までの正本仕様。
- oracle file と realization file の適合性をファイル単位で調査・修正し、調査要求がなくなるまで継続する workload の入口。

## Read this when
- realization refactor fork の動作、調査対象の選択、state の保存・同期、agent call の結果判定を確認するとき。
- unresolved target を含む fork の完了理由、中断時の rollback、終了 report や終了コードの仕様を確認するとき。
- realization apply とは異なる長期的な反復調査 workload の仕様を調べるとき。

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを確認したいとき。
- fork・join・abandon に共通する編集 run の lifecycle だけを確認したいとき。
- oracle と realization の適合性判定基準そのもの、agent call の共通差分検証、または feedback との境界を直接確認したいときは、それぞれ参照先の正本仕様へ進む。

## hash
- 44a7ea834fec19ac273226484168012fb0a152c1c1c81e94480cb4498512e076

# `session_abandon.md`

## Summary
- 現在の session branch を home branch に merge せず破棄する `cmoc session abandon` の正規手順を定義する。事前条件、破棄してよい対象と保持対象、cleanup、状態遷移、失敗時の rollback、primary report の保存内容を確認できる。

## Read this when
- session を merge せず終了・破棄する操作の仕様を確認したいとき
- session branch の削除、session state の abandoned 遷移、未 join run の扱いを実装または検証するとき
- abandon 実行結果や全終了経路の primary report 要件を確認するとき

## Do not read this when
- session を home branch へ取り込む join の仕様を確認したいとき
- 未 join の編集 run 自体を破棄する操作を確認したいときは、先に run abandon の仕様を読むべきとき
- session の fork や共通 session state の一般事前条件だけを確認したいときは、対応する共通仕様を直接読むべきとき

## hash
- 6693d787af8d136f93e9fdd4e763fa320c81acbfb048c6ede2917d1d587144c2

# `session_fork.md`

## Summary
- `cmoc session fork` の引数なし実行について、実行対象ブランチの事前条件、セッションブランチの作成・checkout、初期 session 情報の保存、終了時の primary report を定める仕様。

## Read this when
- 現在のローカルブランチを起点に新しい cmoc セッションを開始する処理の条件や手順を確認するとき。
- セッションブランチの命名、初期状態の保存、または fork 実行結果・失敗時 report の内容を確認するとき。

## Do not read this when
- 任意の start point を指定する操作や、既存セッションの状態遷移そのものを確認したいとき。
- ブランチの役割・分岐関係の正本や session state の schema を直接確認する必要があるとき。

## hash
- e0cb5c94c8eda9ec1bae324fdf4074934553a4e9671a9c02fd7809d2f68e610d

# `session_join.md`

## Summary
- アクティブな session の作業ブランチを home branch に merge して session を joined にする、session 完了専用コマンドの仕様。通常の汎用 git merge 操作用途ではない。
- 実行前提、branch 切替・no-ff merge、conflict marker 解消用 agent call、state 更新、session branch cleanup、primary report 保存までの終了処理を定める。
- session join における branch model、feedback state、oracle file の扱いと、conflict や想定外の失敗時の境界を確認するための入口。

## Read this when
- session を完了して home branch に戻し、session branch を merge したいとき
- session join の事前条件、merge conflict の解消手順、または session state の joined 遷移を確認するとき
- session join 実行後の branch cleanup、primary report、warning・エラー時の次の操作を確認するとき
- conflict 解消用 agent call の仕様上の制約や oracle file の優先順位を確認するとき

## Do not read this when
- 通常の git branch 間の汎用 merge 方法を確認したいとき
- session の開始・編集 run 開始条件そのものを確認したいときは、active session context と共通事前条件の正本を直接読むとき
- branch の対応関係や default branch の扱いだけを確認したいときは branch model の正本を直接読むとき
- repository-local feedback state の所有範囲と配置だけを確認したいときは feedback state の正本を直接読むとき
- エラー分類の一般規則だけを確認したいときは error handling の正本を直接読むとき

## hash
- 6f225eec297c984fa9e2fc9389c51ddcfe2139c4143c8d279c97ce40a39ebcf4

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの責務・実行手順・共通の TUI 起動契約を確認するための正本。ユーザープロンプトの受領から起動パラメータ構築、AI Agent CLI/TUI 起動までの意味上の入口を示す。
- Codex CLI をバックエンドとして起動する際の固有条件と、関連する正本仕様への参照先を確認できる。

## Read this when
- `cmoc tui` の引数、事前条件、実行手順、プロンプト入力 lifecycle を確認したいとき
- TUI 起動時に注入される cmoc 固有契約、installed skill との優先関係、indexing preflight、feedback observation、終了通知の適用条件を確認したいとき
- Codex CLI を `codex` として起動する条件、editor input handoff、環境変数や CLI 設定上書きの扱いを確認したいとき

## Do not read this when
- プロンプトエディタ入力の詳細な正本仕様だけを確認したいときは、指定された prompt editor input の正本を直接読む
- 起動パラメータの正確な prompt part、文面、workload 固有パラメータ、選択理由を確認したいときは、`build_tui_launch_tui_parameter` の正本実装を直接読む
- oracle file と realization file の責務・適合性、indexing、feedback observation、Windows toast、editor input handoff、Codex exec rule の詳細だけを確認したいときは、それぞれ本文で参照されている正本文書を直接読む

## hash
- e65bbdac84bff56e975dc0b64353915a6c2f5b0ac1be94bd3249d6a9033c51c2
