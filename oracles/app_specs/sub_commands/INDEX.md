# `apply.md`

## Summary

- `cmoc apply` サブコマンドの正本仕様断片。`<repo-root>` の実装を `<repo-root>/oracles` の仕様へ近づけるため、Codex CLI による不整合調査・整理・修正ループを実行する仕様を扱う。
- 引数は位置引数なしで、反復回数を指定する `--repeat` / `-r` と、全体適用を指定する `--full` / `-f` を受け取る。デフォルト反復回数は 5。
- 事前条件として、`<cmoc-branch>` 上で実行されていること、および `<repo-root>/oracles` 外に未コミット差分がないことを要求する。
- 部分適用モードと全体適用モードの判定、`--full` 指定時の扱い、削除差分がある場合の全体適用への切り替え、変更ファイルへの絞り込みを定義する。
- 実行作業として、`.cmoc` の git 追跡対象外保証、`oracles` 配下の未コミット差分の自動コミット、不整合調査・整理・修正、編集禁止領域の差分検査、修正差分のコミット、作業レポート作成までの流れを定義する。
- `cmoc apply` は不整合修正ループの実行と判断材料のレポートを責務とし、実装が正本仕様へ完全追従したことや不整合が残っていないことは保証しない。
- 不整合リストアップでは、`oracles` ファイルと実装ファイルを列挙し、各ファイルごとに Codex CLI を起動して Structured Output の `discrepancies` 配列として結果を受け取る仕様を定義する。
- 不整合リスト整理では、ファイルごとの調査結果を連結し、重複や矛盾を整理したリストを Codex CLI に作成させ、空配列の場合のみ検出不整合なしとして扱う。
- 不整合追従作業では、整理された不整合 1 件につき 1 回 Codex CLI を起動し、補足情報として不整合情報をプロンプトに注入して修正を依頼する。
- ループが回数上限に達した場合はエラーではなく作業結果区分を「未収束」とし、検出不整合リストが空で終了した場合は「収束」とする。
- 作業レポートは Codex CLI に執筆させ、作業結果区分、不整合件数の推移、`<cmoc-branch>` 上の全変更内容の意味論的カテゴリ別要約を含め、`<repo-root>/.cmoc/reports/apply/<time-stamp>.md` に保存する。
- サブコマンドの終了コードは、収束・未収束・エラーの 3 種類を区別可能にする必要がある。

## Read this when

