# cmoc コード設計

## CLI まわり

CLI は Typer で実装し、エントリーポイントから引数解釈までを `{{cmoc-root}}/src/main.py` が担う。各サブコマンドの本命処理は、`{{cmoc-root}}/src/sub_commands/{{sub command name}}.py` に分ける。

例えば、`cmoc session fork` の本命処理は、`{{cmoc-root}}/src/sub_commands/session/fork.py` に関数 `cmoc_session_fork_impl` として実装する。`{{cmoc-root}}/src/main.py` の対応する Typer 関数は、`cmoc_session_fork_impl` の呼び出しだけを行う。

## 共通系

複数のサブコマンドで共通して使用する機能は、`{{cmoc-root}}/src/commons` 配下に実装する。例えば、文字列処理のユーティリティ関数、定数定義、エラー処理系などが該当する。
