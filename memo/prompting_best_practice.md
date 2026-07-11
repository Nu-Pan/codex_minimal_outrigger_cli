# prompting best practice

## 概要

- 公式の情報から、cmoc に適用できそうな要素を抽出引き上げてまとめた文章がこれ

## 調査結果

### プロンプトの書き方（お作法）

- プロンプトに何を含めるべきか？　これは `<cmoc-root>/oracle/doc/app_spec/sub_command/tui.md` に反映済み

### 入力キャッシュ

- プレフィックス完全一致で 1K トークン以上だとキャッシュが効いて安く済む
- 動的に変化するプロンプトは末尾側に配置する

### AGENTS.md

- 短く完結に
- `AGENTS.md` は実際に発生した失敗に基づいて更新するべき
- 分散配置する
    - 実装の規約はソースコードのフォルダの AGENTS.md に、テストの規約はテストコードフォルダの AGENTS.md に書く

### プロンプトの改善規則

- 失敗実績に基づいてのない規約追加
    - AGENTS.md を予防的な細則で肥大化させない。
    - 例：「起きたことのないミス対策を大量に追加する。」


## 公式ソース別のメモ

### [Reasoning models | OpenAI API](https://developers.openai.com/api/docs/guides/reasoning)

- Reasoning モデル自体に付いての説明
- GPT-5.5 も当然 Reasoning model に該当する
- Reesponses API を使って直接呼び出す場合の話っぽい
- プロンプトとしてはタスク、制約、出力フォーマットが推奨
- Reasoning Effort は品質回復のための手段ではない

### [Reasoning best practices | OpenAI API](https://developers.openai.com/api/docs/guides/reasoning-best-practices)

- o シリーズを念頭に置いてるっぽいので、情報古い
- GPT-4o とかの時代のまま取り残されている
- スルーする

### [Prompt guidance | OpenAI API](https://developers.openai.com/api/docs/guides/prompt-guidance)

- モデルシリーズ別のプロンプティングガイド
- 手順よりも結果
    - 作業手順を長々と書くよりも、求める結果を短く述べたほうが良い
    - ゴールだけ示して、モデルに解決策を委ねたほうが良いということ
    - Do:
        - 良い状態とは？
        - 重要な制約は？
        - 何を根拠とする？
        - 最終的な回答の用件は？
        - コンテキストとして利用できる情報は？
        - ゴール条件は
        - 成功の基準は？
        - 停止条件は？
- 不要な絶対的ルールは避ける
    - 本当に必要な真の不変条件だけを書く
    - Do:
        - 安全ルール
        - 必須出力フィールド
        - 決死って起こってはいけないアクション
- 根拠の扱い方を明示する
    - Citation Formatting も参照
    - Do:
        - どのような根拠が必要か？
        - 十分な証拠とは何か？
        - 証拠が不足している場合にどうするべきか？
        - 十分な証拠が得られたとできる条件は？
- 自由記述可能な部分は明示する
    - 根拠に基づく必要がある所、自由に記述してよいところ、境界を明示する
- モデルに動作確認を促す
    - 具体的な検証コマンドと、その実行を促す
    - ゴール条件に含めようという話だろう
- phase
    - `phase` を指示に含めることで、中間出力と最終出力を区別出来る？
    - TODO ちょっとよく分からない

### [Citation Formatting | OpenAI API](https://developers.openai.com/api/docs/guides/citation-formatting)

- この文章自体は、Responses API とかをつかってターン単位のプロンプト動的生成をする時に、引用を正しくやるための PUA 記法について説明している
- markdown ドキュメント上の引用系とは全く別の話（別の話としてやるべき）
- Codex CLI のプロンプトとして PUA 記法はやっても良いが、大げさかも
- Codex CLI の最終結果を機械的検証をしたければ PUA を使う？
- どうせ、機械生成するのだから PUA に従っといて損はなさそう

## [Using GPT-5.5 | OpenAI API](https://developers.openai.com/api/docs/guides/latest-model)

- GPT-5.5 のリリースノートのような文章
- 他の文章の短縮版なのでスルー

## [Agents SDK | OpenAI API](https://developers.openai.com/api/docs/guides/agents)

- エージェントを組むなら Responses API じゃなくて Agents SDK 使ったほうが良いよとのこと
- cmoc 的にはそれより更に上位の Codex CLI を使っているので気にしなくて良い

## [Compaction | OpenAI API](https://developers.openai.com/api/docs/guides/compaction)

- コンテキストコンパクションについての文章
- Codex CLI でラップされてるので気にしなくて良い

### [Customization – Codex | OpenAI Developers](https://developers.openai.com/codex/concepts/customization?utm_source=chatgpt.com)

