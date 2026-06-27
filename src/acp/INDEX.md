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
- AI agent に渡すプロンプトを構成するための個別 prompt part 群を収める領域。oracle/realization の基本説明、ファイルアクセス規則、ルーティング規則、各種レビュー・記述品質標準、INDEX エントリー作成標準などを構造化文書として生成する実装がまとまっている。
- 完全な agent call 用プロンプトを組み立てる処理から参照される標準セクションの本文生成箇所であり、個々の規範文書の内容や注入対象となる基本プロンプト片を確認する入口になる。

## Read this when
- AI agent に提示する標準プロンプト片の本文、責務、構成順序、または注入条件を確認・変更したいとき。
- oracle file と realization file の基本概念、oracle 記述規範、realization 品質規範、レビュー所見の判定基準、ルーティング規則、INDEX エントリー作成基準のいずれかをプロンプトとしてどう生成しているか調べたいとき。
- 完全プロンプトに含める標準セクションの依存関係や、追加プロンプトと標準プロンプト片の結合位置を確認したいとき。
- AI 向けのファイルアクセス制約や読み進め規則を、構造化文書としてどの文言で渡しているか確認したいとき。

## Do not read this when
- 個別機能の CLI 挙動、状態ファイル、出力 schema、パス解決、実際のレビュー実行処理など、プロンプト本文生成以外の実装詳細を調べたいとき。
- 構造化文書、標準、要求事項などの基礎データ構造やレンダリング共通処理そのものを確認したいとき。
- 特定の oracle file や realization file の本文内容をレビュー・実装したいだけで、標準プロンプト片の生成内容や判断基準を変更しないとき。
- 実際の INDEX.md エントリー本文を作成・更新する対象ファイルや対象ディレクトリの内容を調べたいだけのとき。

## hash
- 5c666b5f744d6e2fd22a9a20c00e896f11bc406b2fff9c8258559a841a89e223
