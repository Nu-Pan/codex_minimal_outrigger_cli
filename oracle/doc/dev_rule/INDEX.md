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
- この環境で作業するときの基準をまとめた文書。WSL2 上の開発環境、エンコード規約、命名規則、Python 実行環境の前提を確認したい場合に読む。
- 自己開発のための Python 環境確認、仮想環境作成、依存導入、検証コマンドの実行手順を決めるときに読む。実行手順の細部は別の正本にあるので、この文書ではそこへの入口だけを持つ。

## Read this when
- cmoc の開発環境前提や Python 実行方法を確認したいとき。
- 新しい補助ファイル名やディレクトリ名を決める前に、このリポジトリの命名基準を確認したいとき。
- 自己開発用の環境構築や検証手順の正本を探したいとき。

## Do not read this when
- 個別機能の仕様や実装方針を知りたいときは、各機能の oracle 文書を読む。
- 既に開発環境や Python 実行環境の前提を把握していて、別の具体的な作業手順だけを探しているとき。
- `INDEX.md` のルーティング情報だけを更新したいときは、この本文ではなく対象階層の案内をたどる。

## hash
- 8f3c3590f973ea4bc2e2efd00de2ef5f515bc421eb4c5d6624783a9d5f1a714b

# `test_rule.md`

## Summary
- 自己開発時の検証手順と、cmoc managed Ollama の管理・配置・設定注入の正本をまとめたルーティング文書。ここでは実装詳細ではなく、どの仕様断片を読むべきかを案内する。

## Read this when
- cmoc 自身の開発で、テスト実装や focused test、full validation、静的検査、環境隔離、Fake / Real Codex CLI の使い分け、検証結果の報告手順を確認したいとき。
- cmoc managed Ollama の管理主体、ライフサイクル、配置先、可用性、Codex CLI への設定注入について確認したいとき。

## Do not read this when
- cmoc の通常機能や個別コマンドの実装を知りたいときは、より直接の実装・仕様断片を読む。
- 検証手順の詳細な運用例や個別テスト内容だけを探しているときは、この案内ではなく該当する下位の正文を読む。

## hash
- ec6f14f187deda3072f7ecbaeead70cebbc97bf48e6f30da1201ed8c9cbfe7da
