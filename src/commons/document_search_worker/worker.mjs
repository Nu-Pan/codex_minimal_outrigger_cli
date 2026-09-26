// The worker receives only text already authorized by Python. Stdout is JSON only.
import { getLlama } from "node-llama-cpp";
import { readFileSync } from "node:fs";

function parentIsAlive(pid, expectedStartTime) {
  try {
    const fields = readFileSync(`/proc/${pid}/stat`, "utf8").split(") ").at(-1).split(" ");
    return fields[19] === expectedStartTime;
  } catch {
    return false;
  }
}

function fail(message) {
  throw new Error(message);
}

function requireObject(value) {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    fail("invalid worker input");
  }
  return value;
}

function tokensFor(model, chars, start, end) {
  return model.tokenize(chars.slice(start, end).join(""), false).length;
}

function chunkRanges(text, model, chunkTokens, overlapTokens) {
  const chars = Array.from(text);
  const ranges = [];
  let start = 0;
  while (start < chars.length) {
    let low = start + 1;
    let high = chars.length;
    let end = start;
    while (low <= high) {
      const middle = Math.floor((low + high) / 2);
      if (tokensFor(model, chars, start, middle) <= chunkTokens) {
        end = middle;
        low = middle + 1;
      } else {
        high = middle - 1;
      }
    }
    if (end === start) fail("chunk token limit is too small");
    const excerpt = chars.slice(start, end).join("");
    if (excerpt.trim()) ranges.push({ start, end, excerpt });
    if (end === chars.length) break;
    if (overlapTokens === 0) {
      start = end;
      continue;
    }
    low = start + 1;
    high = end;
    let next = end;
    while (low <= high) {
      const middle = Math.floor((low + high) / 2);
      if (tokensFor(model, chars, middle, end) <= overlapTokens) {
        next = middle;
        high = middle - 1;
      } else {
        low = middle + 1;
      }
    }
    start = Math.max(start + 1, next);
  }
  return ranges;
}

function checkedVector(value, dimensions) {
  const vector = Array.from(value?.vector ?? []);
  if (vector.length !== dimensions ||
      !vector.every((item) => typeof item === "number" && Number.isFinite(item)) ||
      !vector.some((item) => item !== 0)) {
    fail("invalid embedding vector");
  }
  return vector;
}

function checkedEmbeddingInput(model, text, contextSize) {
  // 3.20.0 checks the tokenized text before adding BOS/EOS. Reserve both slots.
  if (model.tokenize(text, false).length + 2 > contextSize) {
    fail("embedding context is insufficient");
  }
  return text;
}

async function withModel(modelPath, callback) {
  const llama = await getLlama({
    gpu: false, build: "never", skipDownload: true, logger: () => {},
  });
  const model = await llama.loadModel({ modelPath, gpuLayers: 0 });
  try {
    return await callback(model);
  } finally {
    await model.dispose();
  }
}

async function embedDocuments(request) {
  const { payload, embedding_model: modelPath, dimensions } = request;
  const { documents, config } = requireObject(payload);
  requireObject(documents);
  requireObject(config);
  return withModel(modelPath, async (model) => {
    const context = await model.createEmbeddingContext({
      contextSize: config.embedding_context_tokens,
      batchSize: config.batch_tokens,
      threads: config.threads,
    });
    try {
      const result = {};
      for (const [path, text] of Object.entries(documents)) {
        if (typeof text !== "string" || !text.trim()) fail("invalid document text");
        result[path] = [];
        for (const range of chunkRanges(
          text, model, config.chunk_tokens, config.chunk_overlap_tokens
        )) {
          const vector = checkedVector(
            await context.getEmbeddingFor(
              checkedEmbeddingInput(model, range.excerpt, config.embedding_context_tokens)
            ), dimensions
          );
          result[path].push({ start: range.start, end: range.end, embedding: vector });
        }
        if (result[path].length === 0) fail("document has no chunks");
      }
      return result;
    } finally {
      await context.dispose();
    }
  });
}

async function embedQuery(request) {
  const { payload, embedding_model: modelPath, dimensions } = request;
  const { text, config } = requireObject(payload);
  if (typeof text !== "string" || !text.trim()) fail("invalid query text");
  return withModel(modelPath, async (model) => {
    const context = await model.createEmbeddingContext({
      contextSize: config.embedding_context_tokens,
      batchSize: config.batch_tokens,
      threads: config.threads,
    });
    try {
      return checkedVector(
        await context.getEmbeddingFor(
          checkedEmbeddingInput(model, text, config.embedding_context_tokens)
        ), dimensions
      );
    } finally {
      await context.dispose();
    }
  });
}

async function rerank(request) {
  const { payload, reranker_model: modelPath } = request;
  const { query, documents, config, input_format: inputFormat } = requireObject(payload);
  if (typeof query !== "string" || !query.trim() || !Array.isArray(documents) ||
      inputFormat !== "gguf_template_yes_no") fail("invalid reranking input");
  return withModel(modelPath, async (model) => {
    const context = await model.createRankingContext({
      contextSize: config.reranker_context_tokens,
      batchSize: config.batch_tokens,
      threads: config.threads,
    });
    try {
      if (typeof context._getEvaluationInput !== "function" ||
          typeof context._llamaContext?._ctx?.getEmbedding !== "function" ||
          typeof context._sequence?.eraseContextTokenRanges !== "function") {
        fail("raw ranking API is incompatible");
      }
      const scores = [];
      for (const document of documents) {
        if (typeof document !== "string" || !document.trim()) fail("invalid candidate");
        const input = context._getEvaluationInput(query, document);
        if (!Array.isArray(input) || input.length === 0 ||
            input.length > context._llamaContext.contextSize) {
          fail("reranking context is insufficient");
        }
        await context._sequence.eraseContextTokenRanges([{
          start: 0, end: context._sequence.nextTokenIndex,
        }]);
        const evaluation = context._sequence.evaluate(input, { _noSampling: true });
        for await (const _token of evaluation) break;
        // 3.20.0 rank() maps an empty native array to score zero. Reject it here.
        const raw = context._llamaContext._ctx.getEmbedding(input.length, 1);
        if (raw?.length !== 1 || typeof raw[0] !== "number" ||
            !Number.isFinite(raw[0])) fail("native ranking score is missing");
        const score = context._currentArchRankingAlreadyNormalized
          ? raw[0] : 1 / (1 + Math.exp(-raw[0]));
        if (!Number.isFinite(score) || score < 0 || score > 1) {
          fail("native ranking score is invalid");
        }
        scores.push(score);
      }
      return scores;
    } finally {
      await context.dispose();
    }
  });
}

async function main() {
  let data = "";
  for await (const chunk of process.stdin) data += chunk;
  const request = requireObject(JSON.parse(data));
  if (!Number.isInteger(request.parent_pid) ||
      typeof request.parent_start_time !== "string" ||
      !parentIsAlive(request.parent_pid, request.parent_start_time)) {
    fail("inference parent is unavailable");
  }
  const parentWatcher = setInterval(() => {
    if (!parentIsAlive(request.parent_pid, request.parent_start_time)) process.exit(1);
  }, 250);
  parentWatcher.unref();
  const result = request.operation === "chunk_embed"
    ? await embedDocuments(request)
    : request.operation === "embed_query"
      ? await embedQuery(request)
      : request.operation === "rerank"
        ? await rerank(request)
        : fail("unknown operation");
  process.stdout.write(JSON.stringify({ status: "ok", result }));
}

main().catch((error) => {
  process.stderr.write(`document search worker failed: ${error?.message ?? "unknown"}\n`);
  process.exitCode = 1;
});
