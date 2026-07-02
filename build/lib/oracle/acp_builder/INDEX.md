# `apply`

## Summary
- `cmoc apply` の apply fork 系領域における正本 prompt 断片と Structured Output schema への入口。
- 差分要約、ファイル単位レビュー、所見対応修正の agent call parameter に関する role、goal、制約、model class、reasoning effort、file access mode を扱う下位領域へ進むために読む。
- 変更要約やレビュー所見を機械処理可能な JSON として受け渡す出力契約を確認する起点となる。

## Read this when
- `cmoc apply fork` が差分要約、ファイル単位レビュー、所見対応修正の agent call parameter をどう組み立てるか確認したいとき。
- 作業レポート向けの変更要約や、実装と oracle requirement の不一致を表すレビュー所見の Structured Output schema を確認したいとき。
- apply fork 系 agent に渡す readonly/write 権限、git 操作禁止、所見の扱い、placeholder、補助 prompt、model class、reasoning effort の正本を確認または変更したいとき。

## Do not read this when
- `cmoc apply fork` 全体の実行制御、fork 作成、branch 操作、git 操作、状態管理、所見統合の実装を調べたいとき。
- complete prompt の共通組み立て規則、Structured markdown 描画、path placeholder 解決の一般仕様を調べたいとき。
- 特定の realization file の実装内容、変更内容そのものの妥当性、または oracle file / realization file の基本定義やレビュー判断基準を確認したいとき。

## hash
- ed94803ad5d77258b314369feaca06f500f24218ad9e9bbc488b774830cb1360

# `basic.py`

## Summary
- AI コーディングエージェント呼び出しに使う論理モデルクラス、reasoning effort、ファイルアクセスモード、および呼び出しパラメータのデータ構造を定義する oracle src。
- バックエンド固有のモデル名や reasoning effort 名ではなく、cmoc 内部で扱う抽象的な選択肢と、プロンプト・Structured Output schema path を含む呼び出し単位の入力を示す。

## Read this when
- agent call parameter の正本側定義を確認したいとき。
- モデル選択、reasoning effort、ファイルアクセスモードの論理区分を参照したいとき。
- AI コーディングエージェント呼び出しに渡すパラメータ構造を実装・テストへ反映したいとき。
- Structured Output を要求する呼び出しと要求しない呼び出しで、schema path をどう表すか確認したいとき。

## Do not read this when
- バックエンドが実際に受理するモデル名や reasoning effort 名への変換処理を確認したいとき。
- 各ファイルアクセスモードが生成する具体的なアクセスルール本文を確認したいとき。
- agent call の実行手順、プロセス起動、結果処理、永続状態の扱いを確認したいとき。

## hash
- c2a86abaffb6201c6e5a3f5ee4490bde862d4a6a1e4ae82494c650de9ea0c5f1

# `common`

## Summary
- ファイルアクセス規則違反が発生した agent call を復旧するための再実行用 agent call parameter を組み立てる実装。
- 違反時のアクセス規則、違反ファイル一覧、発生ログをプロンプトへ埋め込み、違反解消と元の作業目的維持を依頼する呼び出し設定を返す。

## Read this when
- ファイルアクセス規則違反を検出した後、その違反を解消するための agent call parameter の内容や生成条件を確認したいとき。
- 違反したアクセス規則、違反ファイル一覧、発生ログ情報をどのように復旧プロンプトへ渡すかを確認したいとき。
- 復旧担当 agent の role、summary、goal、file access mode、model class、reasoning effort の組み立てを変更したいとき。

## Do not read this when
- 通常の agent call parameter 全般の型定義や列挙値を確認したいとき。
- ファイルアクセス規則そのものの文面生成や各 access mode の仕様を確認したいとき。
- 完全なプロンプトを組み立てる共通処理や markdown rendering の詳細を確認したいとき。
- path placeholder の一般的な解決規則を確認したいとき。

## hash
- aa0cf4155c8698ad5a1e7937e37b09bf5017b83803a4f6ee4358c3818f47aef9

# `indexing`

## Summary
- 目次エントリー生成に必要な Structured Output schema と、その schema を用いた AI エージェント呼び出しパラメータ生成を扱う領域。
- 対象内容からエントリー本文を作るための役割設定、読み取り制約、対象本文の埋め込み、出力形式指定、低推論設定を組み立てる実装への入口になる。

## Read this when
- 目次エントリー生成用の agent call parameter がどのように作られるかを確認または変更したいとき。
- 目次エントリー生成結果に必要な項目や値の型を検証したいとき。
- 生成 prompt に含める役割、目的、既存目次を読まない制約、対象本文の渡し方、placeholder 解決、出力 schema 指定を調整したいとき。
- 目次情報生成処理の model class、reasoning effort、file access mode などの呼び出し設定を確認したいとき。

