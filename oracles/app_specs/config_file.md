
# cmoc 設定ファイル

- cmoc の挙動に関するパラメータ (e.g. Codex CLI 出力のパース失敗時のリトライ回数) は、可能な限り設定ファイル経由でユーザーからカスタマイズ可能なものとする
- 設定ファイルの配置先は `<repo-root>/comconfig.json` とする
- `<repo-root>/comconfig.json` は python コード上では専用のクラス `CMOConfig` でラップすることとする
- `CMOConfig` の初期化のタイミングで…
    - `<repo-root>/comconfig.json` が存在しなければ作成する
    - `<repo-root>/comconfig.json` と `CMOConfig` の想定とで、パラメータの過不足がある場合…
        - `<repo-root>/comconfig.json` 側の過剰パラメータは削除する
        - `<repo-root>/comconfig.json` 側の不足パラメータはデフォルト値で追加する
    - `<repo-root>/comconfig.json` からパラメータを読み出してメモリ上にキャッシュする
- `CMOConfig` は各パラメータを `property` として公開する
- `cmoc init` を始めとする各サブコマンドによってデフォルト値でフィルされた `<repo-root>/comconfig.json` が生成され、それをユーザーが編集するフローを想定する
