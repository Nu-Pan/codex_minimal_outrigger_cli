# `__init__.py`

## Summary
- `oracle.acp_builder.apply.fork` と同じ import 経路を実装側に用意するための互換 package 初期化ファイル。本文は互換 package であることを示す docstring のみを持ち、具体的な処理や公開 API の定義は持たない。

## Read this when
- `oracle.acp_builder.apply.fork` 互換 package の存在理由を確認したいとき。
- この package 直下の実装を読む前に、package 自体が処理本体ではなく互換用の入口であることだけを確認したいとき。

## Do not read this when
- fork 適用処理の具体的な実装、関数、クラス、入出力を調べたいとき。
- 互換 package ではなく oracle 側の正本仕様断片を確認したいとき。
- package 初期化 docstring 以外の実行時挙動や副作用を探しているとき。

## hash
- c5707d270af058dc9b548e1d49ffefdd38c20a0785a67a293523f2be83ebc266

# `change_summary.json`

## Summary
- 変更内容を意味上のカテゴリごとにまとめ、各カテゴリで何を変えたかと根拠となる主要な変更箇所を記録するための出力契約を定義する。
- 差分適用や派生作業の結果を、人間がレビューしやすい変更要約として構造化する場面への入口になる。

## Read this when
- 差分適用後の変更要約をどの粒度でカテゴリ分けするか確認したいとき。
- 変更カテゴリ、変更内容の説明、主要な変更箇所をまとめた機械可読なレポートを生成・検証するとき。
- 空ではない変更要約を前提に、レビュー用の結果データを組み立てる処理を確認するとき。

## Do not read this when
- 個々の差分の検出方法、パッチ適用手順、fork 作成や実行制御の挙動を確認したいとき。
- 変更要約の表示文面や CLI 出力全体の整形だけを確認したいとき。
- 特定カテゴリに含めるべき具体的な変更ファイルを調べたいだけのとき。

## hash
- 51ffe6e61588c7c347494a36267c02b8d48f69f6e264fcaf396096938cdd672d

# `change_summary.py`

## Summary
- `cmoc apply fork` が作業レポート用に使う変更要約 agent call parameter を組み立てる builder。対象リポジトリの raw git diff をプロンプトへ埋め込み、効率向けモデル・中程度 reasoning・読み取り専用アクセス・隣接する JSON schema を指定した呼び出し設定を返す。
- 通常起動時に oracle 側を import できない制約を踏まえ、正本仕様断片への対応関係をコメントで残しつつ、実行時は realization 側だけで repo root 解決とプロンプト生成を行う。

## Read this when
- `cmoc apply fork` の作業レポートに含める変更要約を、どのモデル設定・reasoning・ファイルアクセスモード・schema で生成するかを確認または変更したいとき。
- 差分要約担当 agent に渡すプロンプト本文、読み取り専用ルール、ルーティング指示、raw git diff の埋め込み方を確認したいとき。
- 実行時にカレントディレクトリまたは git command から repo root を解決する挙動を確認したいとき。
- oracle 側の正本仕様断片を実行時 import せずに realization 実装へ反映している箇所を確認したいとき。

## Do not read this when
- 差分要約の Structured Output schema の項目や型そのものを確認したいだけのときは、隣接する schema 定義を直接読む。
- `cmoc apply fork` 全体の fork 作成、適用、git 操作、作業レポート保存などの制御フローを追いたいときは、より上位の apply/fork 実装へ進む。
- agent call parameter の共通データ構造、モデル種別、reasoning、ファイルアクセスモードの定義を確認したいときは、共通 ACP 定義を読む。
- oracle file と realization file の一般的な関係や編集ルールを確認したいだけのときは、正本仕様側の基本文書を読む。

## hash
- bfc8d4d052a2b8f867aed1b924fc5b6fedee20c80bca51821518bd659703b85c

# `file_finding_enumeration.py`

## Summary
- 対象は、実装側の同名モジュールを正本側の実装へ委譲する薄い再公開ファイルである。本文自体は独自ロジックを持たず、fork 適用時の file finding enumeration に関する実体は正本側モジュールに置かれている。

## Read this when
- 実装側の import 経路から、fork 適用時の file finding enumeration の定義がどこへ委譲されているかを確認したいとき。
- 同階層の実装ファイル群のうち、この概念の realization 側エントリーポイントだけを確認したいとき。

## Do not read this when
- file finding enumeration の具体的な仕様、関数、型、挙動を調べたいときは、委譲先の正本側モジュールを読む。
- fork 適用処理全体の流れや他の責務を調べたいときは、該当する上位または隣接モジュールを読む。

## hash
- b64c3193ab0469318fecebabc0c2e2ac9d2164d2bcbef9dd8d11362a205ab599

# `finding_application.py`

## Summary
- fork 適用処理で検出された finding の適用仕様を公開する薄い再エクスポート実装。実体は oracle 側の同名モジュールにあり、この realization 側ファイルは src ツリーからその定義を参照可能にする入口として位置づく。

## Read this when
- src ツリー側から fork finding application 関連の公開名がどこへ委譲されているか確認したいとき。
- 実装本体ではなく、realization implementation が oracle 側の正本実装断片を再利用している接続点を確認したいとき。

## Do not read this when
- fork finding application の具体的な関数・型・処理内容を確認したいとき。その場合は再エクスポート先の oracle 側本文を読む。
- fork 適用処理全体の設計や他の適用段階を調べたいとき。その場合は同じ責務領域のより上位または隣接する本文を読む。

## hash
- 055ee85cc2fab78164f4ef81a97d605ec0bc25162c4e7c098fffa72bb1e0eb84
