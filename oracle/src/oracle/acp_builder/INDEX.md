# `basic.py`

## Summary
- cmoc の論理エージェント呼び出しパラメータを定義するデータモデルと、モデル種別・推論強度・ファイルアクセスモードの列挙型を提供する。エージェント呼び出し構築処理で、呼び出し種別、モデル選択、アクセス制約、プロンプト、Structured Output schema、実行ディレクトリなどの設定をまとめて扱う入口。

## Read this when
- エージェント呼び出しのパラメータ構造、論理モデルクラス、推論強度、ファイルアクセスモードを確認・変更するとき。
- エージェント呼び出しに渡すプロンプトや schema パス、cwd、indexing preflight の既定値の契約を確認するとき。

## Do not read this when
- 実際のバックエンドモデル名や推論強度への変換規則を確認したいとき。
- Codex CLI の具体的なファイルアクセス制約の正本や、realization 側のエージェント実装を確認・変更するとき。

## hash
- f8bf61c9a692c82b0c01f3922a0b00946ae526d4e949797512d74dd5565ab990

# `feedback`

## Summary
- feedback issue の同一性正規化と検証に使う ACP builder の入口。既存 issue 候補との同一性判定および candidate の現在状態を検証する Structured Output schema と agent call 構築処理を扱い、feedback 正規化・検証フローから対応する下位ファイルへ進むための起点となる。

## Read this when
- feedback issue が既存候補と同一か新規かを判定する出力契約や agent call の構築内容を確認するとき
- feedback issue candidate の現在状態を検証する verdict、evidence、人間対応の出力契約や agent call 設定を確認するとき

## Do not read this when
- feedback issue の検出、候補生成・保存、報告・観測登録の処理を確認するとき
- 同一性判定や検証の具体的なロジック、candidate の実データ、report cut reference の内容を確認するとき
- 別の ACP builder の出力契約や処理を確認するとき

## hash
- 8b6c479a8d7c77782db5fde58798c4317ca42de3539a80eaadfa2d20f666b36a

# `indexing`

## Summary
- 対象ディレクトリは、`cmoc indexing` における INDEX.md エントリー生成処理の仕様・実装・出力形式をまとめた領域です。`index_entry.py` が agent call の prompt と起動パラメータを組み立て、`index_entry.json` が生成結果の Structured Output 形式を定義します。
- INDEX.md のルーティングやエントリー生成処理を変更・調査する際は、まずこのディレクトリを入口として、agent call 構築は `index_entry.py`、出力形式は `index_entry.json` を確認します。

## Read this when
- `cmoc indexing` の INDEX.md エントリー生成用 agent call の prompt、対象パス解決、読み取り専用設定、モデル・推論・実行パラメータを確認または変更するとき
- INDEX.md エントリー生成結果の Structured Output の必須項目や JSON 構造を確認するとき

## Do not read this when
- 既存の INDEX.md に記載されたルーティング内容を確認したいとき
- INDEX.md 生成用 prompt の共通構築規則だけを確認したいときは、`complete_prompt` の定義を直接読む
- 対象ファイルやディレクトリの実際の責務ではなく、一般的な CLI の別機能を調べるとき

## hash
- c3b0f40290ec11a0b30c626c8eecdd14815a157986b39b0444804c4668c8adcc

# `oracle`

## Summary
- oracle の編集・調査・レビューに用いる agent call 定義をまとめたディレクトリです。各下位項目から、oracle 操作用の起動パラメータ、prompt 経路、出力契約の確認へ進めます。

## Read this when
- `cmoc oracle edit`、`investigation`、`review` の agent call 起動条件やパラメータを確認・変更するとき。
- oracle 編集・調査・レビュー用 prompt の構築経路や参照境界を確認するとき。
- oracle review の Structured Output による出力契約を確認するとき。

## Do not read this when
- oracle file の内容、編集対象の仕様、またはレビューの具体的な判定基準を確認したいとき。
- agent call の一般的な起動パラメータだけを確認したいとき。
- oracle 操作以外の agent call や、agent call 実行そのものの処理を確認するとき。

