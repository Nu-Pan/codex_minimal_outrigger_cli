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
- `cmoc review oracle` でレビュー対象の oracle file から新規所見を列挙するための agent call parameter を組み立てる prompt 正本。既知の関連所見を補助文脈として渡し、oracle review 用の標準・アクセスモード・Structured Output schema を指定する。

## Read this when
- `cmoc review oracle` の新規所見列挙 agent call に渡す role、summary、goal、補助文脈、placeholder、標準読み込み設定を確認したいとき。
- レビュー対象 oracle file と既知所見を入力にして、重複しない新規所見だけを返す prompt 構築の正本を確認したいとき。
- oracle review 用の agent call parameter がどの model class、reasoning effort、file access mode、schema path を使うか確認したいとき。

## Do not read this when
- oracle file レビューの所見 schema そのものを確認したいとき。schema 定義を直接読む方が適切。
- `cmoc review oracle` の所見列挙以外の review 処理、CLI 実装、所見保存処理を確認したいとき。
- oracle review ではなく realization review や index entry 生成の prompt 正本を確認したいとき。

## hash
- 4bab73660afd12977e3febdda67380b02bfd2dbed8ebe2becfebf24dce5ae095

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
- `cmoc review oracle` の所見採否判定を行う agent call parameter を構築する oracle src。判定対象所見、妥当理由、非妥当理由を prompt に埋め込み、pure oracle read のファイルアクセスと review oracle standard を前提にした呼び出し設定を返す。

## Read this when
- `cmoc review oracle` の所見採否判定 prompt や agent call parameter の正本意図を確認したいとき。
- 所見本文、advocate 側理由、challenger 側理由が判定 prompt にどう渡されるかを確認したいとき。
- 所見採否判定で使う model class、reasoning effort、file access mode、structured output schema の対応関係を確認したいとき。

## Do not read this when
- `cmoc review oracle` 全体のレビュー収集、所見生成、表示、採否後処理を確認したいとき。
- oracle review 以外のサブコマンド用 prompt や agent call parameter を確認したいとき。
- prompt 部品の共通組み立て、path placeholder 解決、markdown rendering の実装詳細を確認したいとき。

## hash
- 2673d7d3a6cb6aeadfe266750f53203cd150464b7906f17088c04d57a8d39843

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
- `cmoc review oracle` の所見リストマージ用 AgentCallParameter を構築する oracle src。入力された所見リストを prompt に埋め込み、oracle file レビュー所見の重複・矛盾解消に必要な編集操作を Structured Output で列挙させる呼び出し条件を定義する。

## Read this when
- `cmoc review oracle` の所見リストをマージ・整理する agent call の role、goal、file access mode、補助 prompt、placeholder、model class、reasoning effort、schema path を確認・変更したいとき。
- oracle file レビュー結果の findings をどのように prompt へ渡し、どの Structured Output schema に対応させるかを確認したいとき。

## Do not read this when
- oracle file 本文そのもののレビュー基準や oracle standard の内容を確認したいだけのとき。
- `cmoc review oracle` 以外のサブコマンド、または所見リストのマージではないレビュー処理の agent call 定義を探しているとき。
- Structured Output schema の項目定義そのものを確認したいとき。

## hash
- 00496c930faab30fdf4973fb527f7e8c727ecb25d4daf036c5636a50b3d3acbb

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
- `cmoc review oracle` でレビュー所見が妥当である理由を列挙するための agent call parameter を構築する oracle src。対象所見、既知の擁護理由、既知の反論理由を prompt に埋め込み、純粋な oracle 読み取り権限で新規の根拠理由だけを返させる。

## Read this when
- `cmoc review oracle` の所見検証で、所見を擁護する側の prompt や agent call parameter の意図を確認したいとき。
- 所見が妥当である理由の列挙で、既知理由との重複排除、oracle file 根拠の要求、Structured Output への接続を確認したいとき。
- レビュー所見の擁護担当に渡す入力項目や file access mode、model class、reasoning effort を確認したいとき。

## Do not read this when
- 所見が妥当ではない理由を列挙する challenger 側の prompt を確認したいとき。
- `cmoc review oracle` 以外のサブコマンド用 agent call parameter を確認したいとき。
- prompt 構築共通処理、path placeholder 解決、Structured markdown rendering の詳細を確認したいとき。

## hash
- 0fc6884fa24441f048b7dcc50dfbf6ce1e9e8487676e4919893965e2c197d24a

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
- `cmoc review oracle` でレビュー所見を否定する新規理由を列挙するための agent call parameter を組み立てる oracle src。対象所見、既知の肯定理由、既知の否定理由を prompt に埋め込み、oracle file を根拠にした反証調査用の呼び出し設定を定義する。

## Read this when
- `cmoc review oracle` の所見検証で、所見が妥当ではない理由を探す側の prompt や agent call parameter を確認・変更したいとき。
- 既知理由との重複を避けた否定理由列挙、PURE_ORACLE_READ、出力先 schema、使用 model class・reasoning effort の設定を確認したいとき。

## Do not read this when
- 所見が妥当である理由を列挙する側の prompt を確認したいとき。
- oracle review 以外のサブコマンドや、oracle file ではなく realization file を根拠にするレビュー処理を確認したいとき。

## hash
- 283e960f0a2525200634eafbb5f9ed732bd0f806cbc8a408254639a1697e305c
