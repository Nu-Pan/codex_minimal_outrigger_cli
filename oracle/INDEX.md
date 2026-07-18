# `doc`

## Summary
- cmoc のアプリケーション仕様を定める oracle doc 群の入口。branch・commit・worktree、refactor の不採用案、開発規則など、個別の正本仕様文書へ案内する。

## Read this when
- cmoc のアプリケーション挙動、branch 運用、refactor 判断、または Python・CLI・開発環境・テストの正本仕様を探すとき。
- 個別仕様文書の場所が特定できず、oracle doc の関連領域を横断して入口を探すとき。

## Do not read this when
- 対象となる個別仕様文書を直接特定できており、その本文だけを確認すればよいとき。
- 実装詳細や一般的な調査など、cmoc の正本仕様に関係しない内容を確認するとき。

## hash
- 791bdf395e4924e429a3e74f2073b2477683b9a49b08d0b620a8292baa063887

# `src`

## Summary
- oracle/src contains the source definitions for cmoc’s oracle implementation. It serves as the entry point for ACP call construction, configuration and path handling, rule/document processing, Markdown conversion, prompt construction, and shared standard-rule components; inspect its subdirectories for each responsibility.

## Read this when
- Determining which oracle implementation area handles ACP builders, configuration or paths, rule/document processing, Markdown conversion, prompt generation, or shared standard components.
- Tracing coordination across multiple oracle implementation responsibilities.

## Do not read this when
- Investigating the concrete CLI execution path, agent-call runtime, or TUI behavior.
- Inspecting a specific oracle file or realization file; proceed directly to that file or its responsible subdirectory.

## hash
- a1d4ad70bbf454e8df1e90fcd111c39412028e569ea599ae351b1b78996c65b8
