# `basic.py`

## Summary
- 論理的なファイルアクセスモードと、agent 呼び出しで共有する設定型を定義し、個別の呼び出し builder と共通実行経路をつなぐデータ定義です。
- アクセス制限の文面や完全 prompt の組み立てではなく、それらに渡される共通パラメーターの契約を確認する入口です。

## Read this when
- 共有の agent 呼び出しパラメーターを変更するときや、共通実行経路が受け取る設定を追うとき。
- 論理的なファイルアクセスモードを追加・変更し、その識別子を使う呼び出しとの整合を確認するとき。

## Do not read this when
- アクセスモードごとの制限文面だけを調べるときは、その文面を組み立てる policy builder を直接読む。
- 完全 prompt の構成や policy の注入条件だけを調べるときは、prompt 組み立て側を直接読む。
- 特定の agent 呼び出しの処理や設定だけを変更するときは、その呼び出し専用の builder を直接読む。

## hash
- 543b7fb62130cc282e6ae2c0cb1534f9fa2f7f24016c73d5013bc00d99a04aaa

# `feedback`

## Summary
- feedback issue の同一性判定と remediation に使う agent call 固有の prompt、起動条件、出力 schema を定義する。feedback の issue 処理に関する call の挙動を調べる入口。
- 共通の agent call 基盤や feedback report 全体の実行制御ではなく、正規化と remediation の call 固有の判断・制約を確認するときに対象となる。

## Read this when
- agent observation を既存 issue candidate と照合する判断や、その call が参照できる情報の境界を確認・変更するとき。
- feedback issue の現在状態確認、realization file の修正・検証、または remediation call 固有の起動条件を確認・変更するとき。

## Do not read this when
- feedback report 全体の intake、wave、checkpoint、publication、recovery の流れを調べるときは、feedback report の正本仕様から読む。
- 共通の agent call parameter、prompt 構築、file access policy、provider 設定を調べるときは、それぞれの共通定義から読む。

## hash
- 4233d6d48e0e4c6bc63d9fdfbba2e91b914293377ca8a3d4812ec56c032d7723

# `indexing`

## Summary
- `cmoc indexing` の INDEX.md エントリー生成 agent call に渡す指示文、起動設定、出力制約を組み立てる。

## Read this when
- INDEX.md エントリー生成の呼び出し設定や、対象パスの解決方法を追跡・変更するとき。
- この呼び出しに適用される生成結果の制約を確認するとき。

## Do not read this when
- INDEX.md の生成手順や routing 規則そのものを調べるときは、agent call の実装定義ではなく indexing の正本仕様から確認する。
- 共通の agent call パラメータや prompt 構築の動作を調べるときは、共通定義を読む。別の処理向けの呼び出しを調べるときは、その処理の構築定義へ進む。

## hash
- 4d4c2433d75dca8bbb16c25f34731f6b7bd567719a957176b6c409d81f98ffc8

# `oracle`

## Summary
- `cmoc oracle investigation` と `cmoc oracle edit` の agent call 用 prompt と起動パラメータを組み立てる領域です。調査用の読み取り TUI 呼び出しと、編集用の書き込み `codex exec` 呼び出しの設定を見比べる入口になります。
- 調査用呼び出しは oracle file の読み取り、editor input handoff、indexing preflight を設定し、編集用呼び出しは目標状態と未コミット差分を判断材料にする共通設定を構築します。

## Read this when
- oracle investigation の読み取り境界、TUI 起動、prompt、handoff、または indexing preflight を変更・確認するとき。
- oracle edit の agent call に渡す共通 prompt、oracle file の編集境界、未コミット差分の参照、または indexing の担当箇所を変更・確認するとき。

## Do not read this when
- oracle edit 全体の実行順序や二回実行など、サブコマンドの正本仕様を確認するときは、その仕様を直接参照してください。この領域は共通 agent call の設定を定義します。
- 調査用呼び出しだけ、または編集用呼び出しだけの詳細を確認するときは、該当する個別フローの項目から読み始めてください。

## hash
- 531c5b4f16cd0fe40e11d6852435580547172f4b86d0c93bbfdb9968e61c01e8

# `quota_probe.py`

## Summary
- quota などの可用性回復 probe 用に、短い応答を一度だけ求める読み取り専用 agent call の prompt と固有の起動設定を組み立てる。
- 回復確認の目的や成否判定、待機・再開の制御ではなく、probe が受け取る指示と builder 固有設定を調べる入口。

