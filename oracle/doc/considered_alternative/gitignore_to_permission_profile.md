# .gitignore to permission profile

## 採用結果

- `.gitignore` または他の情報から permission profile を動的に生成する案は採用しない
- 現行のファイルアクセス制限は `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` を正本とし、この不採用案を例外や追加規則として扱わない
- permission profile との記法互換性が将来改善した場合も、この変換を実行時の分岐や fallback として使用しない

## やりたかったこと

- .gitignore 対象のファイルを、通常の読み書き規則の例外として、自由に読み書きできるようにしたかった
    - 厳密には、`git check-ignore` によって git 追跡対象から除外されていると判定されたファイルを指す
- 想定していた状況の例：
    - agent が oracle への書き込みを禁止された作業をしている
    - 作業中に `{{work-root}}/oracle/**/__pycache__` が発生した
    - 作業完了前に agent はこの `__pycache__` を掃除したい
    - しかし、読み書き規則上は `__pycache__` の削除が禁止されているため、残さざるを得ない
    - `__pycache__` は git 追跡対象外なので、agent が自分の判断で削除して構わないと考えていた
- この例外を含む厳密な規則を permission profile に変換し、Codex CLI に渡したかった

## 断念した理由

- `.gitignore` と permission profile の記法に互換性がなく、正しく変換できなかった
- 互換性がない記法の例：
    - .gitignore では `{{dir-name}}/` によって、`{{dir-name}}` とマッチするディレクトリだけを除外できる。permission profile には、ディレクトリだけを対象とする記法がない
    - .gitignore では `?` や `[0-9]` のような柔軟な記法が可能だが、これは permission profile にはない
