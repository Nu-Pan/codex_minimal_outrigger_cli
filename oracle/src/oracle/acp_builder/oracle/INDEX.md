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
- `cmoc oracle investigation` 用の TUI 起動パラメータを構築し、oracle のみを読む調査プロンプト、パス情報、エディタ入力引き継ぎ、インデックス前処理などの実行条件をまとめる定義。

## Read this when
- oracle file を対象にした調査依頼のプロンプト構成や、調査用 TUI の起動条件を確認したいとき。
- ユーザー指示を完全プロンプトへ組み込み、oracle 根拠の提示を要求する調査呼び出しの流れを追いたいとき。

## Do not read this when
- 調査機能の実装全体や、プロンプト部品の詳細を確認する場合は、呼び出される prompt builder・policy 定義を直接読む。
- 実際の ACP 実行処理、TUI 本体、または oracle file の内容を確認したい場合は、それぞれの実装・正本仕様へ直接進む。

## hash
- d5fba5277668e25b089790de50470a4c2378b8d6fe9531350d1abe8fb85a8508

# `review`

## Summary
- 対象ディレクトリ本文が提示されておらず、責務を根拠付きで判断できません。

## Read this when
- 対象ディレクトリの本文が追加され、担当範囲を確認したいとき

## Do not read this when
- 本文がない現状では、このエントリーから具体的なレビュー作業へ進む必要があるとき

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
