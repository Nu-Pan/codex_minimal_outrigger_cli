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
- oracle review における所見の列挙、採否判定、重複・矛盾の整理、妥当性の支持・反証調査を行う agent call の入出力契約と起動条件を扱う入口です。
- 所見の Structured Output schema と、それぞれの prompt・起動パラメータ構築定義を対応づけて確認できます。

## Read this when
- oracle review の所見を生成・判定・統合・検証する agent call の出力契約を確認するとき。
- 所見、既知の理由、oracle file、oracle 限定アクセスなどを agent call に渡す条件を確認するとき。
- finding の重複排除、採否、置換・統合、支持理由・反証理由の追加調査を追跡するとき。

## Do not read this when
- レビュー対象 oracle file の本文、所見の具体的な判定基準、または共通の prompt・agent call 基盤を確認したいとき。
- 所見の保存・表示・判定結果の利用処理そのものを確認したいとき。
- oracle review の所見以外の agent call の入出力契約を確認したいとき。

## hash
- 7a2a526527f576d04784a652e7cd4974ff40eb54db37fd0a641df1244a12f2c1
