# `apply.md`

## Summary

- `cmoc apply` サブコマンドの正本仕様断片。
- `<repo-root>` の実装を `<repo-root>/oracles` の正本仕様断片へ追従させるための事前条件、実行手順、不整合修正ループ、Codex CLI への依頼内容、作業レポート、終了コードを定義する。
- `--repeat`/`-r` による不整合修正ループ回数、デフォルト値 5、回数上限到達時の扱いを定義する。
- 不整合調査では oracle ファイルごとに Codex CLI を呼び出し、Structured Output の `discrepancies` 配列として明確な不整合を受け取る仕様を定義する。
- apply 実行時の oracle 差分自動コミット、実装追従後の編集禁止領域チェック、変更コミット、`.cmoc/reports/apply/<time-stamp>.md` へのレポート保存を扱う。

## Read this when

- `cmoc apply` の引数、事前条件、処理順序、終了コードを実装・確認したいとき。
- `cmoc apply` が `<cmoc-branch>` 上でのみ動作することや、`<repo-root>/oracles` 外の未コミット差分をエラーにする条件を確認したいとき。
- apply 実行時に `<repo-root>/.cmoc` を git 追跡対象外に保証する処理や、`oracles` 配下の未コミット差分を自動コミットする処理を調べたいとき。
- oracles と実装の不整合調査を Codex CLI にどう依頼し、Structured Output の `discrepancies` をどう解釈するか実装したいとき。
- 不整合追従作業で Codex CLI に渡す補足情報、編集禁止ディレクトリの差分検査、実装変更のコミット方針を確認したいとき。
- `--repeat`/`-r` の意味、デフォルト反復回数、不整合修正ループが上限に達した場合の正常系扱いを確認したいとき。
- `cmoc apply` の作業レポートに含める項目、保存先、標準出力へ流すレポートパスを実装・テストしたいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc merge` など apply 以外のサブコマンド仕様だけを調べたいとき。
- Codex CLI 呼び出し表示、stdout 進捗表示、共通エラー処理、タイムスタンプ形式など、サブコマンド横断の共通仕様だけを確認したいとき。
- `INDEX.md` 自動メンテナンスや oracle ファイル列挙など、apply 固有ではない共通処理の詳細を調べたいとき。
- cmoc 自体の Python 実装規約、テスト規約、開発環境、ディレクトリ構成など開発者向けルールだけを確認したいとき。
- `<repo-root>/oracles` に書く仕様断片の内容そのものや、個別機能の正本仕様を探しているとき。
- README、AGENTS、memo、oracles などの閲覧・編集可否に関するリポジトリ運用ルールだけを確認したいとき。

## hash

- 6a256318c99311fac3088517b931206017a786bccbde97db8dda3ce9c5ca3a53

# `branch.md`

## Summary

- `cmoc branch` サブコマンドは、cmoc による開発作業専用の git ブランチ `<cmoc-branch>` を作成するためのショートカットである。
- 引数はなく、サブコマンド固有の事前条件もない。
- 実行手順は `git checkout -b <cmoc-branch>`、`<repo-root>/.cmoc` を git 追跡対象外にする保証、`<repo-root>/.cmoc/branch/<cmoc-branch>.txt` への作成元コミットハッシュ記録である。
- `<cmoc-branch>` は `cmoc_<time-stamp>` 形式で命名し、衝突した場合はリトライする。

## Read this when

- `cmoc branch` サブコマンドの仕様、引数、事前条件、実行手順を実装または確認するとき。
- cmoc が作成する作業用ブランチ `<cmoc-branch>` の命名規則を確認するとき。
- `<repo-root>/.cmoc/branch/<cmoc-branch>.txt` に記録する内容や、ブランチ作成元コミットの扱いを確認するとき。
- `<repo-root>/.cmoc` を git の追跡対象外にする処理が `cmoc branch` に必要か確認するとき。

## Do not read this when

- cmoc のサブコマンド全般の一覧や共通仕様だけを調べたいとき。
- `cmoc branch` 以外のサブコマンドの引数、実行手順、振る舞いを調べたいとき。
- cmoc 自体の開発ルール、コーディング規約、テスト方針、設計方針を調べたいとき。
- `<repo-root>` ではなく `<cmoc-root>` 側のリポジトリ構造や開発作業について調べたいとき。

## hash

- 9eba833d96e6456d7729e92f661147f756eba666ef19fdfd4bf269a8b69c35a9

# `eval-oracles.md`

## Summary

- `cmoc eval-oracles` サブコマンドの仕様断片。
- `<repo-root>/oracles` の現在スナップショットに致命的な問題が無いか評価し、評価結果を人間向けレポートとして保存・提示する挙動を定義する。
- 位置引数なし、`--full` / `-f` オプション、部分評価モードと全体評価モードの切り替え条件、評価対象となる変更済み oracle ファイルの定義を扱う。
- 評価時の `codex exec` 呼び出し単位、関連ファイル参照、致命的な問題の評価観点、レポートの frontmatter・本文構成・保存先・stdout 出力を定義する。

## Read this when

- `cmoc eval-oracles` コマンドの引数、オプション、事前条件、実行手順を実装・確認するとき。
- `--full` の有無、現在ブランチが `<cmoc-branch>` かどうか、oracle ファイル削除の有無によって部分評価・全体評価をどう選ぶか調べるとき。
- 部分評価で「変更があった `oracles` ファイル」をどう列挙し、削除済みファイルや rename をどう扱うか確認するとき。
- `<cmoc-branch>` 作成元 commit を `<repo-root>/.cmoc/branch/<cmoc-branch>.txt` から読み、差分範囲を決める処理を実装するとき。
- oracle ファイルごとの評価を `codex exec` で実行する単位や、評価時に関連ファイルも読ませる方針を確認するとき。
- `cmoc eval-oracles` が注入する「致命的な問題」の定義や、汎用的な評価観点を確認するとき。
- 評価レポートの yaml frontmatter、ファイルごとの結果結合、保存先 `<repo-root>/.cmoc/reports/eval-oracles/<time-stamp>.md`、stdout へのフルパス出力を実装・テストするとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc merge` など、`eval-oracles` 以外のサブコマンド仕様だけを調べたいとき。
- oracle ファイルの一般的な列挙方法、`.cmoc` の git 追跡対象外保証、タイムスタンプ生成など、サブコマンド共通仕様だけを確認したいとき。
- cmoc 自体の Python 実装規約、CLI 配置、テスト規約、開発環境ルールを調べたいとき。
- `oracles` ディレクトリの正本仕様そのものを作成・更新するためのルーティング規則や INDEX.md メンテナンス仕様だけを確認したいとき。
- 評価レポートの実際の内容を読みたいだけで、`cmoc eval-oracles` がレポートをどう生成・保存するかの仕様が不要なとき。

