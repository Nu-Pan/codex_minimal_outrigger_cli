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
- AI agent 呼び出し仕様、共通基盤概念、プロンプト構築仕様を扱う oracle src 領域。AI に渡す論理パラメータ、Structured Output schema、モデル設定、file access profile、パス表記、設定、規範文書モデル、プロンプト標準部品の正本仕様断片へ進む入口になる。
- 機能別の agent call 契約を確認する対象、cmoc 全体で共有される設定・パス・アクセス制御を確認する対象、agent call 用プロンプトの構築順序や注入される標準文書部品を確認する対象に分かれる。

## Read this when
- cmoc が AI agent を呼び出す際の role、goal、prompt、file access profile、モデル設定、reasoning effort、出力契約を確認したいとき。
- apply fork、INDEX.md エントリー生成、oracle review、session join の conflict 解消、tui 起動など、機能別の AI 呼び出し仕様を探したいとき。
- cmoc 全体で共有される設定、パス表記、ファイルアクセス権限、規範文書表現、構造化 Markdown レンダリングの正本仕様断片を確認したいとき。
- agent call 用プロンプトの構築順序、静的・動的プロンプトの配置、標準文書注入フラグ、追加プロンプト、プレースホルダ置換の扱いを確認したいとき。

## Do not read this when
- AI agent 呼び出しの実行手順、プロセス起動、結果取得、エラー処理だけを確認したいとき。
- git 操作、branch 操作、fork 作成・適用、session join 通常処理、CLI 表示など、AI 呼び出し契約の外側にある実行フロー本体を確認したいとき。
- 個別 CLI サブコマンドの利用者向け入出力、状態ファイル仕様、実行フローを探しているとき。
- oracle file と realization file の管理方針そのものや、INDEX.md のルーティング規則を自然言語の規範として確認したいとき。
- Codex CLI の外部仕様、利用可能モデル、最新のモデル情報を調べたいとき。

## hash
- 15d6ffbef305d53c5c7ec20fc76e82a0fe72f643ce27383b73dfd64c53e74682
