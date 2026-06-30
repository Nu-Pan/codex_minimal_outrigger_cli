
# .gitignore to permission profile

## やりたかったこと

- .gitignore 対象のファイル (厳密に言えば `git check-ignore` によって git 追跡対象から除外されていると判定されたファイル) は、通常の読み書き規則とは別の例外規則として、自由に読み書き OK にしたい
- 例えば…
    - agent が oracle 書き込み禁止系の作業中
    - 作業中に `<work-root>/oracle/**/__pycache__` が発生した
    - 作業完了前に agent はこの `__pycache__` を掃除したい
    - しかし、読み書き規則上は `__pycache__` の削除が禁止されているため、残さざるを得ない
    - `__pycache__` は git 追跡対象外なのだから、勝手に消してもらって構わないというのが正直なところ
- この例外を含む厳密な規則を permission profile に変換して Codex CLI に流し込みたかった

## 断念した理由

- .gitignore と permision profile の記法に互換性が無く、正しく変換することが出来なかった
- e.g.
    - .gitignore では `<dir-name>/` とすることで、`<dir-name>` とマッチするディレクトリだけを除外出来るが、permission profile にはその手の「ディレクトリだけ」は存在しない
    - .gitignore では `?` や `[0-9]` のような柔軟な記法が可能だが、これは permission profile にはない
