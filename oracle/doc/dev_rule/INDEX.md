# `coding_rule.md`

## Summary

- cmoc の Python 実装における基本的なコーディング規則を定義している。
- PEP 8、明確な命名・責務・入出力、最小限の変更、適切なコメントと NOTE コメントの使い方を定めている。
- 型ヒント必須、Any の抑制、from __future__ import annotations の禁止を定めている。
- src をルートとした import 前提、可能な限り相対 import を使う方針、循環参照回避と TYPE_CHECKING 使用条件を定めている。
- 関数・クラスの Google style docstring、コメントは基本日本語、ログメッセージは英語、非公開識別子は先頭アンダースコアとする規則を定めている。

## Read this when

- cmoc の src 配下に Python コードを実装・修正するとき。
- 型ヒント、import、docstring、コメント、ログメッセージ、非公開識別子の書き方を確認したいとき。
- 実装方針が過剰設計になっていないか、または既存の開発ルールに合っているか確認したいとき。
- コードレビューやテスト追加時に、cmoc のコーディングスタイル上の期待値を確認したいとき。

## Do not read this when

- cmoc のユーザー向け CLI 仕様、サブコマンド仕様、ワークフロー仕様だけを調べたいとき。
- 開発環境のセットアップ、実行方法、テストコマンドなどの環境情報だけを調べたいとき。
- アーキテクチャや設計判断など、コードスタイル以外の設計ルールを調べたいとき。
- README や AGENTS など、リポジトリ全体の運用ルールやファイルアクセス規則だけを確認したいとき。

## hash

- dd1b5890cf9682753d5854bd2e45baf97a54534fbb194bb7dd5867965d6b0c21

# `design_rule.md`

## Summary

- cmoc のコード設計方針をまとめた文書である。
- CLI 実装は typer を前提にし、エントリーポイントと引数解釈は `<cmoc-root>/src/main.py`、各サブコマンド本体は `<cmoc-root>/src/sub_commands/<sub command name>.py` に置く。
- 共有機能は `<cmoc-root>/src/commons` に置き、関数分割は許容しつつ caller first, callee last を基本とする。

## Read this when

- cmoc の CLI エントリーポイントや引数解釈の配置を決めたいとき。
- `<cmoc-root>/src/main.py`、`<cmoc-root>/src/sub_commands`、`<cmoc-root>/src/commons` の役割分担を確認したいとき。
- 新しいサブコマンドの追加や既存サブコマンド本体の置き場所を判断したいとき。
- 共通ユーティリティ、定数、エラー処理の配置方針を確認したいとき。
- 関数分割の粒度や caller first, callee last の並び順を確認したいとき。

## Do not read this when

- cmoc のユーザー向けコマンド仕様やワークフローだけを確認したいとき。
- 開発環境、依存関係、テスト実行方法など、設計以外のルールを確認したいとき。
- コーディング規約やファイルアクセス規則など、設計方針そのもの以外を確認したいとき。

## hash

- 9072b8512b6671c4550343f461a7c411d7066a9cb5f83108766055e822dff9c5

# `development_environment.md`

## Summary

- cmoc 開発で使う標準環境、ファイルエンコード、Python 実行環境、仮想環境管理の方針を扱う正本仕様断片です。
- WSL2 Ubuntu 24.04 on Windows 11、VS Code Remote Development、指定 workspace、Codex CLI 利用可能環境を前提にします。
- UTF-8 BOM なしの統一、python3>=3.12.3、<cmoc-root>/.venv の使用、pip の実行方法、依存追加時の手順を定めます。

## Read this when

- cmoc の開発環境、前提 OS、エディタ、workspace、Codex CLI 利用前提を確認したいとき。
- Python コマンド、pip コマンド、仮想環境の場所、システム Python の使用可否を判断したいとき。
- .venv を新規作成するとき、.venv に cmoc をインストールするとき、新しい Python 依存パッケージを追加するとき。
- ファイル作成・編集時の文字コード方針を確認したいとき。

## Do not read this when

- cmoc のサブコマンド仕様やワークフロー仕様だけを確認したいとき。
- 実装方針、設計ルール、コーディング規約、テスト規約など、開発環境以外の規約を確認したいとき。
- README、AGENTS、oracle の編集可否やリポジトリ全体のファイルアクセス規則を確認したいとき。

## hash

- f16b03a2822239e136bc0c19443a3e27d8dfed094b641ed574599dd0a950698f

# `test_rule.md`

## Summary

- cmoc のテスト実装規約を定義している。
- pytest を使用し、テストは `<cmoc-root>/test` に実装する。
- 正規の Codex CLI の正常動作に依存するテストは禁止し、Fake Codex CLI を使うテストは許可する。
- cmoc の決定論的な制御ロジックを仕様どおり検証することをテスト目的とする。
- Codex CLI や LLM 自体の挙動や出力品質は自動テストの対象外とする。

## Read this when

- cmoc の自動テストを追加・修正するとき。
- テスト対象を cmoc の制御ロジックにするべきか、Codex CLI や LLM の挙動にするべきか判断したいとき。
- Fake Codex CLI を使ったテスト設計の可否を確認したいとき。
- pytest や `<cmoc-root>/test` に関するテスト配置ルールを確認したいとき。

## Do not read this when

- cmoc の CLI 仕様、サブコマンド仕様、ワークフロー仕様だけを確認したいとき。
- 本体実装のコーディング規約や設計規約を確認したいとき。
- README.md、AGENTS.md、oracle の編集可否など、リポジトリ運用ルールを確認したいとき。
- Codex CLI や LLM の実際の出力品質を評価する手順を探しているとき。

## hash

- e089c0f9f2dc35b7d188a96f58e35da3501bd049dc23499439995b5dffce31ae
