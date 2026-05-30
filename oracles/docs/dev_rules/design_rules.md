
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

## 処理の関数分割

- 処理の関数分割・構造化は基本的には好ましい
- ただし「１箇所からしか呼ばれていない関数」はあまり好ましくない
    - 関数化する明確な目的（e.g. 別の関数に関数を渡す）がある場合は良しとする
    - なんとなく分割されているようなものであれば、その呼出を展開して caller が縦に長くなる方が好ましい
- また、１つのファイル内で呼び出し・被呼び出しの関係にある関数の並び順は caller first, callee last にすること

