# `cmoc_config.py`

## Summary
- cmoc のリポジトリ単位設定を表す dataclass 群を定義し、AI 呼び出し並列数、Codex CLI 向けモデル・reasoning effort 対応、apply fork と review oracle のループ上限などを集約する。
- 設定は開発対象リポジトリごとに変わりうる値として扱われ、永続化時には Enum 系の値を JSON 向けの value に変換する前提を持つ。

## Read this when
- リポジトリごとに永続化される cmoc 設定の項目、既定値、責務境界を確認したいとき。
- Codex CLI に渡すモデル名や reasoning effort 名と、内部の ModelClass・ReasoningEffort との対応を確認または変更したいとき。
- AI エージェント呼び出しの最大並列数、apply fork の処理ファイル数上限、review oracle の所見列挙・マージ・検証ループ上限を確認または変更したいとき。
- 設定 JSON の生成・同期・人間編集を前提に、どの値が利用者調整可能な設定として集約されているかを把握したいとき。

## Do not read this when
- 設定ファイルを実際に読み書きする処理、JSON 変換処理、init 時の生成・同期手順を確認したいとき。
- ModelClass や ReasoningEffort そのものの定義、意味、列挙値を確認したいとき。
- 各サブコマンドの実行ロジック、ループ処理の実装、所見生成や apply fork の詳細挙動を追いたいとき。
- cmoc 全体のパス語彙や repo-root・work-root などの定義を確認したいとき。

## hash
- d102ed1e07a4c9a7241b4e731ec3783b392d8dfb274e702c452dbf9c6b387dc6
