# `app_spec`

## Summary
- CLI 自動補完の起動判定と、補完プローブ時に通常実行の前処理や副作用を混ぜない境界を確認するための入口。補完時の stdout/stderr を CLI ライブラリ向け出力に限定するかを判断するときに読む。

## Read this when
- シェル補完や CLI ライブラリの補完処理に関わる起動経路を実装・修正・テストするとき。
- 通常の CLI 実行前処理、サブコマンド未指定判定、作業ディレクトリ変更、状態検査、ログ作成、索引更新、独自エラー出力を補完前に実行してよいか判断するとき。
- 補完プローブ時に stdout/stderr へ余計な出力や副作用が混入していないか確認するとき。

## Do not read this when
- 通常実行時のサブコマンド仕様、状態ファイル仕様、ログ仕様、索引更新仕様そのものを調べたいだけのとき。
- 補完プローブではない通常の CLI エラー形式や出力仕様を確認したいとき。
- CLI 自動補完に関係しない oracle file と realization file の役割分担や品質基準を調べたいとき。

## hash
- b5243fdae14c4644fbee565b817e8a88b99f8658c5bddb4a9b8f9a44123a840e

# `branch_model.md`

## Summary
- cmoc が管理する branch と worktree の関係、session/run の分岐元・merge 先・命名規則を確認したいときの入口。`session fork` / `session join` / `apply` / `review` の責務境界を読むために使う。
- 通常の local branch や remote-tracking branch を特別扱いしない前提、`session` と `run` の二層で作業を隔離する前提、各 commit 名の意味を把握したいときに読む。

## Read this when
- cmoc がどの branch を基準に session を始め、どの branch に戻すのかを確認したいとき。
- run ごとの作業を session からどう分離するか、`apply` や `review` がどの抽象概念に対応するかを確認したいとき。
- branch 名、commit 名、linked worktree 名の対応関係を知りたいとき。

## Do not read this when
- branch や worktree の具体的な作成処理、merge 実装、CLI 引数の詳細を知りたいときは、各サブコマンドや実装側の本文を直接読む。
- git の一般論だけが必要なときは、この文書ではなく該当する実装や操作手順を読む。
- session/run の命名や対応表だけが必要で、分岐元・merge 先の意味まで不要なときは、より下位の対象を読む。

## hash
- e48fc3d9371ee9b4c447d06cdcb12a96f006afa581263ea87bd285118a7a60ed

# `considered_alternative`

## Summary
- `cmoc` の採用しなかった設計案と、その不採用理由を集めた文書群への入口。`apply` 系の実行フロー、作業計画レビュー、memory の自動注入、`gitignore` 由来の権限例外、事後の file access rule 再検査といった論点について、採用案ではなく見送った案の背景を確認したいときに読む。
- 各文書は現行仕様の手順書ではなく、代替案を退けた判断根拠を残すためのものなので、採用済みの CLI 挙動や保存仕様を知りたい場合は、より直接にその機能を扱う本文を読む。

## Read this when
- `cmoc` の設計で、採用しなかった方式の理由を確認したいとき。
- 作業計画の自動化、review 方式、memory の継続注入、権限例外の扱い、事後検査の再確認など、代替案の採否を比較したいとき。
- `apply` 系フローで、修正点の並べ方や調査対象管理をどうしないことにしたかを追いたいとき。

## Do not read this when
- 現行の `cmoc` CLI の入出力、状態ファイル、検査ロジック、実装手順を知りたいだけのとき。
- 採用済み仕様そのものではなく、却下された案の背景を必要としていないとき。
- `oracle` と `realization` の一般定義や、INDEX 作成規則そのものを確認したいとき。

## hash
- cad9fc4f61a6f59d4a593a1ed5039859c760c986de217d8b353dbe12520073a0

# `dev_rule`

## Summary
- `dev_rule` 配下の正本仕様断片を読むための入口。開発時の作業環境、Python の記述規則、CLI の構成、pytest ベースの realization test の書き方をまとめた文書群へ進むときに使う。

## Read this when
- 作業環境や Python 仮想環境の前提を確認したいとき。
- Python の命名・型注釈・docstring・コメント・import の書き方を揃えたいとき。
- CLI の起点とサブコマンドの責務分担を確認したいとき。
- realization test の追加・修正で、決定論的な制御ロジックの検証方針やテスト隔離の考え方を確認したいとき。

## Do not read this when
- 個別機能の業務仕様やサブコマンド固有の挙動だけを知りたいとき。
- 共有ユーティリティや実装本体の具体的なコードだけを探したいときは、対応する実装側を直接読むべきとき。
- LLM の回答品質そのものや外部 provider の正しさを評価したいだけのとき。
- 仕様そのものの正本断片ではなく、単なる実装や生成物を探しているとき。

## hash
- 27140fd9b30f01a50314ec912654fb571d956951778e3596d606e86a1416efb2
