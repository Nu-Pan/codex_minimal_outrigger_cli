# `cmoc_config.py`

## Summary
- cmoc のリポジトリ単位設定を表す dataclass 群を定義し、並列実行数、Codex CLI 向けモデル・reasoning effort 対応、apply fork と eval-oracle のループ上限などの既定値を集約する。
- 設定値として enum 系のキーを含む構造を持ち、永続化時には enum インスタンスを value 化する前提の設定モデルを扱う入口である。

## Read this when
- リポジトリ単位の cmoc 設定項目、既定値、設定 dataclass の構造を確認・変更したいとき。
- Codex CLI に渡すモデル名や reasoning effort 名と、cmoc 内部の分類 enum との対応を確認・変更したいとき。
- apply fork や eval-oracle の処理回数・処理件数の上限など、サブコマンド挙動を設定で調整する箇所を探しているとき。
- 設定を永続化・同期する処理で、どの値が設定モデルに含まれるか、enum を JSON 化する際にどのような構造を想定しているかを確認したいとき。

## Do not read this when
- 設定ファイルの読み書き、JSON 変換、同期、初期化コマンドの実装手順そのものを確認したいだけのとき。
- CLI サブコマンドの実行フロー、プロンプト生成、外部プロセス呼び出し、評価ロジック本体を調べたいとき。
- path token、作業ツリー、リポジトリルートなどのパス概念の定義を確認したいとき。
- 設定値ではなく、ModelClass や ReasoningEffort 自体の定義や分類意味を確認したいとき。

## hash
- 498fb29ac9726ad974520ed9d7942f48f7b715756d9ce9f24bb95cf9dc164fd3
