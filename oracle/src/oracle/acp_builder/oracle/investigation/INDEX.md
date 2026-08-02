# `launch_tui.py`

## Summary
- `cmoc oracle investigation` の TUI 起動用パラメータを構築する実装。リポジトリルートを作業ディレクトリとして確定し、ユーザー指示を含む完全プロンプトを生成・保存したうえで、固定されたモデル、推論強度、ファイルアクセス権、起動設定を返す。

## Read this when
- `cmoc oracle investigation` の TUI 起動パラメータ、完全プロンプト生成、作業パス確定、起動ログ保存の挙動を変更・調査するとき。

## Do not read this when
- oracle investigation の調査プロンプト本文や一般的なプロンプト組み立て規則だけを確認したいときは、完全プロンプト生成実装や関連する prompt builder を直接読む。
- TUI 起動以外の agent call パラメータ構築を変更するとき。

## hash
- c983f032ef23cefe8a127a9c8dc7a7c864b8f9eb40b8c632b84779eecfc819d2
