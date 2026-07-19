# `coding_rule.md`

## Summary
- Python実装時のコーディング規則を定める正本断片。型ヒント、import 方針、docstring、コメント、命名、非公開識別子の付け方など、実装やレビューの基準を確認したいときに読む。

## Read this when
- `cmoc` の Python 実装方針を決めるとき。
- 型ヒント、import、docstring、コメント、命名規則の解釈を確認したいとき。
- 新規コードや既存コードの書き方を、このリポジトリの規則に合わせて揃えたいとき。

## Do not read this when
- 機能仕様や挙動仕様を確認したいときは、対象機能の oracle doc を直接読む。
- この規則の要約ではなく、個別モジュールの実装詳細を知りたいときは、そのモジュール本文を読む。
- INDEX.md の読み方やルーティング方針そのものを確認したいときは、別の routing 文書を読む。

## hash
- c725d18b649ce36fdca432bb297452492eea1bca900c874e600451769d21d501

# `design_rule.md`

## Summary
- cmoc の CLI 構成と共通モジュール配置の方針を定める。エントリーポイント、サブコマンド本体、`src/commons` に置く共有処理の境界を確認したいときに読む。

## Read this when
- `src/main.py` と各サブコマンド実装の責務分担を決めたいとき
- サブコマンド間で共有する処理をどこに置くか判断したいとき
- CLI の実装配置方針を確認したいとき

## Do not read this when
- Python の文法、型ヒント、docstring、コメントの書き方を確認したいときは `dev_rule/coding_rule.md` を読む
- テストの目的や配置方針を確認したいときは `dev_rule/test_rule.md` を読む
- CLI の挙動や出力内容そのものの正本仕様を確認したいときは `app_spec` 配下を読む

## hash
- e08b233e78e0aa9ec5de1cc287b99c15f953e430fe3626ef2f73f2f533df6c72

# `development_environment.md`

## Summary
- WSL2 の VS Code + Codex CLI 前提で、このリポジトリを作業できる環境条件と Python/venv の運用ルールを案内する。
- `python3` の直接使用を避けて `.venv/bin/python` と `pip -e .` を使う必要がある作業や、新規パッケージ追加の手順を確認するときに読む。
- ファイル命名やエンコードの制約を確認したいときに読む。

## Read this when
- このリポジトリをローカルで開く前提条件や、Codex CLI を使う実行環境を確認したい。
- Python 3.12.3 以上、仮想環境の場所、`pip` の実行方法など、開発時の環境運用ルールを確認したい。
- 新しい依存を `pyproject.toml` に追加して仮想環境へ入れる手順を確認したい。
- ファイル名の付け方や UTF-8 BOM なし運用の制約を確認したい。

## Do not read this when
- 個別の機能仕様、コマンド仕様、実装方針を知りたい場合は、より直接の oracle doc を読む。
- 既存の `INDEX.md` のルーティングだけを更新したい場合は、この文書ではなく対象階層の案内先を探す。
- README だけで足りる一般的な利用方法を知りたい場合は、この環境ルール文書は不要。

## hash
- d1371e90d6e441b3470b215a3f421f05b6c6fec889700442a191f677de0c81b1

# `test_rule.md`

## Summary
- pytest による cmoc realization test の実装・検証規約。決定論的な制御ロジック、Real Codex CLI と cmoc managed ollama を使う結合動作、全公開サブコマンドの本番経路試験、テスト隔離、クラウドバックエンド禁止、Fake Codex CLI の利用条件を定める。

## Read this when
- pytest の実装・実行方法、テスト対象や検証範囲を判断するとき
- realization implementation または realization test の変更後に必要な検証を確認するとき
- Real Codex CLI、cmoc managed ollama、テスト用 SLM、テスト隔離の扱いを確認するとき
- 全サブコマンドの本番経路試験を追加・更新・実行するとき

## Do not read this when
- 実装配置や CLI の責務境界だけを判断する場合は design_rule.md を読む
- Python の実行環境や依存関係の構築方法だけを確認する場合は development_environment.md を読む
- LLM の回答品質や Codex CLI 自体、外部 provider の正しさを検証する場合

## hash
- 9e396e4172f615134632e49b6cae88c875c59f7e20ccebf24c7a478ec7aadd66
