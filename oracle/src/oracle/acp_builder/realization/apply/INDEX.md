# `fork`

## Summary
- `cmoc realization apply fork` 実行用の AgentCallParameter を構築する関数を定義する。コミット範囲と oracle file の raw git diff を追従対象変更として prompt に埋め込み、リポジトリ全体の realization file への反映と整合性検証を指示する。
- linked worktree を agent call の作業ディレクトリに設定し、realization write 権限、flagship モデル、最大推論 effort、ルーティング事前処理などの起動パラメータをまとめて返す。

## Read this when
- `cmoc realization apply fork` の prompt 文面や AgentCallParameter の起動設定を変更・確認するとき。
- oracle file の変更を realization file 全体へ反映する agent call の作業範囲、権限、検証方針を確認するとき。

## Do not read this when
- 通常の realization implementation や realization test の具体的な実装を変更するとき。
- `cmoc realization apply fork` 以外の起動パラメータ構築を確認するときは、対象となる各 launch 定義を直接読む。

## hash
- 416690b0551fcbe93b9166b8f9c175852b41ea1e5f68974fec8ddfd578d8c52c
