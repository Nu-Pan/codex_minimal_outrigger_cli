# `apply.md`

## Summary

- `cmoc apply` の調査・修正ループ、要修正点の抽出と改善、修正作業、レポート出力までを定義する正本仕様断片です。
- `<repo-root>` の実装を `<repo-root>/oracles` と照合し、ベストエフォートで不整合や致命的問題の解消を試みる手順を扱います。
- 実行条件、部分適用・全体適用モードの切り替え、反復回数の上限、Structured Output による要修正点管理、作業結果レポートと終了コードを含みます。

## Read this when

- `cmoc apply` の引数、事前条件、実行フロー、終了条件を実装または確認したいとき。
- `oracles` と実装の不整合を調査し、要修正点の洗い出し・改善・修正を繰り返す処理を設計したいとき。
- 部分適用と全体適用の切り替え条件、`<cmoc-branch>` 上の変更差分の扱い、ファイル単位での Codex CLI 呼び出し方を確認したいとき。
- 作業レポートの保存先、内容、標準出力への表示、および収束・未収束・エラーの区別を確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc merge` など他のサブコマンド仕様だけを調べたいとき。
- Codex CLI の一般的な呼び出し方法や、`INDEX.md` 自動生成の共通仕様だけを知りたいとき。
- `cmoc` 自体の開発ルール、コーディング規約、テスト方針など、実行時仕様ではない開発者向けルールだけを確認したいとき。
- `README.md`、`AGENTS.md`、`oracles`、`memo` などのファイルアクセス可否やリポジトリ運用ルールだけを確認したいとき。

## hash

- c472f5828ee97cf13515b6b71ead18636f5cfba7e801fc9bc09d5979141f03d9

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

# `eval_oracles.md`

## Summary

- `cmoc eval-oracles` の正本仕様断片であり、`<repo-root>/oracles` のスナップショットを仕様だけから評価してレポートする手順を定義する。
- 部分評価と全体評価の切り替え条件、`codex exec` によるファイル単位評価、評価時に参照してよい `oracles` / `INDEX.md` の範囲を扱う。
- 致命的問題の定義、評価結果レポートの YAML frontmatter と本文構成、保存先と stdout 出力の方針を含む。

## Read this when

- `cmoc eval-oracles` の実装・修正・テストを行うとき。
- 部分評価モードと全体評価モードの切り替え条件を確認したいとき。
- oracle ファイル評価時に `codex exec` へ渡す制約や、読んでよい `oracles` / `INDEX.md` の範囲を確認したいとき。
- 評価レポートの構成、保存先、標準出力への表示内容を確認したいとき。

## Do not read this when

- `cmoc eval-oracles` 以外のサブコマンド仕様だけを調べたいとき。
- 実装コードやテストコードを直接検証する処理を調べているとき。
- cmoc ではなく `<repo-root>` 側の個別アプリケーション仕様を調べているとき。
- `INDEX.md` の自動生成規則や目次フォーマットそのものだけを確認したいとき。

## hash

- bba77331f8cf3c09b126137aca557f61a7a355f7d4743b9a94ad680ca888b6e1

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
