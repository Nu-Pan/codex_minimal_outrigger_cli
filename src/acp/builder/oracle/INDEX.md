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
- `cmoc oracle edit` builder の realization adapter パッケージ。oracle edit 用 TUI 起動パラメータの生成入口と関連する配置領域を扱う。

## Read this when
- `cmoc oracle edit` の builder adapter の責務や、TUI 起動パラメータ生成の実装入口を確認するとき。

## Do not read this when
- oracle edit の具体的な prompt 構築仕様や編集処理を確認したいとき。対応する oracle builder または対象実装を直接読む。
- 他の ACP builder や TUI 以外の起動処理を調査するとき。

## hash
- 8eaf93e4d854bf31694349ea8dfbf72a6819a47a09b0f8a42cf7d62f10e377ad

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
- `cmoc oracle review` builder の realization adapter package。oracle review の finding enumeration、judgment、merge-finding、advocate、challenger validation に関する互換入口と限定的な prompt 補正を扱う。各 canonical 実装または oracle 実装への入口として機能する。

## Read this when
- `cmoc oracle review` builder の realization adapter の責務や関連する import 経路を確認するとき
- finding enumeration・judgment・merge-finding・advocate・challenger validation の adapter、委譲、互換性、prompt 補正を変更・移行・削除するとき

## Do not read this when
- oracle review の正本仕様や canonical builder の実装詳細を確認するとき
- builder 以外の CLI 実装や oracle review と無関係な validation 処理を調査するとき

## hash
- 11e6fdf7be033514563cefc3cc093104dec59c25e94ab25764c9a903b2bac4db
