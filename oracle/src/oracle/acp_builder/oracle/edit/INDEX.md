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
- `cmoc oracle edit` の両実行経路で共用する agent call パラメータを構築する。ユーザー指示、oracle の編集範囲、未コミット差分の扱い、編集制約を prompt に組み込み、oracle file のみを書き換える実行設定を返す。

## Read this when
- `cmoc oracle edit` が agent に渡す共通 prompt、oracle file の編集境界、未コミット差分の参照条件を確認したいとき。
- oracle 編集用 agent call の作業ディレクトリ、ファイルアクセスモード、indexing preflight の設定を変更・検証するとき。

## Do not read this when
- `cmoc oracle edit` の仕様本文やユーザー向けサブコマンド仕様を確認したいときは、参照先の oracle doc を直接読む。
- ACP builder の一般的なパラメータ型や prompt の汎用レンダリング処理を確認したいときは、依存する basic または prompt_builder の実装を直接読む。
- INDEX.md の生成や更新処理そのものを確認したいとき。

## hash
- 65c9a27bb8749f0674f3f6c599c4f97ed09837bdb509f03d4625e458e2e7d68a
