# `acp_builder`

## Summary
- AI コーディングエージェント呼び出しの共通パラメータ定義と、oracle・realization・feedback・indexing・session・tui・quota probe 用途別 builder の入口をまとめるディレクトリ。
- basic.py はモデルクラス、推論強度、ファイルアクセスモード、prompt、Structured Output schema、cwd、indexing preflight を含む AgentCallParameter 契約を定義する。
- 下位ディレクトリでは、用途ごとの prompt・アクセス制約・モデル設定・出力 schema を構築する。oracle review、realization の apply/refactor、feedback issue 判定、INDEX.md エントリー生成、session join の conflict 解消、TUI 起動を扱う。

## Read this when
- AgentCallParameter の共通契約や論理的なモデル・推論・ファイルアクセス設定を確認するとき
- 特定の cmoc 機能に対応する agent call builder の所在と、下位の用途別定義へ進む入口を判断するとき
- oracle、realization、feedback、indexing、session join、tui の agent call の prompt・起動設定・Structured Output 契約を横断して調査するとき

## Do not read this when
- 特定用途の prompt 構築や実行制御だけを確認したいときは、対応する下位ディレクトリまたは builder を直接読むとき
- 実際のモデル名やバックエンド固有の解決処理を確認したいときは realization 側の実装を読むとき
- Codex CLI の sandbox や oracle・realization の正本仕様を確認したいときは、対応する oracle 文書を読むとき

## hash
- e7dd952adee515b5bed502af055695f4d777bd687a79431fed01d6cad5d814b4

# `feedback`

## Summary
- 対象ディレクトリは、agent が検出した問題を feedback reporter から collector へ渡すための入力契約を扱う領域です。問題の分類・重要度・影響、人間の対応が必要な理由、原因の確信度、再確認可能な根拠、作業継続状態を表現・検証する下位要素への入口になります。

## Read this when
- feedback reporter の入力形式や、検出した問題を人間向け feedback として構造化する処理を確認するとき。
- 入力契約を構成するスキーマや関連する検証定義を調査・変更するとき。

## Do not read this when
- collector 側の保存、集約、重複判定の仕様だけを確認したいとき。
- feedback の検出方法や、agent が作業を継続するかどうかの判断ロジックだけを確認したいとき。

## hash
- a86d0e0a2687a4eed300cd97383ba6e521f2347418e4446a2bfba702aedcd9ba

# `other`

## Summary
- 対象ディレクトリは、cmoc の設定モデル、パスモデル、構造化 Markdown 文書ノードの実装を扱う。設定項目や既定値、root placeholder と worktree/repository root の解決、文書ノードの Markdown レンダリング規則を確認するための入口である。

## Read this when
- cmoc の設定項目・既定値・シリアライズ構造を変更または確認するとき
- root placeholder、agent call の作業ルート、worktree/repository root の解決規則を確認するとき
- 構造化文書ノードや参照タグを Markdown にレンダリングする挙動を変更または確認するとき

## Do not read this when
- Codex CLI の呼び出し処理や個別 CLI 機能の実装責務を確認したいとき
- oracle review のレビュー処理や所見生成ロジックを確認したいとき
- 設定ファイルの保存内容や人手による調整結果だけを確認したいとき
- Markdown 以外の文書形式や、個別機能におけるパスモデルの利用挙動だけを確認したいとき

## hash
- b97eefaa4d29d7835c2033b91e430e3593bcd5c68643fbc6ef124e09507994df

# `prompt_builder`

## Summary
- agent 向けの完全な prompt を組み立てる prompt-builder の実装群。placeholder 定義、prompt 統合、エディタ入力初期文面、oracle/realization の説明部品、各種 policy 定義を扱い、prompt 生成の共通基盤と個別構成要素への入口となる。

## Read this when
- agent call 用 prompt の構成・統合順序・placeholder 処理を調査または変更するとき
- oracle・realization・routing・file access・feedback reporting など、prompt に注入する policy の構築方法を確認するとき
- エディタ入力用の初期文面や、oracle/realization の説明部品を確認するとき

## Do not read this when
- 生成済み prompt の利用箇所や、oracle・realization 自体の仕様・実装を直接調査するとき
- 個別 policy の本文だけ、または prompt-builder 共通基盤だけを確認したいときは、該当する下位ファイルを直接読む

## hash
- 90684c299a1b98c8a82b7db154a4e7e8285127293212f960dba763f6f10ea2bf
