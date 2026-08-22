# `doc`

## Summary
- cmoc の正本文書を、アプリケーション仕様（app_spec）、開発ルール（dev_rule）、branch・commit・worktree のモデル、採用しなかった代替案の検討資料（considered_alternative）に分類して案内するディレクトリ。CLI の挙動・ライフサイクル、実装・テスト・環境の規約、設計判断の背景を確認する際の入口となる。

## Read this when
- cmoc の正本仕様・開発規約・設計背景を横断して探すとき
- CLI の挙動、branch／worktree のモデル、Python 開発環境、テスト要件や実行手順の参照先を選ぶとき
- 現行設計の背景や不採用となった代替案を調査するとき

## Do not read this when
- 確認対象の仕様・開発ルール・検討資料が既に特定できており、該当する下位ディレクトリや文書を直接読めるとき
- 個別の実装ファイル、具体的なテスト結果、既存 report や生成物だけを調査するとき

## hash
- f407bd0f93ae6eb2c1029707de3b6b3ca415108975e58ecdf1eea860451d8a58

# `src`

## Summary
- AIコーディングエージェント呼び出しに必要なパラメータ、prompt、アクセス規定、パス文脈、構造化文書を構築する oracle 実装のルートディレクトリ。
- `acp_builder` は用途別の agent call パラメータを扱い、indexing、oracle、realization、feedback、session、TUI、quota probe などの処理へ進む入口となる。
- `prompt_builder` は共通 prompt、用途別 policy、入力文面、構造化 Markdown の構築を扱う。
- `other` は設定、パスモデル、構造化文書など、agent call と prompt 構築を支える共通定義を扱う。

## Read this when
- AgentCallParameter の共通契約やモデル・推論強度・ファイルアクセス・cwd・preflight の定義を確認するとき
- 用途別 agent call の起動条件、prompt、Structured Output 契約、またはその builder の配置先を特定するとき
- 共通 prompt の組み立て、アクセス policy、routing policy、oracle・realization policy、feedback policy を調査・変更するとき
- quota probe、INDEX.md 生成、oracle review・edit・investigation、realization apply・refactor、session join、TUI 起動の agent call を調査するとき
- agent call のパス表記、設定値、構造化文書の表現や Markdown レンダリングを確認するとき

## Do not read this when
- 既存 INDEX.md のルーティング内容だけを確認したいとき
- モデル名やバックエンド固有の解決処理だけを確認するときは、対応する realization の定義元を直接読む
- 用途別 agent call の個別実行処理、通常の realization implementation・test・ancillary、session join の具体的な処理、TUI の画面表示や対話操作だけを確認するとき
- 具体的な feedback issue、report cut reference、raw log、個別レビュー対象などのデータ内容を調べるときは、対応する入力定義や状態管理を直接読む

## hash
- 4488247dcbe9407ce23766a52999f1c13d89d39718e20716227cb3b4a381c6d6
