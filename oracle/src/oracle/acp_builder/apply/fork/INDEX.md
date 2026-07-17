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
- `cmoc apply fork` の変更要約生成を組み立てる正本。差分テキストを人間向けの要約入力に変換し、変更レポート用の AI 呼び出しパラメータを返す。
- 同じ `apply fork` 配下でも、所見の列挙や所見への対応ではなく、変更内容の要約を作りたいときに読む。

## Read this when
- `cmoc apply fork` の作業結果を短い要約として出したいとき。
- git 差分をそのまま AI に渡す変更要約用の入力構築を確認したいとき。
- 変更レポート側のエージェント設定や出力先を確認したいとき。

## Do not read this when
- ファイル単位で所見を洗い出したいときは、所見列挙側を読む。
- 見つかった所見に基づいて realization file を修正したいときは、所見対応側を読む。
- 差分そのものの取得方法や生成元を探したいときは、このファイルではなく差分生成側を読む。

## hash
- d1dce570eba6c646ae3efc703b2aa2799a96003b4c97a5a8de1eb5aa58758022

# `file_review_and_fix.json`

## Summary
- 対象の正本スキーマに対応する realization 実装と呼び出し経路を確認した。

## Read this when
- 対象のファイル単位レビュー・修正 agent call の実装経路を調査するとき。

## Do not read this when
- ファイル単位レビュー・修正機能と無関係な apply 処理を調査するとき。

## hash
- 1b2dc00d6fd4ade1aa06b4235d979929db87f61f1f03d05c718b447b63143c9f

# `file_review_and_fix.py`

## Summary
- `cmoc apply fork` のファイル単位レビュー・修正用 AgentCallParameter を構築する oracle src。対象ファイルを起点とした調査・修正・検証を行う完全な作業 prompt と、効率モデル・最大推論・realization write モード・出力スキーマを定義する。apply fork のファイルレビュー処理や、その prompt 構成を確認する入口。

## Read this when
- `cmoc apply fork` のファイル単位レビュー・修正処理を変更・調査するとき
- レビュー用 prompt、対象ファイルの調査範囲、修正後検証、AgentCall のモデルやアクセスモードを確認するとき
- この処理に対応する出力スキーマや prompt builder との接続を追うとき

## Do not read this when
- `cmoc apply fork` 以外のサブコマンドのレビュー処理を調査するとき
- レビュー対象の具体的な realization 実装やテストの内容を直接確認したいとき
- 共通 prompt builder、パス解決、構造化文書の実装詳細だけを調査するとき

## hash
- cb0046860a9a7db5db44e39499c58eae66cb7e688d16aa19b841ebc1ec855200
