# `change_summary.json`

## Summary
- 変更差分を意味カテゴリごとに要約する JSON 出力の構造を定義する Structured Output schema。
- 各カテゴリには、人間向けの変更要約と、その根拠として有用な主要変更パスを含めることを求める。
- 変更報告をカテゴリ単位で機械処理可能に受け渡す箇所の入力・出力契約を確認する入口となる。

## Read this when
- 変更差分サマリーの JSON schema が求める必須構造を確認したいとき。
- 変更カテゴリ、要約文、主要変更パスをどの粒度で返すべきか判断したいとき。
- 差分報告生成や検証で、出力が schema に適合しているかを調べたいとき。

## Do not read this when
- 変更内容そのものの妥当性や、各ファイルで実際に何が変わったかを確認したいとき。
- カテゴリ分けされた差分サマリーを生成する実装ロジックを調べたいとき。
- ルーティング文書の書き方や INDEX.md エントリー一般の基準を確認したいとき。

## hash
- 51ffe6e61588c7c347494a36267c02b8d48f69f6e264fcaf396096938cdd672d

# `change_summary.py`

## Summary
- `cmoc apply fork` の作業レポート向けに、git diff 生テキストから人間向け変更要約を生成する AI 呼び出しパラメータを組み立てる正本 prompt。
- 差分を読み取り専用で扱い、Structured Output schema に従う要約担当 role・summary・goal・補助差分入力・プレースホルダを complete prompt として構成する。
- 利用する model class、reasoning effort、file access mode、出力 schema の対応付けを含み、変更要約生成処理の oracle 側入口になる。

## Read this when
- `cmoc apply fork` の変更要約生成 prompt の意図、入力差分の扱い、AI 呼び出しパラメータの構成を確認したいとき。
- 作業レポートで差分要約を生成する処理について、role・summary・goal・読み取り専用制約・補助プロンプトの正本を確認したいとき。
- 変更要約生成に使う model class、reasoning effort、Structured Output schema への接続を確認したいとき。

## Do not read this when
- 差分要約の実際の生成結果やレポート本文を確認したいだけのとき。
- `cmoc apply fork` 全体の実行フロー、ブランチ操作、git 操作、状態管理を調べたいとき。
- complete prompt の共通組み立て規則、path placeholder 解決、Structured Output 描画の一般仕様を調べたいとき。

## hash
- 6e989f5c5236652fcaa587074dd0aa04df726ac6c636631cdbfdea6e27f4af94

# `file_finding_enumeration.json`

## Summary
- 実装レビュー結果を表す Structured Output schema。所見リストを必須の最上位要素とし、各所見に見出し、根拠位置、oracle 要求、観測された実装、問題理由、修正方針を持たせる。
- 実装と oracle requirement の不一致を、根拠付きで機械的に受け渡すための出力形を定義する。

## Read this when
- 実装レビューや仕様適合性確認の結果を JSON として返す出力形式を確認したいとき。
- 所見に含めるべき根拠情報、oracle 要求、観測実装、問題理由、修正方針の構造を確認したいとき。
- レビュー結果の Structured Output schema に従う生成処理や検証処理を実装・修正するとき。

## Do not read this when
- oracle file や realization file の定義そのものを確認したいとき。
- 実装レビューの判断基準や、何を問題として扱うべきかの規範を確認したいとき。
- 特定の実装ファイルや仕様ファイルの本文を調査したいとき。

## hash
- 0bed168a2a89c47730cdc914c08c08f2a3ad4022595c4b910c5d8ff9ca335524

# `file_finding_enumeration.py`

## Summary
- `cmoc apply fork` で、特定ファイルを起点に realization file の要修正点を列挙するための agent call parameter を組み立てる正本 prompt 断片。
- 対象ファイルとリポジトリルートをプレースホルダとして渡し、readonly の調査、oracle・realization・apply review 各標準の投入、所見リスト用 Structured Output schema の指定を行う。
- ファイル単位に多数呼び出されるが、下流への影響が大きいため MAINSTREAM model と MEDIUM reasoning を選ぶ判断根拠を含む。

## Read this when
- `cmoc apply fork` のファイル単位所見リストアップで、agent に渡す role・summary・goal・標準類・placeholder を確認したいとき。
- apply review standard に従う所見列挙 prompt の入口条件や、対象ファイル以外の oracle file / realization file を読む要求を確認したいとき。
- ファイルごとの所見列挙呼び出しに使う model class、reasoning effort、file access mode、Structured Output schema の選択理由を確認したいとき。

## Do not read this when
- `cmoc apply fork` 全体の実行制御、所見の統合、修正適用、fork 管理の挙動を知りたいとき。
- 所見リストの Structured Output schema 本体や apply review standard の詳細を確認したいとき。
- 特定の realization file の実装修正内容や、oracle と realization の差分そのものを調査したいとき。

## hash
- 9b0f19cf132f0da09b6530de64be558f71605d380949239b6c3c98014b8ad910

# `finding_application.py`

## Summary
- `cmoc apply fork` で検出された所見に対応するための agent call parameter を構築する oracle src。所見 JSON をプロンプトへ埋め込み、realization file の修正担当 agent に渡す役割を持つ。
- 生成される prompt には、所見は絶対指示ではなく作業ヒントであること、git add と git commit を禁止すること、realization write 権限で修正することが含まれる。

## Read this when
- `cmoc apply fork` の所見対応作業で呼び出す agent の role、summary、goal、注意事項、ファイルアクセス権限を確認または変更したいとき。
- 所見リストをどのように prompt 内へ埋め込むか、または FINDING 単位の JSON 表現を確認したいとき。
- apply fork 系の agent call parameter のうち、所見修正担当 agent の model class、reasoning effort、file access mode を調整したいとき。

## Do not read this when
- `cmoc apply fork` の所見検出そのもの、fork 作成、branch 操作、commit 操作の実装を確認したいとき。
- prompt building 共通処理、Structured markdown の描画、path placeholder 解決の詳細を確認したいとき。
- realization standard や oracle/realization の基本定義そのものを確認したいとき。

## hash
- f9f304dfe1dda61a95ab9a19e78c9f09560cf0e018b07acd09e4b4a336332db5
