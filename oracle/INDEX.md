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
- cmoc の正本仕様断片のうち、プログラミング言語・設定ファイルで記述された oracle src をまとめる階層。AI エージェント呼び出し、基礎データ構造、リポジトリ永続設定など、実装として表された正本仕様断片へ進む入口になる。
- 呼び出し prompt・補助文脈・Structured Output 契約・file access mode、root token と実パスの相互変換、構造化文書モデル、cmoc 設定の項目・既定値・JSON 保存仕様などを確認するための領域。
- 自然言語の仕様文書やテストではなく、cmoc 内部で共有される型・設定・パラメータ構築・標準プロンプト部品など、実装形式で管理される oracle file を読むための階層。

## Read this when
- oracle file のうち、実装または設定ファイルとして書かれた正本仕様断片を起点に、cmoc の基本型、パス語彙、設定構造、AI 呼び出しパラメータの仕様を確認したいとき。
- AI エージェント呼び出しで渡す prompt 構成、補助文脈、読み取り・編集権限、モデル種別、reasoning effort、Structured Output schema の扱いを調べたいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` の意味や、root token 付きパス表記と実パスの変換規則を確認したいとき。
- AgentCallParameter、StructDoc、Markdown 描画 helper、oracle / realization の基本概念など、複数領域から参照される基礎的な実装仕様を確認したいとき。
- リポジトリごとに永続化される cmoc 設定、Codex CLI 向け設定、apply fork 向け設定、review oracle 向け設定の項目・既定値・保存上の扱いを確認したいとき。

## Do not read this when
- 自然言語で書かれた正本仕様断片、プロダクト方針、レビュー観点、ルーティング文書の品質基準などを確認したいときは、oracle doc 側を読む。
- oracle src の実装仕様が満たされているかを検証するテスト仕様やテストケースを確認したいときは、oracle test 側を読む。
- cmoc の実際の実装コードや自動テストを修正・確認したいときは、realization implementation または realization test 側を読む。
- CLI 引数解析、git 操作、merge、patch 適用、永続状態の読み書き、端末 UI 描画など、AI 呼び出しパラメータや基本型・設定構造ではない実行フロー本体だけを調べたいとき。
- 個別の patch 内容、merge conflict の具体的な統合判断、oracle file 本文からの所見材料など、対象本文そのものを読んで判断する作業をしたいとき。

## hash
- c3eb2698fa1cbc6a625d1383c2f7b06df65307106dc54c175ba53cb6877f3924
