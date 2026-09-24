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
- Workload を横断する編集 run の開始条件、同時実行制約、共通処理と終了状態を定める。
- 明示的な join・abandon と feedback の自動 join に関する差分検査、merge、復旧、cleanup、および lifecycle の report と terminal result の入口となる。

## Read this when
- 編集 run を開始する際に、共通事前条件や別の active run がある場合の扱いを確認するとき。
- run の join・abandon、自動 join 後の復旧、差分検査、merge、cleanup の共通動作を実装・確認するとき。
- lifecycle 操作の report や terminal result に必要な共通要件を確認するとき。

## Do not read this when
- branch・worktree の隔離資源や agent call の path context を確認するときは、それらを正本とする仕様から読む。
- session・run の永続 schema、field の定義、状態遷移の全体を確認するときは、その state を正本とする仕様から読む。
- 個別 workload の処理手順、編集可能な file、固有 hook や report 項目を確認するときは、その workload の仕様から読む。
- oracle edit、read-only investigation、run を作らない機械的更新、または session join の conflict 解消を扱うとき。

## hash
- 6628d03f20fa0263aac00c7fad8a0f7c4fee22daff0ac0537af0b1a2a5f9f50a

# `feedback_report.md`

## Summary
- `cmoc feedback report` の実行全体を定める。run の開始・再開、observation の intake と issue 処理、修正の検査・commit、自動 join、report の publication、割り込みや失敗からの recovery を扱う。

## Read this when
- feedback report コマンドの orchestration、wave の進行、issue remediation の受理と commit、join・publication、report・終了コードの挙動を変更または確認するとき。

## Do not read this when
- raw observation の入力形式・受付・検出規則を調べるときは、observation 収集仕様から読む。
- feedback の結果分類や自然完了条件を調べるときは、feedback 共通仕様から読む。
- repository-local state の artifact、checkpoint、high-watermark、report cut、atomic publication を調べるときは、feedback state 仕様から読む。
- remediation agent の prompt・起動設定・Structured Output schema の詳細を調べるときは、それぞれの parameter builder と schema を直接読む。
- run の一般的な join・abandon や Codex 実行の共通規則を調べるときは、対応する共通仕様から読む。

## hash
- 3f5ad345b2853ee7abf7a9368cf52acf4930ca304778e37f6e9161a5f1546401

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
- oracle file の最終状態を指示に沿って編集する `cmoc oracle edit` の仕様を定める。共通の prompt と設定で新しい Codex session を直列に 2 回呼び出す手順、編集範囲、終了条件、実行報告を確認する入口。

## Read this when
- `cmoc oracle edit` の実行順序、2 回の agent call、入力や設定の確定方法を変更・確認するとき。
- oracle edit の agent に許される編集範囲や、差分を保持する終了条件を確認するとき。
- oracle edit の事前条件、失敗時の扱い、primary report や通知の要件を調べるとき。

## Do not read this when
- oracle file の調査や質問への回答など、編集を伴わない oracle workload の責務を確認するとき。
- realization apply/refactor や feedback report の fork・join・abandon 共通 lifecycle を確認するとき。
- 共有の editor input handoff lifecycle や Codex exec 共通規則そのものを確認するとき。

## hash
- 78c1f11b1bdeec091edb32b1cc541deed2884539ea8e67ca9d03374b9dfcc485

# `oracle_investigation.md`

## Summary
- oracle file に関する調査指示を受け取り、oracle file を根拠に TUI で回答するサブコマンドの意味上の仕様を定める。
- 調査指示の入力から TUI 起動、調査結果の扱いまでを確認する入口。正確な prompt と workload 固有の起動パラメータは実装側の builder に委譲される。

## Read this when
- oracle file の調査を実行するサブコマンドの責務や処理順序を確認するとき。
- 調査結果の回答方法や、調査中の oracle file と realization file の扱いを確認するとき。

