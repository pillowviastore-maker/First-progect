import { themeCheckRun } from '@shopify/theme-check-node';
const root = process.argv[2];
const res = await themeCheckRun(root, undefined, () => {});
const offenses = res.offenses ?? res;
const mine = offenses.filter(o => true);
for (const o of mine) console.log(o.uri.replace(/^.*First-progect\//,''), o.check, o.message, o.start?.line);
console.log('errors:', mine.length, 'total offenses:', offenses.length);
