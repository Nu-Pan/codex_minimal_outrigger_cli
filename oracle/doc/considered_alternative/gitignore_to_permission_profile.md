# .gitignore to permission profile

## 採用結果

`.gitignore` から permission profile を動的に生成する案は採用しなかった。現行の制限は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「permission profile の不使用と動的生成禁止」を正本とする。

## やりたかったこと

`git check-ignore` で無視対象と判定された未追跡ファイルを、通常の読み書き規則の例外として自由に読み書きできるようにしたかった。この例外を含む厳密な規則を permission profile に変換し、Codex CLI に渡す案だった。

例えば、oracle への書き込みを禁止された作業中に `{{work-root}}/oracle/**/__pycache__` が生成され、agent が作業完了前に削除したい場面を想定していた。当時の規則では削除も禁止されるため残さざるを得なかったが、未追跡かつ無視対象の `__pycache__` なら agent の判断で削除して構わないと考えていた。

## 断念した理由

当時の `.gitignore` と permission profile の記法には互換性がなく、正しく変換できなかった。例えば、次の指定を表現できなかった。

- `.gitignore` の `{{dir-name}}/` は、`{{dir-name}}` とマッチするディレクトリだけを除外できたが、permission profile にはディレクトリだけを対象とする記法がなかった。
- `.gitignore` の `?` や `[0-9]` のようなパターンを、permission profile では表現できなかった。
