// Exercise the actual inline script without navigating or submitting a form.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync(`${__dirname}/../public/index.html`, 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const href = html.match(/<a href="([^"]+)"/)[1];
for (const [query, expected] of [
  ['?ref=123456', '123456'], ['?ref=000123', '000123'],
  ['?v=2&ref=654321', '654321'], ['', null], ['?ref=', null],
  ['?ref=12345', null], ['?ref=1234567', null], ['?ref=ABC123', 'ABC123'], ['?ref=AX2046', 'AX2046'],
  ['?v=2&ref=ax2046', 'ax2046'], ['?ref=ABCDEF', 'ABCDEF'],
  ['?ref=AX204', null], ['?ref=AX20467', null], ['?ref=AX-046', null],
  ['?ref=%C3%89X2046', null],
  ['?ref=%20123456', null], ['?ref=123456%0A', null],
]) {
  const link = { href };
  let target;
  vm.runInNewContext(script, {
    URL, URLSearchParams, document: { querySelector: () => link },
    window: { location: { search: query, replace: value => { target = value; } } },
  });
  assert.equal(link.href, target);
  const url = new URL(target);
  assert.equal(url.origin, 'https://docs.google.com');
  assert.equal(url.pathname, '/forms/d/e/1FAIpQLSfV-G5dIiOWtGfLiEXc2h6JnuvsoAHvLBb0md_haiyWC7QNDQ/viewform');
  assert.deepEqual([...url.searchParams].filter(([key]) => key.startsWith('entry.')),
    expected === null ? [] : [['entry.1217740900', expected]]);
  console.log('PASS: fallback', query || 'absent');
}