- `AGENTS.md`
    - 書くべきこと
        - ビルド・テストコマンド
        - レビュー観点
        - リポジトリ固有の慣習
        - ディレクトリごとの個別の指示
        - 繰り返さえるミスの対策
        - ディレクトリ構造のガイド
    - `AGENTS.md` 外のインフラとの組み合わせる
        - プリコミットフック
        - リンター
        - 型チェッカー
    - 定期実行による `AGENTS.md` のチェック
        - TODO AGENTS.md の内容を AI に任せたら誤りが蓄積して終わるのでは
    - 重要な指示を各ディレクトリに分散配置することが大事
        - TODO 分散配置で何するのか謎
        - 実装・テストで指示を書き分けるとかだろうか
- Skills
    - 毎回従う手順（リリース・レビュー・ドキュメント更新）
    - チーム固有の知識
    - 参考資料、スクリプト

### [Best practices – Codex | OpenAI Developers](https://developers.openai.com/codex/learn/best-practices?utm_source=chatgpt.com)

- Codex のベストプラクティス
- プロンプトに含める項目
    - 目標：何を変えようとしている？　何を構築しようとしている？
    - コンテキスト：このタスクに関連するファイル、フォルダ、ドキュメント、例、エラーログ
    - 制約事項：従うべき規格、アーキテクチャ、安全要件、慣例
    - 完了条件：テストに合格したら、動作を変更したら、バグが再現しなくなったら
- 最初に計画を立てる
    - Plan モードを使う
    - Codex にインタビューさせる
    - `PLANS.md` ってのがあるらしい
- `AGENTS.md`
    - 書くべき
        - リポジトリのレイアウトと重要なディレクトリ
        - プロジェクトの実行方法
        - ビルド、テスト、リンティングのコマンド
        - エンジニアリングの慣習と PR に関する期待
        - 制約事項と禁止事項
        - 作業完了の意味、検証の方法
    - 短く完結に
    - `AGENTS.md` は実際に発生した失敗に基づいて更新するべき
- テストとレビュー
    - ユーザーにターンを返す前に、テストの実行・自己レビューの実行をやらせる
    - 具体的には
        - 変更に対するテストの作成または更新
        - 適切なテストスイートを実行する
        - リンティング、フォーマット、または型チェックの確認
        - 最終的な動作が要求と一致していることを確認する
        - 差分を確認して、バグ、回帰、または危険なパターンがないか調べる
- アンチパターン
    - プロンプトに全部詰め込む
    - ビルド・テストなどの手順をエージェントに確認させる
    - 複雑なタスクで計画を省略
    - サンドボックスの不適切な設定
    - git を使わない
    - 手動でうまくいく感触が得られる前に自動化する
    - Codex と人間とで直列に作業する
    - １つのスレッドをずっと使い回す

### [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans)

- GPT-5.2-codex の自体の資料なのでだいぶ古い
- そもそも、計画を伝えるという考え方自体が GPT-5.5 のベストプラクティスと衝突する
- 気にしなくて良さそう

### [Prompt Caching 101](https://developers.openai.com/cookbook/examples/prompt_caching101)

- めっちゃ古いけど、2026 年冒頭あたりでもまだ有用らしい
- 静的コンテンツや頻繁に再利用されるコンテンツをプロンプトの先頭に配置する
- 一定のパターンのプロンプトを使い続ける
- 指標を監視する

### [Prompt Caching 201](https://developers.openai.com/cookbook/examples/prompt_caching_201?utm_source=chatgpt.com)

- キャッシュ判定
    - プレフィックス完全一致
    - 1K トークン以上
    - 128 トークン単位
- コンパクションでキャッシュが効かなくなる（当たり前）
- 動的に変化する要素はプロンプトの末尾に押し込む
- `metadata`
    - TODO って何？
- dict を json 化する系で、メンバの並び順の不安定さがキャシュヒット率に悪影響を与えているかも…

### [Prompt caching | OpenAI API](https://developers.openai.com/api/docs/guides/prompt-caching?utm_source=chatgpt.com)

- 公式ドキュメントとしてのキャッシュの話なので、これを参照するのが良さそう
- 短時間でリクエストをバーストさせると (>15RPM) 別のマシンにルーティングされてキャッシュが効かなくなるらしい
- 既にブログ (201) で述べられていることばかり

### [Prompt engineering | OpenAI API](https://developers.openai.com/api/docs/guides/prompt-engineering)

- 特に目立った情報は無い（ここまでで既に拾えている）

### [Best practices for prompt engineering with the OpenAI API | OpenAI Help Center](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)

- テキスト情報をソースとしてプロンプトに注入する時は markdown でいうコードブロック的なもので括る
    - `"""` とか `###` とからしい
    - 別にコードブロックで良いのでは
- あれこれ指定しろ系
    - 文脈（補足説明）
    - 何を出力すればよいか？
    - 出力の長さ、フォーマット、スタイル
    - 構造的な出力を望むなら、そのフォーマットを指定する
- 指示は具体的に書いたほうが良い（e.g. 短く返せって具体的には何文字？）
- Don't を書かずに Do だけで済むならそれが良い
- 誘導語を書く (python コードなら import を書く)

### [Frontend prompt instructions | OpenAI API](https://developers.openai.com/api/docs/guides/frontend-prompt)

- フロントエンド開発をする時のサンプル手順書
- Skill を入手すればそれで良いのでは
