# `doc`

## Summary
- cmoc の正本仕様断片のうち、自然言語で書かれた文書群への入口。アプリケーション仕様、branch/worktree モデル、不採用案、開発規則など、実装差を避けたい判断や背景を扱う。
- CLI 挙動、サブコマンド仕様、Codex CLI 呼び出し、ログ、エラー処理、インデクシング、run 隔離、セッション状態、開発時の実装・テスト方針など、自然言語仕様から読むべき下位領域を選ぶための場所。

## Read this when
- cmoc の利用者向け挙動、状態管理、agent call 境界、ログ・出力、作業隔離、ルーティング文書生成などの仕様断片を探すとき。
- session fork / join、run branch、linked worktree、cmoc-managed branch など、git branch / commit / worktree モデルを確認したいとき。
- 機能追加や workflow 変更の前に、過去に検討されたが採用されなかった設計案とその不採用理由を確認したいとき。
- Python 実装、CLI 構成、共通処理配置、開発環境、pytest 方針など、realization code の開発規則を確認したいとき。
- 個別仕様ファイルへ進む前に、アプリケーション仕様、設計背景、開発規則のどの領域を読むべきか判断したいとき。

## Do not read this when
- oracle file と realization file の一般的な責務分担、編集権限、正本仕様断片としての原則だけを確認したいとき。
- path キーワードや repo root / run root / work root などのルートディレクトリ概念そのものの定義だけを確認したいとき。
- 実装ファイルやテストファイルの具体的なコード構造、既存関数、helper 分割、現在のテスト期待値を直接調べたいとき。
- 既に読むべき個別の正本仕様文書が分かっており、その本文へ直接進む方が適切なとき。

## hash
- 2ab8b5bdbea36572376ac9ad6e160df265a9037483e62be11c3797bae0cd1881

# `src`

## Summary
- AI コーディングエージェント呼び出しと cmoc 共通概念に関する oracle src をまとめる領域。agent call parameter、prompt 構築、Structured Output schema、モデル・reasoning effort・ファイルアクセス条件、パスプレースホルダ、規範文書モデル、構造化 Markdown レンダリング helper への入口になる。
- 個別 CLI サブコマンドの実行フローではなく、cmoc 全体で共有される正本仕様断片と、AI へ渡す入力・制約・出力契約を確認するための分岐点として読む。

## Read this when
- cmoc が AI コーディングエージェントを呼び出す際の論理パラメータ、prompt、Structured Output schema、モデルクラス、reasoning effort、ファイルアクセスモードの正本仕様断片を確認したいとき。
- 差分適用後レビュー、ルーティング文書生成、oracle file レビュー、merge conflict 解消、TUI 起動など、用途別の agent call parameter や応答契約を確認・変更したいとき。
- agent call 用 prompt の構築順序、標準文書・規則文書の注入、追加 prompt、プレースホルダ定義、ファイルアクセス規則、ルーティング規則の組み込みを確認したいとき。
- cmoc 全体で共有される設定、ルートパス概念、プレースホルダ付きパスの解決、規範文書モデル、構造化 Markdown レンダリング helper の正本仕様断片を確認したいとき。

## Do not read this when
- 実際の CLI 引数解析、サブコマンド実行制御、git 操作、状態管理、ファイル書き込み、結果集約、表示処理など realization implementation 側の流れだけを調べたいとき。
- 生成済み prompt を受け取った後の agent call 実行処理、バックエンド用の具体的な実行コマンド、サンドボックス設定、結果処理の実装を調べたいとき。
- 個別 CLI サブコマンドの利用者向け入出力、状態ファイル仕様、diff 生成手順、merge conflict marker 検出、TUI 入力取得など、正本仕様断片より外側の処理を確認したいとき。
- oracle file 全般の品質基準、realization standard、review standard、index entry standard など、標準本文そのものを読む必要があり、agent call や共通 helper 側の定義を確認する必要がないとき。

## hash
- 20e25804c4b35450a578420f6a6b2840f58187ab9dfed0efd490513394d89784
