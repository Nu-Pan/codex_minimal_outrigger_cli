# prompting best practice

## 概要

- 公式の情報から、cmoc に適用できそうな要素を抽出引き上げてまとめた文章がこれ

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

- 

### [Customization – Codex | OpenAI Developers](https://developers.openai.com/codex/concepts/customization?utm_source=chatgpt.com)

### [Best practices – Codex | OpenAI Developers](https://developers.openai.com/codex/learn/best-practices?utm_source=chatgpt.com)

### [Prompt Caching 201](https://developers.openai.com/cookbook/examples/prompt_caching_201?utm_source=chatgpt.com)

### [Prompt caching | OpenAI API](https://developers.openai.com/api/docs/guides/prompt-caching?utm_source=chatgpt.com)

### [Prompt engineering | OpenAI API](https://developers.openai.com/api/docs/guides/prompt-engineering)


### [Best practices for prompt engineering with the OpenAI API | OpenAI Help Center](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)


### [Frontend prompt instructions | OpenAI API](https://developers.openai.com/api/docs/guides/frontend-prompt)

- フロントエンド開発をする時のサンプル手順書
- Skill を入手すればそれで良いのでは
