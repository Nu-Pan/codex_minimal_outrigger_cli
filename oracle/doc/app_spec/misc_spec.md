
# cmoc の雑多な仕様

## 実装ファイルの列挙方法

- 「実装ファイルを列挙」と言った場合、以下の方法で機械的に列挙する
    - `<work-root>` 配下の全てのファイルを glob する（拡張子で制限しない）
    - `<work-root>/oracle` は除外
    - `<work-root>/.gitignore` の対象は除外
    - `.git` は対象外
    - `INDEX.md` は除外

## `<work-root>` に対する仮定

cmoc による操作対象リポジトリである `<work-root>` は以下の要件を満たすものと仮定する

- git で管理されている
- `<work-root>/oracle` 配下に断片的な正本情報が記載されている（`<cmoc-root>` 配下がそうであるように）
- `<work-root>` に固有の作業のノウハウは全てリポジトリ上で実装済みである
    - 言い換えれば cmoc が無くても Codex CLI の直接利用でも作業を完遂出来るように `<work-root>` がメンテナンスされている事を仮定する
    - e.g.
        - 「`<work-root>/oracle` 配下のファイル別に `codex exec` セッションを起動する責任」は cmoc が負う
        - 「開発必要な特定のツールの使用方法を説明する責任」は cmoc ではなく `<work-root>/.agents/skills` が担う

## cmoc 実行時のカレントディレクトリ

- cmoc 実行時のカレント (pwd) は必ず  `<work-root>` とする

## `<repo-root>/.cmoc`

- `<repo-root>/.cmoc` は git の追跡対象外とする
- このことは `cmoc init` で保証される
- `<repo-root>/.cmoc` 配下のログファイルが未コミット差分として現れて、各サブコマンドの処理が狂ってしまう可能性を排除するための仕様である

## タイムスタンプのフォーマット

- タイムスタンプ `<time-stamp>` はフォーマット `<year>-<month>-<day>_<hour>-<minute>_<sec>_<msec>` に従うものとする
- year は 4 ケタゼロ埋めとする
- month/day/hour/minute/sec は 2 ケタゼロ埋めとする
- msec は 9 ケタとする
- timezone はそのマシンのローカルとする

## 「`<cmoc-managed-branch>` 上で～」の定義

「`<cmoc-managed-branch>` 上で～」といった時、それは以下の集合の和である

- `<cmoc-managed-branch>` 作成元 commit から `HEAD` までの間の commit 上で起きたこと
- working tree または staging area で起きていること

また、補足として、

- 削除済みファイルは対象から除外する
- rename は rename 後のパスを対象とする

例えば「`<cmoc-session-branch>` 上で変更のあった `<repo-root>/oracle` 配下のファイル」と言った時、それは、

- `<cmoc-session>` 作成元 commit から `HEAD` までの間の commit 上で変更のあった `<repo-root>/oracle` 配下のファイル
- working tree または staging area 上で変更のあった `<repo-root>/oracle` 配下のファイル

のことである。
