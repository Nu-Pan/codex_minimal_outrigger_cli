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
- `cmoc review oracle` でレビュー対象の oracle file を起点に関連 oracle file を読み、新規所見を列挙するための AI 呼び出しパラメータを構築する prompt 正本。
- 既知の関連所見を補助文脈として渡し、重複しない新規所見だけを Structured Output に従って返すこと、所見がなければ空配列にすることを agent に要求する。
- oracle review 用の標準 prompt 部品、oracle/realization の基本前提、oracle 標準、レビュー標準を組み込んだ完全 prompt を生成し、主流モデル・中程度 reasoning・純粋 oracle 読み取りモードで返す。

## Read this when
- `cmoc review oracle` の新規所見列挙 prompt が、どの役割・目標・ファイルアクセス制約・補助文脈を agent に渡すか確認したいとき。
- レビュー対象 oracle file と既知の関連所見から、重複しない新規所見列挙用の AgentCallParameter がどう構築されるか確認したいとき。
- oracle review 系サブコマンドで、完全 prompt の組み立て、Structured Output schema の指定、モデル種別、reasoning effort、file access mode の設定を追うとき。

## Do not read this when
- 通常の実装担当 agent 向け prompt、INDEX.md 生成 prompt、または oracle review 以外のサブコマンド prompt を確認したいとき。
- 新規所見の列挙ではなく、既存所見の保存、集約、表示、またはレビュー結果の後続処理を調べたいとき。
- oracle file と realization file の基本定義、oracle 標準、レビュー標準そのものの本文を確認したいとき。

## hash
- ed4cfcfe7079b85b8e68b2bc29c1d10e9bbb9b63e89910f6dd2a30ef229cf036

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
- `cmoc review oracle` の所見採否判定を行う AI エージェント呼び出しパラメータの正本実装。判定対象所見、採用側理由、却下側理由を補助文脈として渡し、oracle 標準と review oracle 標準に従う完全 prompt を組み立てる入口を担う。
- 採否判定では効率系モデル、中程度 reasoning、純粋 oracle 読み取りの file access mode を使い、対応する Structured Output schema へ結果を返す設定を定義する。

## Read this when
- `cmoc review oracle` で、レビュー所見を人間へ提示するかどうかを判定するプロンプト内容・役割・goal・補助入力の扱いを確認したいとき。
- 所見本文、所見が妥当である理由、所見が妥当ではない理由をどのように agent prompt に渡すか確認したいとき。
- 所見採否判定用 agent call の model class、reasoning effort、file access mode、Structured Output schema の接続を確認したいとき。
- review oracle 標準を有効にした完全 prompt 構築経路を確認したいとき。

## Do not read this when
- レビュー所見の収集、生成、分類、整形など、採否判定以外の `cmoc review oracle` 処理を確認したいとき。
- Structured Output schema そのものの項目定義や判定結果 JSON の意味を確認したいとき。
- 汎用の agent prompt 組み立て処理、Markdown レンダリング、path 解決、file access mode の共通仕様を確認したいとき。
- oracle file と realization file の一般的な責務や編集規則だけを確認したいとき。

## hash
- db0e70e87fafff81bfb61e4ccd0185662810df398bd9b991f8baaf1d1bd32367

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
- `cmoc review oracle` のレビュー所見リストについて、入力された所見群から重複や相互矛盾を解消するための AI 呼び出しパラメータを構築する正本実装。
- レビュー対象の oracle file 群に対する既存所見を補助プロンプトとして渡し、所見整理用の role、goal、標準類を含む完全プロンプトと Structured Output schema 参照を組み立てる。

## Read this when
- `cmoc review oracle` で生成済みの複数所見を、統合・削除・置換などの編集操作として整理する呼び出し仕様を確認したいとき。
- レビュー所見同士の内容的な重複や相互矛盾を解消するため、AI にどの前提・目標・ファイルアクセス制約を与えるかを確認したいとき。
- レビュー所見整理処理が、oracle 標準および review oracle 標準を含む完全プロンプトをどのように構築するかを追いたいとき。

## Do not read this when
- 個別の oracle file をレビューして新しい所見を作る prompt を探しているとき。
- 所見リスト整理後の編集操作 schema の項目定義そのものを確認したいとき。
- レビュー以外のサブコマンドや、oracle file ではなく realization file を対象にした AI 呼び出しパラメータを調べたいとき。

## hash
- 88af6857e331f529f8017682be3fb75d01a7cd10b480906e49beaca208ad5e4c

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
- `cmoc review oracle` でレビュー所見が妥当である理由を追加調査するための AI エージェント呼び出しパラメータを構築する正本実装。対象所見、既知の擁護理由、既知の反証理由をプロンプトへ埋め込み、oracle file を根拠にした新規の擁護理由だけを Structured Output として返させる役割を持つ。
- レビュー所見の妥当性検証フローのうち、所見を支持する根拠列挙側の prompt、モデル設定、推論努力、ファイルアクセス制約、出力 schema の対応先を確認する入口になる。

## Read this when
- `cmoc review oracle` が、あるレビュー所見を妥当とする理由をどのような role・summary・goal で AI に調査させるか確認したいとき。
- 既知の擁護理由や反証理由を踏まえて、新規の擁護理由だけを列挙させる prompt 構成を確認したいとき。
- レビュー所見検証用の AI 呼び出しで、oracle file のみを根拠にする制約、oracle standard、review oracle standard をどう組み込むか確認したいとき。
- 所見擁護理由列挙タスクに使うモデルクラス、reasoning effort、ファイルアクセスモード、対応する Structured Output schema の接続を確認したいとき。

## Do not read this when
- レビュー所見が妥当ではない理由を列挙する prompt を確認したいとき。
- レビュー所見そのものを生成する処理や、所見一覧の集約・表示・CLI 入出力を確認したいとき。
- oracle file ではなく realization file の実装品質やテスト方針を調査したいとき。
- Structured Output schema の項目定義そのものを確認したいとき。

## hash
- fd4941548fcf86db04531ac224b4262d0926c233e9470dbd8aa67b8996803222

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
- `cmoc review oracle` でレビュー所見を否定する理由を列挙するための AI 呼び出しパラメータを組み立てる正本実装。対象所見、既知の肯定理由、既知の否定理由を補助文脈として渡し、oracle file だけを根拠に新規の否定理由を返させる prompt とモデル・推論強度・ファイルアクセス制約を定義している。

## Read this when
- レビュー所見が妥当ではない理由を探索するサブコマンドの prompt、役割、goal、入力文脈、根拠範囲を確認したいとき。
- 所見否定側の AI 呼び出しで、既知理由との重複排除、oracle file 根拠の要求、新規理由がない場合の扱いを確認したいとき。
- レビュー oracle 系 prompt builder のうち、所見を反証する側の呼び出し条件やファイルアクセス制約を実装・検証したいとき。

## Do not read this when
- レビュー所見が妥当である理由を列挙する側の prompt を確認したいとき。
- レビュー結果全体の集約、CLI 入出力、またはサブコマンド実行処理を確認したいとき。
- oracle file の定義、パスキーワード、review oracle 全体の共通標準を確認したいだけのとき。

## hash
- 0e940691ef68bfa6c135c4db3a5df544eb898e6b5945882fa2e8ee7749789e21
