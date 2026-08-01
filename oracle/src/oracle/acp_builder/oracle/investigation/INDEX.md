# `launch_tui.py`

## Summary
- `cmoc oracle investigation` の TUI 起動処理における prompt 正本。oracle file 調査用の完全プロンプトを構築し、ログへ保存したうえで、固定モデル・推論強度・読み取り権限・作業ディレクトリなどを含む起動パラメータを返す。

## Read this when
- `cmoc oracle investigation` の TUI 起動時に渡すプロンプト、ユーザー調査指示の埋め込み、oracle-only のファイルアクセス設定、または起動パラメータを確認・変更するとき。

## Do not read this when
- TUI 起動以外の agent call パラメータ生成を調べるとき。完全プロンプトの共通構築規則を確認する場合は、prompt builder の実装を直接読む。ログ保存の共通仕様やパス解決の詳細だけを調べる場合は、それぞれの共通モジュールを直接読む。

## hash
- c983f032ef23cefe8a127a9c8dc7a7c864b8f9eb40b8c632b84779eecfc819d2
