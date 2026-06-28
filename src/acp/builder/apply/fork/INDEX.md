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
- apply fork ACP builder 群で共有する、実行位置からリポジトリルートを解決し、oracle 側の Python 実装を import 可能にするための補助処理を置く。
- カレントディレクトリの親探索、git コマンドによるフォールバック、oracle/src の sys.path 追加という、各 builder 本体の前提環境を整える責務を持つ。

## Read this when
- apply fork ACP builder の起動前提として、リポジトリルートの解決方法や失敗時の扱いを確認したいとき。
- apply fork ACP builder から oracle 側の Python package を import できるようにする経路を確認・変更したいとき。
- builder 本体ではなく、複数の apply fork builder で共通に使う環境解決 helper の挙動を調べたいとき。

## Do not read this when
- apply fork ACP builder が生成する ACP の内容や、個別 builder の出力仕様を確認したいだけのとき。
- oracle 側 package の中身、正本仕様断片、path model の定義そのものを確認したいとき。
- apply fork 以外の builder や、CLI 全体のコマンドルーティングを調べたいとき。

## hash
- f75e51370608a6ad649e421173d55eaea5862beb70d5078f73b49b2ef8978dcf

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
- `cmoc apply fork` で、指定された対象を起点に realization file の要修正点を列挙するための agent call parameter を構築する builder。
- 実行時に repo root 解決、oracle src import 設定、target path の実パス化を行い、oracle 側の prompt builder と struct doc renderer から read-only の所見列挙プロンプトを生成する。
- モデル種別、reasoning effort、file access mode、対応する JSON schema path を含む agent 呼び出し設定を返す入口として位置づけられる。

## Read this when
- `cmoc apply fork` のファイル単位所見列挙 agent に渡す prompt や agent call parameter の組み立てを確認・変更したいとき。
- 対象 path を起点に oracle file と realization file を読ませ、apply review standard に従う所見リストを返させる指示内容を調べたいとき。
- apply fork 系 builder が oracle src の正本 prompt 断片をどのタイミングで import し、render しているかを確認したいとき。
- 所見列挙用 agent の file access mode、model class、reasoning effort、structured output schema の対応付けを確認したいとき。

## Do not read this when
- `cmoc apply fork` の所見列挙結果そのものの schema 定義だけを確認したいときは、対応する JSON schema を直接読む。
- prompt の正本仕様断片そのものを確認・変更したいときは、oracle src 側の対応する prompt builder を読む。
- apply fork 全体の共通 repo root 解決や oracle import 設定の実装を確認したいだけなら、共通 helper 側を読む。
- 実際の所見検出ロジックや review standard の内容を調べたいときは、この builder ではなく oracle standard、realization standard、apply review standard の本文を読む。

## hash
- 721d2ea1fb9ff072680dc0b1433665dae203581ebc43e6407aefdffa8317bd3a

# `finding_application.py`

## Summary
- `cmoc apply fork` で検出済みの所見を修正担当 agent に渡すための agent call parameter を構築する realization implementation。
- 所見適用用の model class、reasoning effort、file access mode を固定し、所見リストを JSON code block として含む完全 prompt を oracle 側の prompt builder から組み立てる。
- prompt には作業上の注意、所見本文、repo root placeholder、oracle/realization の基本説明、realization standard を含める入口として機能する。

## Read this when
- `cmoc apply fork` の所見適用フェーズで呼び出す agent の model、reasoning effort、file access mode を確認または変更したいとき。
- 所見リストがどのように prompt へ埋め込まれ、修正担当 agent に渡されるかを確認したいとき。
- 所見適用 prompt に含める補助文書、作業上の禁止事項、placeholder、oracle/realization standard の組み込み方を変更したいとき。

## Do not read this when
- 所見の検出、分類、生成そのもののロジックを調べたいとき。
- repo root 解決や oracle src import の共通処理だけを調べたいとき。
- oracle 側で定義される prompt builder、構造化 markdown rendering、または正本 prompt 断片そのものを変更したいとき。

## hash
- add413689c4a9fe189eead9e6ab3e2fcfd524475672367a5fd86d896b3318aad
