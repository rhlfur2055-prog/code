const fs = require('fs');
const path = require('path');

const contentsPath = path.join(__dirname, '..', 'src', 'data', 'contents.json');
const publicPath = path.join(__dirname, '..', 'public', 'study');

console.log('🔍 Starting Content Integrity Verification...');

try {
    const data = JSON.parse(fs.readFileSync(contentsPath, 'utf8'));
    const contents = data.contents;
    
    console.log(`📂 Total entries in contents.json: ${contents.length}`);
    
    let stats = {
        total: contents.length,
        exists: 0,
        missing: 0,
        realContent: 0,
        template: 0
    };

    const missingFiles = [];
    const templateFiles = [];

    contents.forEach(content => {
        const filePath = path.join(publicPath, content.category, content.subcategory, `${content.slug}.html`);
        
        if (fs.existsSync(filePath)) {
            stats.exists++;
            const fileContent = fs.readFileSync(filePath, 'utf8');
            
            // Check for template indicators
            // Assuming "준비 중" or "학습을 진행하며 채워나가세요" or very short content indicates a template
            // Also checking if we specifically marked it as "essential" recently
            
            const isTemplate = fileContent.includes('학습을 진행하며 채워나가세요') || 
                               fileContent.includes('준비 중입니다') ||
                               fileContent.length < 500; // Arbitrary threshold for "too short"

            if (isTemplate) {
                stats.template++;
                templateFiles.push(`${content.category}/${content.subcategory}/${content.slug}`);
            } else {
                stats.realContent++;
            }
        } else {
            stats.missing++;
            missingFiles.push(`${content.category}/${content.subcategory}/${content.slug}`);
        }
    });

    console.log('\n📊 Verification Results:');
    console.log(`✅ Files Found: ${stats.exists}`);
    console.log(`❌ Files Missing: ${stats.missing}`);
    console.log(`📝 Real Content: ${stats.realContent}`);
    console.log(`📄 Template/Placeholder: ${stats.template}`);
    
    if (missingFiles.length > 0) {
        console.log('\n❌ Missing Files (Sample 5):');
        missingFiles.slice(0, 5).forEach(f => console.log(` - ${f}`));
    }

    if (stats.template > 0) {
        console.log(`\n⚠️ Templates Remaining: ${stats.template}`);
    }

} catch (err) {
    console.error('Error reading contents.json:', err);
}
