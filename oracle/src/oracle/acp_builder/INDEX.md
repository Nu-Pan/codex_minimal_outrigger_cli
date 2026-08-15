# `basic.py`

## Summary
- AI コーディングエージェント呼び出し用の論理パラメータを定義するデータモデルと、モデル種別・推論強度・ファイルアクセスモードの列挙を扱う。ACP の呼び出し条件や prompt、Structured Output、作業ディレクトリ、indexing preflight の設定を確認・変更するときの入口となる。

## Read this when
- Agent Call Parameter の構造や既定値を確認するとき
- ModelClass、ReasoningEffort、FileAccessMode の論理的な選択肢や意味を変更するとき
- AI エージェント呼び出しに渡す prompt、schema path、cwd、indexing preflight の保持方法を確認するとき

## Do not read this when
- バックエンド固有のモデル名への解決や実際の呼び出し処理を確認・変更するとき
- ファイルアクセス制限の正本仕様や Codex CLI sandbox への対応を確認するとき
- builder 関数による具体的な prompt 構築ロジックだけを確認するとき

## hash
- 03efbc4692262e7011a5ec10a73003a8097cfbadc32c2ec64668fd558d34460c

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
- `cmoc oracle` 系サブコマンドの agent call 構築実装を扱うディレクトリです。編集、調査、レビューそれぞれの起動条件・prompt・Structured Output・実行範囲を確認する入口になります。

## Read this when
- `cmoc oracle edit`、`investigation`、`review` の agent call 起動設定や prompt 構築を変更・確認するとき
- oracle 操作用 agent call の作業範囲、モデル設定、構造化出力、索引付け前処理をサブコマンド別に調査するとき
- レビュー所見の生成・検証・統合に関する agent call 契約を確認するとき

## Do not read this when
- oracle file の正本仕様や編集ルールそのものを確認するとき
- agent call の共通 prompt 構造・共通起動処理だけを確認するとき
- oracle 以外のサブコマンドや、個別の prompt builder・Structured Output 定義だけを確認すれば足りるとき

## hash
- 66564315e2f9d46e72c663fa1758416b36a3e8bc34437c2ffb5dabcba287239c

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
- realization の agent call 構築定義を扱う領域。apply による変更適用と refactor による変更レビュー・修正の各 fork へ進むための入口で、変更情報、prompt、実行条件、参照規則、検証・結果報告の契約を確認する。

## Read this when
- realization apply fork の起動 prompt、AgentCallParameter、変更情報、実行権限、worktree、モデル設定、実行前 indexing を確認・変更するとき
- realization refactor fork の変更要約、ファイル単位レビュー・修正、参照規則、検証条件、結果報告の契約を確認・変更するとき
- apply または refactor の agent call 構築規則を調査するとき

## Do not read this when
- apply または refactor の Structured Output schema の項目・形式だけを確認するとき
- レビュー対象の oracle file、realization implementation、realization test の具体的内容を調査するとき
- refactor fork 以外の実行系や一般的な prompt 構築規則を調査するとき

## hash
- 6c6a8d1375d98bbd604e57b14e54e6f980a22dbf1b0e80f9baecb0821fa59e2a

# `session`

## Summary
- `cmoc session join` の merge conflict 解消用エージェント呼び出し定義を収めるディレクトリ。conflict 対象パスの解決、解消用 prompt、リポジトリ書き込み権限、作業ディレクトリ、モデル・推論設定を扱い、conflict 解消呼び出しの実装確認・変更時の入口となる。

## Read this when
- `cmoc session join` の merge conflict marker 解消処理を変更するとき
- conflict 対象ファイルの扱い、解消用 prompt、エージェントの起動権限・作業ディレクトリ・モデル設定を確認するとき
- このディレクトリ内の conflict 解消用呼び出し定義へ進む必要があるとき

## Do not read this when
- 通常の session join のマージ処理や conflict 検出ロジックを確認するとき
- 一般的なエージェント呼び出しパラメータや共通 prompt 構築を確認するとき
- conflict 解消対象ファイルの内容や仕様を確認するとき

## hash
- 89258cb41851f41f7f4708488f1197c7d33f7e2db9ffab689f729ff8938b276e

# `tui`

## Summary
- `cmoc tui` 起動時に渡す完全プロンプトと固定の AgentCallParameter を構築する定義を扱う。TUI の起動設定を確認・変更する際の入口となる。

## Read this when
- `cmoc tui` の起動 prompt、オリジナルプロンプトの埋め込み、モデルや推論強度、ファイルアクセス、作業ディレクトリ、インデックス事前実行の設定を確認・変更するとき。

## Do not read this when
- TUI 以外のサブコマンドの起動パラメータや共通プロンプト生成処理を確認・変更するとき。
- AgentCallParameter、パス解決、構造化文書レンダリングの共通仕様だけを確認するとき。

## hash
- bebb717d8f30148f5c7a250a0aeedec99b972d7ee51b8d90bbef8408c1b0e016