## Do not read this when
- oracle file を編集するサブコマンドの仕様を確認するときは、編集専用の仕様へ進む。
- 汎用 TUI の起動条件や共通設定を確認するときは、汎用 TUI の仕様へ進む。
- エディタ入力の共通 lifecycle や正確な prompt 構築を確認するときは、それぞれの共通仕様または実装側の builder を直接読む。

## hash
- 5d3dd339645564c99bee0caf6691554fdbcafc0838ffcc69d2d2cf41383831c7

# `realization_apply.md`

## Summary
- 直近の Git commit 群に含まれる oracle file の変更を realization file に追従させる `cmoc realization apply fork` の workload 仕様。
- 比較範囲と追従対象の決め方、agent 実行の境界、report、および join 後の比較始点更新を定義する。ファイル単位の網羅調査を行う refactor とは担当範囲が異なる。

## Read this when
- apply の比較範囲や、変更・rename を含む oracle file の追従対象を確認するとき。
- apply の agent 実行条件、成果物やエラー時の扱い、join 後に次回の比較始点がどう更新されるかを確認するとき。

## Do not read this when
- oracle file と realization file をファイル単位で網羅的に調査する workload を扱うときは、realization refactor の項目から読む。
- apply と refactor に共通する fork・join・abandon の lifecycle を調べるときは、編集 run の共通仕様から読む。
- oracle file に対する realization file の適合性の判断基準を調べるときは、その基準を定める項目を直接読む。

## hash
- a0db197eb14906040824ae799d0e65afbb3e9bf8eba59b1eb6602e42b37fa9e8

# `realization_refactor.md`

## Summary
- realization refactor fork のファイル単位調査を定義し、対象 file の調査状態、同期、選択順、および full refactor cycle の進行を扱う。
- 処理単位ごとの調査・修正結果の受理、所見の正規化、unresolved target の扱い、完了・中断・エラー時の状態と report を定める。

## Read this when
- realization refactor fork の対象集合、refactor state、調査順、または loop の動作を調べる・変更する場合。
- この fork 固有の所見処理、commit 境界、unresolved 付き完了、終了 report や終了コードを確認する場合。
- ファイル単位で全体を調査する refactor と、直近の oracle 変更を反映する apply の責務の違いを確認する場合。

## Do not read this when
- fork・join・abandon の共通 lifecycle だけを確認する場合は、編集 run の共通仕様へ進む。
- 所見調査 call の正確な prompt、prompt part、workload 固有の起動パラメータを確認する場合は、委譲先の builder へ進む。
- oracle file と realization file の分類・列挙方法や、適合性の共通判断基準だけを確認する場合は、それぞれの正本仕様へ進む。
- サブコマンド共通のユーザー中断規則だけを確認する場合は、中断の共通仕様へ進む。

## hash
- f433e3411f3b2ea38db6893c05435fc315c9e73f4eca934a107ea7739b689317

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
- 現在の session branch を session home branch に merge して session を完了する処理について、事前条件、競合解消、状態更新、branch cleanup、実行要約の記録を定める。

## Read this when
- `session join` の事前条件、merge 手順、状態遷移、branch cleanup を確認するとき。
- join 中の競合解消で両 branch の意図をどう保つか、どの条件で merge を成立させず未解消事項として報告するかを判断するとき。
- join の終了経路や実行要約に記録する内容を確認するとき。

## Do not read this when
- session の作成や分岐元の設定を扱うときは、session fork の仕様を読む。
- session branch を merge せず破棄するときは、session abandon の仕様を読む。
- session と編集 run に共通する状態 schema、事前条件、状態遷移を確認するときは、session state の仕様を読む。
- branch の役割や既定 branch の扱いを確認するときは、branch model の仕様を読む。
- 競合解消用 agent call の正確な prompt・起動パラメータや policy 文面を確認するときは、それぞれを構築する実装を読む。
- repository-local feedback state の lifecycle や、共通のエラー分類・stack trace 規則を確認するときは、それぞれの正本仕様を読む。

## hash
- 07ab427429ba278647f2fd6eeb6e68567cd026f8a3784fd3266c9e60c28e7919

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
