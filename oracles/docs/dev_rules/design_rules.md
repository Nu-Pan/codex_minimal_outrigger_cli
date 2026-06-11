
# cmoc コード設計

## CLI まわり

- CLI 関係は typer で実装する
- エントリーポイント・引数解釈までは `<cmoc-root>/src/main.py` で実装する
- 各サブコマンドの本命処理は `<cmoc-root>/src/sub_commands/<sub command name>.py` で実装する
- e.g.
    - `cmoc session fork` は `<cmoc-root>/src/sub_commands/session/fork.py` に関数 `cmoc_session_fork_impl` として実装する
    - 「`<cmoc-root>/src/main.py` 上の　typer 的に `cmoc session fork` と対応する関数」は「関数 `cmoc_session_fork_impl`」の呼び出しだけを行う

## 共通系

- 各サブコマンド実装で共通して使用するような機能は `<cmoc-root>/src/commons` 配下に実装する
- e.g.
    - 文字列処理のユーティリティ関数
    - 定数定義
    - エラー処理系
    - ...
