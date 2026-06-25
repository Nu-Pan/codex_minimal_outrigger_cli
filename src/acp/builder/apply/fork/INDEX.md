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
- `cmoc apply fork` の作業レポート向けに、差分テキストから人間向け変更要約を生成する AI 呼び出しパラメータを組み立てる実装。
- 対象ワークツリー内の git diff を読み取り専用の補助入力として prompt に埋め込み、効率重視モデル・中程度 reasoning・対応する Structured Output schema を指定して返す。

## Read this when
- `cmoc apply fork` の変更要約生成 prompt、AI 呼び出しパラメータ、または作業レポート用の差分要約入力を確認・変更したいとき。
- `cmoc apply fork` が raw な git diff と作業ルートをどのようにエージェント prompt へ渡すかを追いたいとき。
- 変更要約生成で使うモデルクラス、reasoning effort、ファイルアクセスモード、出力 schema の紐付けを確認したいとき。

## Do not read this when
- fork 適用処理そのもの、git 操作、ブランチ作成・削除、または作業ツリー変更の実行ロジックを調べたいとき。
- 生成された変更要約の JSON schema の項目定義だけを確認したいとき。
- `cmoc apply fork` 以外のサブコマンドの prompt やエージェント呼び出し設定を調べたいとき。

## hash
- c68572e71cf2a410fdadf3ea3e8b503be2865fd692e50b280820e7c1b7bb6377

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
- `cmoc apply fork` で、指定されたファイルを起点に work root 内の realization file の要修正点をファイル単位で列挙させるための AI エージェント呼び出しパラメータを構築する。
- 対象ファイルの実パス解決、work root 解決、oracle・realization・apply review standard を含む完全 prompt の組み立て、MAINSTREAM モデルと medium reasoning の read-only 呼び出し設定を担う。
- ファイル単位の所見列挙が下流処理に影響するため、トークン消費が大きくても主流モデルを選ぶ判断が実装内に含まれる。

## Read this when
- `cmoc apply fork` の中で、oracle file または realization file を起点に要修正点リストアップ用のエージェント呼び出しを作る処理を確認・変更したいとき。
- apply fork の所見列挙 prompt に含める role、summary、goal、各種 standard 指定、file access mode の構成を確認したいとき。
- ファイル単位の所見列挙で使うモデルクラス、reasoning effort、structured output schema の対応ファイル選択を確認したいとき。

## Do not read this when
- 所見列挙結果の schema 定義そのものや JSON の項目構造を確認したいだけのとき。
- apply fork 全体の制御フロー、対象ファイル一覧の作成、または複数ファイル分の呼び出し統合処理を確認したいとき。
- prompt 部品の markdown レンダリング、完全 prompt の共通組み立て、パス解決 helper の詳細実装を確認したいとき。

## hash
- a9e787a6c29429e621e2a956781934e6c4cc8cec04713d256e3de4728c3f5b5b

# `finding_application.py`

## Summary
- `cmoc apply fork` で所見対応作業を担当する AI エージェント呼び出しパラメータを組み立てる実装。所見リストを JSON コードブロックとしてプロンプトに埋め込み、realization file 修正用の役割・目標・注意点・標準参照を含む完全プロンプトを生成して返す。

## Read this when
- `cmoc apply fork` が所見に基づく修正作業をエージェントへ依頼する際のプロンプト内容、モデル種別、推論強度、ファイルアクセス権限を確認・変更したいとき。
- 所見本文がどの形式でプロンプトへ渡されるか、また所見を絶対指示ではなく作業ヒントとして扱わせる制御を確認したいとき。
- realization file 修正タスク向けに、oracle と realization の基本事項や realization standard をプロンプトへ含める経路を確認したいとき。

## Do not read this when
- `cmoc apply fork` のサブコマンド全体の分岐、CLI 引数処理、fork 作成・実行・統合など、所見対応プロンプト生成以外の制御を調べたいとき。
- 生成済みプロンプトの Markdown レンダリングや構造化ドキュメント部品そのものの仕様を調べたいとき。
- 個別の所見検出ロジック、レビュー結果の生成、または所見データの保存形式を調べたいとき。

## hash
- 4c29c6bda0f02f6cb59bff5714b079870eb0ddfc88c4cfe538a7ec5b96afe5f3
