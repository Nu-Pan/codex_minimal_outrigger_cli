# `coding_rule.md`

## Summary
- Python 実装時のコーディング規則をまとめた正本断片。型ヒント、import の選び方、docstring、コメントの書き方、非公開識別子の付け方など、実装を書く前に参照して命名・構成・記述方針を揃えるために読む。

## Read this when
- Python の新規実装や既存コードの修正で、命名・責務分割・型注釈・docstring・コメントの粒度を合わせたいとき。
- import の書き方、循環参照の避け方、`TYPE_CHECKING` の使いどころを確認したいとき。
- 既存コードをこのリポジトリの記述ルールに合わせて整えたいが、細部の実装方針はまだ決めていないとき。

## Do not read this when
- 実装固有の業務仕様や CLI の振る舞いを知りたいとき。
- 既に対象モジュールの個別設計やエラー処理方針が決まっていて、一般的な記述ルールの確認が不要なとき。
- Python 以外の言語や、仕様そのものの正本断片を探しているとき。

## hash
- 5390e60d9b2f0ed11c609a57ddd9f84c963f6e755d6f0e2b4ad714ea219b4974

# `design_rule.md`

## Summary
- `src/main.py` を読む入口として、CLI の起点と引数解釈だけを担当することを示す。サブコマンド本体はここに置かないため、CLI 全体の配線を確認したいときに進む対象になる。
- `src/sub_commands/<sub command name>.py` を読む入口として、個々のサブコマンドの本命処理を探すときに進む対象になる。`main.py` からの呼び出し先として実装を確認したい場合に読む。
- `src/commons` を読む入口として、複数サブコマンドで共有する共通機能を確認したいときに進む対象になる。単一コマンド固有の処理ではなく、再利用されるユーティリティや定数、共通のエラー処理を探す場合に読む。

## Read this when
- CLI のエントリーポイントや引数解釈の責務分担を確認したいとき。
- 特定のサブコマンドの実処理がどこにあるかを探したいとき。
- 複数のサブコマンドから使う共通部品や共通エラー処理の置き場を探したいとき。

## Do not read this when
- サブコマンド個別の業務処理そのものを知りたいときは、まず対応する `src/sub_commands/<sub command name>.py` を読む。
- CLI 全体の配線ではなく、共有ユーティリティの具体実装を知りたいだけなら `src/commons` 側を直接読む。
- 引数解釈の詳細よりもサブコマンド固有の挙動を見たいだけなら `src/main.py` だけを読んでも足りない。

## hash
- e08b233e78e0aa9ec5de1cc287b99c15f953e430fe3626ef2f73f2f533df6c72

# `development_environment.md`

## Summary
- この文書は、`cmoc` 開発時の作業環境の前提と、Python 仮想環境の作成・利用・依存追加の手順をまとめたもの。環境差で判断がぶれやすい事項だけを押さえ、実作業の前提確認に使う。
- 扱うのは、エンコード規約、命名規則、Python 実行環境の固定、`/.venv` の管理方法。実装仕様や個別機能の説明はここでは扱わない。

## Read this when
- このリポジトリをどういう環境で触るかを確認したいとき。
- Python の実行方法、仮想環境の作成、パッケージ追加手順を確認したいとき。
- ファイル名や文字コードの扱いを環境基準で確認したいとき。

## Do not read this when
- 個別機能の仕様や実装方針を知りたいとき。
- サブコマンドやコード構成の詳細を探したいとき。
- 既存の命名や作業ルールの背景説明だけが欲しいとき。

## hash
- d1371e90d6e441b3470b215a3f421f05b6c6fec889700442a191f677de0c81b1

# `test_rule.md`

## Summary
- cmoc の pytest ベースの realization test を書くときに読む入口。決定論的な制御ロジックの検証方針、Real Codex CLI 経路で cmoc managed ollama を使う条件、Fake Codex CLI を使ってよい条件をまとめる。
- この規約は、テストの目的を「cmoc が責任を持つ結合動作と制御ロジックの検証」に絞り、LLM の回答品質や外部 provider 自体の正しさを目的外とする境界を明示する。
- テスト実行時の隔離範囲、共有してよい cmoc managed ollama の扱い、テスト用 SLM、クラウド課金モデル禁止の条件もここで確認する。

## Read this when
- cmoc の `test` 配下に realization test を追加・修正するとき。
- git 状態、作業ディレクトリ、対象ファイル列挙、設定生成、ログ保存、状態更新、エラー処理などの決定論的挙動を検証したいとき。
- Real Codex CLI 呼び出しを含むテストで、cmoc managed ollama を使うべきか Fake Codex CLI で足りるか判断したいとき。
- テスト実行環境を `tmp_path` 上にどう隔離するか、どこまでを共有してよいか確認したいとき。

## Do not read this when
- LLM の回答品質そのものを評価したいだけのとき。
- Codex CLI 自体、外部 provider、課金クラウド backend の正しさや安定性を保証する目的のとき。
- cmoc managed ollama の管理・配置・ライフサイクルの詳細だけを知りたいときは、別の正本仕様を読むべきとき。
- realization test ではなく実装本体や oracle 側の仕様を編集するとき。

## hash
- e8e44f1e9f1d2ea93b2292fde42b9404a2fa58c2c97e92d8a7e3fb2f73fa364f
