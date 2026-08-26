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
- agent call 用の完全 prompt を構築するモジュール群。共通 placeholder 型、選択式の policy・説明部品・追加 prompt・目的を統合し、構造化 prompt として返す。
- prompt の構築順序、policy の有効化、placeholder 定義の競合拒否、変動の大きい定義を末尾へ置く構成を扱う。
- エディタ入力の初期文面を生成する処理を含む。記入指針と完全 prompt のテンプレートを HTML コメント内に埋め込む。
- oracle と realization の基本説明、および feedback、file access、routing、INDEX.md 用エントリー、oracle／realization の扱い・所見、conflict resolution などの policy 部品を下位要素として提供する。

## Read this when
- agent call に渡す完全 prompt の構成順序や、複数の policy・追加 prompt・目的の統合方法を確認・変更するとき。
- placeholder 定義の統合規則や、同名異値の競合処理を確認するとき。
- エディタ経由のプロンプト入力に使う初期文面、記入指針、完全 prompt テンプレートの埋め込み形式を確認・変更するとき。
- oracle と realization の基本概念を prompt に組み込む説明部品を確認するとき。
- prompt に組み込む共通 policy の責務や、feedback、file access、routing、INDEX.md、oracle／realization、所見、conflict resolution の各規定の入口を確認するとき.

## Do not read this when
- 特定の oracle 文書、realization 実装、テストの内容や配置を確認するとき。
- agent call の呼び出し側、path context の生成規則、placeholder の具体的な値の決定処理を確認するとき。
- 個別 policy の本文だけを確認する場合は、該当する下位 policy 部品を直接読む。
- 既存の INDEX.md の案内内容を確認するとき。

## hash
- d6d9e39df6753998c45206855af2b1faf617b5b429af9da642cfac2aa7c539d7
