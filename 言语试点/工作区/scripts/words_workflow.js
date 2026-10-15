export const meta = {
  name: 'gaici-annotate',
  description: '盖词语：147篇文章每篇挑4–6处选词填空式考点词并写辨析（Sonnet）',
  phases: [{ title: 'Annotate', detail: '10批，每批约15篇' }],
}
const SP = '/tmp/claude-0/-home-user-xingce/209cadd4-dba5-515b-8f1c-c663f6e288a0/scratchpad'
const batches = Array.from({ length: args.nb }, (_, i) => `${SP}/words/batches/w${String(i).padStart(2, '0')}.txt`)
const SCHEMA = { type: 'object', properties: { articles: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' },
  words: { type: 'array', items: { type: 'object', properties: {
    p: { type: 'integer' }, s: { type: 'string' }, pre: { type: 'string' },
    type: { type: 'string', enum: ['实词', '成语', '搭配', '关联词'] },
    note: { type: 'string' },
  }, required: ['p', 's', 'pre', 'type', 'note'] } },
}, required: ['id', 'words'] } } }, required: ['articles'] }

const out = await parallel(batches.map(b => () => agent(
  `先读任务说明 ${SP}/words/prompt.md 并严格照做。\n\n文章清单在 ${b}，每行一个 JSON 文件路径（字段 id、title、paras 自然段数组等）。逐篇读取、通读，清单里的每一篇都要交结果。`,
  { label: `words:${b.slice(-7, -4)}`, phase: 'Annotate', schema: SCHEMA, model: 'sonnet' })))
const failed = batches.filter((b, i) => !out[i])
if (failed.length) log('未完成的批次：' + failed.join(', '))
return { results: out.map((r, i) => r && { batch: batches[i], ann: r }).filter(Boolean), failed }
