# `enumerate_finding.json`

## Summary
- oracle レビューで、レビュー対象と関連する正本仕様断片から未登録の所見を列挙するための構造化出力を定義する。
- 所見がない場合も含め、既知の関連所見と重複しない新規所見だけを返す境界を示す。
- 各所見について、重大度、短い見出し、根拠となる正本仕様断片、所見として扱う理由を残すための出力契約を担う。

## Read this when
- oracle レビュー結果として、新規所見をどの粒度で返すべきか確認したいとき。
- 既知の関連所見と重複しない問題だけを報告する出力契約を確認したいとき。
- 正本仕様断片に対する所見の根拠や理由を、レビュー出力へどう含めるか確認したいとき。
- 所見の重大度を、致命的な矛盾・欠落と軽微な曖昧さ・改善余地に分ける基準を確認したいとき。

## Do not read this when
- oracle レビューで実際にどの正本仕様断片を調査するかを探しているだけのとき。
- 所見検出のアルゴリズム、探索順序、既知所見との照合方法などの実装を確認したいとき。
- oracle file や realization file の基本定義、編集責任、配置ルールを確認したいとき。
- INDEX.md エントリーそのものの記述方針やルーティング文書の一般基準を確認したいとき。

## hash
- d1bd69c75e8d60791cc304f06e103a7efdcc6566dc16c1254b8a92d6fcb38c5d

# `enumerate_finding.py`

## Summary
- `cmoc eval-oracle` における oracle file レビューのうち、既知の関連所見を前提に新規所見だけを列挙させる AI 呼び出しパラメータを構築する実装。
- レビュー対象の oracle file と oracle ツリーを起点にした読解範囲、Structured Output schema に従う所見列挙、既知所見との重複除外、所見なし時の空配列返却を prompt に組み込む。
- pure oracle read のファイルアクセス、mainstream model、medium reasoning、対応する schema 指定をまとめて返す入口。

## Read this when
- `cmoc eval-oracle` の新規所見列挙レビューで、AI に渡す prompt の役割・目的・補助情報を確認または変更したいとき。
- レビュー対象 oracle file から oracle ツリー内の関連 oracle file へ読む範囲を広げる指示を扱う実装を確認したいとき。
- 既知の関連所見を prompt に埋め込み、新規所見だけを返させる制御を変更したいとき。
- 新規所見列挙用の model class、reasoning effort、file access mode、出力 schema の指定を確認したいとき。

## Do not read this when
- oracle file の内容そのものや、レビュー基準となる正本仕様断片を確認したいだけのとき。
- `cmoc eval-oracle` 以外のサブコマンドの prompt 構築や AI 呼び出しパラメータを扱うとき。
- oracle レビューのうち、新規所見列挙ではないレビュー種別の prompt や schema を確認したいとき。
- prompt 部品の共通組み立て処理、markdown レンダリング、パス解決、基本データ型の定義を変更したいとき。

## hash
- 3d9a9a45319b3c00f372be03bf0878fb74831a4229e21acd25a1682b8abcced7

# `judge_finding.json`

## Summary
- レビューで得られた対象所見を、人間に要確認項目として提示するかどうかを判定するための出力契約を定める。
- 判定結果だけでなく、所見が妥当と見なせる点と妥当でない点を踏まえた具体的理由を返すことを求める。

## Read this when
- レビュー所見を採用して人間へ提示するか、却下して提示しないかを機械的に受け渡す出力を実装・検証する場合。
- レビュー所見の採否判定を行うプロンプト、ビルダー、レスポンス検証、テストを確認する場合。
- 採否の理由に、妥当性と不妥当性の両面を踏まえた説明が必要かを確認する場合。

## Do not read this when
- レビュー所見そのものの生成条件、検出ルール、重大度分類、表示形式を確認したい場合。
- 人間へ提示された後のレビュー UI、保存形式、集計処理、通知処理を確認したい場合。
- 汎用的な JSON Schema の構文や、他のレビュー用出力契約を調べたい場合。

## hash
- 260ad5636b98dcbb46dc9ebf3181533f5c550384320219dd6c44661e7ec4e53e

# `judge_finding.py`

## Summary
- `cmoc eval-oracle` で、レビュー所見を人間へ提示すべきか判定するための AI 呼び出しパラメータを構築する実装。
- 判定対象所見、妥当性を支持する理由、妥当性を否定する理由を prompt に組み込み、oracle 標準および review oracle 標準を含む採否判定用 prompt と Structured Output schema 参照を返す。

