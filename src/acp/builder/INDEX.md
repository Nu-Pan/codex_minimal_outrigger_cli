# `apply`

## Summary
- `cmoc apply` 配下で、サブコマンド実行前後の検証・準備・適用・後処理を組み立てる builder 群を扱う領域。fork 名や worktree path の検証、prompt/approval/rename 設定、run-root 適用、worktree の git 状態確認、引き継ぎ付きの継続入力生成など、apply 系処理の実行材料を作る入口になる。
- 個別サブコマンドの本体制御ではなく、apply 実行に必要な入力値・プロンプト・状態検証・補助出力をどのように作るかを確認するための領域。

## Read this when
- `cmoc apply` の各処理で、fork 名、対象 path、run-root、worktree、uncommitted change、merge 済み branch などの検証条件や失敗時メッセージを確認・変更したいとき。
- apply 系サブコマンドがエージェントに渡す prompt、approval 設定、sandbox 設定、model effort、構造化出力、作業完了後の引き継ぎ文面を確認・変更したいとき。
- `cmoc apply` が oracle file と realization file の対応、rename 指示、review 所見、git diff、実行ログなどをどのように補助入力として組み立てるかを追いたいとき。
- apply 実行前後に必要な worktree 状態確認、ブランチ適用、実行結果の要約、継続作業用の入力生成など、複数の apply 系処理で使う builder の責務境界を確認したいとき。

## Do not read this when
- `cmoc apply` の CLI 引数定義、サブコマンド選択、全体の制御フロー、複数 builder の呼び出し順を調べたいとき。
- AI 呼び出し基盤、共通 prompt 部品、Markdown レンダリング、Structured Output 実行そのもの、低レベルの path model や git command wrapper の実装を確認したいとき。
- apply 以外のサブコマンドの builder、prompt、schema、実行設定を調べたいとき。
- 実際のファイル編集アルゴリズム、差分分類の中身、git merge や worktree 操作の低レベル手順だけを確認したいとき。

## hash
- 744eb0a9ce32e59348c311dba838c9bc54bf55aaf6cd9aca35a375e3087a7be7

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
- `cmoc session join` で見つかった merge conflict marker を別の AI エージェントに解消させるための呼び出しパラメータを構築する領域。
- 解消対象ファイルの実パス化、対象一覧を含む補助プロンプト、完了条件、編集制約、oracle file への限定的な例外、モデル種別、reasoning 設定、ファイルアクセス方針をまとめて渡す入口になる。
- 通常の join 実行処理ではなく、conflict marker 解消タスクの依頼文とエージェント実行条件を確認するための下位要素へ進む場所。

## Read this when
- `cmoc session join` で検出された merge conflict marker の解消を AI エージェントへ依頼する際の呼び出し内容を確認・変更したいとき。
- conflict 解消対象パスの解決方法、対象一覧の渡し方、作業範囲、完了条件、commit 禁止、marker 残存禁止などをプロンプトへどう含めるか調べたいとき。
- 通常は編集禁止の oracle file に conflict marker がある場合だけ、conflict 解消に必要な最小限の編集を許可する扱いを確認したいとき。
- merge conflict 解消タスクで使う role、summary、goal、補助プロンプト、モデルクラス、reasoning effort、ファイルアクセスモードを調整したいとき。

## Do not read this when
- `cmoc session join` の通常の join 処理、git 操作、branch 操作、worktree 操作を調べたいとき。
- merge conflict marker の検出処理そのもの、または検出後の join 全体の制御フローを調べたいとき。
- conflict marker を実際に解消するアルゴリズム、解消後の検証、テスト実行、残存 marker チェックを探しているとき。
- 汎用的な prompt rendering、構造化ドキュメント表現、path model、work root 解決、実パス解決の詳細仕様を調べたいとき。

## hash
- 9c349137de9dd93d9b9206760be2310b902102e349c94b45d6be693497c0ef57

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
