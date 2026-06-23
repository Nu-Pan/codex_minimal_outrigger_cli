# `doc`

## Summary
- 自然言語 Markdown で書かれた cmoc の正本仕様断片群への入口。利用者向け CLI 挙動、Codex CLI 呼び出し、ログ、エラー処理、インデクシング、実行隔離、セッション状態、標準利用フロー、git branch / worktree モデル、開発時の実装・テスト規則、不採用にした設計案の根拠を扱う。
- 実装やテストへ進む前に、どの仕様断片を正本として読むべきかを切り分けるための領域。個別の外部挙動、横断的な実行規約、開発規約、設計上の non-goal を確認する起点になる。

## Read this when
- cmoc の外部仕様、サブコマンド実行フロー、ログ、エラー、状態管理、Codex CLI 呼び出し、INDEX.md 自動生成、run 隔離、標準利用手順のいずれかを実装・テスト・仕様確認するとき。
- session branch、run branch、session home branch、run worktree、fork / join commit など、cmoc が git branch・commit・worktree をどう扱うか確認したいとき。
- Python 実装、CLI 構成、共通処理の配置、開発環境、pytest による自動テスト方針など、realization code を変更する前の横断的な開発規則を確認したいとき。
- AI-generated memory、作業計画レビュー、apply の独立計画ステップなど、一般には有効に見える設計案を cmoc が採用しない理由を確認したいとき。
- oracle file を根拠に realization file を追従させる作業で、利用者向け仕様・開発規約・設計上の不採用判断のどれを読むべきかまだ絞り込めていないとき。

## Do not read this when
- oracle file、realization file、oracle doc、oracle src、oracle test などの基本分類や、正本仕様断片としての一般原則だけを確認したいときは、より基本的な定義・標準を読む。
- path keyword、repo root、run root、work root などのパスモデルだけを確認したいときは、パスモデルを定義する仕様・実装を直接読む。
- 具体的な realization implementation や realization test の現在のコード構造、関数名、依存関係、既存テスト期待値を調べたいときは、対象の実装・テスト側を読む。
- 特定の下位仕様断片が既に分かっており、その詳細だけが必要なときは、このまとまりから読み始めず、該当する本文へ直接進む。
- INDEX.md エントリーの一般的な品質基準、oracle / realization の一般標準、またはルーティング文書の書き方だけを確認したいときは、この自然言語仕様群ではなく該当する標準を読む。

## hash
- 35b1c35e300c2fdbdbb01e5b30c9b6f33333ebf621d0b32afc99da07c679b333

# `src`

## Summary
- cmoc の正本仕様断片のうち、プログラミング言語や設定ファイルとして記述された oracle src 群への入口。AI agent 呼び出し仕様、共有基礎モデル、リポジトリ設定など、実装に近い形で表現された仕様断片を用途別の下位領域へ振り分ける。
- 自然言語文書としての方針説明ではなく、cmoc 内部の型、パラメータ、prompt 構築、設定値、schema、パス表現など、realization implementation へ反映される正本仕様断片を探すためのルーティング階層。

## Read this when
- cmoc の実装に対応する正本仕様断片のうち、Python 実装や設定ファイルとして書かれた仕様領域を探したいとき。
- AI agent 呼び出しの prompt、file access mode、model/reasoning 設定、Structured Output schema、標準プロンプト断片など、agent call に関する実装寄り仕様を確認したいとき。
- cmoc 内で共有される基本データ構造、path keyword、root token と実パスの対応、規範モデル、構造化自然言語文書の描画 helper などの基礎概念を確認したいとき。
- 開発対象リポジトリ単位の設定 JSON、既定値、Codex CLI 向け model/reasoning 名の対応、AI 呼び出しや review oracle の上限制御値を確認したいとき。
- oracle file のうち、自然言語ドキュメントではなく実装形式で表現された正本仕様断片から、下位ディレクトリへ進む入口を選びたいとき。

## Do not read this when
- oracle doc として書かれた自然言語仕様、設計方針、用語説明、標準規範そのものを読みたいとき。
- oracle test として書かれたテスト形式の正本仕様断片を確認したいとき。
- realization implementation や realization test の現在の実装・テストを調べたいとき。
- 生成済み INDEX.md のルーティング内容だけを確認したいとき。
- README、AGENTS、memo、または oracle 外の補助ファイルを調べたいとき。

## hash
- 7148165b597878459c58e39b38c0844b287dd0fd22abda30453982ceb3db74a9
