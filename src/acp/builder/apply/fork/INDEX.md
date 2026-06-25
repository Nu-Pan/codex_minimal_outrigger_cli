# `change_summary.json`

## Summary
- 差分内容を意味論上のカテゴリごとにまとめるための構造を定義するスキーマ。各カテゴリの人間向け要約と、根拠として読むべき主要な変更対象を対応付ける。
- 実装変更やテスト変更などを混在した差分としてではなく、作業意図ごとのまとまりとして報告・保存したい場面への入口になる。

## Read this when
- 適用・分岐処理の結果として、変更内容をカテゴリ単位で要約する出力仕様を確認したいとき。
- 変更要約に含める粒度が、網羅的な全ファイル一覧ではなく主要な根拠対象の列挙でよいかを判断したいとき。
- 差分要約の各まとまりに、カテゴリ名、何をどう変えたかの説明、主要な変更対象を持たせる必要があるとき。

## Do not read this when
- 個々の差分をどのように検出するか、またはカテゴリへ分類するアルゴリズムを調べたいとき。
- 実際の変更対象ファイルの内容や、適用処理そのものの制御フローを確認したいとき。
- ルーティング文書、テスト、実装など特定カテゴリの詳細な本文を直接確認すれば足りるとき。

## hash
- 51ffe6e61588c7c347494a36267c02b8d48f69f6e264fcaf396096938cdd672d

# `change_summary.py`

## Summary
- `cmoc apply fork` の作業レポート向けに、対象ブランチ上の git diff をそのまま入力として受け取り、変更内容の人間向け要約を生成する AI 呼び出しパラメータを組み立てる。
- 読み取り専用のファイルアクセス、効率重視モデル、中程度の推論量、変更要約用の Structured Output schema を指定し、完全 prompt に差分本文を補助文書として埋め込む。

## Read this when
- `cmoc apply fork` の変更要約 prompt、作業レポート用要約、または git diff を AI に渡す呼び出し条件を確認したいとき。
- 変更内容要約の入力差分をどのように prompt に含めるか、または要約生成時のモデル種別・推論量・ファイルアクセス権限を確認したいとき。
- `cmoc apply fork` の実行後レポートに使う Structured Output schema の参照先や、AgentCallParameter の構築責務を追うとき。

## Do not read this when
- `cmoc apply fork` の実際の branch 作成、差分取得、作業適用、または git コマンド実行処理を調べたいだけのとき。
- 変更要約の JSON schema 自体の項目定義や検証内容を確認したいとき。
- 汎用的な prompt 結合処理、構造化 markdown の描画処理、または path keyword の定義を調べたいとき。

## hash
- e958bca0852f6b124010f16314781a5093835941077ed2faef44217ce9587626

# `file_finding_enumeration.py`

## Summary
- `cmoc apply fork` で、指定された oracle file または realization file を起点に realization file の所見を列挙する AI エージェント呼び出しパラメータを構築する実装。
- リポジトリルートと対象パスを実パスへ解決し、oracle standard、realization standard、apply review standard を含む read-only の complete prompt を組み立て、MAINSTREAM モデル、MEDIUM reasoning、所見リスト用 schema を指定して返す。

## Read this when
- `cmoc apply fork` のファイル単位の所見リストアップ呼び出しで、AI に渡す role、summary、goal、標準群、file access mode を確認または変更したいとき。
- 所見列挙の起点となるパスの解決方法、対象ツリーの扱い、oracle file と realization file を読むよう促す prompt 内容を確認したいとき。
- ファイル単位レビューの品質やコストに関わるモデルクラス、reasoning effort、出力 schema の選択を確認したいとき。

## Do not read this when
- `cmoc apply fork` の所見リストそのものの schema 定義を確認したいだけのときは、schema を定義する隣接ファイルを読む。
- complete prompt の共通組み立て処理や標準文書の本文を確認したいときは、prompt parts や標準定義側を読む。
- 実際に列挙された所見の集約、適用、表示、CLI 引数処理を調べたいときは、それぞれの責務を持つ apply fork 側の別実装へ進む。

## hash
- 828e4f9dfd774dd768a2937f394254c2d7c1f5cc9145338503b6a3f8207b7700

# `finding_application.py`

## Summary
- `cmoc apply fork` で検出された所見に対応する修正作業用の AI 呼び出しパラメータを組み立てる実装。所見本文を補助プロンプトとして埋め込み、realization file の修正担当として動くための role、summary、goal、作業上の注意、oracle/realization 基本情報、realization standard を含む完全プロンプトを生成する。
- 生成される呼び出し条件は、MAINSTREAM モデル、MEDIUM reasoning、realization write 権限で固定され、所見対応作業では git add と git commit を禁止する注意を含める。

## Read this when
- `cmoc apply fork` の所見対応フェーズで、AI エージェントに渡す prompt、role、goal、補助情報、file access mode、model class、reasoning effort の組み立てを確認または変更したいとき。
- 所見本文をどのように作業指示へ埋め込むか、また所見を絶対指示ではなく修正作業のヒントとして扱わせる制御を確認したいとき。
- realization file 修正用のエージェント呼び出しが、oracle/realization 基本情報や realization standard を含む完全プロンプトを使うかどうかを確認したいとき。

## Do not read this when
- `cmoc apply fork` の CLI 引数解析、サブコマンド登録、実行フロー全体、または所見の生成処理を調べたいだけのとき。
- oracle file や realization file の定義そのもの、パスキーワードの定義、またはファイルアクセスモードの一般仕様を確認したいとき。
- AI 呼び出しパラメータのデータ構造、モデル種別、reasoning effort、file access mode の型定義や共通実装を変更したいとき。

## hash
- 5ccbcdfb0b6df05c24d272cc714f85e83eda521118be32160ce9294c947e0064

# `file_finding_enumeration.json`

## Summary
- 実装調査で見つかった問題点を、根拠位置、正本仕様上の要求、観測された実装、問題理由、修正方針として報告するための構造化出力を定義する。
- 仕様と実装の乖離をレビュー結果として人間に渡す場面で使う、所見リストの出力契約を担う。

## Read this when
- 実装レビューや適合性調査の結果として、明確に修正が必要な所見を返す出力形式を確認したいとき。
- 所見に含めるべき根拠情報、仕様要求、観測結果、理由、修正方針の粒度を確認したいとき。
- レビュー結果の生成側または検証側で、所見リストが空でない根拠位置を持つことを前提にしたいとき。

## Do not read this when
- 単に実装対象の仕様そのものを探しているとき。ここには個別機能の要求ではなく、レビュー所見の報告形式だけがある。
- INDEX.md 用エントリーや一般的なルーティング文書の書き方を確認したいとき。
- 所見を JSON 以外の文章、ログ、CLI 表示としてどう見せるかを確認したいとき。

## hash
- 0bed168a2a89c47730cdc914c08c08f2a3ad4022595c4b910c5d8ff9ca335524
