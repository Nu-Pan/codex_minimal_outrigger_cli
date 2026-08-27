# `oracle_and_realization_basic.py`

## Summary
- oracle と realization の基本知識を説明する prompt builder。oracle file・realization file・uncategorised file の役割、下位概念、分類方法を、パス用プレースホルダーを展開可能な構造化文書ヘッダーとして構築する。
- oracle file は人間所有の正本仕様で realization file の生成元、realization file は oracle file の意図を具体化した AI 編集対象、uncategorised file は分類対象外として整理される。

## Read this when
- oracle と realization の責務や分類を説明するプロンプト部分を変更・調査するとき
- oracle file、realization file、uncategorised file の下位概念や配置先を確認するとき
- この基本説明を構造化文書ヘッダーとして組み立てる処理を追跡するとき

## Do not read this when
- oracle と realization の正本仕様そのものを確認したいときは、参照先として明記された oracle doc を直接読む場合
- プロンプト全体の組み立てや PlaceholderMap、SDHeader の一般仕様だけを確認したいとき
- 実装ファイルやテストファイルの具体的な配置・挙動だけを調べるとき

## hash
- a5c6186a3d26152f99210094e1ba6f507852b6faba924c1086e695acd60ac2da
