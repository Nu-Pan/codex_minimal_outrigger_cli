# `change_summary.json`

## Summary
- 変更要約生成エージェントの構造化出力スキーマを定義し、変更内容をカテゴリ別の要約と根拠ファイル一覧として返せるようにする。

## Read this when
- refactor fork の変更要約出力形式や、要約結果の検証項目を確認するとき

## Do not read this when
- ファイル単位レビュー・修正の出力形式を確認したいときは、対応するレビュー用スキーマを直接読む

## hash
- dc922a0d0f2d939d57f9fe06e94599cbe8166bdbfd52c2ff17cd5c65882b6eda

# `change_summary.py`

## Summary
- refactor fork の作業差分を人間向けに要約する AgentCallParameter を構築する正本実装。差分を補助入力として prompt、読み取り専用の実行条件、効率重視のモデル設定、Structured Output schema の参照先をまとめる。

## Read this when
- refactor fork の変更差分を要約する prompt 構築処理や、その AgentCallParameter の実行条件を確認・変更するとき。

## Do not read this when
- refactor fork の変更内容そのものや要約結果の形式だけを確認したいとき。差分入力や Structured Output schema の定義を直接確認する場合は、対応する入力元・schema を読む。

## hash
- af7d317b4f642b2960d33444e913d1f38c4f4a6e05ecc93c5f2844e52253b36a

# `file_review_and_fix.json`

## Summary
- ファイル単位のレビュー・修正処理が発見した所見と、その対応結果を構造化して返すための出力契約を定義する。各所見について、根拠、関連する oracle 要求、実装状況、理由、解決状態、検証結果を記録する。

## Read this when
- ファイル単位レビュー・修正処理の Structured Output 形式を確認または変更するとき。
- 所見の根拠、修正対象、修正結果の表現方法を確認するとき。

## Do not read this when
- レビュー・修正処理のプロンプト本文や実行パラメータを確認したいときは、対応する実装ファイルを直接読む。
- 変更内容だけの要約形式を確認したいときは、兄弟の変更要約用スキーマを読む。

## hash
- df89b1e212bb8ea23fe6670447bc23f1f86a5116fe16c85fbec6027508dd3fff

# `file_review_and_fix.py`

## Summary
- ファイル単位の realization レビュー・修正を行う agent call parameter を構築する。対象ファイルを起点に必要な oracle・realization を調査し、所見対応、再調査、検証までを促す完全な prompt を生成する。
- レビュー対象の作業ディレクトリ、realization への書き込み権限、最大推論設定、構造化出力 schema、indexing preflight を含む実行パラメータを返す。

## Read this when
- ファイル単位の realization レビュー・修正用 agent call の prompt 構成や実行パラメータを確認・変更するとき。
- 対象ファイルを起点とした oracle・realization 調査、修正、検証の責務を確認するとき。

## Do not read this when
- INDEX.md のルーティング内容だけを確認したいとき。
- 個別の realization 実装やテストの挙動を直接調査・変更するとき。

## hash
- c88423754c117cbc4be781a31ec5d63b66bb1b3b042f179dfca6fc60caa6390a
