# `acp_builder`

## Summary
- oracle、realization、feedback、indexing、session、tui などの各 cmoc 機能について、prompt と AgentCallParameter を構築する定義を集約するディレクトリ。
- 共通の AgentCallParameter データモデル、論理モデル種別、推論強度、ファイルアクセスモードは basic.py が提供し、各サブディレクトリが機能別の agent call builder と Structured Output schema を担う。
- oracle 操作、realization 追従・レビュー、feedback issue 処理、INDEX.md 生成、session conflict 解消、TUI 起動、quota probe の具体的な起動契約へ進むための入口。

## Read this when
- cmoc の各機能が agent call を構築する prompt、モデル・推論設定、ファイルアクセス権限、cwd、Structured Output schema、indexing preflight を調査または変更するとき。
- 共通の AgentCallParameter や論理的なモデル・推論・ファイルアクセス種別を確認するときは basic.py を読むとき。
- 特定機能の agent call 定義を確認するときは、該当する oracle、realization、feedback、indexing、session、tui の下位ディレクトリへ進むとき。

## Do not read this when
- agent call の実行処理、Codex CLI への具体的なモデル名・推論強度変換、共通 prompt の生成規則、パス解決の一般仕様を確認したいとき。
- oracle file や realization file の具体的な仕様・実装、または feedback の検出・保存・報告処理を確認したいとき。
- 既存 INDEX.md のルーティング内容を確認したいとき。

## hash
- ba18f48a196713b2de5ceca2156953fa799a3f865c3c705e695b0c51ac75a920

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
- agent call 向けの完全な prompt を構築するための共通実装を収めるディレクトリ。placeholder 型、prompt の統合、エディタ初期入力、oracle／realization 概念の説明、policy 生成群を扱い、個別モジュールの責務を確認する入口となる。

## Read this when
- agent call に渡す prompt の構築やエディタ入力生成の責務を調査・変更するとき。
- placeholder、oracle／realization の説明、または各種 prompt policy の実装箇所を特定するとき。
- prompt builder 配下の複数モジュールを横断して、共通構成と個別責務の関係を確認するとき。

## Do not read this when
- prompt builder の個別機能だけを確認する場合は、該当するモジュールや policy ファイルを直接読む。
- prompt の根拠となる意味仕様、oracle／realization の実装・テスト、既存の INDEX.md エントリーを調査する場合。
- 生成済み prompt を利用する agent call 側の責務や CLI 挙動だけを確認する場合。

## hash
- 5b904fd0a2b3b5053859b0fb285cec55747a23baadca9ebb6317ec824189e6b4
