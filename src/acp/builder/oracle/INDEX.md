# `__init__.py`

## Summary
- oracle command builder の realization package。oracle command builder 関連のパッケージ入口として機能する。

## Read this when
- oracle command builder の realization package の責務や構成を確認するとき。

## Do not read this when
- oracle command builder 以外の処理を確認するとき。

## hash
- 04f29448a0f9d675976d8cda22279a162a5e8e89a169554a4926766bf0f88d6b

# `edit`

## Summary
- oracle edit の TUI 起動パラメータ builder を realization adapter として公開するパッケージ。builder の公開入口と import 経路を扱い、現時点では空の fork ディレクトリも含む。

## Read this when
- `cmoc oracle edit` の builder adapter の責務、公開入口、または TUI 起動パラメータ builder の import 経路を確認するとき。

## Do not read this when
- oracle edit の具体的な編集処理や builder 本体の仕様を確認するとき。oracle 側の正本実装や対象の実装ファイルを直接読む。
- CLI 全体の動作を確認するとき。上位の CLI 関連ファイルを直接読む。

## hash
- da843393a46d7d9c9a6be898ff1af60318dd215160bb60bfc7fcf4866d48ff06

# `investigation`

## Summary
- oracle investigation 用 builder adapter の入口と launch TUI 向け realization adapter を含むパッケージ。下位実装や adapter の引数生成を確認する際の入口となる。

## Read this when
- oracle investigation 用 builder adapter の責務や構成を確認するとき
- launch TUI 用 adapter のパラメータ生成や editor input directory 準備を確認するとき

## Do not read this when
- prompt 内容や AgentCallParameter の組み立て規則そのものを確認したいとき
- oracle investigation 以外の builder、ACP 実装、runtime path の一般仕様を調べるとき

## hash
- 6af54e3acf71f9bdbfaae8c4381164c9395406dca92d9396642915fff83be2e0

# `review`

## Summary
- `cmoc oracle review` builder の realization adapter 群を収めるパッケージ。finding の enumeration、judgment、merge、advocate、challenger 向け parameter builder を canonical 実装へ委譲し、必要な互換 import や限定的な prompt typo 補正を提供する入口。

## Read this when
- `cmoc oracle review` builder の realization adapter の責務、canonical builder への委譲、互換 import、prompt の限定補正を変更・調査するとき。
- oracle review の finding enumeration、judgment、merge、advocate、challenger validation の realization 側の呼び出し経路や旧 caller の移行状況を確認するとき。

## Do not read this when
- oracle review の正本仕様や canonical builder 本体の実装を確認するとき。
- oracle review と無関係な builder、CLI、validation 処理を扱うとき。

## hash
- 513c63cf0edf6bebe3cabb1bbc749aa82aab34fa545ae50eabc161f943e6bbd6