## Do not read this when
- 実際の目次エントリー本文の品質基準や書き方だけを確認したいときは、その基準を定義している文書を直接読む。
- placeholder の意味や実パス解決の仕様だけを調べたいときは、path model 側を読む。
- agent call parameter の共通データ構造や enum 定義そのものを確認したいときは、builder の基本定義を読む。
- 特定ファイルやディレクトリの実際のルーティング文言を知りたいときは、その対象の目次または本文を読む。

## hash
- d51330668664fb862d91e335e32b1a32b42475bb69d3bdc4aa24ffd94e26e446

# `review`

## Summary
- oracle file レビュー用の agent call parameter 正本と Structured Output schema を扱う領域。新規所見の生成、擁護・反証理由の調査、採否判定、所見リスト整理の prompt 構成と出力契約を確認する入口となる。

## Read this when
- oracle file レビューで AI エージェントへ渡す role、goal、補助 prompt、file access mode、model class、reasoning effort、placeholder、標準文脈、出力 schema の対応を確認または変更したいとき。
- oracle file レビュー所見の生成、擁護理由調査、反証理由調査、採否判定、重複・矛盾整理の入出力契約や prompt 構成を確認したいとき。
- 既知所見や既知理由との重複排除、新規所見・新規理由がない場合の表現、所見に必要な重大度・見出し・根拠 oracle file・理由の制約を確認したいとき。

## Do not read this when
- oracle file 本体の仕様内容や、レビュー基準本文そのものを確認したいとき。
- oracle file レビュー以外の review サブコマンドや、oracle review 以外の agent call parameter を調べたいとき。
- agent call parameter の共通データ構造、path placeholder 解決、完全 prompt 構築処理、構造化 markdown rendering などの汎用実装詳細を調べたいとき。
- INDEX.md 用エントリーの生成形式やルーティング方針を確認したいだけのとき。

## hash
- c1d362b9486c12d08cdeeb6b7fb4242f123c881cde1be590d4cac45b78715a5c

# `session`

## Summary
- `cmoc session join` の conflict marker 解消を AI エージェントへ依頼するための agent call parameter 構築を扱う。conflict 対象パスの実パス解決、対象ファイル一覧、追加アクセス規則、oracle/realization 標準を含む prompt、model・reasoning・file access mode の指定を確認する入口。

## Read this when
- `cmoc session join` で conflict marker 解消用エージェントを呼び出す prompt、role、summary、goal の内容を確認したいとき。
- conflict 解消時に oracle file の最小編集を例外的に許可する条件や、git add・git commit を禁止するアクセス規則を確認したいとき。
- conflicted_paths から prompt に提示する対象ファイル一覧を作る処理や、生成される AgentCallParameter の model・reasoning・file access mode を確認したいとき。

## Do not read this when
- `cmoc session join` 全体の制御フロー、merge 実行、conflict 検出、解消結果の取り込みを確認したいとき。
- merge conflict marker の具体的な解消アルゴリズムや、個別ファイル内容をどうマージするかを確認したいとき。
- agent call parameter の基礎データ構造、prompt builder、パスモデルの定義を確認したいとき。

## hash
- 5dc03a6d4d7dcfc4fc12587f89087b97a8c4dc33fc87702c61e29949f605cd0d

# `tui`

## Summary
- AI Agent CLI/TUI の TUI 起動前後で使うエージェント呼び出しパラメータの正本実装と出力契約を扱う領域。ユーザー入力プロンプトから実行時パラメータを解決する prompt、TUI 起動用 prompt、Structured Output schema の対応を確認する入口になる。

## Read this when
- TUI 経由の実行で、元プロンプトからモデル種別、reasoning effort、論理ファイルアクセスモード、Structured Output schema、または標準 prompt の有効化状態をどう決めるか確認・変更したいとき。
- TUI 起動時の AI エージェント呼び出しパラメータがどの入力から構成され、どのように complete prompt 化され、どこへ保存され、どの JSON 契約に対応するかを追いたいとき。
- role、summary、goal、file_access_mode、および oracle・realization・review・index 関連標準を読むべきかどうかの判定結果を返す契約を実装・検証したいとき。

## Do not read this when
- TUI 以外のサブコマンド、作業実行 prompt、レビュー prompt のエージェント呼び出しパラメータを調べたいとき。
- TUI 画面制御、エディタ起動、ユーザー入力のコメント除去や strip 処理を調べたいとき。
- 各標準本文、complete prompt の汎用構築規則、placeholder 解決、パスキーワード、リポジトリルート解決、または実際のサンドボックス制御だけを調べたいとき。

## hash
- f540871e572338ab0dd82881d53f82f2754d59a44efe3a4c0b208430927cc39c
