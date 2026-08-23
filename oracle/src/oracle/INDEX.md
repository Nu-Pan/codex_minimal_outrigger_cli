# `acp_builder`

## Summary
- cmoc の Agent Call Parameter 構築定義をまとめるディレクトリ。共通の呼び出しパラメータ型・論理モデル・推論強度・ファイルアクセスモードを基盤として、feedback、indexing、oracle、realization、session、tui、quota probe 各機能の prompt、Structured Output schema、作業範囲、モデル設定、preflight 設定を定義する。各サブディレクトリは対応するサブコマンドまたは処理系の agent call 構築への入口となる。

## Read this when
- Agent Call Parameter の共通データモデル、論理モデル種別、推論強度、ファイルアクセスモード、prompt、schema パス、cwd、indexing preflight の契約を確認・変更するとき。
- feedback の issue 同一性判定・検証、INDEX.md エントリー生成、oracle の edit・investigation・review、realization の apply・refactor、session join の conflict 解消、TUI 起動、quota probe の agent call 構築を調査するとき。
- 各処理が選択するファイルアクセス policy、モデルクラス、推論強度、Structured Output の有無、起動前 indexing の扱いを確認するとき。

## Do not read this when
- 実際の Codex CLI モデル名や論理推論強度からの変換規則を確認したいとき。
- Codex CLI の具体的な sandbox 制約、共通 prompt のレンダリング規則、agent call の実行基盤、パス解決の共通仕様を確認したいときは、それぞれの共通定義を直接読む。
- 個別の oracle・realization 本文、feedback state、実装・テストの挙動、または各 Structured Output schema の項目・型・形式だけを確認したいとき。
- 既存の INDEX.md に記載されたルーティング内容だけを確認したいとき。

## hash
- ae3877bd8bdc93b202e84edccf0b73f45674a1b35fddaa126fcee2e80300063f

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
