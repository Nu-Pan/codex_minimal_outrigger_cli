# `doc`

## Summary
- cmoc の正本仕様断片のうち、自然言語で書かれた oracle doc 群への入口。利用者に見える CLI 挙動、branch / worktree モデル、開発時の横断規則、採用しなかった設計案と判断背景を扱う。
- 実装・テストへ進む前に、確認したい内容がアプリケーション外部仕様、git 隔離モデル、開発規約、設計判断の背景のどれに当たるかを切り分けるための領域である。

## Read this when
- cmoc のサブコマンド、セッション状態、run 隔離、インデクシング、Codex CLI 呼び出し、ログ、エラー処理など、利用者向け CLI 挙動や共通規約を確認したいとき。
- session branch、run branch、linked worktree、fork / join commit、cmoc-managed branch など、cmoc が扱う git branch / commit / worktree のモデルを確認したいとき。
- Python 実装、CLI 構成、共通処理の配置、開発環境、依存追加、pytest による決定論的テストなど、realization code を追加・修正・検証する際の横断的な開発規則を確認したいとき。
- AI の記憶・改善案・作業計画、apply 系 orchestration など、採用しなかった workflow や設計案の non-goal と判断背景を確認したいとき。
- 正本仕様断片を根拠に実装やテストを進める前に、自然言語仕様として読むべき本文の候補を絞りたいとき。

## Do not read this when
- oracle file、realization file、oracle doc / src / test、realization implementation / test / ancillary など、cmoc 全体の基本分類だけを確認したいとき。
- path keyword、repo root、run root、work root など、パスモデルの定義だけを確認したいとき。
- 特定の実装ファイル、関数、テスト、builder、schema、既存 helper の内部構造や現在の実装詳細だけを調べたいとき。
- 既に読むべき個別仕様本文が特定できており、その詳細だけを確認すればよいとき。
- INDEX.md エントリーの作成基準、oracle / realization の一般原則、正本仕様断片としての文書品質基準そのものを確認したいだけのとき。

## hash
- 74314ba3100906ba48fa0f54cef11a0edbf22079618f480e213f4661eb5a4cd0

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