## Read this when
- quota または一時障害の回復 probe が依頼する内容や、読み取り専用設定・preflight の再帰防止などの起動条件を確認・変更するとき。
- 共通の agent call parameter 定義や他のワークフロー用 builder ではなく、可用性確認 probe 専用の構築箇所を探すとき。

## Do not read this when
- 回復確認を始める条件、probe の成功判定、待機間隔、再開や結果共有の仕様を調べるとき。
- 共通の agent call parameter や完全 prompt の生成規則を変更するときは、それぞれの共通定義を参照し、別ワークフローの呼び出しを変更するときは対応する builder を参照する。

## hash
- 1ac746647bce56257d4ec7e41e2b7113802e8e2926f32e10699b404067da3ad6

# `realization`

## Summary
- fork型の realization apply と refactor 向け agent-call の prompt と起動 parameter を組み立てる定義を束ねる。commit 範囲の oracle 変更を realization に反映する処理と、refactor における差分要約およびファイル単位のレビュー・修正を扱う。

## Read this when
- 複数の fork 処理の分担を見直し、commit 範囲の変更追従と refactor 作業のどちらに agent-call を振り分けるか確認するとき。
- apply と refactor をまたいで fork agent-call の prompt 構成や起動条件を変更するとき。

## Do not read this when
- commit 範囲の oracle 変更を realization に反映する処理だけを修正する場合は、その処理の定義へ直接進む。
- refactor の差分要約またはファイル単位のレビュー・修正の片方だけに関する作業なら、該当する定義へ直接進む。
- fork 以外の realization agent-call や共通 prompt 構築が対象なら、このまとまりから調査を始める必要はない。

## hash
- 31b82bb17ffbff96848c92cef4fdbb63127a7fd62e30023fe68f1a68d6bd01ad

# `run`

## Summary
- run branch を session branch に統合するときの競合解消用 agent call を構築する。
- feedback の自動 join では、封印済み report cut の結果を維持するための指示も組み込む。

## Read this when
- run join の競合解消 call に渡す入力や実行条件を確認・変更するとき。
- feedback 自動 join で封印済み結果を参照し、統合後の維持と検証を求める処理を確認するとき。

## Do not read this when
- session branch を home branch に統合する競合解消を扱うときは、session join 用の builder を読む。
- 共通の競合解消 prompt の内容を確認するときは、その prompt builder を直接読む。
- run join や feedback 自動 join の意味仕様だけを確認するときは、該当する oracle doc を直接読む。

## hash
- b3b8b7437ad2e699724c477d3f9987a835573fe44d120f2f5518ab3c444f88a0

# `session`

## Summary
- session join の merge 競合解消で使う agent call の個別設定を構築し、共通の競合解消 prompt に接続する。

## Read this when
- session join 用 call の起動設定を確認・変更するとき。共通 prompt の定義ではなく session 固有の起動設定を調べる入口。

## Do not read this when
- 共通の競合解消 prompt や policy を変更するときは、共通 prompt 構築の定義へ進む。
- session join の実行手順、競合解消の判断基準、受理・報告・停止条件を確認するときは、対応する仕様を直接読む。

## hash
- cfac7ceaa0be71f7986284b1deb359de21dd7764c8f88997f891d31abfcdb5ee

# `tui`

## Summary
- 一般の `cmoc tui` 向けに、ユーザーの指示へ適用する cmoc の基本規定を含む prompt と、Codex CLI TUI の起動パラメータを組み立てる。サブコマンド固有の構築内容を調べる入口であり、共通の呼び出し型定義や oracle 調査専用の TUI 構築とは責務が異なる。

## Read this when
- `cmoc tui` が送る prompt の構成や、ユーザー指示の受け渡しを追う・変更するとき。
- 一般の `cmoc tui` におけるファイルアクセス方針、indexing preflight、editor input handoff の起動設定を確認するとき。

## Do not read this when
- `cmoc oracle investigation` の oracle file 限定調査向け TUI の prompt や起動設定を調べる場合は、その専用 builder へ進む。
- 共有される呼び出しパラメータ型の項目だけを確認する場合は、共通の型定義へ進む。

## hash
- f28546aef0423a86dd61a08732f512eec7b68a81bb94a95ff72b3c793e49b0b7
