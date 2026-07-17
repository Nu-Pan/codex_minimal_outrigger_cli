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
- `cmoc oracle review` で新規所見を列挙するための prompt 構築実装。レビュー対象 oracle file と既知の関連所見を受け取り、oracle ツリーのレビュー条件・完了条件・読み取り権限を含む agent call parameter を生成する。
- prompt の動的プレースホルダー解決、関連所見の埋め込み、モデル・推論強度・出力 schema の指定までを担当する。

## Read this when
- `cmoc oracle review` の新規所見列挙 prompt の内容、入力値、出力パラメータ、レビュー用 agent 呼び出し設定を変更または確認するとき。
- レビュー対象 oracle file と既知の関連所見を prompt に渡す流れを追跡するとき。

## Do not read this when
- oracle review の所見判定ロジック自体やレビュー基準の正本を確認したいときは、関連する oracle review 用の正本文書を直接読む。
- 一般的な agent call parameter の仕様や prompt 共通生成処理だけを確認したいときは、対応する共通 builder・型定義を直接読む。

## hash
- 3b3ac8494ec951ed01e1afffca20a7489e7f59bb289e364788fd7e7b95f7e2b6

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
- `cmoc oracle review` における所見採否判定用の AI エージェント呼び出しパラメータを構築する。所見本文と賛成・反対理由を埋め込んだ正本仕様レビュー用プロンプトを生成し、効率重視・最大推論 effort・oracle 読み取り専用の実行設定と判定結果スキーマを返す。

## Read this when
- `cmoc oracle review` の所見採否判定プロンプト、エージェント呼び出し設定、または所見・賛成理由・反対理由のプロンプト埋め込み方法を変更・確認するとき。
- oracle 専用読み取りモードや正本仕様レビュー用プロンプトの構築経路を追うとき。

## Do not read this when
- レビュー所見の生成や別の oracle review 処理を確認したいとき。
- 判定結果の Structured Output schema 自体や、プロンプト共通構築処理を直接確認すべきとき。

## hash
- b266f1ff3f9c795ce66f3494c8c6e1b3dac16df0e0850c84f8d1a642a37154e8

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
- `cmoc oracle review` における、oracle file のレビュー所見リストを整理する prompt の正本実装。入力所見を使って AI エージェント呼び出しパラメータを構築し、所見の重複・矛盾解消や空配列返却などの整理目標を指定する。

## Read this when
- `cmoc oracle review` の所見マージ処理を変更・確認するとき。
- レビュー所見リスト整理用の prompt、Structured Output、モデル設定、oracle-only のファイルアクセス制御を確認するとき。

## Do not read this when
- レビュー所見の JSON schema 定義そのものだけを確認したいとき。
- レビュー処理以外の prompt builder や別サブコマンドの実装を確認するとき。

## hash
- cd6c9e8578d0fe1494ebeb75cb7c9d8958f1fdcae32146b92ed4ad45ba3573fc

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
- `cmoc oracle review` における、所見が妥当である理由を列挙するエージェント呼び出しパラメータの正本実装。対象所見・既知の賛成理由・反対理由をプロンプトへ組み込み、oracle file を根拠とする新規理由のみを返すためのモデル設定と出力定義を構築する。

## Read this when
- `cmoc oracle review` の所見擁護処理、プロンプト内容、oracle-only のファイルアクセス制約、またはエージェント呼び出しパラメータ設定を変更・確認するとき。

## Do not read this when
- 所見が妥当ではない理由の列挙処理だけを確認するとき。一般的なプロンプト生成処理や共通の構造化文書レンダリングを確認する場合は、それぞれの実装ファイルを直接読む。

## hash
- 59a258e760fff109cf34e46cf02a86d8bcf8467a07f35cf3d627058fcb84d4e6

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
- `cmoc oracle review` における、所見が妥当ではない理由を列挙するエージェント呼び出しパラメータの正本実装。対象所見・既知理由をプロンプトへ渡し、oracle file を根拠とする新規の反証理由のみを返すようモデル設定と出力先を構成する。

## Read this when
- `cmoc oracle review` の所見否定理由列挙処理を変更・調査するとき
- 反証用プロンプトの入力、oracle 読み取り権限、モデル設定、Structured Output 出力先を確認するとき

## Do not read this when
- 所見が妥当である理由の列挙処理だけを調査するとき
- レビュー結果の表示や CLI コマンド実行処理を直接調査するとき

## hash
- 714b0e5ac710ae1f980ea25e13ae47f7de239048e0940cfeb843f92b58c18833
