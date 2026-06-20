# `cmoc apply fork`

## 概要

- `cmoc apply fork` は、Codex CLI による apply ループを実行する
- この apply ループは以下の状態を目標とする
    - `<work-root>` の実装が `<work-root>/oracle` の正本仕様断片と一致している
    - `<work-root>` の実装が最低限度の品質を満たしている
- `cmoc apply fork` が正常に実行完了したからといって、目標達成が保証されるわけではない
    - あくまで、apply ループの実行し、目標達成のために努力する所までが `cmoc apply fork` の責任範囲である
    - i.e. ベストエフォート的な振る舞いで良い
- `cmoc apply fork` は `<cmoc-session-branch>` と作業用コピーを直接汚すことはしない
    - `<cmoc-apply-branch>` を作成し、そこにコミットを積み上げる

## 引数

- 位置引数なし
- オプション引数 `--scope={rolling|session|full}` を受け取る
    - ショートネームは `-s`
    - デフォルト値は `rolling`
- オプション引数 `--apply-loop` を受け取る
- オプション引数 `--improove-fixing-list-loop` を受け取る

## 事前条件

以下の場合はエラー終了する

- 現在のブランチが `<cmoc-session-branch>` ではない
- 対応する `<cmoc-session-state-file>` が存在しない
- 対応する `<cmoc-session-state-file>` の `session.state` が `active` ではない
- 対応する `<cmoc-session-state-file>` の `apply.state` が `ready` ではない
- git 未コミット差分が存在する

## 実行作業

1. `<work-root>/.cmoc` が git の追跡対象外であることを保証する
2. run の隔離実行を開始する
3. apply ループ
    1. 調査対象となるファイルを列挙する
    2. Codex CLI に、列挙したファイルリストを元に要修正点をリストアップさせる
    3. 要修正点リスト改善ループ
        1. Codex CLI に、要修正点リストを改善させる
        2. 改善点がなければここで要修正点リスト改善ループを抜ける
        3. 要修正点リスト改善ループ先頭に戻る
    4. 改善後の要修正点リストが空であれば、要修正点が検出されなかったものとしてループを終了する
    5. 修正作業ループ（改善後の要修正点リストに対する for-each）
        1. 要修正点 1 つに対する修正作業を Codex CLI に依頼する
        2. `<work-root>/oracle` などの編集禁止ディレクトリに未コミット差分が有る場合はエラー終了
        3. 全ての未コミット差分を git にコミット（コミットメッセージは Codex CLI で適切なものを生成）
    6. apply ループ先頭に戻る
4. `<cmoc-session-state-file>` の状態を更新
5. 作業結果をレポートする

### 「run の隔離実行を開始する」とは

- それ以降の実際の作業を `<cmoc-review-worktree>` 上で隔離実行することを指す
- 詳しくは `<cmoc-root>/oracle/doc/app_specs/run_isolation.md` を参照すること

## `cmoc apply fork` の責務境界

- `cmoc apply fork` の責務は、指定された最大回数の範囲でapply ループを実行し、その結果を人間が判断できる形でレポートすることである
- `cmoc apply fork` は、要修正点が残っていないことを保証しない
- `cmoc apply fork` は、全ての要修正点を漏れなく発見することは保証しない（あくまでベストエフォート的に振る舞う）
- ループが回数上限に達した場合も、コマンド実行としては正常系として扱う
- 回数上限到達後にさらに `cmoc apply fork` を再実行するか、`cmoc review oracle` や人手レビューを行うか、作業を打ち切るかは人間が判断する

## `<cmoc-session-state-file>` 状態遷移

- apply ループ開始直前
    - `apply.state` を `running` に遷移させる
    - `apply` セクションの各フィールドを、適切な値で更新する
- apply ループ完了直後
    - i.e. 全ての処理が正常に完了出来た場合
    - `apply.state` を `completed` に遷移させる
    - `apply` セクションの各フィールドを、適切な値で更新する
- 途中でエラーが発生して処理を中止した場合
    - `apply.state` を `error` に遷移させる

## git worktree と編集操作

- `<cmoc-apply-worktree>` 上の `oracle/` は編集禁止である
- Codex CLI による実装修正が `<apply-worktree>/oracle` を変更した場合はエラー終了する

## ループの反復回数の決め方

- apply ループ
    - サブコマンドの引数 `--apply-loop` で apply ループの反復回数を受け取る
    - デフォルト値は 5 とする
- 要修正点リスト改善ループ
    - サブコマンドの引数 `--improove-fixing-list-loop` で要修正点リスト改善ループの反復回数を受け取る
    - デフォルト値は 1 とする

## 調査対象ファイルリストアップの仕様

### 調査対象 oracle file の snapshot 原則

- `<cmoc-apply-branch>` の HEAD を調査対象とする
    - 本来的には `<cmoc-apply-fork-commit>` を調査対象のスナップショットとして扱うべきである
    - 一方で、「git で過去バージョンのファイルを参照すること」といったような細かいルールは出来るだけ削減したい
    - ところで、apply 系サブコマンドでは oracle file の編集は行われないから、「`<cmoc-apply-fork-commit>` を調査対象とする」と「`<cmoc-apply-branch>` の HEAD を調査対象とする」は意味論的には同値である
    - よって、`<cmoc-apply-branch>` の HEAD を調査対象として代替した
