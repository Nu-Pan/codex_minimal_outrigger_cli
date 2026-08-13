# `oracle`

## Summary
- cmoc の oracle 実装を構成する共通モデル・設定、AI エージェント呼び出しパラメータ、完全 prompt 構築、feedback reporter 入力契約をまとめた領域。用途別の起動定義や prompt 規範、パス解決、構造化文書、設定モデルへ進むための入口。

## Read this when
- AI エージェント呼び出しのモデル、推論強度、ファイルアクセス、cwd、Structured Output、indexing preflight の共通契約を調査・変更するとき。
- agent 向け完全 prompt の構築、placeholder、Standard の合成、パス表現、構造化 Markdown の扱いを確認するとき。
- feedback reporter が collector に渡す入力契約の分類、影響、根拠、継続状態を確認するとき。
- 配下の acp_builder、other、prompt_builder、feedback のどの領域を読むべきか判断するとき。

## Do not read this when
- 特定の用途に固有な prompt、Structured Output、起動パラメータの詳細を直接確認できる場合。
- agent call の実行処理、oracle・realization の個別仕様、collector 側の feedback 保存・集約処理だけを確認したい場合。
- 通常の Markdown 生成や、oracle の共通モデルを利用しない機能の実装詳細だけを調べる場合。

## hash
- 2673ba21cb7014f8bfdcc4e61ff0910696d6f77885c5f888be97030f259f768a
