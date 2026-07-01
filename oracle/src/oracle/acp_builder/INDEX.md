# `apply`

## Summary
- `cmoc apply fork` のレビュー・報告段階で使う agent call の正本仕様への入口。fork 適用後の差分要約、realization file の所見列挙、所見対応作業の委譲に関する prompt、AgentCallParameter、出力契約を扱う。
- git diff 由来の変更説明、人間へ渡すレビュー所見、所見対応エージェントへ渡す作業指示について、出力互換性や根拠情報の粒度を確認するための領域。

## Read this when
- `cmoc apply fork` で、fork 適用後の差分要約、realization file の要修正点列挙、所見対応作業の委譲に使う prompt や AgentCallParameter の正本仕様を確認したいとき。
- 差分要約やレビュー所見の出力契約について、互換性、必須の根拠情報、空でない前提、主要変更箇所や修正方針の粒度を確認したいとき。
- apply fork のレビュー・報告系 agent call に渡す role、summary、goal、file access mode、model class、reasoning effort、placeholder、標準文書の組み込み方を変更または検証したいとき。

## Do not read this when
- `cmoc apply fork` の fork 作成、適用、branch 操作、git 操作、作業レポート保存など、レビュー・報告用 agent call より前後の実行フローを調べたいとき。
- 個別ファイルのパッチ内容、diff 生成手順、実際の realization file 修正結果、または所見の統合・実行結果処理を確認したいとき。
- apply fork 以外のサブコマンドの prompt、AgentCallParameter、共通部品の実装詳細、または一般的なルーティング文書の書き方を探しているとき。

## hash
- c471f88082c2cc273436db5b8e4e2bf40947e4b9a9c20ac95dd298f61404132a

# `basic.py`

## Summary
- AI コーディングエージェント呼び出しに渡す基本パラメータの oracle src。論理モデルクラス、Reasoning effort、ファイルアクセスモード、プロンプト、Structured Output schema パスを 1 つの不変データ構造として定義する。
- バックエンド固有のモデル名や Reasoning Effort 名への解決は扱わず、cmoc 内で使う論理的な選択肢と呼び出しパラメータの形だけを定める。

## Read this when
- agent call の入力パラメータとしてどの項目を持たせるかを確認したいとき。
- モデル選択、reasoning effort、ファイルアクセスモードを表す論理 enum の意味を確認したいとき。
- Structured Output schema を要求する呼び出しと要求しない呼び出しで、schema パスをどう表すかを確認したいとき。

## Do not read this when
- バックエンドが実際に受理する具体的なモデル名や reasoning effort 名への変換処理を確認したいとき。
- 各ファイルアクセスモードが生成する具体的なファイルアクセス規則を確認したいとき。
- agent call の実行手順、プロセス起動、結果処理、エラー処理を確認したいとき。

## hash
- c2a86abaffb6201c6e5a3f5ee4490bde862d4a6a1e4ae82494c650de9ea0c5f1

# `common`

## Summary
- ファイルアクセス規則違反が起きた agent call を修復するための、再呼び出し用パラメータ構築を扱う正本断片への入口。違反時の規則本文、対象ファイル、発生ログをリカバリー担当 agent に渡す設計意図を確認するための領域。

## Read this when
- ファイルアクセス規則違反リカバリー用の agent call parameter の構成意図を確認したいとき。
- 違反ファイル一覧、違反時のアクセスモード、違反ログを動的プロンプトへ渡す仕様断片を確認したいとき。
- 違反修復タスクで指定するモデル種別、推論量、アクセスモードの正本断片を確認したいとき。

## Do not read this when
- 通常の agent call parameter 全般や、違反リカバリー以外の呼び出し種別を調べたいとき。
- ファイルアクセス規則そのものの本文生成や、アクセスモード別の規則内容を確認したいとき。
- パスプレースホルダの一般定義や repo root 解決の仕様だけを確認したいとき。

## hash
- 762d2116b4bf3bb6703a279d25e1debdcea801b946975aa6bb5a4276289fab9c

# `indexing`

## Summary
- INDEX.md エントリー生成の出力契約と、その契約に従う agent call parameter の組み立てを定義する領域。
- ルーティング文書作成担当に渡す role、goal、readonly 条件、既存目次を根拠にしない生成規則、対象内容の埋め込み、Structured Output schema 出力先を確認する入口になる。

## Read this when
- cmoc indexing で、個別対象の INDEX.md エントリーを生成する prompt や agent call parameter を確認・変更したいとき。
- エントリー生成結果に必須となる要約、読むべき条件、読まなくてよい条件の JSON 構造を確認したいとき。
- エントリー生成時に AI へ渡す制約、対象内容の扱い、Structured Output schema の適用方法を確認したいとき。

