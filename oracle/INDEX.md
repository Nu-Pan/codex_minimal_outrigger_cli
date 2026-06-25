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
- `oracle/src` は、自然言語の正本仕様断片を支える oracle source の入口であり、AI エージェント呼び出しパラメータ、プロンプト部品、共通データモデル、パス語彙、構造化 Markdown 生成、リポジトリ単位設定の正本実装をまとめる階層。
- サブコマンド処理そのものではなく、cmoc がどの論理モデル・reasoning effort・ファイルアクセスモード・Structured Output schema・標準文面・設定既定値を前提にするかを確認するための領域。
- 下位には、AI 呼び出し prompt と応答契約を扱う領域、複数領域から参照される基礎型と helper を扱う領域、開発対象リポジトリごとの設定構造を扱う領域がある。

## Read this when
- AI エージェント呼び出しの prompt 構成、モデル選択、reasoning effort、ファイルアクセスモード、Structured Output schema、または標準プロンプト部品の正本仕様断片を確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` のパス表記、実パス解決、worktree root 検出、構造化文書の Markdown 描画、standard 表現など、複数機能の前提になる基礎モデルを確認したいとき。
- 開発対象リポジトリごとに永続化される cmoc 設定の構造、既定値、Codex CLI 向けモデル名・reasoning effort 名の対応、apply fork や review oracle の処理予算を確認したいとき。
- indexing、apply fork、review oracle、session join、tui などで、実行フローが AI に渡す入力境界と期待する応答境界を調べたいとき。

## Do not read this when
- CLI 引数解析、サブコマンド登録、git 操作、merge 実行、patch 適用、永続状態の実際の読み書き、端末 UI 描画など、AI 呼び出しパラメータや基礎仕様ではない実行フロー本体を調べたいとき。
- oracle doc や oracle test の本文、個別仕様レビューの所見材料、realization file の修正対象など、正本仕様断片や実装対象そのものの内容判断をしたいとき。
- 既に確認したい下位領域が AI 呼び出し、基礎モデル、設定仕様のいずれかに絞れており、その下位項目へ直接進めるとき。
- 既存 `INDEX.md` の記述方針やルーティング文書全体の構成だけを確認したいとき。

## hash
- 9e9f0cf86be8634215ead0e24e19c54b86f94798f538628b4374e2456c4963e3