## hash
- b8871049763a070d8479714a59637c145729393e22028eaa26420866d4e66968

# `quota_probe.py`

## Summary
- Codex CLI の quota 回復確認用 agent call を構築する定義。probe 用 prompt の内容、読み取り専用のアクセス設定、最小モデル・低推論強度、agent call の作業ディレクトリ、preflight 無効化などの起動パラメータをまとめる。quota 可用性確認の agent call 構築処理への入口となる。

## Read this when
- Codex CLI の quota 回復確認 probe の prompt や起動パラメータを確認・変更するとき
- quota 可用性確認用 agent call のモデル、推論強度、アクセスモード、preflight 設定を調べるとき

## Do not read this when
- quota probe の実行結果や quota 状態そのものを確認したいとき
- 一般的な prompt 生成処理や agent call の基本型を確認したいときは、それぞれの prompt builder または ACP 基本定義を直接読む

## hash
- d8aef551b3064c128af79d8831de5a0ac8d87610f17cc52351b9f8d777bec991

# `realization`

## Summary
- oracle の変更を realization へ反映する差分追従 Agent と、realization refactor の変更要約・ファイル単位レビュー／修正 Agent の起動定義を扱うディレクトリ。配下の `apply` と `refactor` が、それぞれの agent call builder、prompt、実行条件、Structured Output schema を確認する入口となる。

## Read this when
- oracle file の変更を realization file へ反映する Agent の起動定義を調査・変更するとき
- realization refactor の差分要約、ファイル単位レビュー・修正に関する Agent call の prompt、実行条件、出力契約を調査・変更するとき
- `apply` と `refactor` の起動設定や Structured Output schema の整合性を確認するとき

## Do not read this when
- 個別の oracle file または realization file の要求・実装内容を直接調査するとき
- 共通 prompt 生成、AgentCallParameter の共通仕様、Markdown rendering、path 解決、git 差分生成など、配下の個別 fork に固有でない処理だけを確認するとき

## hash
- c44ffab7712c4feca280196e4ba87bc2fc4873b69ead3d695a415f32b155af49

# `session`

## Summary
- `session/join` は、`cmoc session join` における merge conflict marker 解消用 agent call の構築定義への入口。conflicted paths の実パス解決、対象ファイルの prompt への埋め込み、conflict 解消専用 policy、REPO_WRITE 権限、最高品質の model・reasoning 設定、preflight 無効化を扱う。

## Read this when
- `cmoc session join` の conflict 解消 agent call に渡す対象ファイル、prompt、アクセス権限、適用 policy、model・reasoning、preflight 設定を確認・変更するとき

## Do not read this when
- merge conflict marker を含む対象ファイルを直接確認・編集するとき
- 通常の prompt 生成や session join の別処理を調べるとき。該当する prompt builder または session join 実装を直接読む。

## hash
- 373ae33e1a529b56c51bf23e18583cac2b27ffa5e0bf734f9997254aa7e55799

# `tui`

## Summary
- `cmoc tui` の TUI 起動に使う AgentCallParameter と完全プロンプトを構築する実装。オリジナルプロンプトを埋め込み、リポジトリ書き込みモード、リポジトリルートの作業コンテキスト、モデル・推論設定、oracle/realization と routing policy、起動前 indexing を含む固定パラメータを定義する。

## Read this when
- `cmoc tui` の起動パラメータまたは完全プロンプト skeleton の構築を確認・変更するとき。
- オリジナルプロンプトの埋め込み方、作業ディレクトリ、ファイルアクセスモード、モデル・推論設定、起動前 indexing の設定を確認するとき。

## Do not read this when
- 完全プロンプトの共通レンダリング規則を確認する場合は、`build_complete_prompt` の実装を直接読むとき。
- TUI 起動パラメータの呼び出し元や、別サブコマンドの設定を調べる場合。

## hash
- fe0c844b30d4c5106f83b0c9c65ecff5f2898928445521fb06d060f8f97b8f09
