# `apply`

## Summary
- `cmoc apply fork` の fork 適用フローで AI agent に渡す prompt と Structured Output schema をまとめる領域。
- realization file の所見列挙、所見リストの精査、所見を修正担当 agent に渡す呼び出し、適用後差分の人間向け変更要約生成への入口になる。
- fork 作成や git 操作そのものではなく、apply fork のレビュー所見処理と作業レポート用変更要約に関する agent 呼び出し条件・アクセス制約・出力契約を確認するための下位要素を案内する。

## Read this when
- `cmoc apply fork` で、ファイルを起点に実装所見を列挙し、重複・矛盾・False-Positive を整理した所見リストへ精査する prompt や schema を確認したいとき。
- 精査済みの所見本文を、realization file の修正担当 agent に渡す際の prompt、所見本文の扱い、realization write 権限、git 操作禁止などの制約を確認したいとき。
- fork 適用後の作業レポートに載せる変更要約について、git diff 入力、要約生成 prompt、読み取り専用の agent 呼び出し、カテゴリ別変更要約の schema を確認したいとき。
- 所見リストまたは変更要約の Structured Output schema が、apply fork 系のどの agent 呼び出しで使われるかを追いたいとき。

## Do not read this when
- `cmoc apply fork` の CLI 解析、fork 作成、ブランチ操作、diff 取得、git コマンド実行など、agent prompt 生成や出力 schema 以外の実行フローを調べたいとき。
- oracle file、realization file、path keyword、standard、complete prompt 構築などの共通概念や共通 helper の定義を調べたいとき。
- 個別の realization file を実際にどう修正するか、パッチ内容そのもの、または実装差分の生成方法を調べたいとき。
- `cmoc apply fork` 以外のサブコマンドにおけるレビュー、要約、レポート生成の仕様を探しているとき。

## hash
- 54ce00dfcfc4ca5e9d928ac736b086f4465e7cb09f8af13dc559e753a39e1548

# `indexing`

## Summary
- INDEX.md 用エントリー生成を担う領域。出力契約を固定する schema と、対象本文・生成規則・アクセス制約を含む AI 呼び出しパラメータ構築の仕様断片を扱う。
- ルーティング文書作成担当が、エントリー生成時に AI へ渡す情報、生成結果の必須構造、読み取り専用の前提、構造化出力先の指定を確認する入口になる。

## Read this when
- INDEX.md 用エントリー生成の出力契約や、エントリーに含める情報単位を確認したいとき。
- INDEX.md エントリー生成のために AI へ渡すプロンプト、対象本文の埋め込み方、対象パスの正規化を確認・変更したいとき。
- エントリー生成時のモデル種別、推論強度、ファイルアクセス制約、構造化出力先の指定を確認・変更したいとき。
- 生成結果を検証する実装やテストで、期待する JSON 構造や AI 呼び出しパラメータの組み立てを追いたいとき。

## Do not read this when
- 個別のファイルやディレクトリについて、実際にどのような要約や読む条件を書くべきかを判断したいとき。
- INDEX.md の一般的なルーティング方針やエントリー品質基準だけを確認したいとき。
- 生成済み INDEX.md の内容や各階層のルーティング情報を確認したいだけのとき。
- cmoc の実装・テスト・CLI 挙動、パス語彙、または AI 呼び出し関連型の基礎定義を確認したいだけのとき。

## hash
- fff96c3ca0aa78f29918312fe2c2ad0d63740eb467a3281a21d54a01661d8cae

# `review`

## Summary
- `cmoc review oracle` の AI 呼び出しパラメータと Structured Output schema の正本を、レビュー工程ごとにまとめる領域。
- レビュー対象 oracle file から新規所見を列挙する工程、既存所見に対する擁護理由・反証理由を追加調査する工程、理由を踏まえて採否判定する工程、所見リストの重複や矛盾を整理する工程への入口になる。
- 各工程で prompt に渡す役割、目標、補助文脈、標準類、モデル設定、file access mode と、対応する応答 schema の意味的契約を確認できる。

## Read this when
- `cmoc review oracle` の所見生成、所見検証、採否判定、所見整理に関する prompt builder や応答契約の読む先を選びたいとき。
- oracle file を根拠にしたレビュー所見について、新規所見、擁護理由、反証理由、採否結果、整理操作のどれを確認すべきか切り分けたいとき。
- review oracle 系の AI 呼び出しで、既知所見や既知理由との重複排除、補助文脈の渡し方、Structured Output schema との接続を追いたいとき。
- oracle 標準および review oracle 標準を組み込んだ prompt 構築が、レビュー工程ごとにどう分かれているか把握したいとき。

## Do not read this when
- oracle file や realization file の一般定義、パスキーワード、oracle 標準そのものを確認したいだけのとき。
- `cmoc review oracle` 以外のサブコマンド、通常の実装担当 agent 向け prompt、INDEX.md 生成 prompt を調べたいとき。
- レビュー後の CLI 表示、永続化、集約、実行制御など、AI 呼び出しパラメータや応答 schema 以外の実装詳細を確認したいとき。
- 個別の oracle file 本文を読んで具体的な仕様上の問題を判断したいとき。

## hash
- ebcee5a3357d18805bb6d70bbc56b134668a00d0f49dc738f6185d720a193acf

# `session`

## Summary
- セッション系サブコマンド向けのエージェント呼び出しパラメータ構築仕様へ進むための領域。現時点では、セッション合流時に merge conflict marker 解消エージェントを呼び出すための prompt、対象パス解決、編集許可範囲、モデル・reasoning・ファイルアクセス設定を確認する入口になる。

## Read this when
- セッション合流処理が、merge conflict marker 解消用エージェントをどの role・summary・goal・補助 prompt で呼び出すか確認したいとき。
- conflict 対象パスを作業ルート基準の実パスへ解決し、prompt 内の対象ファイル一覧として渡す仕様を確認したいとき。
- conflict marker 解消作業に限った編集許可範囲、oracle file の扱い、git add / git commit 禁止、作業後に marker を残さない要件を確認したいとき。
- セッション合流時の conflict 解消エージェント呼び出しで使うモデルクラス、reasoning effort、ファイルアクセスモードを確認したいとき。

## Do not read this when
- セッション合流処理全体の制御フロー、merge 実行、conflict 検出、後処理を確認したいだけのとき。
- merge conflict marker の具体的な統合判断アルゴリズムや、対象ファイル本文をどう解釈して解消するかを探しているとき。
- セッション合流以外のサブコマンド向けエージェント呼び出し仕様や、汎用的な complete prompt 構築部品の仕様を確認したいとき。

## hash
- c113d4bfe14ee701ab06d7077e40ba1d21efd4bb21f740645fa0fb92beb07bc9

# `tui`

## Summary
- TUI builder 領域に属する resolve parameter 用パラメータ構築関数の正本実装断片を収めるディレクトリ。現時点の本文は、該当関数が存在し未実装 stub として置かれていることだけを示す。

## Read this when
- TUI の resolve parameter に対応する builder 側の正本断片を確認したいとき。
- TUI builder 配下に resolve parameter 用パラメータ構築関数が用意されているか、また現時点で未実装扱いかを確認したいとき。

## Do not read this when
- TUI の resolve parameter の具体的な入力、出力、制御、エラー処理を調べたいとき。このディレクトリの本文からはまだ読み取れない。
- ACP 全体の builder 設計や、TUI 以外の builder 領域を調べたいとき。より直接その対象を述べる正本断片を読む。

## hash
- 3ee331b739122c1e4e63e0b7852a08045d665df4f68e5eab5c43838199d91c45
