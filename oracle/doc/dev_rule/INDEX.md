# `coding_rule.md`

## Summary
- Python 実装全体の書き方を定める正本。命名、型ヒント、import、docstring、コメント、非公開識別子の扱いを確認したいときに読む。

## Read this when
- このリポジトリで Python の新規実装や修正を行うとき
- 既存コードの命名、型ヒント、docstring、コメントの統一方針を確認したいとき
- 循環参照の回避や相対 import の使い方を判断したいとき

## Do not read this when
- このファイルの内容をそのまま実装に写すだけで足りるとき
- 個別モジュールの業務ロジックや CLI 振る舞いを確認したいとき
- 他言語の実装規約やプロジェクト固有の入出力仕様を調べたいとき

## hash
- 5390e60d9b2f0ed11c609a57ddd9f84c963f6e755d6f0e2b4ad714ea219b4974

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
- pytest を使う `cmoc` のテスト実装方針を案内する入口。決定論的な制御ロジックの検証、Real Codex CLI を含む経路での cmoc managed ollama 利用、Fake Codex CLI を使う場合の位置づけを扱う。
- この文書を読むのは、`cmoc` の実装に対応するテストを追加・修正するとき、特に git 状態確認、作業ディレクトリ決定、対象列挙、設定生成、ログ保存、状態更新、エラー処理、CLI 呼び出し周りの結合動作を確認したいとき。
- `cmoc` の自動テストで LLM の回答品質そのものや外部 provider / 有料クラウド backend の正しさを扱う必要があるときは読まない。そうした対象はこの文書の non-goal に含まれないため、別の正本仕様を探す。

## Read this when
- `cmoc` の決定論的な制御ロジックを pytest で検証したいとき。
- Real Codex CLI 呼び出しを含む経路で、prompt 渡し、出力保存、schema 指定、profile 生成など cmoc が責任を持つ結合動作を確認したいとき。
- テストの実行環境を `tmp_path` 配下に構築する必要があるとき。
- Real Codex CLI 呼び出しのテストで cmoc managed ollama を使うべきか、Fake Codex CLI で十分かを判断したいとき。

## Do not read this when
- LLM の回答品質や、Codex CLI に依頼した仕事の意味的な成功を検証したいだけのとき。
- Codex CLI 自体、外部 provider、有料クラウド backend の正しさや安定性を保証したいとき。
- テスト配置やライフサイクルの正本が `cmoc managed ollama` そのものにあると分かっている場合は、この文書ではなく `cmoc managed ollama` の正本仕様を読むべきとき。

## hash
- e8e44f1e9f1d2ea93b2292fde42b9404a2fa58c2c97e92d8a7e3fb2f73fa364f
