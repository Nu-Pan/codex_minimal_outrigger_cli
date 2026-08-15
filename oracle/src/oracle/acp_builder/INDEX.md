# `basic.py`

## Summary
- AI コーディングエージェント呼び出しに渡すパラメータの論理モデルと、モデルクラス、推論強度、ファイルアクセスモードを定義する。完全な prompt、Structured Output schema、実行 cwd、indexing preflight の扱いを含む agent call 構築の入口であり、これらの呼び出し条件を変更・確認するときに読む。バックエンド固有のモデル名解決やアクセス制限文面の具体的な構築は realization 側・別の正本仕様へ進む。

## Read this when
- cmoc の agent call パラメータ、モデル選択、reasoning effort、ファイルアクセスモード、prompt、Structured Output schema、実行 cwd、indexing preflight の仕様や型を変更・確認するとき。
- builder が呼び出し単位の設定を組み立てる責務と、論理値を定義する列挙型を確認するとき。

## Do not read this when
- バックエンドが受理可能な具体的モデル名への解決方法を調べるとき。
- ファイルアクセスモードごとの Codex CLI sandbox 制限文面や実装責務を調べるときは、指定された正本仕様または realization 側を直接読む。
- agent call パラメータを扱わず、個別のモデル実装・CLI 実行・Structured Output schema の内容だけを確認するとき。

## hash
- 0cadb3701b12e2d826b22976ee92f31098e71a4315020984e0fabb3bb40930a7

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
- `cmoc oracle` 系コマンドの agent call 起動パラメータ構築を扱う領域です。oracle 編集・調査・レビューについて、完全 prompt、読み書き範囲、作業ディレクトリ、モデル・推論設定、Structured Output、起動前処理を確認する入口になります。編集、調査、レビューの具体的な定義は各下位領域へ分かれています。

## Read this when
- `cmoc oracle edit`、`cmoc oracle investigation`、または `cmoc oracle review` の agent call 起動条件や prompt 構築を調査・変更するとき
- oracle 向け agent call の読み書きモード、作業ディレクトリ、モデル設定、推論設定、索引付け前処理、Structured Output の適用範囲を確認するとき
- 各 oracle サブコマンドの起動定義を横断して比較するとき

## Do not read this when
- oracle file 自体の編集規則、調査規範、レビュー規範を確認する場合
- 共通の agent call 型、パス解決、完全 prompt 構築の実装だけを確認する場合
- 特定の oracle サブコマンドの詳細だけを確認すれば足りる場合は、対応する下位領域へ直接進むとき

## hash
- 8d85f3aa4f02e6232c186d90b77db3727084dbf32a321e504bc7d03521b401f0

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
- `cmoc tui` の実行パラメータ解決と、後続の AI Agent CLI/TUI に渡す完全プロンプトの構築を担う。オリジナルプロンプトを埋め込んだ指示を生成し、標準設定の選択や実行場所・アクセス権限を含む起動条件を定義するため、TUI 実行フローの入口となる。

## Read this when
- `cmoc tui` が後続の AI Agent CLI/TUI に渡すプロンプト、標準設定の適用、または実行パラメータの解決を変更・確認するとき。
- TUI 実行時の作業ディレクトリ、ファイルアクセスモード、モデル・推論設定、構造化出力スキーマの指定を変更・確認するとき。

## Do not read this when
- TUI 以外のサブコマンドの実行パラメータを扱うとき。
- 共通の完全プロンプト生成処理や共通データ型の仕様だけを確認するときは、それらの共通実装を直接読む。

## hash
- 88b94f36c12a2f397da25059f98103c7825a0c66aa1031e00cda2f933ff06215
