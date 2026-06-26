# `acp`

## Summary
- AI エージェント呼び出しに渡す prompt と実行条件の正本仕様断片を扱う領域。role・summary・goal・ファイルアクセス規則・ルーティング規則・各種標準文書を組み合わせた完全な prompt 構築と、用途別の呼び出しパラメータ構築を確認する入口になる。
- 下位には、サブコマンドや処理段階ごとの agent call parameter を定める領域と、agent prompt に注入される共通規則・標準断片を生成する領域がある。変更要約、所見列挙、所見対応修正、oracle review、INDEX.md エントリー生成、conflict marker 解消、TUI 実行パラメータ選定など、AI に何を読ませ、どの権限とモデル設定で呼び、どの応答契約を期待するかを追うために読む。
- 実際の CLI 制御、git 操作、差分取得、ファイル編集処理、永続状態更新、端末 UI 描画そのものではなく、それらの処理から呼び出される AI エージェントとの入出力境界と prompt 構成を扱う階層。

## Read this when
- cmoc の処理が AI エージェントを呼び出す場面について、渡す role・summary・goal・補助文脈・ファイルアクセスモード・モデル種別・reasoning effort・Structured Output 契約を確認したいとき。
- agent prompt に必ず入る共通規則、任意で注入される oracle / realization / review / apply review / INDEX.md エントリー標準、標準断片間の依存関係を確認したいとき。
- fork 適用後の差分要約や所見処理、oracle file レビュー、INDEX.md エントリー生成、セッション合流時の conflict marker 解消、TUI 実行前のパラメータ選定について、AI 呼び出しの入力と期待出力を調べたいとき。
- AI 呼び出し結果の実装やテストで、読み取り専用・oracle 読み取り・realization 編集などの権限境界、空配列を返す条件、既知情報と重複しない情報だけを返す条件、標準文書の注入条件を確認したいとき。

## Do not read this when
- CLI 引数解析、サブコマンド登録、branch 作成、merge 実行、git コマンド実行、patch 適用、状態ファイル更新、TUI の描画や入力制御など、AI 呼び出しパラメータ以外の実行フロー本体を調べたいとき。
- oracle file や realization file の個別本文から、具体的な仕様内容・実装差・merge conflict の統合内容・修正方針そのものを判断したいとき。
- StructDoc、Standard、Requirement、AgentCallParameter、FileAccessMode、path model など、prompt やパラメータ構築で使われる基盤データ構造や共通型そのものを確認したいとき。
- INDEX.md エントリーや各種レビューの一般的な品質基準本文だけを確認したい場合で、agent call 用 prompt への組み込み条件や呼び出しパラメータには関心がないとき。

## hash
- cb7722b023ffe0cee9df102a0ca38a8efd00c80b049769621bd8e96ec5e9459e

# `basic`

## Summary
- cmoc の基礎概念を支える小さな仕様実装群を扱う領域。エージェント呼び出し条件、root token と実パスの相互変換、規範モデル、階層文書の Markdown レンダリングなど、上位機能から再利用される基本データ構造と変換処理への入口になる。
- バックエンド実行、CLI 個別フロー、永続状態、具体的な仕様本文ではなく、それらを組み立てる前提となる抽象値・パス表記・文書構造・規範構造を確認するための読む先である。

## Read this when
- cmoc 内部で共有される基本型、値オブジェクト、文書生成 helper、root token 解決規則のいずれかを確認・変更したいとき。
- エージェント呼び出し要求をバックエンド固有値へ解決する前段の論理パラメータとして扱う処理を調べたいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` の意味、検出、実パスとの相互変換、git worktree 判定に関わる作業をするとき。
- 規範断片を背景・要求・判断例を持つ構造化文書へ変換するためのデータ構造や入力検証を確認したいとき。
- 見出し階層、本文、コードブロックから Markdown 文字列を生成する処理や、三重引用文字列由来本文の正規化を確認したいとき。

## Do not read this when
- 個別サブコマンドの CLI 引数、実行フロー、プロセス制御、入出力処理を調べたいだけのとき。
- バックエンドが受理する具体的なモデル名、Reasoning effort 値、ファイルアクセス設定への変換規則を確認したいとき。
- プロンプト本文、Structured Output schema の具体内容、個別の仕様文書やテスト本文を探しているとき。
- ファイル保存先、永続状態、ログ、設定、補助スクリプトなど、基本型や root token 解決や文書レンダリングに直接関係しない実装を調べたいとき。
- oracle file と realization file の関係、INDEX.md のルーティング方針、一般的な Markdown 構文や pathlib・git worktree の一般仕様だけを確認したいとき。

## hash
- 468195e72367e959321ba6360654f9c98ad6a166f7e6a0e1dc5c0e2ed8b41f2d

# `config`

## Summary
- 開発対象リポジトリ単位で永続化される cmoc の設定仕様を扱う領域。全体設定、Codex CLI 向け設定、apply fork 向け設定、review oracle 向け設定の構造、既定値、JSON 保存時の Enum 値の扱いを確認する入口になる。

## Read this when
- リポジトリごとに保存される cmoc 設定の項目、入れ子構造、既定値を確認したいとき。
- 初期化処理が生成または同期する、人間編集対象の設定内容について正本仕様を確認したいとき。
- AI エージェント呼び出しの並列数、Codex CLI のモデルや reasoning effort、apply fork の処理上限、review oracle のループ回数上限に関わる仕様変更を扱うとき。

## Do not read this when
- 設定ファイルの実行時の読み書き、JSON 変換、CLI コマンド処理の実装だけを確認したいとき。
- パス語彙やルートディレクトリの定義を確認したいとき。
- apply fork や review oracle の処理アルゴリズム、所見生成、マージ、検証の詳細挙動を確認したいとき。

## hash
- a7101c642419b144683a448b15f7b8720bab8601f12897491ec4c7ae00454cd6
