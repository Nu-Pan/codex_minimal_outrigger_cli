# `enumerate_finding.json`

## Summary
- oracle file のレビュー結果として、新規所見の一覧を返すための Structured Output schema。
- レビュー対象および関連 oracle file から、既知の関連所見と重複しない問題だけを所見として列挙する役割を持つ。
- 所見がない場合も同じ出力契約で空の一覧を返すため、レビュー処理の出力境界を確認する入口になる。

## Read this when
- oracle file レビュー機能が返す所見一覧の契約を確認したいとき。
- 新規所見と既知の関連所見の重複排除を、出力上どの単位で表すか確認したいとき。
- 所見ごとに重大度、見出し、根拠となる oracle file、理由をどの意味で持たせるか確認したいとき。
- レビューで問題が見つからない場合の出力を確認したいとき。

## Do not read this when
- oracle file レビューで所見をどう発見するかという探索手順や判定アルゴリズムを知りたいとき。
- oracle file 全般の品質基準や、仕様断片として何を問題扱いするかの基準を確認したいとき。
- 個別の既知所見リストや、重複判定に使う入力側の構造を確認したいとき。
- INDEX.md エントリーやルーティング文書そのものの生成規則を確認したいとき。

## hash
- d1bd69c75e8d60791cc304f06e103a7efdcc6566dc16c1254b8a92d6fcb38c5d

# `enumerate_finding.py`

## Summary
- `cmoc review oracle` で oracle file をレビューし、新規所見を列挙するための agent call parameter を組み立てる正本実装。
- レビュー対象 oracle file、既知の関連所見、oracle 読み取り専用の file access profile、Structured Output schema、標準群を含む complete prompt の構成方針を定義する。

## Read this when
- `cmoc review oracle` の新規所見列挙プロンプトや agent call parameter の正本仕様を確認したいとき。
- oracle file レビューで、既知所見との重複を避けて新規所見だけを返す挙動の根拠を確認したいとき。
- oracle レビュー用 agent に許可するファイルアクセス範囲、参照 placeholder、利用する標準群を確認したいとき。

## Do not read this when
- realization 側の CLI 実装、実行制御、入出力処理だけを確認したいとき。
- oracle 以外のレビュー対象や、所見列挙以外の review 用 prompt を確認したいとき。
- file access profile、path 解決、complete prompt レンダリングなどの共通部品そのものの仕様を確認したいとき。

## hash
- 61cb4d0c11b4a526f8cf4b15d26e2eaf839865c735e708139c1d1e17518d1cc1

# `judge_finding.json`

## Summary
- レビュー所見を人間へ提示するかどうかを判定するための、採否判断結果を表す JSON Schema。対象所見を要確認として扱うかを示し、その判断理由を具体的に記録する応答構造を定義する。

## Read this when
- レビュー所見の採否判定を返す処理やプロンプト出力の schema を確認したいとき。
- 所見を人間に提示すべきか、提示しないべきかの判断結果を機械可読な形で扱う箇所を実装・検証するとき。
- 採否理由に、所見が妥当である理由と妥当ではない理由の両面を踏まえた説明が必要か確認したいとき。

## Do not read this when
- レビュー対象そのものの解析方法、所見の生成方法、またはレビュー手順全体を知りたいとき。
- 採否判定後に人間へ表示する UI や CLI 出力の具体的な整形だけを確認したいとき。
- JSON Schema の共通構造や他の応答 schema を横断的に確認したいとき。

## hash
- 260ad5636b98dcbb46dc9ebf3181533f5c550384320219dd6c44661e7ec4e53e

# `judge_finding.py`

## Summary
- `cmoc review oracle` で検出された仕様断片レビュー所見について、賛成理由と反対理由を材料に、人間へ提示すべきかを判定する agent call parameter の正本実装。読み取り対象を oracle と INDEX に限定し、realization を読ませない所見採否判定用 prompt を組み立てる。

