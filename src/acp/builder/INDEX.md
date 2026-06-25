# `apply`

## Summary
- `cmoc apply fork` の適用・レビュー工程で使う AI 呼び出しパラメータ群と、その入出力に使う構造化スキーマをまとめる領域。ファイル単位の所見列挙、所見リストの整理、所見に基づく realization file 修正、作業後の差分要約という一連のエージェント呼び出し条件を確認する入口になる。
- 各呼び出しでは、対象パスや git diff、所見リスト、個別所見を補助プロンプトに埋め込み、参照する標準、ファイルアクセス権限、モデルクラス、reasoning effort、Structured Output schema の選択を組み立てる。

## Read this when
- `cmoc apply fork` のレビュー・修正・レポート生成で、AI エージェントに渡す role、summary、goal、補助プロンプト、参照標準、ファイルアクセスモードを確認または変更したいとき。
- ファイル単位の所見列挙、集約済み所見リストの改善、個別所見への修正作業、git diff からの変更要約という各段階の呼び出し条件を追いたいとき。
- apply fork の所見一覧や変更要約が、どの Structured Output schema に従い、どの粒度の情報を保持するかを確認したいとき。
- レビュー所見を重複・矛盾・False-Positive の除去を経て作業可能な順序に整理する prompt、または所見本文を修正担当エージェントへ渡す prompt を調整したいとき。

## Do not read this when
- `cmoc apply fork` のサブコマンド登録、CLI 引数解析、branch 作成、git コマンド実行、差分取得などの実行フロー本体を調べたいとき。
- 完全プロンプトの共通組み立て処理、構造化 markdown の描画、path keyword の定義、AgentCallParameter やモデル種別などの共通型定義を変更したいとき。
- oracle file、realization file、各種 standard の本文そのものを確認したいとき。
- 実際の変更対象ファイルの内容、個別の修正コード、またはテスト実装を調べたいとき。

## hash
- e857dc5a93020e28075d60a291c6eed21cd3384dea8bfaed2c216d31657b670f

# `indexing`

## Summary
- 目次エントリー生成に必要な Structured Output schema と、その schema を使って AI 呼び出しパラメータを組み立てる実装を扱う領域。生成結果に含める意味情報の単位、対象本文を根拠にする制約、読み取り専用プロンプト、モデル設定、schema 指定までを確認する入口になる。
- 目次エントリーそのものの内容ではなく、目次エントリーを生成するための入力制約・出力制約・呼び出し設定を追うための実装まとまり。

## Read this when
- 目次エントリー生成で AI に渡す role、summary、goal、補助プロンプト、読み取り専用条件を確認または変更したいとき。
- 目次エントリー生成結果に求める意味情報の構造や必須要素を確認したいとき。
- 対象本文だけを根拠にし、既存の目次を根拠にしないという生成制約を確認したいとき。
- 目次エントリー生成用のモデル設定、reasoning effort、構造化出力 schema の指定、対象パスや対象本文の埋め込み処理を追うとき。

## Do not read this when
- 個別ファイルや個別ディレクトリの目次エントリー文面を確認または作成したいだけのとき。
- 目次探索順、読み進め方、正本仕様断片と実装ファイルの関係など、ルーティング運用全体の規則を確認したいとき。
- 実際の indexing サブコマンドの CLI 引数処理、ファイル走査、目次ファイルの読み書き処理を調べたいとき。
- 共通プロンプト構築、Markdown レンダリング、構造化ドキュメント部品など、目次エントリー生成呼び出しより下位または周辺の処理を詳しく調べたいとき。

## hash
- 3d74f86c0f07eeb37d348cf3ebd89582c24295b63d48819c6db3a347ad83f2dc

# `review`

## Summary
- レビュー系 AI 呼び出しの AgentCallParameter 構築と Structured Output schema をまとめる領域。現状は `cmoc review oracle` の oracle file レビューに特化しており、新規所見列挙、所見の肯定理由・反証理由の列挙、採否判定、所見リスト整理の各段階へ進む入口になる。
- 各段階では、対象 oracle file、対象所見、既知の関連所見、既知の肯定理由・反証理由、現状の所見リストなどを補助文脈として渡し、oracle file 読み取り専用アクセス、モデル種別、推論量、対応 schema を組み合わせた呼び出し設定を構築する。

## Read this when
- `cmoc review oracle` で、oracle file レビューのどの段階にどの AI 呼び出し設定や Structured Output schema を使うか確認したいとき。
- oracle file レビューで、新規所見、所見を妥当とする理由、所見を妥当ではないとする理由、所見の採否、所見リストの重複・矛盾解消操作の出力契約を確認したいとき。
- 対象 oracle file、関連所見、対象所見、既知の肯定理由・反証理由、現状の所見リストが、各レビュー用プロンプトへどう渡されるかを追いたいとき。
- review oracle 用プロンプトで使う役割、目標、oracle 標準・review oracle 標準、ファイルアクセスモード、モデル種別、reasoning effort、schema の対応関係を確認・変更したいとき。

