# `edit`

## Summary
- oracle edit の起動処理に関する実装の入口で、ユーザー指示・oracle file・未コミット差分から編集用 prompt と実行パラメータを組み立てる。

## Read this when
- `cmoc oracle edit` の初回 agent call に渡す prompt、oracle 専用書き込み権限、作業ディレクトリ、indexing preflight 無効化、または共通起動パラメータの構築条件を確認・変更するとき。

## Do not read this when
- oracle edit の意味仕様や編集方針そのものを確認するとき。
- 一般的な prompt 構築処理や構造化文書のレンダリングを確認・変更するとき。
- この配下の具体的な実装ファイルを直接確認でき、ディレクトリ単位の案内が不要なとき。

## hash
- b6de0a31af20ff4a66983cc26e233f190ebc0c996d24b4a24d10314c5cc9dccc

# `investigation`

## Summary
- `cmoc oracle investigation` 用の完全プロンプトと Codex CLI TUI 起動パラメータを構築する。
- ユーザー指示を調査タスクへ埋め込み、関連する oracle file のみを根拠とする読み取り専用調査経路への入口を提供する。

## Read this when
- oracle 調査の完全プロンプトに、ユーザー指示・調査範囲・完了条件をどう組み込むか確認または変更するとき。
- oracle 調査用 TUI の起動時設定、読み取り専用アクセス、エディタ入力引き継ぎ、インデックス事前処理の構築を確認または変更するとき。

## Do not read this when
- oracle の調査結果や個別の oracle file の内容を確認するときは、生成されたプロンプトではなく対象の oracle file を直接読む。
- 一般的な ACP 起動パラメータや、`cmoc oracle investigation` 以外のコマンドの挙動だけを確認するとき。

## hash
- cda250c1f5b522edf0c9b6f4645c9169f5f7f3418e796c85e3ab82d4b3ef1c5a

# `review`

## Summary
- 対象ディレクトリ本文が提示されておらず、責務を根拠付きで判断できません。

## Read this when
- 対象ディレクトリの本文が追加され、担当範囲を確認したいとき

## Do not read this when
- 本文がない現状では、このエントリーから具体的なレビュー作業へ進む必要があるとき

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
