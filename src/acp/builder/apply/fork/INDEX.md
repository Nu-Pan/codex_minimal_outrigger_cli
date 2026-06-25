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

# `file_finding_enumeration.py`

## Summary
- `cmoc apply fork` で、特定ファイルを起点に realization file の要修正点を列挙する AI 呼び出しパラメータを構築する実装。
- 起点パスを実パスへ解決し、リポジトリ全体を調査範囲として、関連する oracle file と realization file の読解、Structured Output schema への準拠、apply review standard への準拠を求める完全 prompt を組み立てる。
- ファイル単位で繰り返し呼ばれる重い処理であることを踏まえ、下流への影響を避けるため MAINSTREAM model と MEDIUM reasoning を指定する。

## Read this when
- `cmoc apply fork` のファイル単位の所見リストアップ用 prompt や AI 呼び出しパラメータを確認・変更したいとき。
- apply fork の所見列挙が、どの役割・調査範囲・標準・ファイルアクセスモードでエージェントに依頼されるかを確認したいとき。
- 起点ファイル以外の oracle file / realization file を読むことや、apply review standard を満たす所見リストを返すことが prompt に含まれているか確認したいとき。
- この所見列挙処理で使用する model class、reasoning effort、出力 schema の参照先を確認したいとき。

## Do not read this when
- `cmoc apply fork` の実際の所見統合、修正適用、差分反映、または Git 操作の制御フローを調べたいとき。
- oracle standard、realization standard、apply review standard の本文そのものを確認したいとき。
- AgentCallParameter、path 解決、完全 prompt 生成、markdown rendering などの共通部品の詳細実装を調べたいとき。
- ファイル単位ではなく、ディレクトリ単位・サブコマンド全体・CLI entrypoint のルーティングを確認したいとき。

## hash
- 8c27e836c8957d364dacd591645166d9aa1b00ef081fc85e523add1c6a97963d

# `finding_application.py`

## Summary
- `cmoc apply fork` で検出済みの所見に対応する修正作業を AI エージェントへ依頼するための呼び出しパラメータを構築する実装。
- 所見リストを JSON コードブロックとして prompt に埋め込み、realization file の修正担当向けの role、goal、作業上の注意、oracle/realization standard 参照を含む完全 prompt を生成する。
- 生成される呼び出し条件は mainstream model、medium reasoning、realization write 権限で、所見対応作業用の単一エントリーポイントとして位置づく。

## Read this when
- `cmoc apply fork` が所見対応作業用にどのような AI 呼び出しパラメータを作るか確認したいとき。
- 所見本文の prompt への埋め込み形式、作業担当 role、goal、git 操作禁止などの補助指示を変更したいとき。
- 所見対応作業で realization file の書き込み権限や利用 model class、reasoning effort がどう設定されるか調べたいとき。

## Do not read this when
- 所見を検出・生成する処理そのものを調べたいとき。
- `cmoc apply fork` の CLI 引数解析、サブコマンド登録、または実行フロー全体を調べたいとき。
- 所見対応作業ではない通常の apply prompt、review prompt、または complete prompt の共通構築処理を変更したいとき。

## hash
- 61fdb8a4dc76cc84716908dffb8d88e88ff5636b58d7589e4c6abfb89d52d93a