## Do not read this when
- INDEX.md エントリーの記述品質基準そのものを確認したいときは、基準を定義する正本仕様を読む。
- cmoc indexing 全体の CLI 起動、対象探索、既存目次更新、ファイル書き込みの処理を調べたいときは、それぞれを担う実装へ進む。
- complete prompt の汎用組み立て、構造化 markdown 描画、path placeholder 解決、agent call parameter 型そのものを調べたいときは、それぞれの定義元を読む。

## hash
- 04a6b74e91c790dccfdd14ced597201bc24e638e15a879eec0fe96e7a409ce26

# `review`

## Summary
- `cmoc review oracle` の各段階で使う oracle file レビュー用 agent call parameter と Structured Output schema をまとめるディレクトリ。
- 新規所見の列挙、所見の擁護・反証、採否判定、重複・矛盾の整理について、AI 呼び出しへ渡す prompt 断片、読み取り制約、モデル設定、出力契約を確認する入口になる。
- レビュー所見の生成から検証・整理までの出力境界や prompt 接続を段階別にたどるための下位ファイルを収める。

## Read this when
- `cmoc review oracle` の oracle file レビュー処理で、所見列挙、所見検証、採否判定、所見マージのいずれかの agent call parameter や出力 schema を確認・変更したいとき。
- レビュー対象 oracle file、既知所見、既知の擁護理由・反証理由、所見リストが、各レビュー段階の prompt や Structured Output にどう渡るか調べたいとき。
- oracle file を根拠にした新規所見、新規理由、採否理由、重複・矛盾整理の応答契約を段階別に確認したいとき。
- `PURE_ORACLE_READ`、review oracle standard、対応 JSON schema、reasoning effort、モデル設定など、oracle review 用 agent call の正本 prompt 断片を探すとき。

## Do not read this when
- `cmoc review oracle` サブコマンド全体の CLI 引数、実行制御、結果集約、表示処理など realization implementation 側の挙動を確認したいとき。
- oracle file 全般の品質基準、oracle standard、review oracle standard の本文そのものを読みたいとき。
- oracle review 以外の agent call parameter、または oracle file 以外を読むレビュー処理を調べたいとき。
- INDEX.md エントリーやルーティング文書の生成規則を確認したいとき。

## hash
- 7370093ef92dff663fd969b7476e80fa1eb8d31a250d6403255eb66b0d226ba7

# `session`

## Summary
- `cmoc session join` の merge conflict marker 解消用 agent call parameter 生成に関する正本実装領域。conflict 対象パス、例外的な oracle file 編集許可、作業範囲、禁止事項、完了条件を含む prompt 生成の入口になる。

## Read this when
- `cmoc session join` で merge conflict marker 解消用 agent を呼び出すための prompt や agent call parameter の仕様を確認したいとき。
- conflict 対象ファイル一覧を agent prompt に渡す扱い、model、reasoning effort、file access mode を確認したいとき。
- merge conflict 解消時に oracle file の最小編集を例外的に許可する条件や範囲を確認したいとき。

## Do not read this when
- 通常の session join 処理、git 操作、branch 統合、状態管理を調べたいとき。
- merge conflict marker の検出方法や conflicted paths の収集方法を調べたいとき。
- 汎用 prompt builder、構造化 markdown レンダリング、path placeholder 解決の実装を調べたいとき。

## hash
- 5c74a34b38d44d8ccd1049c61e73da7fd68ce6299fb0acc6afbfde7ebbd6bea7

# `tui`

## Summary
- `cmoc tui` の agent call parameter 構築に関する正本実装と Structured Output schema を置くディレクトリ。TUI 起動時の呼び出しパラメータ、ユーザー入力プロンプトからの実行条件解決、解決結果 schema への入口になる。
- TUI が使うファイルアクセスプロファイル、complete prompt、モデルクラス、推論強度、標準文書参照フラグ、パラメータ解決結果の構造を確認するための対象を含む。

## Read this when
- `cmoc tui` の起動または実行前解決で、AI Agent に渡す AgentCallParameter の正本仕様断片を確認・変更したいとき。
- TUI 起動時の complete prompt、モデルクラス、推論強度、保存先、ファイルアクセスプロファイル、標準フラグの組み立てを確認したいとき。
- ユーザー入力プロンプトから役割、概要、ゴール、論理ファイルアクセスモード、参照すべき標準文書を構造化する schema や出力要求を確認したいとき。

## Do not read this when
- TUI 以外のサブコマンドにおける agent call parameter 構築を確認したいとき。
- ユーザー入力取得、エディタ起動、コメント除去、strip など TUI 入力フローの実装だけを調べたいとき。
- AgentCallParameter、ModelClass、ReasoningEffort、PlaceholderMap、complete prompt 構築などの共通部品そのものの定義を調べたいとき。
- 個々の標準文書の本文、ファイルアクセス属性、パスモデル、INDEX.md エントリー作成規則そのものを確認したいとき。

## hash
- f50ccba3761276eb29fc0a31a2dfef25297ad15c127525ba62f530da031b72c7
