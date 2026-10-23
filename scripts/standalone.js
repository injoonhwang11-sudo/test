import {readFileSync,writeFileSync} from 'node:fs';
const model=readFileSync(new URL('../src/model.js',import.meta.url),'utf8').replaceAll('export ','');
const app=readFileSync(new URL('../src/app.js',import.meta.url),'utf8').replace(/^import .*;\n/gm,'');
const css=readFileSync(new URL('../src/style.css',import.meta.url),'utf8').replace(/^@import .*;\n/,'');
const html=`<!doctype html><html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#101311"><title>셋업 노트 · 트레이딩 저널</title><style>${css}</style></head><body><div id="app"></div><script type="module">${model}\n${app}</script></body></html>`;
writeFileSync(new URL('../setup-note.html',import.meta.url),html);
console.log('Created setup-note.html — open directly in Chrome, no server required.');
