# `doctor.md`

## Summary
- `cmoc doctor` による doctor preprocess の明示実行と、実行結果を要約する primary report の保存要件を定める。
- 共通の検査・修復の内容は Doctor Preprocess の仕様が担い、この項目はコマンドの呼び出しと報告の入口となる。

## Read this when
- `cmoc doctor` の実行手順や、正常完了・エラー終了時の primary report の要件を確認するとき。

## Do not read this when
- doctor preprocess が行う検査・修復、その順序、reporter の事前検証や commit の条件を調べるときは、Doctor Preprocess の仕様を読む。
- doctor preprocess 後に検証される別サブコマンド固有の事前条件や処理手順を調べるときは、そのサブコマンドの仕様を読む。

## hash
- e004c75b5a42802cdae0ddd2d023d7ccf4b5fcc7f7065f6ee33a285dd6ad1330

# `editing_run.md`

## Summary
- realization apply、realization refactor、feedback report の編集 run に共通する開始条件、状態遷移、同時実行制約、差分確定、join・abandon の lifecycle を扱う。
- 共通の join 検査、merge と競合解消、後処理、cleanup、report の入口となる。workload 固有の処理や隔離資源・session state の正本定義は、それぞれの仕様に委ねる。

## Read this when
- 編集 run を開始できる条件や、active run の状態によって許される操作を確認するとき。
- join・abandon の共通事前条件、差分検査、merge、競合解消、失敗時の復旧、cleanup、report の扱いを確認するとき。
- realization apply・refactor の明示的 join と feedback report の自動 join に共通する lifecycle の範囲を確認するとき。

## Do not read this when
- realization apply の比較範囲、本命 call、fork report、join 後 hook の詳細を確認するときは、その workload 固有仕様を読む。
- realization refactor の state、調査 loop、処理単位、完了条件を確認するときは、その workload 固有仕様を読む。
- feedback report の intake、issue remediation、publication、固有 recovery を確認するときは、その workload 固有仕様を読む。
- run の隔離資源や session state の正本定義を確認するときは、各共通定義を直接読む。session fork・join・abandon、oracle edit・investigation、run を作らない更新、session join の競合解消も、それぞれの専用仕様を読む。
- workload または競合解消 call の正確な prompt、引数、起動パラメータを確認するときは、該当する builder 実装を読む。

## hash
- 0d7455112605d5b68550bed8daface9bacf931f6288aaee020e7a9cc4ce43570

# `feedback_report.md`

## Summary
- `cmoc feedback report` の実行を定め、observation の取り込みから issue の処理、intake wave、自動 join、publication と recovery までの流れを扱う。
- 安全な修正の issue 単位の確定と、人間の対応が必要な issue の報告がどう連携するかを確認する入口。

## Read this when
- `cmoc feedback report` の開始・再開条件、observation の検証や正規化、issue の処理・再確認、wave の完了条件を確認または変更するとき。
- 自動 join 後の検証、report の公開、中断や失敗からの recovery の動作を確認するとき。

## Do not read this when
- observation の収集基準や reporter の入力契約を確認するときは、feedback observation の仕様を直接読む。
- feedback の用語・結果分類・処理モデルを確認するときは、その定義を扱う仕様を読む。
- feedback の永続 state や checkpoint の契約、編集 run に共通する join・abandon の lifecycle を確認するときは、それぞれの共通仕様を直接読む。

## hash
- 311bf1eeee02e6cf556a695445c41a5c876567d297483dd3dcb7eca60649aea1

# `indexing.md`

## Summary
- `cmoc indexing` の引数、未コミット差分がないことを求める事前条件、doctor preprocess からインデクシングを実行する順序を定める。
- 正常終了とエラー終了の両方で保存する実行要約レポートの扱いを定める。

## Read this when
- `cmoc indexing` の実行条件、手順、エラー時の挙動を調べる・変更する場合。
- 実行要約レポートがいつ保存され、何を記録するか確認する場合。

## Do not read this when
- インデクシング自体の規則や `INDEX.md` エントリーの内容を調べる場合は、一般のインデクシング仕様を直接読む。
- doctor preprocess の責務や動作を調べる場合は、そのサブコマンドの仕様を直接読む。

## hash
- 8a2acc19195064829931578f12875ea420efb5ab64e1889c6c68e9ebfbad5381

# `oracle_edit.md`