## Read this when
- `cmoc eval-oracle` のレビュー所見採否判定で、どの role・summary・goal・file access mode・補助 prompt が使われるかを確認したいとき。
- 判定対象所見と、支持側・反対側の理由が AI prompt にどのように渡されるかを確認したいとき。
- 採否判定用エージェント呼び出しの model class、reasoning effort、file access mode、schema ファイル参照の設定を確認または変更したいとき。

## Do not read this when
- oracle file と realization file の基本定義や、oracle 標準そのものを確認したいだけのとき。
- レビュー所見の抽出、advocate/challenger 側の理由生成、または判定結果 schema の中身を確認したいとき。
- 汎用的な prompt 構築処理や markdown rendering の実装を確認したいとき。

## hash
- b153e2aa4b5a90dda227402d4a763b31684a0fd14f862de3f9f7931b54e31807

# `merge_finding.json`

## Summary
- 入力された所見リストについて、重複や矛盾を解消する編集方針を返すための構造を定めるスキーマ。
- 十分に整理済みの所見群は変更なしとして扱い、必要な場合だけ削除・置換・統合によって新しい所見内容へまとめる境界を示す。

## Read this when
- 複数の oracle review 所見を後段で整理し、重複・矛盾・過剰な細分化を解消する出力を生成または検証する。
- 所見を削除する場合と、単一所見を置き換える場合と、複数所見を統合する場合の扱いを揃える必要がある。
- 編集後に残す所見へ重大度、短い見出し、根拠となる oracle file、整理理由を持たせる処理を確認する。

## Do not read this when
- 個別の oracle file から新しい所見そのものを発見する基準を確認したい。
- 整理済み所見の表示順、CLI 表示、保存先、レポート文面など、編集操作の構造以外を扱う。
- oracle file と realization file の基本概念やレビュー対象の選び方を確認したい。

## hash
- ef00100875ad3a93bd012fc2fe2f8dceb892a60020b8f202a80594e2426a60c0

# `merge_finding.py`

## Summary
- `cmoc eval-oracle` で、oracle file レビュー所見のリストを整理するための AI エージェント呼び出しパラメータを構築する実装。
- 入力された所見リストをプロンプト本文に埋め込み、重複や相互矛盾を解消する編集操作を Structured Output として返させるための role、summary、goal、読み取り権限、対応 schema を設定する。
- oracle 標準および review oracle 標準を適用した complete prompt を組み立て、効率重視モデル・中程度 reasoning・pure oracle read の呼び出し条件として返す。

## Read this when
- `cmoc eval-oracle` のレビュー所見リストを、統合・削除・置換などの編集操作へ変換するプロンプト構築を確認または変更したいとき。
- oracle file に対する複数の所見について、内容的な重複や相互矛盾を解消する AI 呼び出しの role、goal、参照権限、補助プロンプトを調べたいとき。
- 所見リストマージ処理で、入力所見の識別子を編集対象として扱う方針や、十分に整理済みなら空の操作列を返す方針を確認したいとき。
- レビュー系 oracle prompt で oracle 標準と review oracle 標準を同時に適用する呼び出しパラメータの具体例を探しているとき。

## Do not read this when
- 個別の oracle file 本文をレビューして所見を生成するプロンプトを探しているとき。
- 所見リストの Structured Output schema 自体の項目定義や JSON 形式を確認したいとき。
- 生成済みの編集操作を実際に oracle file へ適用する処理を探しているとき。
- `cmoc eval-oracle` 以外のサブコマンド、または一般的な AgentCallParameter 構築規約だけを確認したいとき。

## hash
- 531a71f4786064d75a6553cfcabbe4aadd4fb6420458c8584e653b117e448f48

# `validate_finding_advocate.json`

## Summary
- レビュー対象の所見について、正本仕様断片に基づき妥当性を支持できる新規根拠だけを返すための構造を定める。
- 既知の根拠と重複しない理由があるかを判定し、推測ではなく oracle file の記述に基づく根拠へ限定する出力契約として位置づけられる。

## Read this when
- レビュー所見が正本仕様断片に照らして妥当かどうかを、追加の根拠として列挙する出力を扱うとき。
- 既に提示済みの根拠と重複しない、新規の妥当性理由だけを返す必要がある処理を確認するとき。
- oracle file の記述を根拠にしたレビュー検証結果の構造を実装・テスト・調整するとき。

