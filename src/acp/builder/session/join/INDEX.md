# `conflict_resolution.py`

## Summary
- `cmoc session join` で検出済みの merge conflict marker を解消するため、対象パス一覧を含む AI エージェント呼び出しパラメータを組み立てる実装。
- 作業範囲を conflict marker 解消に限定し、通常は編集不可の oracle file も conflict 解消に必要な最小範囲だけ編集可能にする prompt を生成する。
- work root と実パス解決、完全 prompt 構築、モデル種別・推論強度・ファイルアクセスモード・編集対象パスの設定をまとめて扱う。

## Read this when
- `cmoc session join` の join 処理中に、merge conflict marker 解消用のエージェント呼び出し内容を確認・変更したいとき。
- conflict marker 解消タスクに渡す role、summary、goal、追加ルール、対象ファイル一覧の prompt 文面を調整したいとき。
- conflicted paths を実パスへ解決し、AgentCallParameter の編集対象パスとして渡す流れを確認したいとき。
- merge conflict 解消時だけ oracle file 編集を最小限許可する例外ルールや、git add・git commit を禁止する制御を確認したいとき。

## Do not read this when
- 通常の `cmoc session join` 全体の orchestration、branch 操作、merge 実行、conflict 検出の流れを知りたいだけのとき。
- merge conflict marker を実際に解析・削除するアルゴリズムや、解消後の内容選択ロジックを探しているとき。
- AgentCallParameter、ModelClass、ReasoningEffort、FileAccessMode そのものの定義や共通仕様を確認したいとき。
- complete prompt の共通構築規則、oracle/realization 標準 prompt の詳細、StructDoc の markdown rendering を調べたいとき。

## hash
- d5cf6e98245985065e627071215cb070a4e415d761eabd0420b177e316242b1a
