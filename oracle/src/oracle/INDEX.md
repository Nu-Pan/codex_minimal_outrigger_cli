# `acp_builder`

## Summary
- ACP builder の agent 呼び出しパラメータと Structured Output スキーマを定義する oracle src 群。共通のモデル・推論強度・ファイルアクセス表現と、apply fork、indexing、review oracle、session join、TUI 向けの個別設定を扱う入口。

## Read this when
- ACP builder の AgentCallParameter、モデルクラス、推論強度、ファイルアクセスモードの定義を確認するとき。
- 変更要約、ファイルレビュー・修正、indexing、oracle review、merge conflict 解消、TUI の prompt と実行設定を実装・検証するとき。
- 各用途の Structured Output スキーマ、入力条件、出力契約、oracle・realization standard の適用範囲を確認するとき。

## Do not read this when
- cmoc の各サブコマンドの実行フローや、agent 呼び出し後の差分適用・conflict 解消処理を調査するとき。
- レビュー対象ファイルや TUI の画面制御など、realization 側の具体的な実装・テストだけを確認したいとき。
- 共通 prompt builder、パス解決、構造化文書処理そのものの実装詳細だけを調査するとき。

## hash
- 570c08961715b33fbec48be5bb45a08f182ccbcd9d0af79a0e9c98c64a52a836

# `other`

## Summary
- `oracle/src/oracle/other` 配下の、cmoc の設定モデル、ルートパス解決、規範文書のデータ化、構造化 markdown 組み立てをまとめて扱う入口。個別ファイルを選ぶ前に、この層でどの共通基盤を読むべきかを判断したいときに使う。

## Read this when
- cmoc の永続設定モデルや、その既定値・保存方針を確認したい。
- ルートパスのプレースホルダ解決や、実パスとの相互変換を確認したい。
- 規範文書を保持するデータ構造や、markdown への落とし込み方を確認したい。
- 階層付き markdown のレンダリング、`cmoc_ref` と `cmoc_block` の検査、文字列やコードブロックの正規化を確認したい。

## Do not read this when
- `cmoc` の各サブコマンドの実行手順や CLI の入出力を追いたい。
- 設定読み書きの具体的な永続化処理や、サブコマンド固有の業務ロジックを見たい。
- 構造化文書やパス解決以外の別系統の共通処理を探したい。

## hash
- 6139c507e1f8a0fcd13dc8bbffa88ee7e994d18d1b93d3403a866d084f29eca8

# `prompt_builder`

## Summary
- oracle と realization の定義・各種 standard・ファイルアクセス規則・INDEX.md ルーティング規則を、プロンプトへ注入する部品群を収めるディレクトリ。個別の規範文面を構造化プロンプトへ変換する入口として、standard の追加・変更や組み合わせを確認する際の起点になる。

## Read this when
- oracle・realization の基本定義や記述標準を確認・変更するとき。
- レビュー基準、ファイルアクセス規則、INDEX.md ルーティング規則の注入内容を確認・変更するとき。
- これらの正本文面を組み合わせたプロンプト生成処理を調査するとき。

## Do not read this when
- 完全な prompt 列の構成順序やプレースホルダ合成を確認したいときは、親のプロンプト組み立て実装を読む。
- CLI の引数、入出力、ファイル探索、agent の実行フローを調べるとき。
- 個別の oracle file・realization file の本文や実装内容を調査するとき。
- INDEX.md の実ファイル自体を編集・評価するとき。

## hash
- ace53d578195f8b13ffb7dcbe200d4686670144db5121460dd5d2828b13768ef