## Summary
- `cmoc oracle edit` の仕様として、入力指示から oracle file の目標状態を整えるための実行順序、事前条件、編集境界を定める。
- 同じ prompt と設定を使う独立した編集 agent call を 2 回直列に実行し、差分を保持して人間が最終確認する運用を定める。
- 実行要約の保存と、console・ログ・Windows toast の共通仕様との境界を示す。

## Read this when
- `cmoc oracle edit` の実行条件、2 回の agent call、oracle file の編集権限、差分の扱いを変更または調査するとき。
- oracle edit 固有の report や、実行状況の console・ログ・toast 通知を確認するとき。

## Do not read this when
- oracle file の調査と回答だけが目的で、編集を伴わないときは `oracle_investigation.md` を読む。
- エディタ入力や handoff の共通 lifecycle、Codex CLI 呼び出し、indexing、doctor preprocess、共通通知の規則だけを確認するときは、それぞれの共通仕様を直接読む。

## hash
- 13e191ee31907d371d5d46e93487996c75c9297fab63c0e0f5bf2c78958b5305

# `oracle_investigation.md`

## Summary
- `cmoc oracle investigation` の責務と実行の流れを定める。oracle file に関する依頼を受けて Codex TUI で調査し、根拠を示して回答する。
- 調査中の oracle file の扱いと、このサブコマンド固有の境界を定める。エディタ入力、handoff、共通の起動設定や通知、indexing、正確な prompt 構築は各共通仕様や builder に委ねる。

## Read this when
- `cmoc oracle investigation` の調査範囲、TUI 起動、回答時の根拠提示や agent の権限を確認・変更するとき。
- oracle 調査の入力から回答までの流れを確認し、oracle 編集や汎用 TUI の仕様と区別するとき。

## Do not read this when
- oracle file と realization file の共通の分類・判断基準だけを確認するときは、その共通仕様を読む。
- 共通の editor input lifecycle や handoff、Codex TUI の起動設定・通知、indexing の動作だけを確認するときは、それぞれの共通仕様を読む。
- 正確な prompt 文面や workload 固有の起動パラメータを確認するときは、その構築を担う builder を読む。
- oracle file の編集を行う場合や、汎用の `cmoc tui` の挙動を確認する場合は、それぞれのサブコマンド仕様を読む。

## hash
- d5295b18621f394969c8c60274d0383e734ae5a34427a4e0d7d487fc2863a920

# `realization_apply.md`

## Summary
- 直近の oracle file 変更を commit 範囲から特定し、realization file に反映する短周期 workload の適用範囲と完了条件を定める。
- apply 固有の agent call 制約、変更許可、report、join 後の比較始点更新を確認する入口となる。

## Read this when
- realization apply fork がどの commit 範囲の oracle 変更を追従させるかを確認・変更するとき。
- apply 固有の agent call、変更可能な成果物、エラーや report の扱い、次回の比較始点を更新する条件を確認するとき。
- apply と、oracle file と realization file をファイル単位で繰り返し調査する workload との責務境界を確認するとき。

## Do not read this when
- oracle file と realization file の全体をファイル単位で調査し、未解決項目を追跡する作業では、realization refactor の仕様から読む。
- fork、join、abandon の共通 lifecycle だけを確認する場合は、編集 run の共通仕様から読む。
- 適合性の一般的な判断基準だけが必要なら、その判断基準の正本を読む。prompt の正確な文面や builder の選択・引数を確認する場合は、委譲先を直接読む。

## hash
- b3d6e03203a8dfe1e0af1c0ad00e30f655d71c87c2abcc10f24606eb2e3d567b

# `realization_refactor.md`

## Summary
- oracle file と realization file を起点にファイル単位の調査を繰り返し、所見に応じて realization file を修正する refactor workload の仕様。
- 調査要求の同期、対象選択、処理単位の確定、unresolved を残した完了、中断・エラー時の扱いと報告を定める。

## Read this when
- oracle と realization 全体を対象とするファイル単位の追従調査や修正、および調査要求 state の同期・選択・更新を実装または変更するとき。
- refactor workload 固有の完了条件、unresolved の扱い、中断・エラー経路、report 内容を確認するとき。

## Do not read this when
- 直近の oracle 差分を短い変更ループで realization に反映する作業では、その apply workload の仕様を読む。
- 共通の fork・join・abandon lifecycle だけを確認する場合は、編集 run の共通仕様を読む。
- 適合性の判断基準だけを確認する場合は oracle と realization の責務を定める仕様へ、prompt と起動パラメータの構築を確認する場合は refactor 用 builder の実装へ進む。

