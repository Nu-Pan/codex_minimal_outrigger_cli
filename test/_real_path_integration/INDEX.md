# `sitecustomize.py`

## Summary
- 実経路統合テストの subprocess 専用の Python 起動時フック。対象ディレクトリを PYTHONPATH に加えた場合のみ、AgentCallParameter のモデル種別と推論強度をテスト用の最小・低設定へ上書きする。

## Read this when
- 実経路統合テストの subprocess でモデル設定がどのようにテスト専用値へ変更されるか確認するとき
- sitecustomize による AgentCallParameter の初期化差し替えや、実経路統合テストの実行環境を調査するとき

## Do not read this when
- 通常の AgentCallParameter のモデル設定や builder の実装を確認するときは、basic.acp または builder の実装を直接読む
- 実経路統合テスト以外の subprocess 起動設定や、テストケースの期待動作を調査するとき

## hash
- 6d7489648f9840d3b97de6fd9d74e5408a172504727844b0ede6e65379e8a8f0
