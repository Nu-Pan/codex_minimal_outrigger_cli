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
- apply fork フェーズで使う agent call parameter builder 群と、その agent 出力を検証するための契約、複数 builder で共有する実行環境解決 helper をまとめる領域。
- 変更要約、file 単位の所見列挙、所見適用という apply fork 作業レポート・レビュー・修正の各 agent 呼び出しを組み立てる入口として位置づけられる。
- builder は repo root 解決、必要に応じた oracle src import 設定、model class、reasoning effort、file access mode、prompt、出力契約の対応付けを扱う。

## Read this when
- apply fork フェーズで agent に渡す呼び出し parameter の組み立て方を確認または変更したいとき。
- apply fork の変更要約、所見列挙、所見適用の各フェーズで、prompt に含める作業指示・読み書き制約・対象差分・所見本文・補助 standard の扱いを調べたいとき。
- apply fork 系 builder が repo root をどのように解決し、oracle 側の prompt builder や補助 API を import 可能にしているかを確認したいとき。
- apply fork 関連 agent の出力契約を、変更要約または所見列挙の用途ごとに確認・検証したいとき。
- oracle 側の正本仕様断片に追従する realization 実装として、通常起動時に oracle src を runtime import しない builder と、prompt 構築時に oracle src を読む builder の境界を確認したいとき。

## Do not read this when
- apply fork 全体の fork 作成、git 操作、作業ディレクトリ管理、レポート保存などの実行制御そのものを追いたいとき。
- 所見検出の判断基準、apply review standard、oracle standard、realization standard の本文を確認したいとき。
- oracle 側の正本 prompt 断片や prompt builder 本体を変更したいとき。
- apply fork 以外の builder、CLI コマンドルーティング、または package 全体の公開 API を調べたいとき。
- agent 出力を人間向けに表示する CLI 文面や整形処理だけを確認したいとき。

## hash
- a6be384ee55c9996879980470424bcd6c1ebdb0bfa8309a99da12fea2a7fa1d7
