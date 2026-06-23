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
- `cmoc apply fork` で、指定された起点ファイルから realization file の所見を列挙するための AI 呼び出しパラメータを構築する実装。
- 起点パスとリポジトリルートを解決し、oracle・realization・apply review の各 standard を含む完全 prompt を組み立て、所見リスト用の Structured Output schema とともに返す入口である。

## Read this when
- `cmoc apply fork` のファイル単位の所見リストアップで、AI に渡す role・summary・goal・参照 standard・読み取り専用アクセス設定を確認または変更したいとき。
- 所見列挙用の AgentCallParameter のモデルクラス、reasoning effort、file access mode、prompt 生成、出力 schema の接続を追いたいとき。
- 起点として渡された oracle file または realization file から、対象リポジトリ内の realization file を調査させる prompt 文面の責務を確認したいとき。

## Do not read this when
- 所見リストの JSON schema 自体の項目や形式を確認したいだけのときは、所見リスト用 schema の本文を読む。
- complete prompt の共通組み立て規則、各 standard の本文挿入方法、markdown レンダリングの詳細を調べたいときは、それぞれの共通 prompt 構築や構造化文書レンダリングの実装を読む。
- `cmoc apply fork` の実際の fork 適用処理、所見の評価基準そのもの、またはパス解決 helper の挙動を調べたいときは、この prompt パラメータ構築ではなく該当する実装や正本仕様を読む。

## hash
- 0afe13d940c449eb500b7516868d85ccaac1ffe20a43e645c1558ae157322dda

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

# `finding_list.json`

## Summary
- 実装調査で見つかった、正本仕様・標準・実装の不一致や品質上の問題を機械処理しやすい所見一覧として表すためのデータ構造を定義する。
- 各所見は、根拠位置、要求される仕様・規範、観測された実装、問題と言える理由、修正方針をひとまとまりで保持する。
- 仕様適合性レビューや実装修正タスクへ渡す診断結果の形を確認する入口になる。

## Read this when
- 実装に対する所見一覧を生成・検証・消費する処理を扱うとき。
- 所見に含めるべき根拠、仕様要求、観測事実、理由、修正方針の責務境界を確認したいとき。
- 実装レビュー結果を後続の修正判断に渡すため、所見単位の情報が十分かを確認したいとき。

## Do not read this when
- 個別の正本仕様や標準そのものの内容を確認したいとき。
- 実装ファイルの具体的な不具合箇所や修正コードを調べたいとき。
- 所見一覧ではなく、別種の出力や一般的なエラー報告の構造を確認したいとき。

## hash
- 0bed168a2a89c47730cdc914c08c08f2a3ad4022595c4b910c5d8ff9ca335524

# `refine_finding.py`

## Summary
- `cmoc apply fork` で集約済みの所見リストを改善するための AI 呼び出しパラメータを組み立てる実装。
- 入力されたファイル別所見の集合を JSON として補助プロンプトに埋め込み、重複・矛盾・明らかな False-Positive の除去、新規所見の追加、作業順に消化可能な所見リストへの整理を要求する。
- oracle・realization・apply review の各標準を含めた read-only の完全プロンプトを生成し、改善結果の出力先 schema を指定して返す。

## Read this when
- `cmoc apply fork` の所見リスト改善ステップで、AI に渡す role・summary・goal・補助プロンプト・参照標準を確認または変更したいとき。
- 所見リスト改善用の AgentCallParameter が、どの model class、reasoning effort、file access mode、出力 schema を使うか確認したいとき。
- apply fork のレビュー所見から、重複除去・矛盾解消・False-Positive 除外・新規所見追加を促すプロンプト文面を調整したいとき。

## Do not read this when
- 所見リストを生成する前段の探索・レビュー処理を調べたいだけのとき。
- 改善後の所見リスト schema 自体の定義や、schema ファイルの内容を確認したいとき。
- 完全プロンプト共通部品の組み立て規則、StructDoc の描画、path 解決、AgentCallParameter 型そのものを調べたいとき。

## hash
- dbcd18cc3d27d4bf74eb05d955961889209e4d95d238beac43350f7867314d6a
