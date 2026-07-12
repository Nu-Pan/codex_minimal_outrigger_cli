# `apply`

## Summary
- `cmoc apply fork` の差分要約・file 単位の所見列挙・所見適用を担う領域。作業レポート向けの要約、file ごとの所見抽出、所見本文を起点にした適用呼び出しの入口として読む。
- 変更要約だけを確認したいなら `change_summary.*`、file 単位の所見抽出条件と出力形を確認したいなら `file_finding_enumeration.*`、所見本文から修正作業への呼び出し条件を確認したいなら `finding_application.py` を見る。

## Read this when
- `cmoc apply fork` で fork 後の差分を人間向けに要約・分類して出力する仕様を確認したい。
- file 単位の所見を列挙する入力条件、読む範囲、出力の形を確認したい。
- 所見本文から修正作業用の agent 呼び出し条件や prompt 構成を確認したい。
- 差分要約、所見列挙、所見適用のうち一つだけを追いたい。

## Do not read this when
- fork の作成、branch 操作、diff 取得、保存など実行フロー全体を追いたい。
- 個別の所見内容や実装修正そのものを確認したい。
- `cmoc apply fork` 以外のサブコマンドの prompt や agent call 条件を探している。

## hash
- 09e5dbe80ac9950010abe43c2103b02d3f427af1626f858002c51efbc0f316ae

# `basic.py`

## Summary
- agent call の入力パラメータを表す型定義を置く。モデル選択、推論強度、ファイルアクセス方針、プロンプト、Structured Output schema、preflight 実行有無、作業ディレクトリをまとめて扱う。

## Read this when
- Agent Call Parameter の構造や既定値を確認したいとき。
- モデルクラスや reasoning effort の候補、ファイルアクセスモードの意味境界を見たいとき。
- Structured Output schema の有無や indexing preflight の実行条件を確認したいとき。

## Do not read this when
- 実際のモデル名への解決や file access rule の詳細実装を知りたいときは、別の実装側を読む。
- agent call の実行フロー全体やコマンド組み立てを知りたいだけなら、この型定義ではなく呼び出し側を読む。

## hash
- 9b49b16ddc0c2310a2c8fcc49b4b529db8fd22b35753ccd71c3be38db2bd9f25

# `common`

## Summary
- oracle ACP builder の共通部品を定義する oracle src 群への入口。ACP builder の各生成処理で共有される状態、ルール、出力結果の正本仕様断片を扱う。
- 個別の builder 実装ではなく、builder 間で共有される概念や型の仕様を確認するためのまとまり。

## Read this when
- ACP builder 全体で共通して使う状態、ルール、結果表現の正本仕様断片を確認したいとき。
- ACP builder の複数領域にまたがる挙動を実装・テストへ反映する前に、共有概念の境界を確認したいとき。
- 下位要素のどれを読むべきか、共通部品の責務から絞り込みたいとき。

## Do not read this when
- 特定の builder の個別仕様だけを確認したいとき。
- realization code 側の実装詳細やテスト構成を確認したいとき。
- ACP builder と無関係な oracle src の仕様を探しているとき。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `indexing`

## Summary
- INDEX.md エントリー生成の出力契約を定義する正本 schema。人間向け要約と、読むべき条件・読まなくてよい条件だけを必須にして、余分な項目を持たせない。
- この schema は、INDEX.md の各エントリーを同じ情報粒度で揃えたいときの基準になる。

## Read this when
- INDEX.md エントリー生成の期待値を確認したいとき。
- エントリーに必須の情報単位と、余計な項目を許さない方針を確認したいとき。
- エントリー生成結果を検証する実装やテストで、JSON 構造の基準を見たいとき。

## Do not read this when
- 個別の対象について、実際にどんな要約や読む条件を書くべきかを判断したいとき。
- INDEX.md のルーティング方針や記述品質の基準を確認したいとき。
- cmoc の実装・テスト・CLI 挙動を確認したいとき。

