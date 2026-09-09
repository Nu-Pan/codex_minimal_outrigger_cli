
# cmoc コード設計

## CLI まわり

- CLI は typer で実装する
- エントリーポイントから引数解釈までを `{{cmoc-root}}/src/main.py` で実装する
- 各サブコマンドの本命処理は `{{cmoc-root}}/src/sub_commands/{{sub command name}}.py` で実装する
- 例：
    - `cmoc session fork` は `{{cmoc-root}}/src/sub_commands/session/fork.py` に関数 `cmoc_session_fork_impl` として実装する
    - `{{cmoc-root}}/src/main.py` で typer の `cmoc session fork` に対応する関数は、`cmoc_session_fork_impl` の呼び出しだけを行う

## 共通系

- 各サブコマンドで共通して使用する機能は、`{{cmoc-root}}/src/commons` 配下に実装する
- 例：
    - 文字列処理のユーティリティ関数
    - 定数定義
    - エラー処理系
    - ...
