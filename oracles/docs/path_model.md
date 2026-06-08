
# Path model

## パス表記の基本ルール

- cmoc 上では、ファイル・ディレクトリパスを絶対パス・相対パスどちらで書いても良い
- 相対パスを書く時は、そのルートディレクトリパスを `<root-token>/relative/path/to/file` のように、ルートトークン＋相対パスの形式で表記する
- `src/foo.py` のようなルートトークンを持たない相対パスでの表記は禁止

## ルートトークン一覧

- `<cmoc-root>`
    - cmoc 自体のリポジトリのルートディレクトリ
    - cmoc 自体のソースコード・ドキュメントを指す時に使う
- `<repo-root>`
    - cmoc を用いた開発を行う対象となる git リポジトリの main worktree のルートディレクトリ
    - より平易に git リポジトリ本体のルートディレクトリとも言える
    - 直下に `.git` ディレクトリを持つ
- `<run-root>`
    - cmoc が run の隔離作業用に作る linked worktree のルートを指す
    - 直下に `.git` ファイルを持つ
- `<work-root>`
    - ユーザーが cmoc を呼び出した cwd から最近傍の `.git` ディレクトリ・ファイルで解決される worktree root
    - 直下に `.git` ディレクトリ・ファイルを持つ

## パスの表記例

- ユーザーは `<repo-root>` をカレントとして `<cmoc-root>/bin/cmoc` を呼び出す
- `cmoc apply fork` は `<repo-root>` を pwd として呼び出されて、 run の作業隔離のために `<run-root>` を git linked worktree として作成する
- run の作業隔離のための linked worktree は `<repo-root>` 内に作成されるから、「`<repo-root>` のフルパス」は「`<run-root>` のフルパス」の部分文字列となる
- `<run-root>` 内で cmoc を起動した場合 `<run-root>` と同値
- `<run-root>` 外の `<repo-root>` 内で cmoc を起動した場合 `<repo-root>` と同値
