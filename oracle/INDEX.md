# `doc`

## Summary
- cmoc の正本文書を領域別に案内する上位入口。アプリケーション挙動、branch・commit・worktree、採用しなかった代替案、開発ルールを扱う下位文書群へのルーティングを提供する。

## Read this when
- cmoc の仕様・設計・開発ルールに関する正本文書を探すとき
- CLI の挙動、session・run の分岐、採用しなかった設計案、Python 開発やテスト手順のいずれかを調査・変更・レビューするとき

## Do not read this when
- 対象となる下位文書が明確で、その本文だけを直接確認すれば足りるとき
- 具体的な CLI 実装、個別のテスト、または個別の oracle・realization の内容だけを調べるとき

## hash
- d047f74262b69e21b1e96d6268734595af827083fa1fab429e39a3e75b125a7d

# `src`

## Summary
- cmoc の agent 呼び出し定義を構成する Python パッケージのルート。共通モデル、パス・文書処理、完全 prompt と policy の構築、用途別の agent call パラメータ、feedback 入力契約を扱う。
- 共通モデルや文書処理を確認する場合は `other`、完全 prompt や policy の構築を確認する場合は `prompt_builder`、用途別の agent call 設定を確認する場合は `acp_builder`、feedback の入力契約を確認する場合は `feedback` へ進む入口となる。

## Read this when
- cmoc の agent 呼び出しに関わる prompt、policy、ファイルアクセス制約、作業ディレクトリ、Structured Output の構成を調査・変更するとき
- 複数の agent call 定義や prompt 構築部品にまたがる構成を確認し、対象領域の下位パッケージを選ぶとき

## Do not read this when
- 実際の CLI サブコマンドの実行処理や、agent call 後の Git・worktree 制御だけを確認するとき
- 特定の prompt、policy、agent call、feedback 契約の場所が明らかな場合は、このルートではなく対応する下位パッケージへ直接進むとき
- oracle file や realization file の正本仕様そのものを確認するときは、対応する oracle または realization の文書を直接読むとき

## hash
- fdf354ecc8b0c19738a593bc01a58269248358f7244f2bb336092e17849d0a82
