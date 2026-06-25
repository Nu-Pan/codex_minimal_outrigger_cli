# `apply`

## Summary
- `cmoc apply fork` の fork 適用工程で使う AI エージェント呼び出しパラメータと Structured Output schema の正本断片をまとめる領域。
- 適用後差分の変更要約、realization file の要修正所見列挙、検出済み所見への修正依頼など、fork 適用時のレビュー・報告・修正支援に関わる入出力契約と prompt 構成を扱う。
- 実際の branch 操作や patch 適用ではなく、fork 適用フロー内で AI に何を読ませ、どの role・goal・制約・出力 schema で呼び出すかを確認する入口となる。

## Read this when
- `cmoc apply fork` で、適用後差分の変更要約、実装調査の所見列挙、所見対応修正依頼に使う AI 呼び出しの構成を確認したいとき。
- fork 適用後のレビューや作業レポートで、差分要約や所見リストの Structured Output schema と prompt 側の対応を確認したいとき。
- oracle file、realization file、起点パス、差分テキスト、検出済み所見を AI エージェント呼び出しへどう渡すかを調べたいとき。
- apply review standard や realization standard を含む読み取り専用調査、または修正作業用のファイルアクセス権・モデル種別・推論努力量の指定を確認したいとき。

## Do not read this when
- `cmoc apply fork` の CLI 引数解析、サブコマンド登録、branch 作成、git 操作、差分取得、patch 適用などの実行フロー本体を調べたいとき。
- 個別ファイルの patch 内容そのものや、実際に realization file をどう修正するかという修正ロジックを探しているとき。
- oracle standard、realization standard、apply review standard、path 語彙、共通 prompt 部品、AgentCallParameter 型定義そのものを確認したいとき。
- INDEX.md 用エントリーや一般的なルーティング文書の書き方を確認したいとき。

## hash
- 9b3736053b7c27af9ce3aedde50c576f7638c51774f5437e04388828fcc7c0f0

# `indexing`

## Summary
- INDEX.md エントリー生成に関する出力契約と、対象内容からエージェント呼び出しパラメータを組み立てる prompt 正本を扱う。
- ルーティングエントリーに含める情報単位の固定と、既存目次を根拠にせず対象本文からエントリーを生成させる制約を確認する入口になる。

## Read this when
- INDEX.md エントリー生成の出力形式、必須要素、余分な項目を許可しない契約を確認したいとき。
- cmoc indexing が目次情報生成用エージェントに渡す prompt 内容、モデル種別、推論量、読み取り専用アクセス、出力 schema 指定を確認したいとき。
- 対象パスと対象内容を、INDEX.md 用エントリー生成 prompt にどう埋め込むかを確認したいとき。
- 生成された INDEX.md エントリーを検証する実装やテストで、期待される JSON 構造と呼び出し条件を確認したいとき。

## Do not read this when
- 個別の対象について、実際にどの要約や読む条件を書くべきかを判断したいとき。
- INDEX.md 全体のルーティング方針、記述品質基準、またはエントリー生成結果の内容評価を確認したいとき。
- パスキーワードや実パス解決の概念定義そのものを確認したいとき。
- cmoc indexing 全体の走査、ファイル発見、INDEX 更新処理、CLI 引数処理を確認したいとき。

## hash
- 9fa9555cb34bb7d3b900c7bd72c5a5497aeca97dc2010f5ba8bb182e9f431f72

# `review`

## Summary
- `cmoc review oracle` で oracle file をレビューする AI 呼び出し群の仕様断片。新規所見の列挙、所見を擁護・反証する理由の追加調査、人間へ提示するかの採否判定、所見リスト内の重複・矛盾整理について、prompt 構築、補助文脈、読み取り権限、モデル設定、Structured Output 契約への接続を扱う。
- レビュー対象 oracle file、関連 oracle file、既知所見、既知の擁護理由・反証理由、入力済み所見リストを各段階の補助文脈として渡し、既知情報と重複しない新規情報だけを返す境界や、該当項目がない場合に空配列を返す境界を定める入口になる。

## Read this when
- `cmoc review oracle` の AI 呼び出しが、所見生成、理由検証、採否判定、所見整理のどの段階で何を入力し何を返すか確認したいとき。
- レビュー対象 oracle file から新規所見を列挙し、既知の関連所見との差分を保つ prompt と出力契約を確認したいとき。
- 対象所見について、妥当である理由または妥当ではない理由を、既知理由と重複しない単位で oracle file に基づいて追加調査する境界を確認したいとき。
- 擁護理由と反証理由を踏まえて、所見を人間へ提示すべきか判定する AI 呼び出しの入力と判定結果の契約を確認したいとき。
- 複数の所見に含まれる内容的な重複や相互矛盾を、削除・置換・統合の編集操作として整理する契約を確認したいとき。
- review oracle 系の prompt に、oracle 標準、review oracle 標準、純粋 oracle 読み取りモード、reasoning effort、モデル種別、Structured Output schema がどう組み込まれるか追いたいとき。

## Do not read this when
- oracle file と realization file の基本定義、oracle 標準、review oracle 標準そのものの本文を確認したいだけのとき。
- 通常の実装担当 agent、INDEX.md 生成、または oracle review 以外のサブコマンド向け prompt を確認したいとき。
- レビュー所見の保存、集約、CLI 表示、永続状態、編集操作の実行など、AI 呼び出しパラメータと応答 schema 以外の実装を調べたいとき。
- 個別の oracle file 本文を読んで、具体的な所見や理由の根拠材料を探したいとき。
- 共通 prompt 部品、Markdown 構造化描画、path 解決、AgentCallParameter、file access mode の一般仕様だけを確認したいとき。

## hash
- 8585468de6b3af4848231fc90f9f1fd7299d204d08763f59c619545f1c036dab

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
- TUI サブコマンドで、ユーザー入力プロンプトを AI Agent CLI/TUI に渡す前に実行パラメータを選定するための正本仕様断片を扱う。
- 元プロンプト、リポジトリ・作業ルート、論理ファイルアクセスモード説明、各種標準文書を統合した読み取り専用の判定用プロンプトと、その判定結果のデータ契約を確認する入口になる。

## Read this when
- TUI 実行前に、AI Agent CLI/TUI へ渡すモデル種別、推論強度、論理ファイルアクセスモード、出力先の選定方針を確認したいとき。
- ユーザーが入力した元プロンプトを、実行パラメータ選定担当向けの complete prompt にどう埋め込むか確認したいとき。
- TUI のパラメータ解決で、oracle と realization の基本、各種標準文書、ファイルアクセスモード説明を prompt に含める条件を確認したいとき。
- プロンプト解析結果として、必要な論理ファイルアクセス範囲や読むべき標準文書群を値と理由の組で返す契約を確認したいとき。

## Do not read this when
- 実際に AI Agent CLI/TUI プロセスを起動する処理、端末 UI の描画、エディタ入力の取得、コメント除去の実装を探しているとき。
- path キーワード、リポジトリルート、作業ルートの定義そのものを確認したいとき。
- ファイルアクセスモードごとの説明文生成、complete prompt の共通構成、各標準本文そのものを変更したいとき。
- 個別作業に必要な標準の内容を読みたいとき。この対象は標準本文ではなく、標準を読む必要性を判定するための TUI 側入口を扱う。
- TUI 以外のサブコマンドにおける実行パラメータ解決を調べているとき。

## hash
- 8006f473686ea8b0e7872274bb8487a8394120c1c65e61533eca00778e5777a7