## Read this when
- 仕様断片レビュー所見の採否判定で、判定担当 agent に渡す role、summary、goal、動的入力、参照可能領域、モデル種別を確認したいとき。
- 所見本文、所見が妥当である理由、所見が妥当ではない理由を prompt にどう含めるか確認したいとき。
- `cmoc review oracle` の判定フェーズで realization を読ませず oracle と INDEX だけを参照させる根拠を確認したいとき。

## Do not read this when
- 仕様断片レビュー所見そのものを生成する prompt を確認したいとき。
- oracle file 以外の realization code や test を対象にしたレビュー、修正、実装判断の agent call parameter を確認したいとき。
- agent call parameter の共通データ構造、モデル種別、reasoning effort、markdown rendering の一般仕様だけを確認したいとき。

## hash
- 1bc2bcb9683ee512d791c8d9aaa756fae9feaac1bfa53e6b264f859b2bd60caa

# `merge_finding.json`

## Summary
- レビューで得た複数の所見を、重複・矛盾の解消という観点で整理する応答の構造を定める。
- 十分に整理済みの所見群では何も変更しない判断を表せる一方、不要な所見の除去、単一所見の差し替え、複数所見の統合を区別して扱うための制約を持つ。
- 整理後に残す所見について、重大度、見出し、根拠となる正本仕様断片、整理理由を保持させることで、所見の内容と編集判断の根拠を同時に検証できるようにする。

## Read this when
- レビュー所見リストから重複した指摘や互いに矛盾する指摘を整理する処理を実装・確認するとき。
- 所見整理の応答で、何を削除し、何を置き換え、何を統合として扱えるかの境界を確認したいとき。
- 整理後の所見に、重大度・要点・根拠・整理理由としてどの意味情報を残すべきかを確認するとき。
- 入力所見群がすでに十分コンパクトで整合している場合に、変更不要として扱えるかを確認するとき。

## Do not read this when
- 個々の正本仕様断片から新しいレビュー所見を検出する基準を知りたいだけのとき。
- 所見整理ではなく、レビュー対象の正本仕様そのものの品質基準や記述原則を確認したいとき。
- 単一の所見内容の意味を読むだけで、所見リスト間の重複・矛盾・統合判断を扱わないとき。
- 実装側のファイル編集、テスト追加、CLI 出力など、所見整理応答の構造と直接関係しない挙動を調べるとき。

## hash
- ef00100875ad3a93bd012fc2fe2f8dceb892a60020b8f202a80594e2426a60c0

# `merge_finding.py`

## Summary
- `cmoc review oracle` で使う、oracle file レビュー所見リストのマージ用 AI 呼び出しパラメータを組み立てる oracle src。所見同士の重複・矛盾を解消する編集操作を Structured Output として返させる prompt、ファイルアクセスプロファイル、モデル設定、出力 schema パスを定義する。

## Read this when
- `cmoc review oracle` の所見リストマージ処理に渡す prompt 内容、role、summary、goal、補助入力、placeholder を確認・変更したいとき。
- 所見マージ用 agent call のファイルアクセス範囲、モデルクラス、reasoning effort、schema 対応を確認したいとき。
- oracle file レビュー結果の重複・矛盾整理に関する AI 呼び出し仕様を追うとき。

## Do not read this when
- oracle レビューの個別所見を生成する prompt や判定基準を確認したいだけのとき。
- `cmoc review oracle` 以外のサブコマンド、または所見リストのマージ後の適用処理を調べたいとき。
- ファイルアクセスプロファイル、Structured Document、path placeholder 解決、AgentCallParameter の汎用仕様を確認したいとき。

## hash
- e6f3ed13811c175a85f945f7e4c14e7e12bb6c675d1385a2439e60dcf1d8b394

# `validate_finding_advocate.json`

## Summary
- レビュー対象の所見について、oracle file の記述に基づき、その所見が妥当だと言える新規理由だけを返すための構造を定める oracle src。
- 既知理由と重複しない根拠を列挙し、重複しない根拠が無い場合は空の一覧として扱う境界を示す。

## Read this when
- レビュー所見の妥当性を支持する理由を、oracle file に基づいて返す処理の出力契約を確認したいとき。
- 既知理由との重複を除いた新規理由の扱いや、理由が無い場合の返し方を実装・テストしたいとき。
- 理由として推測ではなく oracle file 由来の具体的根拠を要求する箇所を確認したいとき。

