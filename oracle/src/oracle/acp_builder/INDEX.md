# `basic.py`

## Summary
- AI コーディングエージェント呼び出しに必要な論理モデルクラス、推論強度、ファイルアクセスモード、および呼び出し設定を定義する基礎データモデル。バックエンド固有のモデル解決やアクセス規則の具体化ではなく、呼び出しパラメータの共通契約を確認するための入口。

## Read this when
- Agent call のパラメータ構造、モデル選択区分、推論強度、ファイルアクセスモード、または indexing preflight の既定値を確認・変更するとき

## Do not read this when
- バックエンドが受理可能なモデル名への解決やファイルアクセス規則の具体的な文面を確認するとき
- Agent call の生成処理や個別 builder の挙動だけを調べるとき

## hash
- fea717dae8c45705bc5fb1af10be854cbfdbb80b1b58c8d24eb2713a1998da67

# `feedback`

## Summary
- feedback issue の同一性判定と report cut 時点の検証に使う Structured Output schema と agent call 定義を収録する。
- 同一性判定では observation と絞り込み済み候補を比較し、既存 issue への対応付けまたは新規 issue の判定を扱う。
- 検証では固定済みの report cut reference だけを根拠に、issue の状態と人間対応の要否を判定する。配下の normalize_issue 系・verify_issue 系ファイルが、それぞれの出力契約と起動パラメータを確認する入口になる。

## Read this when
- feedback issue の同一性を判定する処理の出力契約、入力候補との照合境界、または読み取り専用の agent call 設定を確認するとき
- issue candidate を report cut 時点の固定参照から検証し、未解決・解決済み・報告対象外・判定不能の扱いを確認するとき
- feedback issue の判定用 schema と、それを使用する prompt・agent call parameter の対応を調べるとき

## Do not read this when
- feedback issue の報告、保存、候補の絞り込み、または feedback state の更新処理を調べるとき
- issue の具体的な内容や現在の repository 状態を確認したいとき
- 一般的な JSON Schema の仕様や、個別の issue の原因・重要度・関係を調べるとき

## hash
- 8abb284879cab91ac4cba3a7527753d92cb311416e6f96b4afe079187bd2c16e

# `indexing`

## Summary
- `cmoc indexing` が INDEX.md エントリー生成用 agent call を起動するための定義を集約する。Structured Output schema と、対象本文を埋め込んだ prompt・起動パラメータの構築実装を扱う。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成について、出力契約と agent call の prompt、モデル、推論設定、読み取り権限、cwd、preflight 設定を確認・変更するとき。
- エントリー生成の下位ファイルへ進む前に、schema とパラメータ構築実装の責務を把握するとき。

## Do not read this when
- INDEX.md エントリーのルーティング内容や対象ファイル・ディレクトリの実際の責務を判断するときは、生成対象の本文を直接読む。
- Structured Output schema の制約だけを確認するときは、schema 定義を直接読む。
- `cmoc indexing` 以外の agent call パラメータや共通 prompt 生成規則を確認するときは、それぞれの担当実装や共通 prompt builder を直接読む。

## hash
- 59b72c73168652c15f8779d97428d9ab0a2f6c649e1ca87a27c0ea19bdab197d

# `oracle`

## Summary
- oracle の各処理領域における起動設定、プロンプト構築、Structured Output 契約の確認先を提供するディレクトリ。編集・調査・レビューの具体的な実装や設定へ進むための入口。

## Read this when
- oracle 編集処理の TUI 起動条件、編集担当 agent call のプロンプト、モデル・権限・作業ディレクトリなどの実行条件を確認するとき。
- oracle investigation 用 TUI の起動条件、完全プロンプトの構成・保存、および調査用 agent call の設定を確認するとき。
- oracle review の所見列挙、妥当性検証、採否判定、重複・矛盾の統合に関する入出力契約や agent call 設定を確認するとき。

## Do not read this when
- 具体的な oracle file の編集内容、調査対象、レビュー対象の仕様や実装を確認するとき。
- oracle の各処理に共通する prompt 構築規則、agent call 基盤、TUI 一般実装だけを確認するとき。
- 対象となる下位ファイルを直接特定でき、親ディレクトリの処理領域一覧を確認する必要がないとき。

## hash
- a67775393bbe8072d6c3a179057ab51f0d7b1b0fd032fda1ed5907f677d42e8a

