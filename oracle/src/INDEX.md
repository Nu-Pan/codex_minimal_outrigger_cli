# `oracle`

## Summary
- ACP builder の oracle src をまとめる領域。AI エージェント呼び出しパラメータ、cmoc サブコマンドごとの prompt・Structured Output 設定、実行時のファイルアクセス方針を扱う。下位要素で各仕様を確認するための入口。
- cmoc の設定モデル、ルートパス解決、規範文書のデータ化、構造化 markdown 処理など、複数機能から利用される共通基盤をまとめる領域。個別の共通処理を選ぶ前に確認する入口。
- agent call 用の完全なプロンプトを組み立てる実装と、その構成要素を扱う領域。oracle／realization の規範、ルーティング規則、プレースホルダ展開、standard の prompt への注入処理を確認する入口。

## Read this when
- ACP builder の agent call パラメータやファイルアクセスモードを確認するとき。
- cmoc apply fork、indexing、review oracle、session join、tui の prompt 構築や Structured Output 設定を調査するとき。
- 設定モデル、既定値、保存方針、ルートパスのプレースホルダ解決を確認するとき。
- 規範文書のデータ構造や markdown への変換、構造化 markdown のレンダリング・検査・正規化を確認するとき。
- 完全な agent 用プロンプトの構成、静的・動的 prompt の統合、各 standard の注入処理を調査・変更するとき。
- プレースホルダ展開に使う型や、oracle／realization の定義を prompt に組み込む処理を確認するとき。

## Do not read this when
- ACP builder の実行本体、下流の realization 実装・テスト、CLI の実行手順や入出力を調査するとき。
- 共通 prompt builder、パス解決、構造化文書処理の実装詳細を直接調査するとき。
- 個別の oracle file や realization file の仕様・実装そのものを確認するとき。
- レビュー結果の保存・表示形式、JSON schema、prompt builder 全体の呼び出し側を確認するとき。
- oracle と realization の一般的な責務定義や INDEX.md の生成規則だけを確認したいとき。

## hash
- cd37019dd3d3de2c0d8fc9415269342cacc44691186e5fe5f29fad7b8f4b74d6
