# realization standards

## 前提

- realization files の基本情報は `<cmoc-root>/oracles/docs/app_specs/realization/basics.md` を参照すること
- realization standards とは realization files の内容が標準的に従うべき事項である
- cmoc による realization files 編集作業 (e.g. `cmoc apply` サブコマンド) の実装は realization standards と整合しなければならない
- `<cmoc-root>` 配下の realization files それ自身もまた realization standards に従わなければならない

## 記述標準

### realization files の総文字数の最小化を目標とする

- 前提
    - 実装担当者である AI に与える課題の難易度という観点で realization files の規模は小さい方が望ましい
    - トークン消費という観点で realization files の規模は小さい方が望ましい
- 規則
    - 必ず守らなければならない要件を満たしている範囲内（解空間内）で、realization files 全体で見た時の総文字数が最小となること（文字数最小解）を目指す
- e.g.
    - 複数個所で出現するよく似た処理は関数化し、それを各所で使い回すべきである
    - 意味的に重複している実装は１つに集約するべきである
    - 現行の仕様と関係のない、過去の仕様に基づく実装は削除されるべきである

### realization files の高品質化は望ましいことである

- 前提
    - realization files は cmoc により継続的にメンテナンス (i.e. `cmoc apply` サブコマンドによる oracles の反映) される
    - メンテナンスにかかるコスト (i.e. AI が消費するトークン数) の観点から realization files の品質は高いほうが望ましい
- 規則
    - 
- e.g.
    - 複数個所で出現するよく似た処理を関数化し、それを各所で使い回すべきである
    - コード・実装の意味的なブロックごとに、なぜその実装でなければいけないのか？　その根拠をコメントとして書くべきである
