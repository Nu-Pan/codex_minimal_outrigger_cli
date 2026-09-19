# `fork`

## Summary
- 現時点で本文ファイルを含まない空のディレクトリです。

## Read this when
- このディレクトリにファイルが追加され、その内容や用途を確認する必要があるとき。

## Do not read this when
- このディレクトリ配下の具体的なファイルを直接確認できる場合。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `launch_exec.py`

## Summary
- `cmoc oracle edit` の起動実行で共用する AgentCallParameter を構築する oracle 実装。ユーザー指示、oracle の編集範囲・完了条件・各種制約、Git 未コミット差分の参照方針を完全 prompt にまとめ、oracle 専用の書き込み設定と実行コンテキストを返す。

## Read this when
- `cmoc oracle edit` が agent 起動時に渡す prompt や編集制約を確認したいとき。
- oracle 編集用のファイルアクセスモード、作業ディレクトリ、indexing preflight の設定を調べるとき。

## Do not read this when
- oracle 編集 prompt の中身ではなく、一般的な agent パラメータ構築や realization 編集の起動処理を調べるとき。
- ACP builder の別の起動経路や、実際の oracle ファイル編集ロジックを確認したいとき。

## hash
- 191187e210a251ab2a10cda576f1f7c6da445e17dbd13414ca42268e1d47aaf1
