
# cmot アプリケーション仕様

## `<repo-root>` に対する仮定

cmot による操作対象リポジトリである `<repo-root>` は以下の要件を満たすものと仮定する

- git で管理されている
- `<repo-root>/oracles` 配下に断片的な正本情報が記載されている（`<cmot-root>` 配下がそうであるように）
- そのリポジトリ上で必要な作業のノウハウは全てリポジトリ上で実装済みである
    - 言い換えれば cmot が無くても Codex CLI の直接利用でも作業を完遂出来るように `<repo-root>` がメンテナンスされている事を仮定する
    - e.g.
        - 「`<repo-root>/oracles` 配下のファイル別に `codex exec` セッションを起動する責任」は cmot が負う
        - 「`oracles` を評価する際の観点をエージェントに説明する責任」は cmot ではなく `<repo-root>/.agents/skills` が担う

## Codex CLI の実行方法

- cmot からの Codex CLI はすべて `codex exec` で行う
- `.agents` 配下を編集出来ない問題の扱い
    - `.agents` 配下は Codex CLI で特別扱いされているため、人間が approve しないと編集出来ない
    - `codex exec` は個別に approve が出来ないので `<repo-root>/.agents` 配下は絶対に編集できない（やろうとして失敗する）
    - この問題は `<repo-root>` 側で対策を行う事とする
    - e.g. AI 行動原則「明確な指示があった場合のみリポジトリローカルスキルを編集する」＋ユーザー運用規則「スキル編集をしたい場合は Codex CLI を直接起動したうえで明確に指示をする」

## cmot のエンドユーザー呼び出し方法

- `<cmot-root>/bin` を環境変数 `PATH` に追加し `cmot` コマンドで呼び出すものとする

## 実行時のカレントディレクトリ

- cmot が呼び出された時のカレントを起点に、ルートに向けて「直下に `.git` ファイル・ディレクトリを持つディレクトリ」を探索する
- 最初に見つかったディレクトリを `<repo-root>` とする
- cmot 実行時のカレントは必ず `<repo-root>` に変更する

## ワークフロー

1. 人間が `<repo-root>` の git 未コミット差分が無いクリーンな状態にする
2. 人間が `cmot fork` を実行
3. 人間がやってほしいと思っている事を `<repo-root>/oracles` に反映（e.g. 正本仕様を追加）
4. `<repo-root>/oracles` 修正ループ
    1. 人間が `cmot eval-oracles` を呼び出して、評価レポートを読む
    2. 人間が現状の `<repo-root>/oracles` で問題なしと判断したら、ここでループ終了
    3. 人間が `<repo-root>/oracles` の内容を修正
    4. ループ先頭に戻る
5. 人間が `cmot apply` を呼び出して、作業レポートを読む
6. 現状の実装に人間が満足しなければ「4. `<repo-root>/oracles` 修正ループ」に戻る
7. 人間が `cmot merge` を呼び出す

## サブコマンド別仕様

### `cmot fork`

- コマンド呼び出し時点で git 未コミット差分が有る場合はエラー終了とする
- 既に cmot feature branch をチェックアウトしている場合はエラー終了とする
- git default branch の最新コミットを分岐元として、新規に cmot feature branch を作成・チェックアウトする
- cmot feature branch の命名規則は `cmot_<year>-<month>-<day>_<hour>-<minute>-<sec>` とする

### `cmot eval-oracles`

- cmot feature branch 上に居なければエラー終了とする
- 現在の `<repo-root>/oracles` の内容に致命的な問題が無いか評価し、評価結果を人間にレポートする
- 具体的には以下の手順で評価レポートを作成する
    1. `oracles` ファイルを列挙
    2. ファイルごとに個別に評価を行う
        - １回の `codex` 呼び出しで、ファイル１つを評価する
        - 評価にあたっては、関係するファイルも読みに行くこととする
    3. 全てのファイルを読んで、ファイル間の関係性を評価する
        - １回の `codex` 呼び出しで、全てのファイルを読ませる
    3. これまでに出した評価を１つのレポートにまとめる
- 評価レポートは `<repo-root>/.cmot/logs/eval-oracles/*.md` にファイルに保存し、そのフルパスを標準出力に流す

### `cmot apply`

- cmot feature branch 上に居なければエラー終了とする
- `<repo-root>` の実装を `<repo-root>/oracles` で記述している仕様断片に追従させる
- 具体的には以下の手順を最大３回繰り返す
    1. `<repo-root>/oracles` と実装との明確なズレを調査
    2. ズレがなければこの時点でループ終了
    3. 「`<repo-root>` の実装を `<repo-root>/oracles` に追従させてください。」を codex にやらせる（この時、ズレ調査結果を一緒に渡す）
    4. 発生した差分を git にコミット（コミットメッセージは codex で適切なものを生成）
    5. 1. に戻る
- 作業完了後、結果をレポートする
    - レポートは「現状の cmot feature branch を default branch の最新コミットにマージした時の変更内容の要約」を書く（この `cmot apply` で行った作業内容の要約ではない）
    - レポート本体は `<repo-root>/.cmot/logs/apply/*.md` にファイルに保存する
    - レポート執筆は codex にやらせる
    - レポートのフルパスを標準出力に流す

### `cmot merge`

- cmot feature branch 上に居なければエラー終了とする
- 以下の手順を実行
    1. default branch を checkout する
    2. default branch を最新化する
    3. cmot feature branch を default branch に merge する
    4. merge 後の default branch に居る事を確認
    5. マージ済みの cmot feature branch を削除

## 各処理の補足

### `<repo-root>/oracles` ファイルの列挙方法

- `<repo-root>/oracles/docs` 配下の全てのファイルを glob する（拡張子で制限しない）
- `<repo-root>/.gitignore` の対象は除外
- `ROUTING.md` は除外
- これは codex を使わずに機械的に行う

### `<repo-root>/oracles` と実装との明確なズレを調査

- `<repo-root>/oracles` ファイルごとに「`<repo-root>/oracles` ファイルと実装との明確な差異が無いかを確認して、差異とその説明を報告してください」を codex にやらせる
- 確認結果を１つのファイルにして、これを「`<repo-root>/oracles` と実装の差異」とする