- `cmoc apply` の CLI 引数、`--repeat` / `-r`、`--full` / `-f` の意味やデフォルト値を実装・確認したいとき。
- `cmoc apply` 実行前に満たすべき条件、`<cmoc-branch>` 判定、`oracles` 外の未コミット差分チェックを調べたいとき。
- 部分適用モードと全体適用モードの切り替え条件、削除差分がある場合の扱い、変更ファイルへの絞り込み仕様を確認したいとき。
- `cmoc apply` の全体フロー、`.cmoc` の git 追跡対象外保証、`oracles` 差分の自動コミット、不整合修正ループ、最終レポート作成までの順序を実装したいとき。
- Codex CLI に不整合を調査させる呼び出し単位、対象ファイル列挙、Structured Output schema、`discrepancies` の各フィールドを確認したいとき。
- 複数の不整合調査結果を整理・統合し、重複や矛盾する修正方針を処理する仕様を知りたいとき。
- 整理済み不整合リストに基づき、Codex CLI に修正作業を依頼する単位やプロンプトへ注入する補足情報を設計したいとき。
- 修正後に `<repo-root>/oracles` など編集禁止ディレクトリへ差分が発生していないか検査する仕様を確認したいとき。
- 不整合修正ループが収束した場合と回数上限に達した場合の扱い、未収束をエラーにしない方針を確認したいとき。
- `cmoc apply` の作業レポートに含める内容、保存先、標準出力へ流すレポートパスの仕様を実装したいとき。
- `cmoc apply` の終了コードで収束・未収束・エラーを区別する必要があるとき。
- `cmoc apply` が保証する範囲と保証しない範囲、つまり完全な仕様追従の保証ではなく修正ループ実行とレポートが責務であることを確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc merge` など、`apply` 以外のサブコマンド固有仕様だけを調べたいとき。
- Codex CLI の共通呼び出し方法、サンドボックス指定、ログ保存、リトライ、自然言語方針など、サブコマンド横断の実行時仕様だけを調べたいとき。
- `<repo-root>` の発見、oracle ファイル列挙、`.cmoc` の git 追跡対象外保証、タイムスタンプ形式などの共通補助仕様そのものを調べたいとき。
- `INDEX.md` の自動生成・更新、Structured Output による目次情報生成、ハッシュ不一致時の扱いなど、ルーティング文書管理仕様を調べたいとき。
- cmoc 自体の Python コーディング規約、テスト規約、開発環境、実装配置など、開発者向けルールだけを確認したいとき。
- リポジトリ運用上の閲覧禁止・編集禁止ファイル、README や AGENTS.md の扱いなど、ファイルアクセス規則だけを確認したいとき。
- `cmoc apply` の実装コードやテストコードの現在の具体的な状態を調査したいだけで、正本仕様断片が不要なとき。
- Codex CLI や git の一般的な使い方を知りたいだけで、cmoc 固有の apply ワークフロー仕様が不要なとき。

## hash

- a98ae2f57b7d0d14193c7ed0f80e080a035edcff95ade080ea1dc83685198072

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

- `cmoc eval-oracles` サブコマンドの正本仕様断片。
- 現在の `<repo-root>/oracles` スナップショットを評価し、致命的な問題がないか人間向けにレポートする目的を定義している。
- 位置引数を持たず、`--full` または `-f` によって全体評価モードを明示できる。
- `<cmoc-branch>` 上かどうか、`--full` の有無、`oracles` ファイル削除の有無に応じて、部分評価モードと全体評価モードを切り替える条件を定義している。
- 実行手順として、`<repo-root>/.cmoc` の git 追跡対象外保証、`oracles` ファイル列挙、部分評価時の変更ファイルへの絞り込み、ファイル単位の `codex exec` 評価、評価結果のレポート統合を定義している。
- 致命的な問題を、仕様だけから判断・実装した場合に主要ワークフローが壊れる、完了判定できない、または cmoc の中核目的を満たしたと判定できない問題として定義している。
- 評価レポートは yaml frontmatter と本文で構成し、環境・事前条件、部分または全体評価モード、ファイルごとの評価結果を含める。
- 評価レポートは `<repo-root>/.cmoc/reports/eval-oracles/<time-stamp>.md` に保存し、そのフルパスを stdout に出力する。

## Read this when

- `cmoc eval-oracles` サブコマンドの目的、引数、実行モード、処理手順を実装または確認したいとき。
- `cmoc eval-oracles` が部分評価モードと全体評価モードのどちらを選ぶべきか判断する条件を確認したいとき。
- `<cmoc-branch>` 上での `oracles` 変更ファイルの絞り込みや、`oracles` ファイル削除時の全体評価への切り替えを実装したいとき。
- `oracles` ファイルごとの評価を `codex exec` でどのように呼び出すか、関係ファイルの参照を許すかを確認したいとき。
- 評価プロンプトに注入する「致命的な問題」の定義を確認したいとき。
- `cmoc eval-oracles` の評価レポートの構成、yaml frontmatter、本文の区切り方、保存先、stdout への提示方法を確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc merge` など、`cmoc eval-oracles` 以外のサブコマンド仕様だけを調べたいとき。
- Codex CLI 呼び出し、Structured Output、ログ保存、リトライ、stdout 進捗表示など、サブコマンド横断の共通実行仕様だけを調べたいとき。
- `oracles` ファイル列挙、`<repo-root>` 探索、`.cmoc` の git 追跡対象外保証、タイムスタンプ形式などの共通補助仕様だけを確認したいとき。
- cmoc 自体の Python 実装規約、CLI 設計規約、テスト規約、開発環境ルールを調べたいとき。
- `<repo-root>` 配下に自動生成される `INDEX.md` の対象、除外規則、目次情報フォーマット、生成タイミングを調べたいとき。

## hash

- b9e543cf37c45f5813eff8db74aa07f346c9e2b3c3168330963a123e21c9c548

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
