const fs = require('fs');
const path = require('path');

const targetFile = path.join(__dirname, 'src/components/compare/ComparisonMatrixTab.tsx');
let content = fs.readFileSync(targetFile, 'utf8');

// Fix the cascade of replacements:
// bg-white dark:bg-slate-900 dark:bg-slate-50 -> bg-white dark:bg-slate-900
content = content.replace(/bg-white dark:bg-slate-900 dark:bg-slate-50/g, 'bg-white dark:bg-slate-900');

// text-slate-900 dark:text-slate-50 dark:text-slate-900 -> text-slate-900 dark:text-slate-50
content = content.replace(/text-slate-900 dark:text-slate-50 dark:text-slate-900/g, 'text-slate-900 dark:text-slate-50');

// bg-slate-900 dark:bg-slate-50 dark:bg-slate-50 -> bg-slate-900 dark:bg-slate-50
content = content.replace(/bg-slate-900 dark:bg-slate-50 dark:bg-slate-50/g, 'bg-slate-900 dark:bg-slate-50');

// text-white dark:text-slate-900 dark:text-slate-50 -> text-white dark:text-slate-900
content = content.replace(/text-white dark:text-slate-900 dark:text-slate-50/g, 'text-white dark:text-slate-900');

// text-slate-900 dark:text-slate-900 -> text-slate-900 dark:text-slate-50
content = content.replace(/text-slate-900 dark:text-slate-900/g, 'text-slate-900 dark:text-slate-50');

fs.writeFileSync(targetFile, content, 'utf8');
console.log('Fixed overlapping dark mode classes');