# `quota_probe.py`

## Summary
- Codex CLI の quota 回復確認用 agent call を構築する定義。probe 専用の短い prompt と、読み取り専用・最小モデル・低推論強度などの起動パラメータを組み立てる。quota availability probe の呼び出し条件や設定を確認するときの入口となる。

## Read this when
- Codex CLI の利用可能性確認用 agent call の prompt または起動パラメータを変更・確認するとき。
- quota probe の cwd、アクセスモード、モデル設定、終了判定に関する定義を調べるとき。

## Do not read this when
- quota probe 以外の agent call 構築定義を調べるとき。
- quota availability の判定結果や呼び出し実行処理そのものを確認するときは、実行側の対象を直接読む。

## hash
- 6672e90eae1840a676b53dd2b4435362b16946cd9045feb31bfcffae81ebfe4a

# `realization`

## Summary
- realization apply fork で oracle file の差分を realization file へ追従させるための AgentCallParameter 構築を担う領域。commit 範囲と raw git diff の prompt 組み込み、および差分追従 agent call の実行設定を確認・変更する入口。
- refactor fork で変更差分の要約とファイル単位のレビュー・修正を行う agent call の定義および Structured Output スキーマを扱う領域。変更要約、oracle・realization の調査、修正、検証の流れを確認する入口。

## Read this when
- cmoc realization apply fork の oracle file 差分追従処理、commit 範囲や oracle diff の prompt 組み込みを確認・変更するとき
- 差分追従 agent call のモデル、推論強度、ファイルアクセス、linked worktree、実行前 indexing などの設定を確認・変更するとき
- refactor fork の変更差分を構造化して要約するとき
- ファイル単位のレビュー・修正 agent の呼び出し条件、調査範囲、修正権限、検証規則を確認・変更するとき

## Do not read this when
- 通常の realization 実装やテストの挙動を確認するとき
- 一般的な prompt 生成や共通の AgentCallParameter 構築規則を確認するとき
- cmoc realization apply fork 以外の起動経路を調査するとき
- 個別のレビュー対象ファイルの実装内容や具体的なレビュー所見を調査するとき
- 変更要約またはレビュー結果の項目・型・形式だけを確認するときは、対応する JSON スキーマへ直接進む
- 共通の prompt 構築処理や path 解決処理だけを確認するときは、共通実装へ直接進む

## hash
- 98783ed60e9af1a84d178cd245aab3c250d1e64c2ca956244f5f8d44bcec4b9e

# `session`

## Summary
- `cmoc session join` で merge conflict marker を解消するための AI エージェント呼び出しパラメータを定義する入口。conflict 対象、専用 prompt、モデル・推論設定、リポジトリ書き込み権限、作業ディレクトリ、事前 indexing の扱いを確認する。

## Read this when
- `cmoc session join` の conflict marker 解消処理に使う prompt、モデル、権限、パス、実行設定を確認または変更するとき。

## Do not read this when
- 通常の session join 処理だけを確認するとき。
- conflict 解消以外の一般的な prompt 構築や agent call parameter を確認するとき。

## hash
- 7f2353693d7930ad2c85442d36020c96e7d3a8bd7c3d0cc575e3f4bba6ce2e7d

# `tui`

## Summary
- `cmoc tui` の起動パラメータを構築し、ユーザー入力を埋め込んだ完全プロンプトをログへ保存する。リポジトリを作業ディレクトリとし、TUI 用のモデル、推論強度、書き込み権限、インデックス事前処理などの固定設定を定義する。

## Read this when
- `cmoc tui` の起動条件や `AgentCallParameter` の設定を確認・変更するとき。
- ユーザーのオリジナルプロンプトから完全プロンプトを生成し、TUI 起動へ渡す処理を追うとき。
- TUI 起動時の作業ディレクトリ、ファイルアクセスモード、モデル、推論強度、インデックス事前処理を確認するとき。

## Do not read this when
- TUI 以外のサブコマンドの起動パラメータを確認するとき。
- 完全プロンプトの共通生成規則を確認するときは、共通の prompt builder 定義へ直接進む。
- パス解決や構造化文書の共通仕様だけを確認するときは、それぞれの共通定義へ直接進む。

## hash
- 2b5867bd3514e27cc77d20353576225d43b67fab175fa5c0583be14f8644756c
