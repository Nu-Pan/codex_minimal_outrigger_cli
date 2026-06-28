# `doc`

## Summary
- cmoc の oracle file のうち、自然言語 markdown で書かれた正本仕様断片を集めた領域。利用者向けアプリケーション挙動、git branch / commit / worktree のモデル、採用しなかった設計案、realization code 開発時の横断規則を扱う。
- 外部 CLI 挙動や実行時制御を確認する仕様、ブランチ分離モデル、設計判断の non-goal、Python 実装・テスト・開発環境の規則へ進むための入口になる。

## Read this when
- cmoc の正本仕様断片のうち、自然言語で書かれた仕様文書から読むべき対象を選びたいとき。
- CLI サブコマンド、Codex CLI 呼び出し、ログ、エラー処理、インデクシング、実行隔離、セッション状態など、利用者に見える挙動や実行時制御の仕様を探したいとき。
- session / run / apply / review などで使う branch、commit、linked worktree の関係や命名モデルを確認したいとき。
- AI 記憶、作業計画レビュー、apply 系 orchestration など、採用しなかった workflow や設計案の背景を確認したいとき。
- realization code を追加・変更・検証する前に、Python コーディング、CLI 構成、共通処理、開発環境、テスト方針の横断規則を確認したいとき。

## Do not read this when
- oracle file と realization file の一般的な定義、責務分担、正本仕様断片としての基本原則だけを確認したいとき。
- パスキーワード、root 種別、作業ディレクトリ概念そのものの定義だけを確認したいとき。
- プログラミング言語や設定ファイルで書かれた oracle src、または oracle test の具体的な schema、parameter builder、prompt 生成、テスト実装を探しているとき。
- realization implementation や realization test の現在のファイル配置、関数、クラス、既存テスト期待値など、実装側の具体構造だけを調べたいとき。
- 対象がすでに特定の CLI 挙動、サブコマンド、branch モデル、不採用案、開発規則に絞れている場合は、その責務を直接扱う下位文書へ進む。

## hash
- 3692f17696531d3fb7a3bb1dd1ee0fb1ab6a338f1fa3f230238cb2b8b99f98e9

# `src`

## Summary
- AI agent 呼び出しに渡す論理パラメータ、完全プロンプト、標準プロンプト部品、Structured Output schema、共有補助モデルを実装形式で定義する正本仕様断片群への入口。モデル品質区分、reasoning effort、ファイルアクセスモード、用途別の呼び出し契約、設定、パス表記、規範、構造化 Markdown の基礎型を扱う。
- 本文は自然言語仕様そのものではなく、cmoc が AI agent に渡す契約や正本仕様断片を生成・表現するための Python 実装と JSON schema で構成される。用途別の呼び出しパラメータ、共通プロンプト構成、標準文書生成、共有データ構造のどれを確認すべきかを切り分ける起点になる。

## Read this when
- AI agent 呼び出しに使う論理モデル区分、reasoning effort、ファイルアクセスモード、prompt、Structured Output schema の正本仕様断片を確認したいとき。
- indexing、oracle review、apply fork、session join、TUI 実行など、用途別の AI 呼び出しがどの role・summary・goal・標準プロンプト・schema・権限を使うか調べるとき。
- 完全プロンプトの構成順、静的プロンプトと動的プロンプトの分離、標準プロンプト注入フラグの依存関係、プレースホルダ定義の扱いを確認するとき。
- oracle file と realization file の基本説明、oracle standard、realization standard、review/apply/indexing 向け standard、ルーティング規則、ファイルアクセス規則がどのようにプロンプト化されるか確認するとき。
- cmoc 全体で共有される永続設定、root path placeholder と実パス解決、規範データ構造、階層化文書の Markdown レンダリング helper の正本仕様断片を調べるとき。

## Do not read this when
- 利用者向け CLI サブコマンドの実行フロー、状態ファイルの読み書き、git 操作、外部プロセス起動、画面操作、バックエンド CLI への実パラメータ変換だけを調べたいとき。
- 自然言語で書かれた oracle doc の要求本文や、oracle test の検証内容そのものを読みたいとき。
- realization implementation や realization test の現在の実装・修正対象を探しており、正本仕様断片としての型・構築規則・AI 呼び出し契約を確認する必要がないとき。
- 特定用途の prompt 構築、schema、設定モデル、パスモデル、規範モデルなど、読むべき下位対象がすでに分かっているとき。
- AI agent への依頼文の最終レンダリング結果だけ、または実行時に解決された実パラメータだけを確認したいとき。

## hash
- 67bc0488d3d8e9271367801fb22dcf857bbc7952d4d1b166f8b547ae74a3a68c
