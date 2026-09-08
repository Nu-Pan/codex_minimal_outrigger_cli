# `acp_builder`

## Summary
- AI コーディングエージェント呼び出しの共通パラメータ型とファイルアクセスモードを定義する。
- quota availability probe、INDEX.md エントリー生成、feedback issue 処理、oracle・realization・session・TUI など、用途別の agent call builder への入口をまとめる。
- 各用途に応じた prompt、Structured Output schema、作業ディレクトリ、editor input handoff、indexing preflight の設定を確認できる。

## Read this when
- agent call の共通パラメータ、アクセスモード、prompt、Structured Output schema、cwd、editor input handoff、または indexing preflight の設定を確認するとき。
- 用途別の agent call builder を探すとき。
- quota probe、indexing、feedback、oracle、realization、session、TUI の agent call 構築責務の入口を確認するとき。

## Do not read this when
- 特定の agent call の prompt や出力契約の詳細を確認したいときは、該当する下位ファイルを直接読む。
- agent call の共通実行処理や Codex CLI の実際の挙動を調査するとき。
- oracle・realization file の具体的な内容、編集手順、または feedback issue の保存・受付処理を確認するとき。

## hash
- 1c30d36fd04b48d7e50c884f1e64ee15f70f18d6731aa581d251b69cfd0c1ed5

# `editor_input_handoff`

## Summary
- cmoc のエディタ入力上書きツールが受け取る入力契約を定義する JSON Schema です。
- 上書き対象を識別する値と、対象へ渡す内容を指定するための直接の参照先です。

## Read this when
- エディタ入力上書きツールの呼び出し形式を確認するとき。
- 上書き対象と書き込む内容に必要な入力項目を確認するとき。

## Do not read this when
- エディタ入力上書き処理の実装やワークフローを確認するとき。
- エディタ入力上書き以外のツール入力契約を確認するとき。

## hash
- ab2b3f70177976188963683a20698484d105ee1df31cc928aa2c4f2b6ecbdd56

# `feedback`

## Summary
- フィードバック問題報告入力の正本スキーマを扱う領域で、分類・重要度・影響・未解消制約・原因・再確認用根拠・継続状態の入力契約への入口。

## Read this when
- cmoc_feedback.submit_observation に送る問題報告の入力項目、許容値、文字数制約、根拠に応じた path 条件を確認するとき。
- 問題報告を JSON として組み立てる際に、reporter input の形式と根拠記述の要件を確認するとき。

## Do not read this when
- 問題報告の送信手順や collector の処理を確認したいとき。
- reporter input のスキーマではなく、フィードバック収集結果や重複判定の実装を確認したいとき。

## hash
- 709d2b0ca7660b1772a43fe8fdaed710d40142564511ba28a435a49b6776aa67

# `other`

## Summary
- 開発対象リポジトリ単位で変化する cmoc 設定を集約し、Codex CLI の provider・agent call 設定、並列数、アクセス規定違反時の復旧試行回数を定義する設定モデル。
- agent call で共有するパスコンテキストと、{{cmoc-root}}・{{repo-root}}・{{run-root}}・{{work-root}} の解決・変換規則を提供するパス基盤。Git worktree metadata に基づく各ルートの探索も担う。
- 構造化された文書ノードを Markdown へレンダリングし、見出し階層、参照可能ブロック、コードフェンス、規定文、三重引用文字列の整形を扱う下位ヘルパー。

## Read this when
- cmoc の設定項目、既定値、Codex CLI 呼び出し単位のモデル設定、provider-local 設定、並列数、復旧試行回数、または設定ファイルの扱いを確認・変更するとき。
- agent call の cwd から worktree root や main repository root を導出する規則、root placeholder の解決・実パス変換、Git worktree metadata に基づく探索を確認・変更するとき。
- 構造化データから cmoc 用 Markdown を生成する処理、見出し深度、cmoc_block 参照タグ、可変長コードフェンス、規定文のレンダリング、ntqs の整形を確認・変更するとき。

## Do not read this when
- agent call のプロンプト生成や Codex CLI の実行フローそのものを調べるとき。設定値の永続化・同期処理だけを調べる場合は、その処理を実装する対象を直接読む。
- 個別の CLI 機能や realization の実装責務だけを確認するとき。パスモデルを介さない一般的なファイル操作や、Git・root placeholder と無関係な仕様を調べるとき。
- INDEX.md の構造やルーティング規則そのものを確認するとき。Markdown 以外の文書形式や、このレンダリングヘルパーを利用しない CLI 処理を調べるとき。

## hash
- d05479d0fdfdc7f2d0f470cd2e5fd2e5d21cae1728681206596d6710fcda7ee2

# `prompt_builder`

## Summary
- agent call 向けの完全な構造化 prompt を、基礎文面、選択可能な各種 policy、目的、追加 prompt、path context の placeholder 定義から組み立てる prompt 構築層。
- prompt editor の初期入力として、記入案内と完全 prompt の HTML コメント埋め込み文面を生成する入口。
- oracle file と realization file の基本関係・分類を説明する共有 prompt 部品と、各 policy の生成定義を下位入口として提供する。
- policy 配下には、file access、routing、INDEX.md エントリー、oracle／realization、feedback、conflict resolution、editor handoff など、個別規定の prompt 生成処理が分かれている。

## Read this when
- agent call に渡す prompt の全体構成、構成要素の選択条件、placeholder の統合や競合拒否を確認したいとき。
- prompt editor に表示する初期入力文面や、完全 prompt の埋め込み形式を確認・変更したいとき。
- oracle file と realization file の基本的な役割・分類説明を prompt に組み込む箇所を確認したいとき。
- 個別 policy の文面や生成条件を確認したいときは、policy 配下の対応する定義から調査を始めるとき。

## Do not read this when
- 個別 policy の具体的な要求・禁止・許可事項だけを確認したいときは、prompt_builder 全体ではなく対応する policy 定義を直接読むとき。
- oracle／realization の正本仕様、ファイル列挙規則、CLI の実装責務を確認したいときは、prompt builder ではなく対応する oracle file を読むとき。
- prompt editor の Markdown ノード構造やレンダリング仕様だけを確認したいときは、editor input の構築処理ではなく struct_doc の実装を直接読むとき。
- 生成済み prompt の実行方法や、policy に含まれない共通型の実装だけを調べるとき。

## hash
- aeb93dfe1782811a44a35abb54d531084743b733f2f1fd65ba202a8c461b2ddf
