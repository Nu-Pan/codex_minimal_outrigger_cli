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
- `apply` は、`cmoc realization apply fork` における AgentCallParameter 構築の入口です。追従対象の commit 範囲と oracle file の raw git diff を prompt に組み込み、realization file 全体への反映と整合性検証を行う agent call の起動契約を扱います。具体的な `fork` 起動定義を確認する前のルーティング対象です。
- `refactor` は、realization refactor の agent call builder と Structured Output schema を扱います。変更差分の意味論的カテゴリ別要約、および oracle file・realization file 単位の所見調査、修正、検証に関する prompt、権限、実行条件、作業ディレクトリ、indexing preflight、出力契約を確認する入口です。

## Read this when
- `cmoc realization apply fork` の prompt、作業範囲、realization write 権限、モデル、推論 effort、linked worktree、ルーティング事前処理を確認・変更するとき。
- oracle file の変更を realization file 全体へ反映する agent call の起動契約を確認するとき。
- realization refactor の変更差分要約 agent call の出力契約、prompt、入力差分、実行条件を確認・変更するとき。
- realization refactor のファイル単位レビュー・修正 agent call の findings、根拠、変更、oracle 要求、修正結果、検証に関する出力契約を確認・変更するとき。
- realization refactor の二つの agent call の Structured Output schema と builder 設定の整合性を確認するとき。

## Do not read this when
- 通常の realization implementation、realization test、realization ancillary の具体的な実装を変更するとき。
- `fork` 用起動定義の本文を直接確認すれば足りるとき。
- `cmoc realization apply fork` 以外の起動パラメータを確認するとき。
- 変更差分の実装内容や要約結果そのものを確認したいとき。
- レビュー対象の oracle file や realization file の要求・実装を直接確認したいとき。
- 共通 prompt 生成、構造化文書の Markdown rendering、path 解決の一般仕様を確認するとき。
- realization refactor の fork 以外の agent call、別の出力 schema、または git 差分生成そのものを調査するとき。

## hash
- f58663721f3bccc66a153bb1c26f4b4a400985c2b75ec2b26257337d2399111c

# `session`

## Summary
- session join の merge conflict 解消に使うエージェント呼び出し設定と専用 prompt を定義する入口。競合対象パスの解決、conflict marker の解消方針、モデル・推論設定、リポジトリ書き込み権限を扱う。

## Read this when
- session join の merge conflict 解消処理を実装・変更・レビューするとき
- conflict 解消用エージェントの prompt、対象パス解決、モデル設定、ファイル権限を確認するとき
- conflict 解消時に余計な差分や仕様変更を避ける呼び出し条件を確認するとき

## Do not read this when
- 通常の session join の結合処理や conflict 以外のサブコマンドを確認するとき
- 一般的な prompt 生成や共通のエージェント呼び出し型を確認するとき
- 競合解消対象以外のファイル編集・リファクタリング方針を確認するとき

## hash
- 5a792915b867b8c81bc898d563685fc4fff89d1393a1bc8d55bcb8a466fb5e0c

# `tui`

## Summary
- `cmoc tui` の起動パラメータ構築実装を収めるディレクトリ。オリジナルプロンプトを完全プロンプトへ埋め込み、リポジトリ書き込み権限、モデル・推論設定、作業ディレクトリ、構造化出力設定、起動前インデックス処理をまとめた `AgentCallParameter` を生成する。個別の起動規則を確認・変更する場合は `launch_tui.py` が入口となる。

## Read this when
- `cmoc tui` の起動方法、起動時パラメータ、完全プロンプトへのオリジナルプロンプト埋め込みを調査または変更するとき
- TUI 起動時のファイルアクセス権限、モデル、推論強度、作業ディレクトリ、インデックス前処理の設定を確認するとき

## Do not read this when
- 完全プロンプトの共通生成処理そのものを調査・変更するときは `build_complete_prompt` の定義を直接読む
- `AgentCallParameter`、各種列挙型、パス解決処理の仕様を確認するときは、それぞれの定義元を直接読む
- TUI 以外のサブコマンドの起動パラメータを扱うとき

## hash
- 3d5c0196bca3ffe6cf05960fa0c839e8efb21568e15d5ef317f8d0ef436bf88d
