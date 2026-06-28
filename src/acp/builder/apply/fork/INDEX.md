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

# `_common.py`

## Summary
- apply fork 系の builder で共通利用する、リポジトリルート解決の補助処理を収める。現在の作業ディレクトリから親方向に git 管理ディレクトリを探し、見つからない場合は git コマンドの結果からルートを導く。

## Read this when
- apply fork の builder 実装で、実行位置に依存せずリポジトリルートを得る処理を確認・変更したいとき。
- 作業ディレクトリ配下の git 管理ディレクトリ探索と、git コマンドによるフォールバックの失敗時挙動を確認したいとき。
- apply fork 配下の複数処理から共有される、ルートパス解決 helper の責務境界を確認したいとき。

## Do not read this when
- apply fork の個別生成内容、ACP 文字列、ファイル更新手順、または分岐ごとの builder 本体を確認したいとき。
- リポジトリルート以外のパスモデル、work-root や run-root などの概念定義を確認したいとき。
- git 操作全般の実行ロジック、branch 操作、commit 操作、または fork 適用後の副作用を確認したいとき。

## hash
- ea60e209134538d8c4711567f78dbca18c863787a438a901a5684682003188d2

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
- `cmoc apply fork` の作業レポート向けに、git diff の生文字列から変更要約生成用の agent call parameter を組み立てる realization 実装。効率重視モデル、中程度 reasoning、読み取り専用アクセス、隣接 JSON schema を使い、prompt には対象リポジトリ範囲・INDEX.md ルーティング・差分本文・パス置換定義を埋め込む。
- 対応する oracle src を正本仕様断片として参照しつつ、通常起動時は realization 側の `src` だけが公開される制約により oracle 実装を runtime import しないことを明示している。

## Read this when
- `cmoc apply fork` で作業レポート用の変更要約 agent を呼ぶための parameter 構築処理を確認・変更したいとき。
- 変更要約 agent に渡す prompt の role、goal、読み書き制約、INDEX.md 利用指示、raw git diff の埋め込み方法、パス置換定義を確認したいとき。
- apply fork 系 builder が oracle src を直接 import せず realization 実装として正本仕様断片に追従する理由を確認したいとき。

## Do not read this when
- 差分要約そのものの JSON schema や出力項目の定義だけを確認したいときは、隣接する schema 定義を直接読む。
- repo root の解決方法や apply fork builder 共通処理を変更したいときは、共通 helper 側を読む。
- `cmoc apply fork` 全体の fork 作成、git 操作、作業ディレクトリ管理、またはレポート保存処理を追いたいだけなら、それぞれの責務を持つ apply fork 実装へ進む。

## hash
- 9b11c45d41ca497ff81a8efe314d74590500e9cb49f01f1871d53e5834615d30

# `file_finding_enumeration.json`

## Summary
- 実装調査で見つかった問題点を、根拠位置・要求仕様・観測された実装・修正方針とともに列挙するための JSON Schema。
- apply fork 周辺の実装レビュー結果を機械的に検証できる形で返すための出力契約を定める。

## Read this when
- 実装に対する所見を出力する処理の契約を確認したいとき。
- 仕様・実装ファイル上の根拠位置を含むレビュー結果を生成または検証するとき。
- 所見ごとに要求、現状、問題理由、修正方針を揃えて扱う必要があるとき。

## Do not read this when
- 実装差分そのものや修正対象のコードを調べたいだけのとき。
- ファイル探索や fork apply の制御フローを理解したいとき。
- INDEX.md 用のルーティング文書の一般規約を確認したいとき。

## hash
- 0bed168a2a89c47730cdc914c08c08f2a3ad4022595c4b910c5d8ff9ca335524

# `file_finding_enumeration.py`

## Summary
- `cmoc apply fork` で特定ファイルを起点に realization file の要修正点を列挙するための agent call parameter を組み立てる builder。
- 実行時に oracle 側の正本 prompt builder を import 可能にし、対象 path と repo root を埋め込んだ read-only の所見列挙プロンプトを生成する入口を担う。

## Read this when
- apply fork のファイル単位レビューや所見列挙用 agent call parameter の model、reasoning effort、file access mode、schema 対応を確認・変更したいとき。
- 所見列挙プロンプトに渡す target path、repo root、oracle standard、realization standard、apply review standard の組み込み方を確認したいとき。
- oracle src を実行時に import できるようにする探索経路や、見つからない場合の失敗挙動を確認したいとき。

## Do not read this when
- apply fork 全体の制御フロー、サブコマンド実行、または fork 作成・適用処理そのものを調べたいとき。
- 所見列挙の正本プロンプト内容やレビュー基準自体を確認したいとき。この実装ではなく oracle 側の該当正本断片を読む方が直接的。
- 生成された所見リストの JSON schema の詳細だけを確認したいとき。schema 対応ファイルを読む方が直接的。

## hash
- 9342009ed7211ac290eb3e764f5e9e81d6a0894a71e40a3f82250590953e825a

# `finding_application.py`

## Summary
- `cmoc apply fork` で、所見本文を realization file 修正担当 agent へ渡すための agent call parameter を構築する実装。
- 所見一覧を JSON としてプロンプトへ埋め込み、読み書き範囲、ルーティング方針、作業上の禁止事項、place holder definition を含む修正依頼文を生成する。

## Read this when
- `cmoc apply fork` が所見を適用する agent をどの model class、reasoning effort、file access mode、prompt で呼び出すかを確認したいとき。
- 所見本文が修正担当 agent のプロンプトへどのように渡されるか、また修正担当 agent にどの作業制約が与えられるかを確認したいとき。
- realization file 修正担当 agent 向けの読み書き規則、`INDEX.md` 利用方針、git add・git commit 禁止の指示を調整したいとき。

## Do not read this when
- 所見の検出、分類、生成、妥当性評価そのものを確認したいとき。
- `cmoc apply fork` 以外の apply 系処理や、所見適用以外の agent call parameter 構築を確認したいとき。
- repository root の解決方法そのものを確認したいとき。
- 修正担当 agent が実際に編集する個別 realization file や、その修正ロジックを確認したいとき。

## hash
- 43c0b963de149d2a846c5bb0ff27d28af87db8042e59363963439c793d625c6c
