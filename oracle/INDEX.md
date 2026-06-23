# `doc`

## Summary
- cmoc の正本仕様断片のうち、自然言語で書かれた設計・運用・開発規約を集める領域。利用者向け CLI 挙動、branch / worktree モデル、不採用設計の理由、実装・テスト時の横断的な開発規則など、コードではなく人間が所有する仕様判断の入口になる。
- サブコマンド仕様、実行状態、Codex CLI 呼び出し、ログ、エラー処理、インデクシング、ブランチ分離、開発品質基準、設計上の non-goal を確認し、実装やテストをどの正本仕様断片に合わせるべきかを切り分けるために読む。

## Read this when
- cmoc の CLI 外部挙動、状態遷移、サブコマンド、ログ、エラー、Structured Output、retry / resume、INDEX.md 生成など、利用者に見える仕様を確認したいとき。
- session branch、run branch、linked worktree、fork / join commit、cmoc-managed branch など、git branch / worktree に関する cmoc 固有のモデルを確認したいとき。
- memory、kaizen、作業計画レビュー、後続実行への自動注入など、採用しない設計案の理由や、人間と AI の責務分担の背景を確認したいとき。
- Python 実装、CLI 構成、共通処理配置、開発環境、依存追加、pytest の範囲、実装・テストの品質基準など、realization code を変更する前の横断的な開発規則を確認したいとき。
- oracle file の正本仕様断片としての自然言語仕様を根拠に、realization implementation や realization test の変更方針を判断したいとき。

## Do not read this when
- oracle file、oracle doc、oracle src、oracle test、realization file などの基本分類や、正本仕様断片と実装成果物の一般的な責務分担だけを確認したいとき。
- パスキーワードや root model の定義そのものを確認したいとき。
- プログラミング言語や設定ファイルで書かれた正本実装、正本テスト、具体的な AgentCallParameter の組み立て仕様を直接確認したいとき。
- 既存の realization implementation や realization test の具体的な関数、クラス、現在のコード構造、テスト期待値だけを調べたいとき。
- 生成済みログや実行成果物の事後解析だけが目的で、CLI 仕様、ログ仕様、状態遷移、開発規則を変更または確認しないとき。

## hash
- 2d5078ab8344c042c7db4316b28345b9892b289171a9bb71ab843563db2b624d

# `src`

## Summary
- cmoc の oracle file のうち、Python や JSON で記述された実装系正本仕様断片を収める領域。AI agent 呼び出しパラメータ、共通の基礎モデル、リポジトリ単位の設定モデルなど、realization implementation が従うべきソースコード形式の仕様を扱う。
- 用途別 prompt builder と Structured Output schema、prompt に挿入する標準文書断片、agent call parameter の論理モデル、root token を使うパス解決、構造化 Markdown 描画、規範モデル、cmoc 設定の既定値と保存形を確認するための入口である。
- 実行される製品コードそのものではなく、人間所有の正本仕様断片として実装・テスト生成の根拠になるコード形式文書へ進むための階層である。

## Read this when
- cmoc の実装が従うべき正本仕様断片を、自然言語ドキュメントではなく Python / JSON 形式の oracle file から確認したいとき。
- AI agent 呼び出しに渡す role、goal、補助文脈、file access mode、model class、reasoning effort、Structured Output schema の正本を調べたいとき。
- oracle file / realization file、routing rule、INDEX.md entry standard、oracle review standard、realization standard など、agent prompt に含める標準文書断片の生成元を確認したいとき。
- cmoc 内部で共有される AgentCallParameter、ModelClass、ReasoningEffort、FileAccessMode、root token、構造化文書、規範モデルなどの基礎的な仕様を確認したいとき。
- 開発対象リポジトリごとに永続化される cmoc 設定、Codex CLI 向けモデル名・reasoning effort 名の対応、apply fork や review oracle の上限値を確認したいとき。

## Do not read this when
- 自然言語で書かれた正本仕様断片、概念説明、運用方針、利用者向け仕様を確認したいだけのとき。
- realization implementation や realization test の実際の実装、CLI サブコマンドの実行処理、ファイル I/O、git 操作、状態保存、画面表示を調べたいとき。
- oracle file の内容ではなく、生成済み INDEX.md の現在のルーティング文言だけを確認したいとき。
- 個別の prompt builder、Structured Output schema、基礎モデル、設定モデルの所在がすでに分かっており、その下位対象へ直接進めるとき。
- 既存実装の挙動やテスト結果だけを根拠に修正方針を決めたいとき。

## hash
- 996f32bcdf355efccbac3c71c871d872422d7962962ff32d2837ba146b267d1e
