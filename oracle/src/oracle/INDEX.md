# `acp_builder`

## Summary
- ACP builder の共通パラメータ定義、quota probe、feedback issue の正規化・検証、INDEX.md エントリー生成、TUI 起動など、各種 agent call の prompt と起動設定を構築する領域です。
- 共通の `AgentCallParameter` と列挙型を確認する場合は `basic.py`、機能別の agent call や Structured Output 契約を調査する場合は対応する下位ディレクトリ・ファイルへ進みます。

## Read this when
- agent call の prompt、モデル・推論強度、ファイルアクセスモード、cwd、Structured Output schema、indexing preflight の設定を確認または変更するとき
- feedback、indexing、oracle、realization、session、quota probe、TUI の agent call 構築処理の入口を探すとき
- agent call の共通データモデルや論理モデル種別を確認するとき

## Do not read this when
- Codex CLI の具体的な実行処理や backend モデル名への変換規則を調べるとき
- 共通 prompt のレンダリング規則、パス解決、oracle・realization の正本仕様など、別の直接的な実装・仕様対象を確認するとき
- 個別の oracle・realization file、feedback state、INDEX.md の既存ルーティング内容そのものを調べるとき

## hash
- d129b5e484e9d3f024688b993953b90b67f1362e2cbd38bff9838e48c26c7556

# `feedback`

## Summary
- 対象ディレクトリは、agent が検出した問題を feedback reporter から collector へ渡すための入力契約を扱う領域です。問題の分類・重要度・影響、人間の対応が必要な理由、原因の確信度、再確認可能な根拠、作業継続状態を表現・検証する下位要素への入口になります。

## Read this when
- feedback reporter の入力形式や、検出した問題を人間向け feedback として構造化する処理を確認するとき。
- 入力契約を構成するスキーマや関連する検証定義を調査・変更するとき。

## Do not read this when
- collector 側の保存、集約、重複判定の仕様だけを確認したいとき。
- feedback の検出方法や、agent が作業を継続するかどうかの判断ロジックだけを確認したいとき。

## hash
- a86d0e0a2687a4eed300cd97383ba6e521f2347418e4446a2bfba702aedcd9ba

# `other`

## Summary
- cmoc の設定モデル、パス表記・ルート解決、構造化文書の Markdown レンダリングを扱う補助モジュール群。設定値や既定値、agent call のパス境界、文書要素の整形規則を確認する際の入口となる。

## Read this when
- cmoc の設定項目、Codex CLI 設定、oracle review のループ上限、設定値の JSON/TOML 表現を確認するとき
- agent call の cwd から work root・repository root を導出する規則や、ルートプレースホルダー付きパスの解決・変換を確認するとき
- 構造化された見出し、参照可能な cmoc ブロック、コードブロック、規定文を Markdown へレンダリングする挙動を確認するとき

## Do not read this when
- Codex CLI の実際の呼び出し処理や CLI 実装の責務を確認するとき
- oracle review のレビュー処理や所見生成ロジックそのものを確認するとき
- 設定ファイルの保存内容・人手による調整結果だけを確認するとき
- 具体的な正本仕様や生成文書の内容を確認する必要があり、別の仕様・呼び出し元を直接読むべきとき

## hash
- 6125a10678c23ca628f6b05330ed05e7e19dcdfdc72e272f7ec6c54533ce00a1

# `prompt_builder`

## Summary
- プロンプト生成に必要な共通型、完全 prompt 構築、エディタ初期入力、oracle／realization 概念部品、各種 policy 定義をまとめたディレクトリ。prompt_builder の構成要素と、目的別に読むべき下位対象への入口を提供する。

## Read this when
- agent call 用 prompt の構築順序、policy・追加 prompt・目的・placeholder の統合方法を確認したいとき。
- エディタへ注入する初期入力や、完全 prompt のテンプレート埋め込み形式を確認したいとき。
- oracle と realization の基本概念、分類、配置、関連する prompt 部品を確認したいとき。
- prompt_builder 配下の policy の責務や、目的に応じた個別 policy への到達先を判断したいとき。
- placeholder 対応表の共通型定義を確認したいとき。

## Do not read this when
- 特定の policy 本文や prompt part の詳細を確認したい場合は、該当する下位ファイルを直接読む。
- 具体的な oracle 文書・realization 実装・テストの内容や配置を確認したい場合は、対象ファイルを直接読む。
- agent call の呼び出し側、path context、placeholder の具体的な生成規則を確認したい場合は、担当モジュールを直接読む。
- プロンプト生成と無関係な構造化文書や CLI 挙動の仕様を確認したい場合。

## hash
- a93fc8f4f30fd2118222301e85d81817a7c117be0680504282cb6289b69ff4c1
