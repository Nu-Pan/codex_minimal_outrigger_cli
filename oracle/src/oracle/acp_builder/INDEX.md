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
- AI エージェントへ渡すプロンプト本文を構築する oracle src 群であり、基本プロンプトに加えてファイルアクセス規則、ルーティング規則、oracle / realization の基本概念、oracle / realization の標準、レビュー標準、INDEX.md エントリー標準を StructDoc として生成する入口をまとめている。
- 完全な agent call 用プロンプトを組み立てる処理と、各標準断片の本文生成処理が同じ階層に置かれており、標準フラグ間の依存関係や、個々の標準プロンプトの要求・禁止・許容事項を確認するための起点になる。

## Read this when
- agent に渡す標準プロンプトの構成順序、必ず含まれる規則、任意に追加される標準断片、標準フラグ間の依存関係を確認したいとき。
- ファイルアクセス制約、INDEX.md を使った読み進め方、oracle file と realization file の基本概念、oracle file の書き方、realization file の実装規範を agent 向けプロンプトとしてどう表現しているか確認したいとき。
- oracle file レビューや oracle file と realization file の適用レビューで、どの問題を所見として扱うか、どの問題を所見にしないかの規範本文を確認したいとき。
- INDEX.md エントリー生成・レビュー時に、読む先を選ぶためのルーティング情報として何を書くべきか、何を混ぜるべきでないかの標準本文を確認したいとき。
- 既存の標準プロンプト断片を追加・変更・整理し、agent call 用プロンプトへ注入される条件や本文内容を調整したいとき。

## Do not read this when
- 特定の CLI サブコマンド、出力 schema、状態ファイル、パスモデル、個別機能の正本仕様本文を探しているとき。
- StructDoc や Standard / Requirement のデータ構造、整形、表示、連結の基盤実装そのものを確認したいとき。
- 実際のファイル権限チェック、サンドボックス制御、エージェント実行経路、外部プロセス呼び出しの挙動を調べたいとき。
- oracle file と realization file の概念や標準本文ではなく、具体的な realization implementation や realization test の現在の実装箇所を探しているとき。

## hash
- ae5f6662284ea4d2966aed850a5513f855bd22edc5190c5b4d972d5c1c292a8d
