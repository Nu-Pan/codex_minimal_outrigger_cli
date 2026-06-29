# `doc`

## Summary
- cmoc の正本仕様断片のうち、自然言語の markdown ドキュメント群を収める領域。CLI 外部挙動、実行基盤、branch/worktree モデル、開発規則、不採用設計案など、人間が直接所有する仕様判断を文章として確認する入口になる。
- 利用者に見えるサブコマンド仕様や状態・ログ・出力・隔離境界だけでなく、実装・テスト時に守る横断的な品質基準や、現行方針の背景にある non-goal も扱う。
- 実装ファイルやテストそのものではなく、realization code を正本仕様断片に沿わせるために、どの公開面・制御境界・設計判断を優先すべきかを探すための文書領域である。

## Read this when
- cmoc の CLI 挙動、サブコマンド、利用手順、状態遷移、出力、ログ、エラー処理、run 隔離、agent call 境界など、利用者や外部連携に見える仕様を確認したいとき。
- session fork / join、session branch、run branch、linked worktree、cmoc-managed branch など、git branch・commit・worktree の cmoc 用語と責務を仕様から確認したいとき。
- Python 実装、CLI 構成、共通処理の配置、開発環境、pytest 方針など、realization code を追加・修正する前の横断的な開発規則を確認したいとき。
- AI 記憶、kaizen、自動注入、作業計画レビュー、apply 系 orchestration など、採用しなかった設計案の理由や non-goal を確認して現行方針を変えるべきか判断したいとき。
- oracle file に書かれた人間意図を根拠に、実装差を避けるべき公開面・保存先・失敗時挙動・責務分担を確認したいとき。

## Do not read this when
- path キーワード、root 種別、oracle file / realization file の基本定義だけを確認したいときは、基礎概念やパスモデルを扱う仕様へ直接進む。
- 自然言語仕様ではなく、具体的な関数、クラス、helper、テスト期待値、既存実装の現在構造を調べたいときは、実装またはテストを読む。
- 個別の prompt builder や AgentCallParameter builder が生成する具体的な値、引数、profile 内容だけを確認したいときは、それらの正本となる実装側を読む。
- INDEX.md エントリー生成の一般基準、oracle file の正本性、realization file の編集責務など、リポジトリ全体に共通する基本標準だけを確認したいときは、その標準を扱う文書へ進む。
- 対象が特定の文書領域や単一仕様に絞れているときは、この領域全体ではなく、その下位の直接該当する文書へ進む。

## hash
- eff0885158e480807893633e66a9f8c15363820f859b6148ed69e6cdfbf1205e

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
