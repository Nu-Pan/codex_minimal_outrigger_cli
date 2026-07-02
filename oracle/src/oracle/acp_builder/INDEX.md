# `apply`

## Summary
- `cmoc apply fork` 向けの AI エージェント呼び出しパラメータと出力契約を扱う。
- 差分要約、ファイル単位の所見列挙、所見対応作業に使う prompt、モデル設定、ファイルアクセス方針、Structured Output schema への入口となる。

## Read this when
- `cmoc apply fork` の作業レポート向け差分要約、実装レビュー所見の列挙、または検出所見への対応 agent call parameter を確認するとき。
- fork 適用後の差分や対象ファイルを AI に渡す prompt、placeholder、readonly/write 権限、model class、reasoning effort、Structured Output schema の指定を確認したいとき。
- 変更要約や所見リストの JSON 出力契約と、それを生成・利用する apply fork 用 oracle src の対応関係をたどりたいとき。

## Do not read this when
- `cmoc apply fork` 全体の CLI 引数解析、git 操作、branch 操作、作業レポート保存、所見統合などの実行フローを調べたいとき。
- apply fork 以外のサブコマンド用 prompt、agent call parameter、出力 schema を探しているとき。
- AgentCallParameter、complete prompt builder、path placeholder 解決、markdown rendering などの共通部品そのものの実装詳細を確認したいとき。

## hash
- 6965fe0f3359098b85dc1f37d601f441b5a4b3afc4ab56802f1807a95e677e39

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
- ファイルアクセス規則違反が発生した agent call のリカバリー用パラメータを構築する oracle src を扱う。違反時のアクセス規則、違反ファイル一覧、発生ログをプロンプトへ渡し、リカバリー担当 agent の完全プロンプトと実行条件を定義する。

## Read this when
- ファイルアクセス規則違反リカバリー用 agent call の role、summary、goal、補助プロンプトを確認したいとき。
- 違反ファイル一覧、違反時のファイルアクセスモード、発生ログのタイムスタンプがプロンプトへどう渡されるかを確認したいとき。
- ファイルアクセス規則違反リカバリーの AgentCallParameter、モデル種別、reasoning effort、file access mode の正本仕様断片を確認したいとき。

## Do not read this when
- 通常の agent call パラメータ全般や、モデル種別、reasoning effort、file access mode の型定義だけを確認したいとき。
- ファイルアクセス規則そのものの文章生成や、各アクセスモードの具体的な規則を確認したいとき。
- 完全プロンプトの共通組み立て処理や markdown rendering の仕様を確認したいとき。

## hash
- 118c4466ad2a34587fbc2709af936f495b9ec760662e1ea9b96398735de6459f

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
- `cmoc session join` における merge conflict marker 解消用 agent call parameter の正本実装を扱う領域。
- 衝突対象パスの prompt への提示、complete prompt の構成、モデルクラス・reasoning effort・ファイルアクセス権限など、session join の conflict 解消 agent call 条件を確認する入口。

## Read this when
- `cmoc session join` が merge conflict marker 解消エージェントへ渡す prompt、目標、呼び出し条件を確認または変更したいとき。
- conflict 対象ファイル一覧が実パスへ解決され、prompt 内に提示される方法を確認したいとき。
- oracle file の conflict 解消時だけ許可される追加編集規則を確認したいとき。
- `oracle_and_realization_basic`、`oracle_standard`、`realization_standard` を含む complete prompt 構成が必要な session join 用 agent call parameter を調べるとき。

## Do not read this when
- merge conflict marker の検出処理、git merge の実行、または `cmoc session join` 全体の制御フローを調べたいだけのとき。
- complete prompt builder、構造化 markdown rendering、path placeholder 解決、agent call parameter 型そのものの汎用仕様を調べたいとき。
- session join 以外のサブコマンドや、merge conflict marker 解消以外の agent call prompt を確認したいとき。

## hash
- 088e0aff40eb39bdcf24e7eece505ca6ecf057ef5733490bde12a05f8c554c03

# `tui`

## Summary
- TUI 起動時に AI Agent CLI/TUI へ渡す実行パラメータを、元プロンプト、固定プロンプト、ファイルアクセスプロファイル、モデル設定、Structured Output schema へ接続する正本仕様断片を収める。
- ユーザー入力プロンプトから作業条件を構造化する前段のパラメータ解決と、実際の TUI agent call 起動用パラメータ構築の入口になる。

## Read this when
- `cmoc tui` が agent call に渡すモデルクラス、推論強度、ファイルアクセス範囲、保存先、完全プロンプトを確認・変更したいとき。
- TUI 起動前にユーザー入力プロンプトから role、summary、goal、file access mode、参照すべき標準群を選ぶ処理を確認・変更したいとき。
- TUI 向け agent call parameter の Structured Output 要求、根拠行提示要求、標準文書参照フラグの扱いを確認したいとき。

## Do not read this when
- TUI 以外のサブコマンド向け agent call parameter 構築を確認したいとき。
- AgentCallParameter、ModelClass、ReasoningEffort、PlaceholderMap、complete prompt 構築などの共通部品そのものを調べたいとき。
- ユーザー入力取得、エディタ起動、コメント除去、文字列整形など、TUI の入出力処理を調べたいとき。
- oracle file、realization file、index entry、各 standard の本文や定義そのものを確認したいとき。

## hash
- dc7ec765166481a217e83dee235d8554aeb3e96c8b7ab7023fdb2146f9c9223f