## Do not read this when
- 所見が不当である理由、反証、修正提案、設計改善案を返す構造を探しているとき。
- レビュー対象そのものの検出ロジックや、oracle file の読み取り・探索手順を確認したいとき。
- 正本仕様断片に基づかない一般的なレビュー品質評価や、LLM 出力文面の改善を扱うとき。

## hash
- f265bb48178831b146ee5d071395ff0dd9dfb6bb509f2d062fa54e3243f4cb4e

# `validate_finding_advocate.py`

## Summary
- `cmoc eval-oracle` で、レビュー所見が妥当である理由を列挙させるための AI エージェント呼び出しパラメータを構築する実装。
- 対象所見、既知の擁護理由、既知の反証理由を補助プロンプトに含め、oracle file を根拠にした新規の擁護理由だけを返すよう指示する。
- 効率重視のモデル、medium の推論努力、純粋な oracle 読み取り権限、対応する schema 出力先を組み合わせて返す。

## Read this when
- `cmoc eval-oracle` のレビュー所見検証で、所見を妥当とみなす理由を探すプロンプトやエージェント呼び出し条件を確認・変更したいとき。
- 既知の擁護理由や反証理由をプロンプトへ渡し、重複しない新規理由だけを列挙させる制御を確認したいとき。
- oracle file を根拠にすること、推測表現を根拠にしないこと、理由が無い場合は空配列にすることなどの指示内容を調整したいとき。

## Do not read this when
- レビュー所見が妥当ではない理由を列挙させる側のプロンプト構築を確認したいとき。
- `cmoc eval-oracle` 以外のサブコマンドや、レビュー所見検証以外の prompt 構築を調べたいとき。
- Structured Output schema の具体的な項目定義そのものを確認したいとき。

## hash
- d5125bd55fd53d7ae9f2fac71ca85160f0a6bc8b7b19a92e7f64c3f35618aca0

# `validate_finding_challenger.json`

## Summary
- 対象所見が妥当ではないと判断できる新規理由だけを返すための Structured Output schema。
- 理由は推測ではなく oracle file の記述に基づく具体的根拠に限定し、既知理由と重複するものがなければ空のリストで表す。

## Read this when
- レビュー所見に対して、oracle file を根拠に反証・異議申し立てとなる理由を構造化して返す処理を確認する。
- 既知の反証理由と重複しない、新しい不当性の根拠だけを出力すべき場面の出力契約を確認する。
- oracle file の記述に基づく理由と、推測や実装都合に基づく理由を区別する必要がある。

## Do not read this when
- レビュー所見そのものを生成するための出力契約を確認したい。
- 所見が妥当である理由、修正案、実装方針、テスト方針を扱いたい。
- oracle file ではなく realization file、一般的なベストプラクティス、推測に基づく判断理由を扱いたい。
- 個々の oracle file の内容や、所見の妥当性判断に使う正本仕様断片そのものを読みたい。

## hash
- a90232c11fe6071e9aaf6200efe525e546aef4775f06fb11cc71018c28f1d214

# `validate_finding_challenger.py`

## Summary
- `cmoc eval-oracle` で、レビュー所見が妥当ではない理由を新規に列挙させるための AI 呼び出しパラメータを構築する実装。
- 対象所見、既知の妥当理由、既知の反証理由を補助文脈として渡し、oracle file を根拠に重複しない反証理由だけを返すよう促す prompt を組み立てる。
- 呼び出しモデル、推論努力、ファイルアクセス制約、Structured Output schema の対応先を含むパラメータ生成の入口になる。

## Read this when
- `cmoc eval-oracle` のうち、所見を否定する理由を探す側の prompt 内容や AI 呼び出し条件を確認・変更したいとき。
- 対象所見や既知理由が prompt 内でどのように渡されるか、既存理由との重複回避や oracle file 根拠要求がどこで指定されるかを確認したいとき。
- レビュー所見検証用の challenger 側で使うモデル種別、推論努力、ファイルアクセスモード、出力 schema の対応関係を追いたいとき。

## Do not read this when
- 所見が妥当である理由を列挙する advocate 側の prompt 構築を確認したいとき。
- `cmoc eval-oracle` 以外のサブコマンド、またはレビュー所見検証以外の prompt 構築を調べたいとき。
- 生成された反証理由の JSON schema 自体や、oracle file の本文仕様を確認したいだけのとき。

## hash
- 7d570ad55da8b075ec961e68e9c48b8a8f0e69251f36878c338e8df423b0ba3f
