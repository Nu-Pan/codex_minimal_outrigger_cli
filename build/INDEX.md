# `bdist.linux-x86_64`

## Summary
- ビルド処理が作成する一時的な配布用作業領域であり、現在この対象内に本文として参照できる内容はない。
- 正本仕様、実装、テスト、または補助的な手作業対象への入口ではない。

## Read this when
- ビルド成果物や配布パッケージ生成中の一時ディレクトリが存在するかだけを確認したいとき。

## Do not read this when
- 仕様、実装、テスト、開発手順、または永続的に管理される補助ファイルを探しているとき。
- 配布物の生成ロジックやパッケージ設定を確認したいとき。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `lib`

## Summary
- 生成済み配布用コードの上位領域であり、CLI 入口、サブコマンド実装、共有 runtime helper、oracle 由来の prompt・型・設定モデル、旧 import 経路の互換層へ進むための入口になる。
- 正本仕様や正本実装そのものではなく、realization 側の実行コードと互換公開面を、責務別の下位領域へ切り分けて読むためのルーティング対象。

## Read this when
- 生成済み実装側で、CLI 入口、サブコマンド制御、共通 runtime、Codex 呼び出し、設定、git、状態管理、ログ、path、INDEX.md 更新などの読む先を選びたいとき。
- 旧 import 経路や公開済み module 名が、oracle 側の正本由来実装または既存 runtime 実体へどう接続されているか確認したいとき。
- AI エージェント呼び出しパラメータ、prompt 構築、Structured Output schema、file access mode、path model、構造化 Markdown などの正本由来実装へ進む入口を探したいとき。
- apply、indexing、init、review、session、tui などのサブコマンド実行フローや、その周辺の runtime 接続、git/worktree/state 操作、cleanup、レポート生成を調べたいとき。
- 生成済み実装内で、どの責務の下位領域を読むべきかをまず切り分けたいとき。

## Do not read this when
- oracle file の正本仕様本文、人間意図、生成規則そのものを確認したいときは、oracle 側の仕様断片や正本実装を読む。
- 特定のサブコマンド、helper、互換 import 層など読む対象が既に分かっているときは、この領域全体ではなく該当する下位対象を直接読む。
- 生成済み配布用コードではなく、正本の実装ソースやテストを編集したいときは、対応する source 側の対象を読む。
- Typer、Click、git、Codex CLI など外部ツールの一般的な使い方だけを調べたいとき。

## hash
- 6fced9f3d02d84228d12311cc3840f7e2d079adb38bb711d68a880b9d96b3e81