## Do not read this when
- レビュー所見が妥当でない理由や反証を返す出力契約を確認したいとき。
- oracle file の内容そのものや、どの記述を根拠として採用するかの判定基準を調べたいとき。
- レビュー全体の手順、対象ファイル探索、または CLI の入出力全体を確認したいとき。

## hash
- f265bb48178831b146ee5d071395ff0dd9dfb6bb509f2d062fa54e3243f4cb4e

# `validate_finding_advocate.py`

## Summary
- `cmoc review oracle` で、レビュー所見が妥当である理由を列挙する擁護担当 agent call parameter を構築する oracle src。対象所見、既知の擁護理由、既知の反対理由を prompt に埋め込み、oracle file の具体根拠に基づく新規擁護理由だけを Structured Output で返す呼び出し条件を定義する。

## Read this when
- `cmoc review oracle` の所見検証で、所見を擁護する理由を列挙する agent call の role、goal、入力文脈、file access profile、model class、reasoning effort、出力 schema 参照先を確認したいとき。
- 既知の擁護理由や反対理由を踏まえて、新規の擁護理由だけを返す prompt の構成を確認したいとき。
- oracle file を根拠とするレビュー所見擁護調査で、realization file を読ませないアクセス制御や `<oracle-root>` placeholder の扱いを確認したいとき。

## Do not read this when
- レビュー所見が妥当ではない理由を列挙する challenger 側の prompt を確認したいとき。
- `cmoc review oracle` 全体のコマンド実装、入出力処理、レビュー結果の集約処理を確認したいとき。
- oracle レビュー以外のサブコマンド用 agent call parameter や、汎用 prompt builder の実装を確認したいとき。

## hash
- 89ded525c6bbeceecf54a076b41edd57efd1b5bf3233f662a8729e0a4ce28bc4

# `validate_finding_challenger.json`

## Summary
- レビュー所見に対する反証候補を返すための構造を定める oracle src。対象所見が妥当ではないと言える新規理由だけを、oracle file の記述に基づく具体的根拠として列挙する境界を担う。

## Read this when
- レビュー所見を検証し、既知理由と重複しない反証理由を抽出する出力契約を確認したいとき。
- 所見が妥当ではない理由を書く際に、推測ではなく oracle file の記述を根拠にする必要があるか確認したいとき。
- 反証理由が存在しない場合の扱いを確認したいとき。

## Do not read this when
- レビュー所見そのものの生成、重大度判定、修正案作成の契約を確認したいとき。
- oracle file と realization file の一般的な責務分担や編集権限を確認したいだけのとき。
- 反証理由の具体的な判定材料となる個別の oracle file 本文を探しているとき。

## hash
- a90232c11fe6071e9aaf6200efe525e546aef4775f06fb11cc71018c28f1d214

# `validate_finding_challenger.py`

## Summary
- `cmoc review oracle` で、レビュー所見を否定する根拠を列挙するための AI エージェント呼び出しパラメータを組み立てる正本実装。
- 対象所見、既知の肯定理由、既知の否定理由を動的入力として受け取り、oracle file だけを根拠に新規の否定理由を返す prompt とファイルアクセス制約を定義する。

## Read this when
- `cmoc review oracle` の所見検証で、所見が妥当ではない理由を調査する agent call の役割、入力、出力条件を確認したいとき。
- 既知理由との重複を避けて新規の反証理由だけを列挙する prompt 方針を確認したいとき。
- oracle file のみを根拠にし、realization file を読ませないレビュー調査用ファイルアクセス制約を確認したいとき。

## Do not read this when
- 所見が妥当である理由を列挙する advocate 側の prompt を確認したいとき。
- `cmoc review oracle` 全体の CLI 挙動、サブコマンド構成、結果集約処理を確認したいとき。
- oracle review 以外の agent call parameter、または一般的な complete prompt 構築処理を確認したいとき。

## hash
- 5c28f87f30c5df052a13db42d23c9a83cfd233ca4c970717669f88e01e641dd6
