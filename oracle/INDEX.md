# `doc`

## Summary
- cmoc の正本仕様ドキュメント群を置く領域であり、アプリケーション仕様、branch/worktree モデル、採用しなかった代替案、開発規則など、自然言語で書かれた oracle doc への入口になる。
- 利用者向け外部挙動、git branch / worktree の概念、設計判断の背景、realization code の開発基準などを、下位領域や個別文書ごとに分けて扱う。

## Read this when
- cmoc の仕様を自然言語の正本仕様断片から確認したいとき。
- CLI 挙動、サブコマンド仕様、Codex CLI 呼び出し、ログ、エラー、セッション状態、INDEX.md 自動生成、run 隔離などのアプリケーション仕様文書へ進む入口を探すとき。
- session fork / join、cmoc-managed branch、run branch、linked worktree、fork / join commit などの git branch / worktree モデルを確認したいとき。
- 採用されなかった設計案の背景や、不採用理由を確認して、自然に見える代替案を再導入してよいか判断したいとき。
- Python 実装、CLI 構成、開発環境、pytest 方針など、realization code を追加・変更する前の横断的な開発規則を確認したいとき。

## Do not read this when
- oracle file と realization file の一般的な責務分担、編集権限、品質基準、INDEX.md エントリー生成基準そのものを確認したいだけのとき。
- パスキーワードやルートディレクトリ概念そのものの定義だけを確認したいとき。
- 現在の実装ファイル、テストファイル、既存関数、内部 helper、依存関係など realization code の具体構造を調べたいとき。
- 既に読むべき個別の正本仕様文書や下位領域が特定できており、その本文を直接読む方が早いとき。

## hash
- 70d66840404497d3494dcf52385a33c7ce77c82bd116110b178b148893699d30

# `src`

## Summary
- cmoc の oracle src として、AI agent 呼び出しパラメータ、プロンプト構築部品、設定、パス表記、規範文書、構造化 Markdown などの正本実装断片を収める領域。
- AgentCallParameter、論理モデル種別、Reasoning Effort、ファイルアクセスモード、Structured Output schema 付き agent call、完全プロンプトへの規範注入、ルートパスプレースホルダ解決、リポジトリ別設定の既定値を確認する入口になる。
- apply fork、review oracle、indexing、tui、session join、ファイルアクセス規則違反リカバリなど、cmoc が別 agent call に渡す prompt と呼び出し条件の正本を探す分岐点になる。

## Read this when
- cmoc の oracle src に定義された実装形式の正本仕様断片を確認・変更したいとき。
- AI agent 呼び出しで使う model class、reasoning effort、file access mode、prompt 本文、Structured Output schema の扱いを調べたいとき。
- apply fork や review oracle などのサブコマンドが、どの役割・ゴール・規範・ファイルアクセス規則で agent call を組み立てるか確認したいとき。
- 完全プロンプトに oracle standard、realization standard、review oracle standard、apply review standard、index entry standard、routing rule、file access rule がどう注入されるか確認したいとき。
- cmoc 設定の既定値、Codex CLI 向けモデル名対応、並列数、各レビュー・適用ループの予算、ルートパスプレースホルダの解決規則、構造化文書の Markdown レンダリングを調べたいとき。

## Do not read this when
- 利用者向け CLI の実行フロー、プロセス起動、git 操作、状態ファイル更新、結果表示など、実際に動く realization implementation を調べたいとき。
- 自然言語 Markdown の正本仕様文書そのものを読みたいとき。
- oracle src ではなく realization test、realization implementation、補助スクリプト、生成物、または実際の差分適用箇所を探しているとき。
- 個別ファイルの修正 diff、レビュー結果の保存・集約処理、TUI 入力処理、merge conflict marker の検出処理など、oracle src の prompt 正本ではなく実装側の処理を確認したいとき。

## hash
- 83c7ac54e4115d17dc1a7da0bf6a22b64df58a743f021041951ac0cdd3e2a441
