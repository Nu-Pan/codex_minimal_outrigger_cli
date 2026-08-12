# `launch_tui.py`

## Summary
- `cmoc oracle investigation` の調査用 TUI 起動パラメータを構築する実装。oracle file 調査向けの完全プロンプトを固定要素とユーザー指示から組み立て、管理ログへ保存したうえで、モデル・推論強度・読み取り範囲・作業ディレクトリなどの起動条件を返す。調査用プロンプトの構成や TUI 起動条件を変更・確認するときの入口。

## Read this when
- `cmoc oracle investigation` の TUI 起動パラメータ、調査用完全プロンプト、またはその保存先を変更・確認するとき。
- oracle file 調査に使うモデル、推論強度、ファイルアクセスモード、作業ディレクトリ、インデックス事前処理の設定を確認するとき。

## Do not read this when
- oracle investigation の調査内容そのものや oracle file の仕様を確認したいときは、生成された完全プロンプトまたは対象の oracle file を直接読む。
- 一般的な prompt の共通構築規則を確認したいときは、共通 prompt builder の定義を直接読む。

## hash
- c1cf3a64169f0e00403c21c7ec332d6d3b25499456e8d11183eea5afd55924f3
