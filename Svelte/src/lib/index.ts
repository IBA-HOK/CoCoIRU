// よく使うリソースをここで再エクスポート（Re-export）するためのファイルです。
// ここに登録すると、どの階層からでも `import { Name } from '$lib';` で呼び出せるようになります。
//
// メリット:
// 1. インポートのパス記述が短くなり、可読性が上がる
// 2. ファイルの場所が変わっても、ここでパスを修正するだけで済む

export { default as Button } from './components/Button.svelte';
export { default as Surface } from './components/Surface.svelte';
export { default as Title } from './components/Title.svelte';
export { default as Footer } from './components/Footer.svelte';