# `change_summary.json`

## Summary
- 差分全体を意味ごとの変更カテゴリに分け、人間向けの要約と主要な変更箇所を記録するための構造を定める。
- 変更の網羅一覧ではなく、要約の根拠として有用な主要箇所を添えて、レビューや報告で変更意図を把握しやすくするための出力契約を扱う。

## Read this when
- fork 適用後の差分を、人間が読める変更カテゴリ別サマリーとして出力・検証する処理を実装または確認するとき。
- 変更カテゴリ、変更内容の説明、主要な変更箇所の対応関係について、出力互換性を固定したいとき。
- 差分要約が空でない前提や、詳細な変更一覧ではなく主要箇所を選ぶ方針を確認したいとき。

## Do not read this when
- 個別ファイルのパッチ内容そのもの、diff 生成手順、または git 操作の仕様を確認したいとき。
- fork の作成・適用・分岐制御など、差分要約の出力契約より前後の実行フローを調べたいとき。
- ルーティング文書、テスト、実装などの変更種別ごとの具体的な判定ロジックを探しているとき。

## hash
- 51ffe6e61588c7c347494a36267c02b8d48f69f6e264fcaf396096938cdd672d

# `change_summary.py`

## Summary
- `cmoc apply fork` の作業レポート向けに、適用対象ブランチ上の生の差分を人間向け変更要約へ変換させる AI 呼び出しパラメータを組み立てる正本実装。
- 差分テキストを入力として、読み取り専用の完全 prompt、効率モデル、中程度推論、Structured Output schema への参照を持つ呼び出し設定を生成する。

## Read this when
- `cmoc apply fork` が生成する作業レポートの変更要約 prompt の役割、入力差分の扱い、または AI 呼び出しパラメータを確認したいとき。
- 適用対象ブランチ上の `git diff` 出力を、解析・整形せず prompt に埋め込む仕様を確認したいとき。
- 変更要約生成で使うモデル種別、推論強度、ファイルアクセス権限、出力 schema の決め方を確認したいとき。

## Do not read this when
- `cmoc apply fork` の fork 作成、branch 操作、差分取得、または実際の適用処理を調べたいとき。
- 変更要約の Structured Output schema 自体の項目定義を確認したいとき。
- 完全 prompt の共通部品、path 語彙、または基本的な AgentCallParameter 型の定義を調べたいとき。

## hash
- e67af8eaca19963295dc8e237d26d5d2619001f6757af6a00da778a4cbccc002

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
- `cmoc apply fork` で、指定された oracle file または realization file を起点に、関連する正本仕様断片と実装を読みながら realization file の要修正点をファイル単位で列挙するための AI エージェント呼び出しパラメータを構築する正本実装。
- 読み取り専用モードで complete prompt を組み立て、oracle standard、realization standard、apply review standard を適用した所見リストアップを MAINSTREAM モデルと MEDIUM 推論で実行させる入口を定めている。
- 起点パスを実パスへ解決し、リポジトリルート内の調査範囲を prompt に埋め込み、呼び出し結果の Structured Output schema を対応する JSON 定義へ結びつける。

## Read this when
- `cmoc apply fork` がファイル単位で realization file の要修正点を列挙するエージェント呼び出しをどう構成するか確認したいとき。
- apply review standard を満たす所見リストアップ用 prompt に、oracle file、realization file、起点パス、リポジトリルートをどう渡すか調べたいとき。
- ファイル単位の所見列挙で使うモデルクラス、推論努力、読み取り専用アクセス、Structured Output schema の紐づけを確認したいとき。

## Do not read this when
- `cmoc apply fork` の所見列挙結果を統合したり、修正適用全体の制御フローを確認したいだけのとき。
- oracle standard、realization standard、apply review standard の中身そのものを読みたいとき。
- 個別の realization file を実際に修正する実装や、所見リストの schema 定義そのものを確認したいとき。

## hash
- 8c27e836c8957d364dacd591645166d9aa1b00ef081fc85e523add1c6a97963d

# `finding_application.py`

## Summary
- `cmoc apply fork` で検出済み所見に対応する修正作業を AI エージェントへ依頼するための呼び出しパラメータを構築する正本実装。所見リストを JSON コードブロックとしてプロンプトへ埋め込み、realization file の修正、realization standard 準拠、git add/commit 禁止などの作業条件を含む完全プロンプトを生成する。
- モデル種別、推論努力量、ファイルアクセスモード、生成済みプロンプト本文をまとめた `AgentCallParameter` を返す責務を持つ。

## Read this when
- `cmoc apply fork` が所見対応作業用エージェントをどの role・goal・注意事項で呼び出すかを確認または変更したいとき。
- 所見本文の渡し方、複数所見のプロンプト内表現、JSON コードブロック化の扱いを確認したいとき。
- 所見対応作業に与えるファイルアクセス権、モデルクラス、推論努力量、realization standard 指示の有無を確認したいとき。
- `cmoc apply fork` の修正担当エージェントに、oracle/realization 基本情報や realization standard を含めるかどうかを扱うとき。

## Do not read this when
- `cmoc apply fork` 全体の CLI 引数解析、サブコマンド登録、実行フローを確認したいだけのとき。
- 所見そのものを生成・検出・レビューする処理を探しているとき。
- 実際に realization file を修正するエージェント側の作業手順や修正ロジックを探しているとき。
- 共通の完全プロンプト生成処理や `AgentCallParameter` の型定義そのものを確認したいとき。

## hash
- 61fdb8a4dc76cc84716908dffb8d88e88ff5636b58d7589e4c6abfb89d52d93a
