# `edit`

## Summary
- `cmoc oracle edit` の共通編集パラメータを構築する実装を含むディレクトリ。ユーザー指示、oracle の編集範囲、未コミット差分の確認、編集制約、oracle 書き込み権限、実行時パス、prompt、preflight 無効化をまとめて設定する。

## Read this when
- `cmoc oracle edit` の agent 呼び出し用 prompt や実行パラメータを変更・確認するとき
- oracle 編集時のファイルアクセス権限、Git 差分の扱い、編集制約、実行コンテキストを確認するとき

## Do not read this when
- oracle edit 以外のサブコマンドの agent 呼び出しパラメータを確認するとき
- 共通 prompt 構築関数やパスモデル自体の実装を直接確認すべきとき

## hash
- 32eab9c41322d7aa05de231fd3c417958aa7a571a2cdecd155553c54cc8d1579

# `investigation`

## Summary
- `cmoc oracle investigation` 用の調査プロンプトと TUI 起動パラメータを構築する正本実装への入口。oracle-only 読み取り、各種ポリシー、エディタ入力引き渡し、indexing preflight の設定を扱う。

## Read this when
- `cmoc oracle investigation` の調査プロンプト生成や TUI 起動設定を確認・変更するとき。
- oracle file のみを根拠に調査させる呼び出し条件や、調査指示の引き渡し方法を確認するとき。

## Do not read this when
- 調査プロンプトの共通構築処理そのものを確認する場合は、prompt builder の実装を直接読むとき。
- TUI 起動以外の ACP builder 呼び出しや、oracle file の内容自体を確認する場合。

## hash
- 0dc9302904bfa30c7eb493ac1e19a98aa05fa49bc876497e5fb29dafb0d034d3

# `review`

## Summary
- 対象ディレクトリ本文が提示されておらず、責務を根拠付きで判断できません。

## Read this when
- 対象ディレクトリの本文が追加され、担当範囲を確認したいとき

## Do not read this when
- 本文がない現状では、このエントリーから具体的なレビュー作業へ進む必要があるとき

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