## hash

- 32c17262f5488f8610f6ddd374f35a8fdfbb3cd0196a4992c2fb709a291bc282

# `init.md`

## Summary

- `cmoc init` サブコマンドの正本仕様断片。
- `<repo-root>` を cmoc で作業可能な状態に初期化するための引数、事前条件、実行手順を定義する。
- `<repo-root>/.cmoc` を git 追跡対象外にする具体的な操作と完了判定を定義する。

## Read this when

- `cmoc init` の仕様を実装・修正・確認するとき。
- `cmoc init` が引数なしで動作することや、固有の事前条件がないことを確認したいとき。
- `<repo-root>/.cmoc` を `.gitignore` に追加し、既に tracked な `.cmoc` 配下ファイルを追跡解除する処理を実装するとき。
- `.cmoc` 追跡対象外保証の完了判定として、`git ls-files -- .cmoc` と `git check-ignore -q .cmoc/.__cmoc_ignore_probe__` を使う仕様を確認するとき。
- 初期化処理の最後に、ここまでの作業で発生した差分を git commit する必要があるか確認するとき。

## Do not read this when

- `cmoc init` 以外のサブコマンド仕様を調べたいとき。
- cmoc 自体の開発ルール、コーディング規約、テスト規約、開発環境だけを調べたいとき。
- Codex CLI 呼び出し、Structured Output、コンソール出力、共通エラーハンドリングなど、サブコマンド横断の共通仕様だけを調べたいとき。
- `<repo-root>/.cmoc` の git ignore 保証や init 時の commit に関係しない機能を実装するとき。

## hash

- b3b7cca844c91f7ba5a4e8d4592f0c2fb5510aa4ab31fbb1c114b7fd62574175

# `merge.md`

## Summary

- `cmoc merge` サブコマンドの正本仕様断片。`<cmoc-branch>` を現在の `HEAD` にマージし、コンフリクト解決支援まで扱う。
- 引数として省略可能な `<cmoc-branch>` を受け取り、省略時は未マージかつ命名規則に合うローカルブランチから best effort で自動解決する。
- 実行前にマージ先へ移動済みであること、未コミット差分がないこと、`<repo-root>/.cmoc` が git 追跡対象外であることを前提・確認する。
- `git merge` がコンフリクトした場合は Codex CLI に conflict marker 解消を依頼し、cmoc 側で marker 残存確認、対象ファイルの `git add`、unmerged path 確認、merge commit 作成を行う。
- 想定外の失敗時はロールバックせず処理を打ち切り、手動解決が必要なことを stderr で通知する。
- `<cmoc-branch>` の削除は作業結果が失われない安全性の裏付けが取れた場合のみ実行し、確認失敗時は warning として残す。

## Read this when

- `cmoc merge` サブコマンドの実装・修正・テストを行うとき。
- マージ元 `<cmoc-branch>` の引数仕様、自動解決条件、候補絞り込みロジックを確認するとき。
- マージ実行前の precondition、未コミット差分チェック、`.cmoc` の git 追跡除外保証を扱うとき。
- git merge のコンフリクト発生時に Codex CLI へ依頼する範囲、cmoc 側で行う `git add` や unmerged path 確認、merge commit 作成手順を確認するとき。
- マージ失敗時や想定外エラー時のロールバックしない挙動、stderr 通知方針を実装・検証するとき。
- マージ完了後に `<cmoc-branch>` を削除してよい条件や、削除できない場合の warning 挙動を確認するとき。

## Do not read this when

- `cmoc merge` 以外のサブコマンド仕様を調べたいだけのとき。
- cmoc 全体の設計、開発ルール、ディレクトリ構成、コーディング規約を調べるとき。
- Codex CLI の一般的な起動方法、プロンプト設計全般、または merge 以外の Codex 連携仕様を調べるとき。
- git の一般的な merge 操作やコンフリクト解決方法だけを調べるとき。
- `<cmoc-branch>` の命名規則そのものの正本仕様を調べるとき。ただし merge の自動解決で命名規則を利用する文脈では読む。
- README、AGENTS、oracles の編集可否など、リポジトリ運用ルールを確認するとき。

## hash

- f8c2bba0366f1460bfe8cb568ea929626bd5d49cbd128aca62c140c2fee1a56f
