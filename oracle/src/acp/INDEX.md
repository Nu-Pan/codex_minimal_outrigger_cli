# `builder`

## Summary
- AI エージェント呼び出しパラメータ構築に関する正本仕様断片を集める領域。サブコマンドごとに、どの補助文脈を読み取り、どの role・goal・制約・モデル設定・reasoning effort・ファイルアクセス範囲・Structured Output 契約でエージェントを呼び出すかを扱う。
- fork 適用時の差分要約・所見列挙・所見対応修正、INDEX.md エントリー生成、oracle review の所見生成・理由調査・採否判定・整理、セッション合流時の conflict 解消、TUI 実行前のパラメータ選定など、AI 呼び出しの入出力境界を確認する入口になる。
- 実際の CLI 制御フロー、git 操作、ファイル修正アルゴリズム、TUI 描画、永続状態更新そのものではなく、それらの処理から呼び出される AI エージェントへ何を渡し何を返させるかを読むための階層。

## Read this when
- cmoc の各処理が AI エージェントを呼び出す場面で、prompt 構成、補助文脈、読み取り・編集権限、モデル種別、reasoning effort、Structured Output schema の対応を確認したいとき。
- fork 適用後レビュー、INDEX.md エントリー生成、oracle review、セッション合流時の conflict 解消、TUI 実行パラメータ選定のいずれかについて、エージェント呼び出しに渡す入力情報と期待する応答契約を調べたいとき。
- oracle file、realization file、差分テキスト、既知所見、理由、対象パス、元プロンプト、標準文書などの補助情報を、AI 呼び出し用 prompt にどう組み込むか追いたいとき。
- AI 呼び出しの結果を検証する実装やテストで、空配列を返す境界、既知情報と重複しない情報だけを返す境界、修正用と読み取り専用のアクセス条件などを確認したいとき。

## Do not read this when
- CLI 引数解析、サブコマンド登録、branch 作成、merge 実行、git 操作、差分取得、patch 適用、永続状態更新、端末 UI 描画など、AI 呼び出しパラメータ以外の実行フロー本体を調べたいとき。
- 個別ファイルの patch 内容、merge conflict の具体的な統合判断、realization file の修正ロジック、oracle file 本文からの具体的な所見材料など、対象本文そのものを読んで判断する作業をしたいとき。
- oracle standard、realization standard、review oracle standard、path 語彙、共通 prompt 部品、AgentCallParameter 型、file access mode などの共通定義そのものを確認したいとき。
- INDEX.md 全体のルーティング方針、エントリー記述品質基準、生成結果の内容評価、または一般的なルーティング文書の書き方を確認したいとき。

## hash
- 8477935ea87066eb3eff8ae75c41dffee5f719231533ca0cee71623b4f09fff7

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
