const fs = require('fs');
const path = require('path');

const targetFile = path.join(__dirname, 'src/components/compare/ComparisonMatrixTab.tsx');
let content = fs.readFileSync(targetFile, 'utf8');

const replacements = [
  { regex: /\bbg-white\b/g, replacement: 'bg-white dark:bg-slate-900' },
  { regex: /\bbg-slate-50\b/g, replacement: 'bg-slate-50 dark:bg-slate-800' },
  { regex: /\bbg-slate-100\b/g, replacement: 'bg-slate-100 dark:bg-slate-800' },
  { regex: /\btext-slate-900\b/g, replacement: 'text-slate-900 dark:text-slate-50' },
  { regex: /\btext-slate-800\b/g, replacement: 'text-slate-800 dark:text-slate-200' },
  { regex: /\btext-slate-700\b/g, replacement: 'text-slate-700 dark:text-slate-300' },
  { regex: /\btext-slate-600\b/g, replacement: 'text-slate-600 dark:text-slate-400' },
  { regex: /\btext-slate-500\b/g, replacement: 'text-slate-500 dark:text-slate-400' },
  { regex: /\bborder-slate-200\b/g, replacement: 'border-slate-200 dark:border-slate-700' },
  { regex: /\bborder-slate-100\b/g, replacement: 'border-slate-100 dark:border-slate-800' },
  { regex: /\bborder-slate-300\b/g, replacement: 'border-slate-300 dark:border-slate-700' },
  { regex: /\bbg-emerald-50\b/g, replacement: 'bg-emerald-50 dark:bg-emerald-950/30' },
  { regex: /\bbg-emerald-100\b/g, replacement: 'bg-emerald-100 dark:bg-emerald-900/50' },
  { regex: /\bbg-blue-50\b/g, replacement: 'bg-blue-50 dark:bg-blue-950/30' },
  { regex: /\bbg-rose-50\b/g, replacement: 'bg-rose-50 dark:bg-rose-950/30' },
  { regex: /\bbg-slate-900\b(?! dark:bg-slate-900)/g, replacement: 'bg-slate-900 dark:bg-slate-50' },
  { regex: /\btext-white\b(?! dark:text-slate-900)/g, replacement: 'text-white dark:text-slate-900' },
];

for (const { regex, replacement } of replacements) {
  content = content.replace(regex, replacement);
}

// Clean up any double replacements just in case
content = content.replace(/dark:bg-slate-900 dark:bg-slate-900/g, 'dark:bg-slate-900');
content = content.replace(/dark:text-slate-50 dark:text-slate-50/g, 'dark:text-slate-50');

fs.writeFileSync(targetFile, content, 'utf8');
console.log('Applied dark mode classes to ComparisonMatrixTab.tsx');
