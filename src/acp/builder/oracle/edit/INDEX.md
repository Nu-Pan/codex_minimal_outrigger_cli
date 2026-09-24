# `__init__.py`

## Summary
- `cmoc oracle edit` builder の realization adapter package を位置付ける初期化説明です。edit 用 builder package の役割を確認する入口になります。

## Read this when
- `cmoc oracle edit` builder package の役割や位置付けを確認するとき。

## Do not read this when
- exec builder が公開する関数やパラメータ構築の詳細を確認するときは、対応する `launch_exec` の実装へ進んでください。

## hash
- aceb2892c60c365c1ab63b37a6a8264fbaf18cc2d0e146e7f8d370741f78ac55

# `fork`

## Summary
- 現在あるのは Python の import キャッシュだけで、builder の現行責務や agent への指示を定義するソース本文はありません。

## Read this when
- この場所に残る import キャッシュの生成・残存や、キャッシュが原因の挙動を調べる場合。

## Do not read this when
- oracle edit builder の挙動や仕様を確認・変更する場合は、正本仕様または実装ソースを直接読んでください。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `launch_exec.py`

## Summary
- oracle edit の main-worktree 実行用パラメータ builder を realization 側の import 経路として公開する adapter。prompt と起動設定の定義は oracle 側の実装が担う。

## Read this when
- `cmoc oracle edit` がこの builder をどこから参照するか、subcommand との import 接続を追うとき。

## Do not read this when
- 生成する prompt や agent call parameter、oracle 編集ルールを調べるときは、定義を持つ oracle 側の実装と正本仕様を直接読む。
- CLI runtime の実行手順や事前条件を調べるときは、subcommand の実装を直接読む。

## hash
- bee79dd76db49ad009b73aec73e6fb73843ea6fb66e8dde551e967d1019e7195
