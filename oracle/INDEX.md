# `doc`

## Summary
- 自然言語の markdown で書かれた cmoc の正本仕様断片を集める領域です。利用者向け CLI 挙動、サブコマンドの事前条件・状態遷移・出力、Codex CLI 呼び出し、ログ、エラー処理、インデクシング、run 隔離、session state、branch / worktree モデル、開発時の実装・テスト規則を確認する入口になります。
- 採用済み仕様だけでなく、AI 記憶の自動注入、作業計画レビュー、apply orchestration などの不採用案と判断背景も含むため、現在の workflow や責務分担を変更する前に設計意図を確認する場所でもあります。
- 個別サブコマンド仕様と横断仕様、開発規則、不採用案が分かれているため、cmoc の公開挙動を実装へ反映する作業と、realization code の書き方を判断する作業の両方で、読むべき正本仕様断片を選ぶ起点になります。

## Read this when
- cmoc の CLI としての外部挙動、標準 workflow、session fork / join、apply fork / join / abandon、review oracle、init、tui、明示的な indexing 実行などのサブコマンド仕様を確認したいとき。
- Codex CLI 呼び出し、Structured Output、ログ保存、エラー処理、プロンプト規範、run 隔離、session state、INDEX.md 自動生成など、複数機能から参照される横断的なアプリケーション規約を実装・修正・テストするとき。
- session branch、session home branch、run branch、linked worktree、fork / join commit など、cmoc が git branch / commit / worktree をどう扱うか確認したいとき。
- Python 実装、CLI 構成、共通処理配置、開発環境、pytest による自動テストなど、realization code を追加・変更する際の共通開発規則を確認したいとき。
- AI の継続的な記憶、kaizen 自動注入、作業計画レビュー、apply の並列所見リストアップや所見単位修正など、過去に採用しなかった workflow や orchestration を再検討するとき。
- 採用済みの正本仕様断片と不採用案の背景を読み分けながら、cmoc の公開面、状態管理、agent call 境界、人間と AI の責務分担を判断したいとき。

## Do not read this when
- oracle file と realization file の基本的な定義、所有責任、編集可否、正本仕様断片としての一般原則だけを確認したいとき。
- path keyword や root model の定義そのもの、またはパス解決用の実装詳細だけを確認したいとき。
- AgentCallParameter builder が生成する具体的な schema やパラメータ内容、または oracle src / oracle test に書かれた実行可能な仕様を直接確認したいとき。
- 特定の realization implementation や realization test の現在の関数、クラス、helper、既存テスト期待値など、実装側の具体的なコード構造だけを調べたいとき。
- INDEX.md エントリーの書き方、ルーティング文書一般の品質基準、oracle / realization 全体の記述標準だけを確認したいとき。
- Codex CLI や LLM の実際の応答品質、生成結果の妥当性、または一般的なツール利用方法を評価したいだけで、cmoc 固有の正本仕様断片を必要としていないとき。

## hash
- 9a59a718e772f9232e681e7ffd595c7923581b9dac80e07c5b0e224e4dde2033

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
