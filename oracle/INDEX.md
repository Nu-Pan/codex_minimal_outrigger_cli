# `doc`

## Summary
- cmoc のアプリケーション仕様を定義する正本文書群。CLI、agent call、ログ、prompt、session/run lifecycle、branch・commit・worktree、サブコマンドなどの利用者向け挙動を扱う。個別仕様文書を探すための入口。

## Read this when
- cmoc のアプリケーション挙動や CLI・agent call・ログ・prompt・session/run の正本仕様を探すとき
- session fork、run の隔離、branch・commit・worktree の関係やライフサイクルを確認するとき
- 開発環境、CLI 実装配置、Python 規則、realization test の方針を確認するとき
- 採用されなかった設計案や作業方式の背景を確認するとき

## Do not read this when
- 確認したい個別仕様文書が明確なときは、その文書を直接読む
- 構築済み環境での具体的なテスト・Ruff・mypy の実行手順だけを確認するときは、repository local の run-cmoc-tests skill を読む
- 実装構造やテストの詳細だけを確認するときは、対応する realization file を直接読む

## hash
- c9903d04fb12d273403652e166563d4280695065e928b889089088a4e8a0c7d8

# `src`

## Summary
- AIエージェント呼び出しに関する正本ソースを扱うディレクトリ。agent call のパラメータ・起動条件、設定と root 解決、Structured Document、prompt builder の実装を調査する入口。

## Read this when
- Agent Call Parameter、Structured Output、agent call の起動条件やパラメータを変更・調査するとき
- CmocConfig、root 解決、Standard・Requirement・StructDoc の定義や Markdown レンダリングを調査するとき
- prompt builder、プレースホルダ、入力エディタ初期文、oracle・realization・INDEX.md 関連のプロンプト生成規則を調査するとき

## Do not read this when
- CLI サブコマンドの実際の処理や画面操作の挙動を調査するとき
- 共通の prompt 構築・実行フローやバックエンド固有のモデル解決を調査するとき
- 個別の oracle 文書や realization 実装の内容だけを調査するとき

## hash
- 2abeba640329884146f2dec5837e62b0faa8a473b298b5f2e1e81b50877c99a2
