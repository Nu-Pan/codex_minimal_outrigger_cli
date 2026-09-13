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
- `cmoc oracle edit` の起動時に、ユーザー指示・oracle file・未コミット差分をもとに編集用の完全 prompt と実行パラメータを構築する共通定義。

## Read this when
- `cmoc oracle edit` の編集処理で、初回 agent call の prompt、oracle 専用書き込み権限、作業ディレクトリ、または indexing preflight 無効化の設定を確認・変更するとき。
- oracle edit の両回で共用される起動パラメータの構築条件や、編集判断に渡すユーザー指示・差分情報を追跡するとき。

## Do not read this when
- oracle edit の意味仕様や編集方針そのものを確認したいときは、参照先の oracle edit 仕様を直接読む。
- prompt の一般的な構築処理や構造化文書のレンダリングだけを確認・変更するときは、それぞれの prompt builder または struct_doc の定義を直接読む。

## hash
- f5b097e49881c316fd51016432ba38f20a21cc70a29ebd8a4be536a286108635
