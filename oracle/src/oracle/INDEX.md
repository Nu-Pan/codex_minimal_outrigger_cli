# `acp_builder`

## Summary
- AIコーディングエージェント呼び出しのパラメータ契約と、indexing・oracle・realization・session・tui など各用途別の AgentCallParameter 構築定義を扱うディレクトリ。モデル、推論強度、ファイルアクセス、prompt、Structured Output schema、cwd、preflight などの用途別設定を確認する入口であり、具体的な処理は対応する下位定義へ進む。

## Read this when
- 特定用途の agent call の起動パラメータ、prompt、アクセス範囲、cwd、モデル設定、Structured Output 契約の所在を判断するとき
- indexing、oracle、realization、session、tui などの agent call 構築定義を横断して調査・変更するとき

## Do not read this when
- AgentCallParameter や prompt rendering などの共通仕様を確認したいとき
- oracle や realization の正本ファイル、通常の CLI 動作、TUI の画面表示、具体的な処理実装を調べるとき
- 対象用途の具体的な prompt・実装・出力 schema が特定できている場合は、対応する下位ファイルを直接読むとき

## hash
- 49461539615e06edb22f938557755d61e38e7b236814c6243cad6bdb34960d30

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
- agent 呼び出し向けの完全プロンプトを組み立てる prompt-builder 配下の実装群を扱うディレクトリ。placeholder 型、完全プロンプト構築、エディタ入力文面、oracle／realization 説明部品、各種 prompt policy builder を下位要素への入口としてまとめる。

## Read this when
- agent 呼び出し用プロンプトの構成や、基礎規定・ポリシー・目的・placeholder の統合を確認したいとき
- エディタ入力用の初期文面や、oracle／realization の説明文を確認・変更したいとき
- file access、INDEX.md routing、feedback 報告、oracle／realization などの prompt policy の生成方法を確認したいとき

## Do not read this when
- 個別ポリシーの本文や生成文面の詳細だけを確認したいときは、対象の policy ファイルを直接読む
- oracle／realization の個別文書・実装・テストの内容を確認したいときは、それぞれの対象を直接読む
- 生成済みプロンプトの解釈・実行や agent 呼び出しの制御を確認したいときは、呼び出し側・実行側を直接読む

## hash
- 4aad91651aa316a59ca8a465d805b91fa9e2104696ede1c7beade198af50ecb5
