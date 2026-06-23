# `cmoc_config.py`

## Summary
- 開発対象リポジトリごとに変わりうる cmoc の挙動設定を集約する設定データクラス群を定義する。
- 永続化される設定の最上位構造、Codex CLI 向けのモデル名・推論 effort 名の対応、`apply fork` と `review oracle` のループ回数上限を扱う。
- 設定値として `ModelClass` や `ReasoningEffort` を Codex CLI が受理できる文字列へ対応づける箇所への入口になる。

## Read this when
- 開発対象リポジトリごとの cmoc 設定項目、既定値、設定データクラスの構造を確認・変更したいとき。
- Codex CLI 呼び出しに使うモデル名または reasoning effort 名の対応を確認・変更したいとき。
- `apply fork` の apply ループや所見リスト改善ループの上限回数を確認・変更したいとき。
- `review oracle` の所見列挙・マージ・検証ループの上限回数を確認・変更したいとき。
- 永続化される config の dataclass 構造や Enum 系設定値の value 化前提に関わる実装を追うとき。

## Do not read this when
- CLI 引数の定義、サブコマンドの実行フロー、または設定値を実際に読み書きする処理だけを調べたいとき。
- `ModelClass` や `ReasoningEffort` 自体の定義・意味を確認したいとき。
- 個別サブコマンドの処理内容や所見リストの生成・改善・検証ロジックを調べたいとき。
- リポジトリルート、作業ディレクトリ、実行ディレクトリなどのパス概念の定義を確認したいとき。

## hash
- ccea2a3965b4022ccab0f635678dd917808b71820431e9e91f76f699315338f6
