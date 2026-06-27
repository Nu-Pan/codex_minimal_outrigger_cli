# `builder`

## Summary
- AI エージェント呼び出し用のパラメータ構築を集約する領域。各コマンドや処理フェーズごとに、complete prompt、補助入力、file access mode、model/reasoning、応答契約をどう組み立てるかを確認する入口になる。
- 扱う範囲は、apply fork の変更要約・所見列挙・所見対応、indexing の目次エントリー生成、review oracle の所見列挙・理由調査・採否判定・整理、session join の conflict marker 解消、TUI の実行パラメータ選定である。
- 実際の CLI 制御、git 操作、作業ツリー変更、所見や目次の保存・描画ではなく、AI に何を読ませ、どの権限で呼び出し、どの返却形を期待するかを定義する層である。

## Read this when
- cmoc の各機能が AI エージェントへ渡す role、summary、goal、補助文脈、標準文書参照、ファイルアクセス権限をどのように構成しているかを全体から探したいとき。
- apply fork、indexing、review oracle、session join、TUI parameter resolve のうち、どの AI 呼び出しパラメータ構築へ進むべきかを判断したいとき。
- AI 呼び出しで使う model class、reasoning effort、file access mode、complete prompt、structured output の対応関係を処理種別ごとに追いたいとき。
- 新しい AI 呼び出しフェーズを追加または既存フェーズを変更する前に、同種の prompt 構築・補助入力埋め込み・応答契約指定の既存パターンを確認したいとき。
- 実装やレビューや目次生成そのものではなく、それらを AI に依頼するための入力条件と出力制約の設計を確認したいとき。

## Do not read this when
- CLI 引数解析、サブコマンド登録、実行順序、状態管理、保存、表示、git branch 操作など、AI 呼び出し前後の制御フローを調べたいとき。
- complete prompt の共通構築、Markdown rendering、StructDoc、path model、AgentCallParameter、file access mode などの基盤型や共通部品そのものを確認したいとき。
- 特定の oracle file や realization file の本文、具体的な仕様内容、実装修正箇所、テスト内容を直接調べたいとき。
- 生成された所見、変更要約、目次エントリー、TUI パラメータ選定結果を保存・集約・描画・適用する処理を確認したいとき。
- AI 呼び出しパラメータではなく、差分検出、対象ファイル列挙、レビュー対象選定、conflict 検出、エディタ入力処理などの前段ロジックを調べたいとき。

## hash
- e4c670091bf23bb726f4c7bd4f6e921828358f97f583b3527e0ad90c057a2196

# `prompt_parts`

## Summary
- AI agent に渡す各種プロンプト断片を構築する実装群を集めた領域。oracle/realization の基本概念、ファイルアクセス制約、ルーティング規則、レビュー判定基準、品質標準、INDEX エントリー標準、完全プロンプト組み立てなどを、それぞれ構造化文書として生成する責務を持つ。
- 個別の標準文書本文を作る構築関数と、複数の標準・基本情報・追加プロンプトを agent call 用の完全なプロンプトへまとめる処理への入口になる。

## Read this when
- AI agent に渡すプロンプト全体へ、どの基本情報・制約・標準文書が含まれるかを確認または変更したいとき。
- oracle file、realization file、review、INDEX エントリー、routing、file access などの標準プロンプト本文を生成する実装を探したいとき。
- 標準プロンプト断片の注入条件、注入順序、前提となる基本情報との依存関係を確認したいとき。
- レビュー所見の判定基準や、oracle/realization の品質基準を agent 向け文書としてどう表現しているか調べたいとき。

## Do not read this when
- StructDoc、Standard、Requirement などの構造化文書データ型や汎用変換処理そのものを調べたいとき。
- CLI コマンド、状態ファイル、パス解決、実際のレビュー実行、ファイル入出力など、プロンプト本文生成以外のプロダクト挙動を調べたいとき。
- 特定の oracle file や realization file の実際の仕様内容・実装内容を確認したいだけのとき。
- テストコードやテスト fixture の挙動を確認したいとき。

## hash
- ed88ede9e86903da2bf67f9d5ace776655545aaf50d815c8eaf2b1a413c4df42
