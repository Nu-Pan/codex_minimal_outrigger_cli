# `doc`

## Summary
- cmoc の正本仕様断片のうち、自然言語 Markdown で書かれた仕様文書群への入口。利用者に見える CLI 挙動、session/run の branch・worktree モデル、Codex CLI 呼び出し、ログ、エラー処理、状態、インデクシング、開発時の実装・テスト規則、採用しなかった設計案の判断背景を扱う。
- ここに含まれる文書は、実装やテストを直接読む前に、人間が責任を持つ仕様判断、公開挙動、実装者である AI に任せてよい範囲、過去に退けた workflow や状態管理方針を確認するための正本側の入口である。
- 下位領域は、アプリケーション外部仕様、branch/worktree 用語、開発規則、不採用案の背景に分かれるため、cmoc 全体の仕様判断から個別サブコマンドや開発ルールへ読み先を絞る起点として使う。

## Read this when
- cmoc の CLI としての利用手順、サブコマンドの外部挙動、標準 workflow、stdout・stderr・ログ・エラー処理、Structured Output、Codex CLI 呼び出し規約を確認したいとき。
- session branch、session home branch、run branch、linked worktree、fork/join commit、cmoc-managed branch など、session/run の git モデルと隔離単位を実装・修正・テストする前。
- oracle を正本として realization を追従させる開発で、Python 実装、CLI 構成、共通処理配置、開発環境、pytest による決定論的テストの方針を確認したいとき。
- インデクシング、agent call 前後の制御、prompt 方針、session/apply 状態、run 隔離、quota 待機や resume など、複数機能にまたがる横断仕様を読む必要があるとき。
- AI-generated kaizen、作業計画レビュー、apply 系 orchestration などの設計を再検討しており、なぜ採用しなかったのか、人間の認知負荷や暗黙仕様化をどう避ける方針なのかを確認したいとき。

## Do not read this when
- oracle file と realization file の基本的な定義、所有者、編集権限、正本仕様断片としての位置づけだけを確認したいとき。
- パスキーワードや root model の実装上の定義そのもの、またはプログラムとしての path utility の詳細を調べたいとき。
- 特定の実装ファイル、関数、クラス、テスト fixture、現在の内部ロジックだけを調べたいときは、正本仕様ではなく realization 側の該当箇所を直接読む。
- oracle src や oracle test に置かれたプログラム・設定・テスト形式の正本断片そのものを確認したいとき。
- 既に対象の個別サブコマンド、ログ仕様、状態 schema、開発規則、不採用判断の範囲が明確で、下位の該当本文へ直接進めるとき。

## hash
- 38e2ec1f89238683a19417f7e05b17fdfa1178e588e1767d30052737e32a7af8

# `src`

## Summary
- cmoc の正本仕様断片のうち、プログラミング言語や設定ファイルとして書かれた仕様実装をまとめる階層。AI エージェント呼び出しパラメータ構築、標準プロンプト部品、共通基礎型、パス語彙、構造化 Markdown 生成、リポジトリ単位設定の仕様へ進む入口になる。
- サブコマンド別に AI へ渡す role、summary、goal、補助文脈、ファイルアクセス権限、モデル種別、reasoning effort、Structured Output schema の対応を確認するための領域である。
- CLI の実行制御そのものや git 操作そのものではなく、それらの処理から参照される正本仕様断片、共通値、標準文面、保存される設定構造を確認するための階層である。

## Read this when
- cmoc の処理が AI エージェントを呼び出す場面で、呼び出しパラメータ、prompt 構成、補助文脈、権限モード、モデル種別、reasoning effort、Structured Output schema の仕様を確認したいとき。
- apply fork、review oracle、indexing、session join、tui などの AI 呼び出しで、どの標準文面や入力情報を組み込み、どの応答契約を期待するかを調べたいとき。
- ファイルアクセス規則、ルーティング規則、oracle / realization の基本概念、oracle standard、realization standard、review / apply / index entry 向け standard を prompt 部品としてどう構築するかを確認したいとき。
- cmoc 内部で共有される論理モデル種別、reasoning effort、ファイルアクセスモード、AgentCallParameter、root token と実パスの変換、構造化文書レンダリング、規範文書のデータ構造を確認したいとき。
- 開発対象リポジトリごとに永続化される設定の構造、既定値、Codex CLI 向けのモデル・reasoning effort 対応、apply fork や review oracle の処理上限を確認したいとき。

## Do not read this when
- CLI 引数解析、サブコマンド登録、プロセス制御、git branch・merge・diff・patch 操作、永続状態の読み書き、端末 UI 描画など、AI 呼び出しパラメータ構築以外の実行フロー本体を調べたいとき。
- oracle doc の自然言語仕様本文、oracle test のテスト仕様、または realization 側の実装・テストを直接確認したいとき。
- 個別の patch 内容、merge conflict の意味的な統合判断、所見の妥当性、実装修正方針など、対象ファイル本文や差分そのものを読んで判断する作業をしたいとき。
- 設定ファイルの実行時ロード・保存処理、JSON 変換実装、設定同期コマンドの制御フローだけを確認したいとき。
- INDEX.md 全体のルーティング文書としての書き方やエントリー品質基準だけを確認したい場合で、prompt 部品としての組み込み仕様を読む必要がないとき。

## hash
- 721648fe44fd811a8a25a71e331cb9c156af1a89696628a9ea6fd7f89e782d25