## Do not read this when
- oracle file や realization file の基本概念、正本仕様断片としての一般原則、レビュー基準そのものを確認したいだけのとき。
- `cmoc review oracle` 全体の CLI 引数解析、サブコマンド登録、実行制御、結果の保存・集約・表示処理を調べたいとき。
- 汎用的な AgentCallParameter のデータ構造、共通プロンプト組み立て、構造化 markdown レンダリング、パス解決の実装詳細を調べたいとき。
- oracle file 本文の具体的な仕様内容や、個別の正本仕様断片そのものを読みたいとき。
- oracle file レビュー以外のレビュー処理、または review 以外のサブコマンドの AI 呼び出し設定を調べたいとき。

## hash
- 75efcf37f2080925b304bedbe32ffe2c4d2024d77fa1015d46cbf12e55023a85

# `session`

## Summary
- `cmoc session join` で検出された merge conflict marker を別 AI エージェントに解消させるための呼び出しパラメータを組み立てる領域。
- conflict 対象パスを実パスへ解決し、対象ファイル一覧、作業範囲、対象外編集禁止、oracle file の例外的な必要最小限編集許可、`git add` / `git commit` 禁止を含む complete prompt を生成する。
- 返却するエージェント設定は、主流モデル、中程度 reasoning、conflict 解消用の書き込み権限、生成済み Markdown prompt に固定される。

## Read this when
- `cmoc session join` の merge conflict marker 解消用エージェント呼び出しで、prompt・権限・モデル・reasoning 設定がどう決まるかを確認または変更したいとき。
- conflict 対象ファイル一覧、作業範囲、対象外ファイル編集禁止、oracle file の例外的編集許可、`git add` / `git commit` 禁止が prompt にどう埋め込まれるかを追いたいとき。
- conflict 対象として渡されたパスが、作業ルートや実パス解決を経て prompt 内の対象一覧になる流れを確認したいとき。

## Do not read this when
- 通常の `cmoc session join` の合流処理全体、git 操作、conflict 検出、join 後の状態更新を調べたいだけのとき。
- complete prompt の共通構築、構造化 Markdown レンダリング、パスモデル、ACP の基礎型そのものを調べたいとき。
- merge conflict の具体的な解消アルゴリズムや、対象ファイル本文をどう編集するべきかの方針を探しているとき。

## hash
- 2c5f65ab7fb89a2799af6c84b62bf58a98dcd9b8bb2d46d103eaeb6f88c090c8

# `tui`

## Summary
- TUI 実行前に、ユーザーの作業依頼から AI Agent CLI/TUI へ渡す実行パラメータを選定するための builder 群を扱う。
- 元プロンプト、候補となる論理ファイルアクセスモード、oracle・realization・review・INDEX.md エントリー関連標準を含む完全プロンプトを組み立て、効率重視モデル・中程度 reasoning・readonly 実行・対応 schema を指定した呼び出しパラメータへ変換する実装と、その選定結果 schema がまとまっている。
- 権限選択と標準参照要否を、理由付きの構造化出力として扱う領域への入口になる。

## Read this when
- TUI でユーザー入力を実行する前に、AI Agent CLI/TUI へ渡すモデル種別、reasoning effort、論理ファイルアクセスモード、出力 schema の選び方を確認・変更したいとき。
- ユーザーの元プロンプトを、実行パラメータ選定担当向けの完全プロンプトへどう埋め込み、どの標準群を同梱するかを確認したいとき。
- 作業依頼に対する権限選択や、oracle・realization・review・INDEX.md エントリー関連標準を読む必要があるかどうかの判定結果を、実装やテストで扱うとき。

## Do not read this when
- TUI のユーザー入力取得、コメント除去、strip、サブコマンド起動フローなど、実行パラメータ解決を呼び出す側の挙動だけを調べたいとき。
- 個々のファイルアクセスモードの規則本文そのものを確認したいとき。
- oracle file や realization file の責務、編集可否、品質基準そのもの、または INDEX.md エントリー本文の書き方だけを確認したいとき。
- 実行パラメータ選定後の実際の AI Agent CLI/TUI 実行、TUI 表示、対話フロー、ファイルシステム操作を調べたいとき。

## hash
- 313e4db46a1cb446d666a4a752425c28963d3fdaee76062389ea280ba4be8e41