- `cmoc apply fork` 開始後に `<cmoc-session-branch>` が進んでも、実行中の apply はその変更を取り込まない
- `cmoc apply fork` の収束・未収束判定は `<cmoc-apply-fork-commit>` に対する判定である

### 候補ファイルリスト、ダーティフラグ

- `cmoc apply fork` の対象なるファイルの候補は「oracle file 全て」「実装ファイル全て」である
- この候補ファイルリストを元に、本当に調査すべきファイルの絞り込みが行われる
- この絞り込み処理は「ダーティフラグ」で管理される
- ダーティフラグが true のファイルのみ、実際にファイル単位調査が行われる

### スコープモード、ダーティフラグ

- `cmoc apply fork` は以下の 3 つのスコープモードを持つ
    - `--scope rolling` ならローリングスコープ（デフォルト値）
    - `--scope session` ならセッションスコープ
    - `--scope full` ならフルスコープ
- ローリングスコープ
    - 「前回の apply の `<cmoc-apply-join-commit>`」から「今回の apply の `<cmoc-apply-fork-commit>`」の間に変更があったファイルだけ、ダーティーフラグの初期値を true とする
    - そのセッションの最初の apply の場合は、セッションモードにフォールバックする
    - i.e. `cmoc apply fork` 後に変更があったファイルについて、最低 1 回は調査が行われるということ
- セッションスコープ
    - `<cmoc-session-fork-commit>` から `<cmoc-apply-fork-commit>` の間で変更があったファイルだけ、ダーティーフラグの初期値を true とする
    - i.e. そのセッション上で変更のあったファイルについて、最低 1 回は調査が行われるということ
- フルスコープ
    - 候補ファイル全てのダーティフラグを true で初期化する
    - i.e. 全候補ファイルについて、最低 1 回は調査が行われるということ

## ダーティフラグの更新規則

- ダーティフラグは `cmoc apply fork` 処理の過程で逐次更新される
- 規則は以下の通り
    - 改善済みの最終的な要修正点リスト上、修正内容と関係すると判定されたファイルはダーティフラグを true に、そうではないファイルは false にする
    - Codex CLI による修正作業の結果として差分が発生したファイルはダーティーフラグを true にする

## 要修正点リストアップの仕様

- 具体的な `codex exec` 呼び出しの仕様は `build_apply_fork_file_audit_parameter` を正本とする
- このファイル起点の依頼は、事前に列挙したファイルリスト上のファイル全てに対して個別に行う
    - i.e. 調査対象となる oracle file が N 件と実装ファイルが M 件存在するのであれば `codex exec` を N + M 回呼び出すということ
- このファイル起点の依頼は並列に実行する
- 要修正点の agent 向け定義は `build_apply_reviewpoint` を正本とする

## 要修正点リスト改善の仕様

- `codex exec` 呼び出しの仕様は `build_apply_fork_fixing_point_refinement_parameter` を正本とする
- ファイルごとに個別に要修正点リストを列挙した後、それを１つに連結する
- 要修正点リストが空の場合のみ「検出された要修正点なし」と扱う

## 要修正点対応作業の仕様

- 改善後の要修正点リストに含まれる要修正点 1 件ごとに、独立した agent call を行う
- 具体的な `codex exec` 呼び出しの仕様は `build_apply_fork_fixing_point_application_parameter` を正本とする
- cmoc は agent call 後に、編集禁止ディレクトリの差分検査とコミット処理を行う

## 回数上限でループを抜けた場合

- エラーとみはみなさず、作業結果の区分「未収束」として処理を続行する

## 作業レポートの仕様

- レポートの形式は markdown + YAML Front Matter とする
- YAML Front Matter に必ず含める項目
    - `<cmoc-session-branch>`
    - `<cmoc-session-fork-commit>`
    - `<cmoc-apply-branch>`
    - `<cmoc-apply-fork-commit>`
    - `<cmoc-apply-worktree>`
- レポート本文に必ず含める項目
    - 作業結果
        - 収束 : 「検出された要修正点リストが空」によりループを終了した
        - 未収束 : 「回数上限に達した」によりループを終了した
        - エラー : 途中でエラーが起きてループを正常に終了出来なかった
    - 要修正点件数の推移
        - ループごとに何件の要修正点を見つけたかを書く
        - 「未収束」の場合は、まだ要修正点が残っている可能性を定型文で追記する
    - `<cmoc-apply-branch>` 上の全ての変更内容に対する要約
        - この `cmoc apply fork` で行った作業内容だけの要約に限定する
        - 変更内容の意味論に基づいたカテゴリ分けを行うこと
- レポート本体は `<repo-root>/.cmoc/reports/apply/fork/<time-stamp>.md` にファイルに保存する
- 作成したレポートのフルパスを標準出力に流すこと (内容は流さない)

## `<cmoc-apply-branch>` 上の全ての変更内容に対する要約の生成方法

- `<cmoc-apply-branch>` 上の全ての変更内容に対する要約の生成を agent call に依頼する
- この agent call の詳細仕様は `build_apply_fork_change_summary_parameter` を正本とする
 - cmoc は Structured Output を作業レポート用 Markdown にレンダリングする

## サブコマンドの終了コード

- 収束・未収束・エラーの３種類を区別可能であること
