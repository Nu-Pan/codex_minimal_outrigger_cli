# `__init__.py`

## Summary
- `cmoc oracle edit` builder の realization adapter package。対象パッケージの入口として、oracle edit 用 builder 実装を扱う。

## Read this when
- `cmoc oracle edit` の builder adapter の責務や実装入口を確認するとき。

## Do not read this when
- oracle edit の具体的な編集処理や CLI 全体の動作を確認したいとき。対象の実装ファイルや上位の CLI 関連ファイルを直接読む。

## hash
- aceb2892c60c365c1ab63b37a6a8264fbaf18cc2d0e146e7f8d370741f78ac55

# `fork`

## Summary
- 内容がない空ディレクトリで、現時点では案内対象となる実装・テスト・補助ファイルを含まない。

## Read this when
- このディレクトリにファイルが追加されたか確認するとき。

## Do not read this when
- 既存の実装やテストを調査するとき。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `launch_exec.py`

## Summary
- oracle edit の正本 exec builder を呼び出す realization adapter。main 用では、正本 builder が完全 prompt の skeleton を保存する editor input log directory を準備してから launch parameter を返す。仕様削減用では、正本 builder が構築した固定 launch parameter をそのまま返す。oracle edit の launch exec parameter 生成処理へ進むための adapter 層。

## Read this when
- oracle edit の main または仕様削減用 launch exec parameter の呼び出し入口を確認するとき
- 正本 builder 呼び出し前に必要な editor input log directory の準備責務を確認するとき

## Do not read this when
- 正本 builder が生成する完全 prompt や仕様削減 prompt の内容を確認するとき
- prompt 保存先のパス解決や editor input log directory 自体の仕様を確認するときは、それぞれの正本実装を直接読む

## hash
- 862ec2be7b0be49c3db10908ec9b291d4d742eb593b6e2543931e941e1ab0d62
