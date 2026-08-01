# `edit`

## Summary
- oracle 編集向け TUI 起動処理を扱うディレクトリ。現時点では、リポジトリルートを作業ディレクトリとして確定し、完全な prompt を構築・保存して Codex CLI 起動パラメータを返す実装への入口です。

## Read this when
- `cmoc oracle edit` の TUI 起動処理や、起動時 prompt、agent call パラメータを変更・調査するとき。
- prompt の構成・保存先、モデルや推論設定、ファイルアクセスモード、作業ディレクトリ指定を確認するとき。

## Do not read this when
- oracle file の編集内容や仕様そのものを確認・変更するとき。
- TUI 起動以外の agent call や prompt 構築処理を確認・変更するとき。
- このディレクトリに具体的なファイルが追加され、そのファイルを直接確認できるとき。

## hash
- 9f2a364ef1511a844eb166efa92c893d8ff5c632585fdf9636d252b3e739dd11

# `investigation`

## Summary
- `cmoc oracle investigation` の TUI 起動処理を扱う領域。完全な oracle 調査プロンプトの構築・ログ保存と、固定モデル、推論強度、読み取り権限、作業ディレクトリなどの起動パラメータ生成を担う。

## Read this when
- `cmoc oracle investigation` の TUI 起動時プロンプトやユーザー調査指示の埋め込みを確認・変更するとき
- oracle-only のファイルアクセス設定や TUI 起動パラメータを確認・変更するとき

## Do not read this when
- TUI 起動以外の agent call パラメータ生成を調べるとき
- 完全プロンプトの共通構築規則を確認するときは prompt builder を直接読むとき
- ログ保存の共通仕様やパス解決の詳細だけを調べるとき

## hash
- 4b8e91f02a0cbc1814d86e74fce265c56c2c18045f8a0e539d69e095191183c8

# `review`

## Summary
- `cmoc oracle review` における所見レビュー用の oracle src と Structured Output schema をまとめたディレクトリ。新規所見列挙、採否判定、所見の擁護・反証理由列挙、所見リストのマージ処理を扱い、それぞれの prompt builder と入出力契約の確認入口となる。

## Read this when
- `cmoc oracle review` の所見レビュー処理を変更・調査するとき。
- 新規所見、採否判定、擁護理由、反証理由、所見マージの prompt 構築や agent call 設定を確認するとき。
- レビュー処理で利用する Structured Output schema の入出力形式を確認するとき。

## Do not read this when
- oracle review の所見内容そのものや正本仕様を確認したいとき。
- レビュー以外の ACP builder 実装や、一般的な prompt 構築・パス解決・構造化文書レンダリングの共通実装を調査するとき。
- レビュー所見を扱わない通常の ACP builder 実装を読むとき。

## hash
- 3024ba3ba0da0040c32a93c1607bed8b4f97bba8501a480d7a6aa4f869c0fe28
