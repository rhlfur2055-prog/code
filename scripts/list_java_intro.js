const fs = require('fs');
const path = require('path');

const contentsJsonPath = path.join(__dirname, '..', 'src', 'data', 'contents.json');
const contentsData = JSON.parse(fs.readFileSync(contentsJsonPath, 'utf8'));

const javaIntroFiles = contentsData.contents.filter(c => 
    c.category === 'java' && c.subcategory === '01_입문'
);

console.log(`Found ${javaIntroFiles.length} files in Java/01_입문:`);
javaIntroFiles.sort((a, b) => a.order - b.order).forEach(c => {
    console.log(`${c.order}. [${c.slug}] ${c.title} (${c.type})`);
});
