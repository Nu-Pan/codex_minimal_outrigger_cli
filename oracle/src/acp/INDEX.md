# `builder`

## Summary
- 各サブコマンドや用途別に、AI agent 呼び出しパラメータを組み立てるための正本仕様断片へ進む入口。
- レビュー、apply fork 後の確認・修正支援、INDEX.md エントリー生成、セッション合流時の conflict 解消、TUI 実行前のパラメータ選定について、prompt、補助文脈、ファイルアクセス制約、モデル設定、reasoning effort、Structured Output 契約との接続を扱う下位領域をまとめる。
- 実際の CLI 制御フロー、git 操作、端末 UI、永続状態更新、本文標準そのものではなく、それらの処理から呼び出される判定・レビュー・整理・修正支援 agent へ何を渡し何を受け取るかを確認するための分岐点になる。

## Read this when
- cmoc の各機能が AI agent を呼び出す際の role、summary、goal、補助 prompt、参照 standard、ファイルアクセスモード、モデル種別、reasoning effort、出力 schema の正本値を探したいとき。
- oracle review、apply fork 後レビュー、INDEX.md エントリー生成、セッション合流時の conflict 解消、TUI 実行前パラメータ選定のいずれかについて、呼び出し入力と応答契約の対応を調べたいとき。
- 対象機能の実処理ではなく、AI に渡す文脈の組み立て方や、AI から返る Structured Output をどの意味単位で期待するかを確認したいとき。
- 同階層の下位領域のうち、どの agent 呼び出し仕様へ進むべきかを、サブコマンドや用途別に切り分けたいとき。

## Do not read this when
- CLI 引数解析、サブコマンド全体の制御フロー、fork 作成、ブランチ操作、merge 実行、差分取得、端末 UI 描画、永続状態更新など、AI 呼び出しパラメータ以外の実装仕様を調べたいとき。
- oracle file、realization file、path keyword、repo root、work root、各種 standard 本文、共通 prompt 構築部品の一般定義だけを確認したいとき。
- 個別の oracle file 本文を読んで具体的なレビュー所見、変更判断、conflict 解消方針、INDEX.md エントリー内容そのものを考えたいとき。
- 実装ファイルやテストにおける具体的な関数、CLI 表示、保存形式、git command 実行手順、パッチ生成手順を探しているとき。

## hash
- a123ebbec96bc631fe91246edac90bb495b1958e5aa81517fd1cc4116532674b

# `prompt_parts`

## Summary
- agent call に渡す各種プロンプト部品を構築する oracle src 群への入口である。
- ファイルアクセス規則、ルーティング規則、oracle / realization の基本概念、oracle / realization / review / INDEX エントリーの標準、完全なプロンプトへの組み立て方を扱う。
- 個別機能仕様そのものではなく、AI に渡す作業規範や標準断片の文面と、それらを完全なプロンプトへ含める条件を確認するための階層である。

## Read this when
- agent に渡す標準プロンプト部品の本文、責務、組み立て順序、依存関係を確認したいとき。
- ファイルアクセス規則、INDEX.md を使ったルーティング規則、oracle file / realization file の基本概念をプロンプトとしてどう提示しているか確認したいとき。
- oracle file、realization file、oracle review、oracle と realization の比較レビュー、INDEX.md エントリー生成の各標準を確認または変更したいとき。
- 新しい標準プロンプト断片を追加する前に、既存の標準断片の範囲、重複、完全プロンプトへの注入条件を把握したいとき。

## Do not read this when
- 特定の CLI サブコマンド、出力 schema、状態ファイル、パスモデルなど、cmoc の個別機能仕様を探しているとき。
- 実際の realization implementation や realization test の現在のコード挙動を調査したいだけのとき。
- StructDoc など、プロンプト部品を表現する下位データ構造そのものの実装を確認したいとき。
- 生成されたプロンプトをどの agent 実行経路へ渡すか、または実際のファイル操作・権限チェック・サンドボックス制御の実装を確認したいとき。

## hash
- f505b8893bffe7a604ba8388cedb63a259644b7e827b79d0884cfc6b0e98c8c9