## hash
- 338fd72c0049371a7dba1589e72a39ee54897621e2b6da8ae0e0d93a8b26ff92

# `session_abandon.md`

## Summary
- `cmoc session abandon` が、session branch を home branch に merge せず終了する際の条件と手順、破棄・保持する資源、失敗時の扱いを定める。session join 後の変更を取り消す用途には使えない。
- session の状態遷移、branch cleanup、terminal result と primary report の要件を確認する入口。

## Read this when
- active session 全体を home branch に取り込まず破棄する正規の手順や、実行前提・保持すべき資源を確認するとき。
- abandon の途中で失敗した場合の rollback と再実行、および各終了経路での report 要件を確認するとき。

## Do not read this when
- session branch を home branch に merge して完了する手順や conflict の扱いを確認するときは、`cmoc session join` の仕様へ進む。
- 未 join の編集 run だけを破棄し、session を保持する手順を確認するときは、編集 run の共通仕様へ進む。
- session と編集 run の共通 state schema や事前条件を確認するときは、共通 lifecycle の仕様へ進む。

## hash
- ffd3b1f597884c62786ac8e70163fb71116742e2d3a73500231b187d2e2b9f36

# `session_fork.md`

## Summary
- `cmoc session fork` の事前条件、local branch からの session branch 作成、初期状態の保存、および実行要約の扱いを定める。

## Read this when
- 新しい session の分岐元や fork の実行条件、branch 作成・初期化、失敗時を含む実行要約の仕様を確認または変更するとき。

## Do not read this when
- session の取り込みや破棄を扱うときは、それぞれの join または abandon の仕様へ進む。
- branch の共通命名・役割や session state の共通スキーマ・遷移だけを調べるときは、それぞれの正本へ進む。

## hash
- ecba04632a0bb7a01b4f1564c7c549999206201fe1c990f8297f3d9ed56e3267

# `session_join.md`

## Summary
- `cmoc session join` が現在の session branch を session の home branch に merge して session を完了する際の、コマンド固有の実行と後処理を定める。
- home branch の進行、競合解消の呼び出しと失敗時の扱い、安全な branch cleanup、実行要約の保存を確認する入口。

## Read this when
- `cmoc session join` の実行順序、session state の遷移、merge 後の cleanup や実行要約を変更・調査するとき。
- session join が home branch への merge をどう進め、競合解消や失敗をどう扱うか確認するとき。

## Do not read this when
- session の作成や、merge せずに破棄する手順を確認するときは、それぞれの session fork / abandon の仕様を読む。
- branch と commit の共通定義、session の共通事前条件・state schema、共通の競合解消判断やエラー分類が必要なときは、それらを定める仕様を直接読む。この文書は session join 固有の利用方法を定める。
- `cmoc run join` や feedback report による自動 join の実行手順を確認するとき。これらは別のコマンド仕様で扱う。

## hash
- ec27889b327dd0f6adbc0741aa24d24339f24cb60e6a69a06a3f955f01b9e926

# `tui.md`

## Summary
- `cmoc tui` の実行順序、未コミット差分がある場合の扱い、AI Agent CLI/TUI 起動に共通する契約と Codex CLI 固有の契約を定める。
- 起動パラメータの詳細や関連する各 lifecycle の意味仕様への委譲先を示し、TUI 起動全体の責務分担を確認する入口となる。

## Read this when
- `cmoc tui` の前処理からプロンプト受領、起動パラメータ構築、TUI 起動までの流れや実行条件を確認するとき。
- TUI に注入する cmoc 基本規定の適用境界、または Codex CLI 起動時の契約を確認するとき。

## Do not read this when
- エディタ入力の確定手順や editor input handoff の詳細を確認するときは、それぞれの共通仕様を直接読む。
- TUI の正確な prompt part、文面、workload 固有パラメータ、またはその選択理由を確認するときは、委譲先の builder 定義を読む。
- 注入される oracle・realization 規定の意味、indexing、feedback observation、Windows toast の詳細を確認するときは、それぞれの正本仕様を直接読む。
- Codex CLI の環境変数、preflight validation、設定上書き、editor input handoff MCP の詳細を確認するときは、Codex CLI 共通規則を直接読む。

## hash
- bf2c7386391bfad7fdb2fbd081d3d5fda57bf91649fb4f3d12c2862e79fce97c
