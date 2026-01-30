const fs = require('fs');
const path = require('path');

const projectRoot = path.join(__dirname, '..');
const contentsJsonPath = path.join(projectRoot, 'src', 'data', 'contents.json');
const publicStudyPath = path.join(projectRoot, 'public', 'study');

console.log(`Checking content quality...`);

try {
    const contentsData = JSON.parse(fs.readFileSync(contentsJsonPath, 'utf8'));
    const contents = contentsData.contents;
    
    const missingFiles = [];
    const placeholderFiles = [];
    const realFiles = [];
    
    // Strings that indicate a file is just a template/placeholder
    const placeholderIndicators = [
        '자세한 내용은 학습을 진행하며 채워나가세요',
        '// 예제 코드가 여기에 들어갑니다',
        '학습을 진행하며 직접 작성해보세요'
    ];
    
    contents.forEach(content => {
        const { category, subcategory, slug, title } = content;
        const filePath = path.join(publicStudyPath, category, subcategory, `${slug}.html`);
        
        if (!fs.existsSync(filePath)) {
            missingFiles.push({
                id: content.id,
                title,
                path: `${category}/${subcategory}/${slug}.html`
            });
        } else {
            const fileContent = fs.readFileSync(filePath, 'utf8');
            const isPlaceholder = placeholderIndicators.some(indicator => fileContent.includes(indicator));
            
            if (isPlaceholder) {
                placeholderFiles.push({
                    id: content.id,
                    title,
                    path: `${category}/${subcategory}/${slug}.html`
                });
            } else {
                realFiles.push({
                    id: content.id,
                    title,
                    path: `${category}/${subcategory}/${slug}.html`
                });
            }
        }
    });
    
    console.log('---------------------------------------------------');
    console.log(`✅ Real Content Files: ${realFiles.length}`);
    console.log(`⚠️  Placeholder Files: ${placeholderFiles.length}`);
    console.log(`❌ Missing Files: ${missingFiles.length}`);
    console.log('---------------------------------------------------');
    
    if (placeholderFiles.length > 0) {
        console.log('\nTop 10 Placeholder Files (Need Content):');
        placeholderFiles.slice(0, 10).forEach(file => {
            console.log(`- [${file.path}] ${file.title}`);
        });
    }

} catch (error) {
    console.error('Error running verification:', error);
}
