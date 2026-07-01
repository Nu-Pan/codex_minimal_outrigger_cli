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
- `cmoc review oracle` で oracle file をレビューし、新規所見を列挙するための AI エージェント呼び出しパラメータを組み立てる oracle src。レビュー対象パス、既知の関連所見、oracle 読み取り専用のアクセス条件、Structured Output schema、関連する標準群を complete prompt に渡す。

## Read this when
- `cmoc review oracle` の新規所見列挙エージェントに渡す role、summary、goal、補助情報、placeholder、参照標準、モデル設定、reasoning effort、file access mode を確認または変更したいとき。
- レビュー対象 oracle file と既知の関連所見から、どのような AgentCallParameter が生成されるかを確認したいとき。
- oracle review の新規所見列挙 prompt と対応する Structured Output schema の接続箇所を探しているとき。

## Do not read this when
- oracle review の所見データそのものの保存形式、重複判定、集約処理、表示処理を調べたいとき。
- oracle file の一般的なレビュー基準や標準本文を読みたいだけのとき。
- complete prompt の共通組み立て処理、path placeholder の解決処理、AgentCallParameter 型の定義を確認したいとき。

## hash
- c0ba0303bddf30b463e595a94cc6e4b8d1ad8da4611c37d3bb73747ee246fe32

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
- `cmoc review oracle` におけるレビュー所見の採否判定用 agent call parameter を構築する oracle src。判定対象所見、採用側理由、不採用側理由を動的プロンプトへ埋め込み、oracle 読み取り専用の採否判定担当 prompt と Structured Output schema の出力先を組み立てる。

## Read this when
- `cmoc review oracle` の所見採否判定プロンプト、agent call parameter、モデルクラス、reasoning effort、file access mode を確認または変更したいとき。
- 所見本文・妥当理由・非妥当理由が、採否判定エージェントへどのような補助情報として渡るかを確認したいとき。
- レビュー所見の採否判定で参照される oracle standard や review oracle standard の有効化有無を確認したいとき。

## Do not read this when
- oracle レビュー所見を生成する側、所見に反論する側、または所見を集約する側の prompt を確認したいときは、それぞれの担当ファイルを読む。
- `cmoc review oracle` サブコマンド全体の CLI 実装や実行フローを確認したいときは、realization implementation 側のコマンド実装を読む。
- Structured Output schema の具体的な項目や型を確認したいだけのときは、対応する schema 定義を読む。

## hash
- 40c7fd2c40eec83d0287b4c617caa9e274e52845e9cd11d8739bd49e792226ce

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
- `cmoc review oracle` で得た oracle file レビュー所見リストを、重複・矛盾の解消に必要な編集操作へ整理するための agent call parameter を構築する正本仕様断片。
- 入力所見リストを動的プロンプトとして渡し、pure oracle read の権限、効率重視モデル、中程度推論、対応する Structured Output schema を指定する。

## Read this when
- `cmoc review oracle` の所見リストマージ段階で、どの役割・目的・制約を AI 呼び出しへ渡すか確認したいとき。
- 所見の `finding_id` を編集操作の `target_ids` に対応させる仕様や、十分コンパクトで整合的な場合に空配列を返す仕様を確認したいとき。
- oracle file レビュー結果の重複・相互矛盾を解消するためのマージ用プロンプト構成を変更・検証したいとき。

## Do not read this when
- oracle file 自体のレビュー観点や判定基準を確認したいだけのとき。
- `cmoc review oracle` のマージ以外の段階、または oracle 以外のレビュー処理の agent call parameter を調べたいとき。
- Structured Output schema の具体的な項目定義や型を確認したいとき。

## hash
- 121f1c8d5a7d7310ce88be0c545eb6c131ea0f58f23aa5db12331d2576bda0d9

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
- `cmoc review oracle` で検出されたレビュー所見について、所見が妥当である理由を追加調査する AI agent call parameter を構築する oracle src。
- 対象所見、既知の擁護理由、既知の反論理由を prompt に埋め込み、oracle file の具体的根拠に基づく新規の擁護理由だけを Structured Output として返させる。

## Read this when
- `cmoc review oracle` の所見検証で、所見を妥当とみなす追加理由を列挙する agent call の役割、入力、制約を確認したいとき。
- レビュー所見擁護担当の prompt が、既知理由との重複回避、oracle file 根拠限定、理由なし時の空配列返却をどう要求しているか確認したいとき。
- `review_oracle_standard` や `PURE_ORACLE_READ` を使う所見擁護側の agent call parameter を実装・更新する前に、正本 prompt 断片を確認したいとき。

## Do not read this when
- 所見が妥当ではない理由を列挙する challenger 側 prompt を確認したいとき。
- `cmoc review oracle` 全体の実行制御、CLI 引数、結果集約、出力形式を確認したいとき。
- oracle file 以外も含めた realization 実装やテストを根拠にレビュー所見を検証したいとき。

## hash
- 51d5566db5aec3c28a53aadf595bd5c5c24b0fec1d5c6a2cd3186fea3a2646bf

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
- `cmoc review oracle` の所見について、妥当ではない理由を列挙する AI 呼び出しパラメータを構築する prompt 正本。対象所見、既知の肯定理由、既知の否定理由を入力にし、oracle file を根拠にした新規の反証理由だけを返すための role、goal、参照制約、出力先 JSON を定義する。

## Read this when
- `cmoc review oracle` で、レビュー所見が妥当ではない理由を調査・列挙する agent call の prompt 内容やモデル設定を確認したいとき。
- 既知理由との重複排除、oracle file に基づく根拠要求、反証理由が無い場合の扱いを確認したいとき。
- 所見否定理由列挙用の `AgentCallParameter` 生成処理、Structured Output 用 JSON パス、`PURE_ORACLE_READ` 制約との対応を確認したいとき。

## Do not read this when
- 所見が妥当である理由を列挙する prompt を確認したいとき。
- oracle review 全体の実行制御、所見生成、結果集約、CLI 入出力の実装を確認したいとき。
- oracle file 以外の realization file を読む agent call や、oracle review 以外のサブコマンド用 prompt を確認したいとき。

## hash
- 16c35263efbf43d122010deeb0ebd707263b51dbe28cad39611624cf3a462b96
