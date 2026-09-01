# `edit`

## Summary
- `cmoc oracle edit` の編集 agent call 起動処理を扱うディレクトリです。空の `fork` と、編集 call および仕様削減 call の起動パラメータを構築する `launch_exec.py` を入口として含みます。

## Read this when
- `cmoc oracle edit` の agent call 起動条件、prompt 構成、起動パラメータ、または編集後の仕様削減 call の責務分担を確認するとき。

## Do not read this when
- oracle file の編集処理そのものや仕様削減の判断基準を確認するとき。
- session の join・競合解決、または `cmoc oracle edit` 以外の agent call 起動処理を調べるとき。

## hash
- 1eb610342b71ff8cafcb6c5f9b78e7d7a511e756c84d0ca8efcf60e6716fe9fa

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
