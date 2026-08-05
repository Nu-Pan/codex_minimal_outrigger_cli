# `__init__.py`

## Summary
- `cmoc oracle investigation` 用 builder adapter パッケージの入口。oracle investigation 向け builder 機能へ進む際の参照先。

## Read this when
- oracle investigation 用 builder adapter の構成や入口を確認するとき
- 該当パッケージ内の下位実装へ進む前に責務を確認するとき

## Do not read this when
- builder adapter の具体的な実装詳細を確認したいとき
- oracle investigation 以外の builder や ACP 実装を調べるとき

## hash
- c4c41f07d0b59e430e93561b97dcc2321301abc3cedb93fdeb0ef16a0c9a9637

# `launch_tui.py`

## Summary
- 対象は、oracle investigation の正本 builder を呼び出す realization adapter です。エディタ入力用ディレクトリを準備したうえで、正本 builder に時刻情報とユーザー指示を渡し、AgentCallParameter を返します。エディタ入力ディレクトリの準備と正本 builder への委譲が、この対象へ進む理由です。

## Read this when
- oracle investigation の launch TUI 用パラメータ生成の realization adapter を確認するとき
- 完全な prompt の保存先ディレクトリ準備や、正本 builder への委譲経路を追うとき

## Do not read this when
- oracle 側の launch TUI builder の仕様や prompt 構築詳細を確認したいとき。対応する oracle ファイルを直接読む
- launch TUI 以外の builder や、エディタ入力ディレクトリの一般的な実装だけを調べるとき

## hash
- 96b75359027bd8481745a87868524bee4e86525e77f0f65b4b519ff3c00a126a
