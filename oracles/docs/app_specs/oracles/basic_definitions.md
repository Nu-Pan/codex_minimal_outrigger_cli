## oracles ファイルの基本的な定義

## 「oracles ファイル」の定義

正本仕様中で「oracles ファイル」と言った場合、それは以下の条件をすべて満たしたファイルの事を指す

- `<work-root>/oracles` 配下である（サブディレクトリを含む）
- `<work-root>/.gitignore` の対象ではない
- `INDEX.md` ではない

## oracles ファイルの役割

- oracles ファイルは人間が所有し 100% の責任を負う正本仕様断片である
- oracles ファイルの内容について AI は提案を行うことは出来るが、実際の編集を行うのは必ず人間である
- oracles を正本仕様として実装が生成されるものとし、その逆は禁止である

## oracles ファイルの構成

- `<work-root>/oracles` 配下にはサブディレクトリを作成しても良い
- 具体的にどのようなサブディレクトリを作成するかは cmoc としては制限をしない
- 典型的には以下のような構成を想定する
    - `<work-root>/oracles/docs`: 自然言語の markdown ドキュメント形式で仕様断片を記述する
    - `<work-root>/oracles/schema`: 入出力・ステートなどの構造を定義するスキーマを記述する
    - `<work-root>/oracles/src`: ソースコードを配置する
    - `<work-root>/oracles/tests`: 

## oracles ファイルと Codex CLI による読み書き

- Codex CLI は oracles ファイルを読んで良いが、書き換えてはいけない
- Codex CLI は `<work-root>/oracles` 配下の非 oracles ファイル (e.g. `INDEX.md`) を読み書きして良い

## Codex CLI 実行後の oracles 検査規則

- Codex CLI の workspace-write 実行後、cmoc は以下のことを検査する
    - oracles ファイルに未コミット差分がないこと
    - Codex CLI 実行前 HEAD から実行後 HEAD までの commit range に oracles ファイルの変更がない事
- 検査の結果、差分・変更が見つかった場合、cmoc はの場でコマンドを失敗させる
- この検査は、仕様上明記された例外ケースにおいてのみ、無効化できる