## hash
- d356e82b6f62b8db20434389b978ed426fe725dfa8a1fd90a85f2b70a1609f02

# `review`

## Summary
- `cmoc review oracle` の所見レビュー処理で使う prompt 生成と応答 schema を扱う入口。新規所見の列挙、既知所見との重複排除、採否判定、所見群の整理、擁護・反証の各段階を分けて確認したいときにここから入る。
- レビュー結果の作成フロー全体を追うときのルーティング先であり、対象ごとに確認すべき段階がまだ定まっていない場合の起点にもなる。

## Read this when
- `cmoc review oracle` の所見レビュー全体の流れを追いたいとき。
- 新規所見の列挙、採否判定、所見整理、擁護理由、反証理由のどれを実装・確認すべきか切り分けたいとき。
- レビュー用 prompt が、どの種類の所見や既知情報を入力に取り、どの応答契約を返すかを確認したいとき。
- レビュー結果の扱いを変更したいが、対象が新規所見・採否・整理・理由生成のどれかまだ特定できていないとき。

## Do not read this when
- `cmoc review oracle` 以外のサブコマンドの prompt 生成や出力契約を確認したいとき。
- oracle file 全般の品質基準や、何を問題として扱うかという正本仕様そのものを確認したいとき。
- 個別の所見本文や oracle file 本体の内容を確認したいとき。
- CLI の表示整形や保存処理だけを追いたいとき。

## hash
- b02adf32279141d84554a1210f319e28170448b28f93971d37d5267872008ca4

# `session`

## Summary
- `cmoc session join` の merge conflict 解消向けパラメータ生成をまとめて見る入口。対象パスの正規化、conflict 対象ファイル一覧、追加編集の許容範囲、実行設定を確認したいときにここから進む。

## Read this when
- `cmoc session join` の conflict resolution 用パラメータ生成を変更・確認したい。
- conflict 対象パスの扱い、実行モデル、推論強度、repo write 前提の設定を確認したい。
- merge conflict 解消時に AI に渡す制約や追加ファイルアクセス条件を確認したい。

## Do not read this when
- 通常の `session join` の接続処理やセッション管理だけを見たい。
- 共通の prompt 生成や markdown 化の実装だけを見たい。
- conflict 解消以外のサブコマンド向けエージェントパラメータを探している。

## hash
- 8aa49882fdce0a9bdeda3d8f1f5069408a9d6a426373f6f2ec4e941d920ef6d8

# `tui`

## Summary
- `cmoc tui` の起動時に使う呼び出し条件と起動パラメータを扱う領域。元プロンプトの束ね方、完全プロンプトの保存、モデル・推論強度・ファイルアクセス方針の固定値、そこから `AgentCallParameter` を組み立てる流れを確認したいときに読む。
- TUI の対話本体や編集画面そのものではなく、起動前にどの入力をどの形で実行用条件へ変換するかに責務が絞られている。

## Read this when
- `cmoc tui` の起動パラメータ、保存される完全プロンプト、または起動時に固定されるモデル・推論強度・ファイルアクセス方針を変えたいとき。
- 元プロンプトをどう共通プロンプトへ束ね、どのファイルへ保存してからエージェント呼び出しに渡すかを確認したいとき。
- `cmoc tui` の実行フローのうち、起動用の `AgentCallParameter` を生成する部分だけを追いたいとき。

## Do not read this when
- `cmoc tui` の対話 UI や編集画面の制御を追いたいだけのとき。
- 実行条件の判定ルールや、入力を role・summary・goal・file_access_mode へ構造化する定義だけを見たいときは、そちらの定義側を読む。
- `AgentCallParameter` 型そのものや、共通のプロンプト定義だけを確認したいとき。

## hash
- 7053fdb0b134818ec54c1473fc7c59b50da39f3f9f7d4c802d0b677cf8e46a38
