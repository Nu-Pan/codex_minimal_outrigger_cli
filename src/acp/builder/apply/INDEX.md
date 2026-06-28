# `__init__.py`

## Summary
- oracle 側の apply builder package と対応する互換 package であることだけを示す package 初期化要素。実処理や公開 API の定義ではなく、同領域を package として扱うための入口に位置づけられる。

## Read this when
- apply builder 領域が oracle 側の package 構造と対応しているかを確認したいとき。
- package 初期化部分に実装意図や互換性メモがあるかを確認したいとき。

## Do not read this when
- apply builder の具体的な処理、変換、適用ロジックを調べたいとき。その場合は同 package 内の実装本体を読む。
- 公開関数、クラス、入出力仕様、エラー処理を確認したいとき。この対象にはそれらの定義は含まれない。

## hash
- a6df93a5897c266e6f48287739c8bf8192733ea9fb19e2f6eb05a302f4165b06

# `fork`

## Summary
- apply fork 周辺で使う agent call parameter builder と、その出力契約、共有 helper をまとめる領域。差分要約、所見列挙、所見適用など、fork 適用作業を agent に委譲するための prompt・model 指定・file access 制約・schema 参照を扱う。
- 正本仕様断片に追従する realization 実装として、通常実行時に oracle 側を runtime import しない前提や、作業リポジトリ範囲、INDEX.md ルーティング指示、readonly または書き込み可能範囲などを agent prompt に埋め込む処理への入口になる。

## Read this when
- apply fork の中で、差分要約・所見列挙・所見適用を担当する agent をどの条件、prompt、schema、file access mode で呼び出すかを調べたいとき。
- raw git diff、対象 realization file、所見一覧などの入力が、agent call parameter や prompt にどう組み込まれるかを確認・変更したいとき。
- apply fork 系 builder が共有する repo root 解決 helper や、git 管理ディレクトリ探索と git コマンド fallback の境界を確認したいとき。
- apply fork 関連の Structured Output schema のうち、変更要約やファイル単位の所見列挙の契約を確認したいとき。
- oracle 側の正本仕様断片と realization 側 builder の関係、特に runtime import を避ける理由を確認したいとき。

## Do not read this when
- fork の作成、branch 操作、commit 操作、作業ディレクトリ管理、レポート保存など、apply fork 全体の実行制御や git 副作用を追いたいとき。
- agent が実際に編集する個別 realization file の修正内容や、各対象ファイル固有の実装ロジックを調べたいとき。
- oracle file と realization file の基本定義、path model、work-root や run-root などの概念定義そのものを確認したいとき。
- 変更要約や所見列挙の結果を表示する CLI 出力整形だけを確認したいとき。
- 正本仕様断片そのものを確認したいとき、または oracle 側の実装・文書・テストを読むべき作業をしているとき。

## hash
- e8d48ed6fa3b3037c6a1a09e7068d48d25d28ace653bf47f679ee573d080ab1b
