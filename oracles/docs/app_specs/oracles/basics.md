## oracles 基本情報

## oracles files の定義

正本仕様中で「oracles files 」と言った場合、それは以下の条件をすべて満たしたファイルの事を指す

- `<work-root>/oracles` 配下である（サブディレクトリを含む）
- `<work-root>/.gitignore` の対象ではない
- `INDEX.md` ではない

## oracles files の役割

- oracles files は人間が所有し 100% の責任を負う正本仕様断片である
- oracles files の内容について AI は提案を行うことは出来るが、実際の編集を行うのは必ず人間である
- oracles を正本仕様として実装が生成されるものとし、その逆は禁止である

## oracles files の構成

- `<work-root>/oracles` 配下にはサブディレクトリを作成しても良い
- 具体的にどのようなサブディレクトリを作成するかは cmoc としては制限をしない
- 典型的には以下のような構成を想定する
    - `<work-root>/oracles/docs`: 自然言語の markdown ドキュメント形式で仕様断片を記述する
    - `<work-root>/oracles/schema`: 入出力・ステートなどの構造を定義するスキーマを記述する
    - `<work-root>/oracles/src`: ソースコードを配置する
    - `<work-root>/oracles/tests`: 

## oracles files と Codex CLI による読み書き

- Codex CLI は oracles files を読んで良いが、書き換えてはいけない
- Codex CLI は `<work-root>/oracles` 配下の非 oracles files  (e.g. `INDEX.md`) を読み書きして良い
