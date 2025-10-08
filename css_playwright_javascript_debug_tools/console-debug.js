// CONSOLE CSS DEBUG SCRIPT - Paste this into browser console (F12)
// Navigate to: http://localhost:8000/index.php?main_page=index&cPath=14
// Then paste and run this script

console.clear();
console.log('%c🚀 CSS WHITE BLOCK DETECTOR', 'color: #ff6b6b; font-size: 20px; font-weight: bold; background: #fff; padding: 5px;');

// Find elements causing layout issues
const problems = [];
const viewport = { width: window.innerWidth, height: window.innerHeight };

document.querySelectorAll('*').forEach(el => {
    const rect = el.getBoundingClientRect();
    const style = window.getComputedStyle(el);
    
    // Check for elements extending beyond viewport
    const extendsLeft = rect.left < -10;
    const extendsRight = rect.right > viewport.width + 10;
    const isLargeWhite = rect.width > 500 && rect.height > 100 && 
                        (style.backgroundColor.includes('255') || style.backgroundColor === 'white');
    
    if (extendsLeft || extendsRight || isLargeWhite) {
        problems.push({
            element: el,
            issue: extendsLeft ? '⬅️ EXTENDS LEFT' : 
                   extendsRight ? '➡️ EXTENDS RIGHT' : 
                   '⬜ LARGE WHITE BLOCK',
            left: Math.round(rect.left),
            right: Math.round(rect.right),
            width: Math.round(rect.width),
            height: Math.round(rect.height),
            selector: el.tagName.toLowerCase() + 
                     (el.id ? '#' + el.id : '') + 
                     (el.className ? '.' + el.className.split(' ').slice(0,3).join('.') : ''),
            position: style.position,
            marginLeft: style.marginLeft,
            marginRight: style.marginRight,
            transform: style.transform,
            overflow: style.overflow
        });
    }
});

// Sort by severity (left extension is worst)
problems.sort((a, b) => {
    if (a.left < b.left) return -1;
    if (a.right > b.right) return -1;
    return 0;
});

console.log(`\n%c🔍 FOUND ${problems.length} LAYOUT ISSUES:`, 'color: #ffa500; font-size: 16px; font-weight: bold;');

problems.forEach((prob, i) => {
    console.group(`%c${i+1}. ${prob.issue}: ${prob.selector}`, 'color: #ff6b6b; font-weight: bold; font-size: 14px;');
    
    console.log(`📐 Position: left=${prob.left}px, width=${prob.width}px (extends to ${prob.right}px)`);
    console.log(`🎯 CSS Position: ${prob.position}`);
    console.log(`📏 Margins: ${prob.marginLeft} / ${prob.marginRight}`);
    if (prob.transform !== 'none') console.log(`🔄 Transform: ${prob.transform}`);
    console.log(`💾 Element:`, prob.element);
    
    // Highlight the element
    prob.element.style.outline = `4px solid ${i === 0 ? '#ff0000' : '#ff6b6b'}`;
    prob.element.style.outlineOffset = '2px';
    prob.element.style.zIndex = '999999';
    
    console.groupEnd();
});

// Specific generator parts analysis
console.log('\n%c🎯 GENERATOR PARTS CONTAINER ANALYSIS:', 'color: #4ecdc4; font-size: 16px; font-weight: bold;');
const container = document.querySelector('.holder.fullwidth.full-nopad.out-banners-generator-parts');

if (container) {
    const rect = container.getBoundingClientRect();
    const style = window.getComputedStyle(container);
    
    console.group('Container Details:');
    console.log('📍 Position:', style.position);
    console.log('📐 CSS Width:', style.width, '| Actual:', Math.round(rect.width) + 'px');
    console.log('📏 CSS Height:', style.height, '| Actual:', Math.round(rect.height) + 'px');
    console.log('⬅️ Left position:', Math.round(rect.left) + 'px');
    console.log('📦 Margins:', style.marginLeft, '/', style.marginRight);
    console.log('🔄 Transform:', style.transform);
    console.log('🎨 Background:', style.backgroundColor);
    console.log('💾 Element:', container);
    console.groupEnd();
    
    // Check what's pushing it out
    if (rect.left < -10 || rect.right > viewport.width + 10) {
        console.log('%c❌ CONTAINER IS THE PROBLEM!', 'color: #ff0000; font-size: 16px; font-weight: bold;');
        
        // Find the specific CSS rule causing the issue
        console.log('\n%c🔧 SUGGESTED FIXES:', 'color: #2ecc71; font-size: 14px; font-weight: bold;');
        
        if (style.marginLeft.includes('calc')) {
            console.log('1. margin-left calc() is extending beyond viewport');
            console.log('   Fix: Set margin-left: 0 !important;');
        }
        
        if (style.width === '100vw') {
            console.log('2. width: 100vw is too wide with margins');
            console.log('   Fix: Set width: 100% !important;');
        }
        
        if (style.transform !== 'none') {
            console.log('3. Transform is shifting the element');
            console.log('   Fix: Set transform: none !important;');
        }
    }
    
    // Scroll to container
    container.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
} else {
    console.log('❌ Generator parts container not found!');
}

// Show quick fix suggestions
console.log('\n%c🛠️ QUICK FIX COMMANDS:', 'color: #2ecc71; font-size: 16px; font-weight: bold;');
console.log('Copy and paste these commands to test fixes:');

console.log('\n// Fix 1: Reset container positioning');
console.log(`const container = document.querySelector('.holder.fullwidth.full-nopad.out-banners-generator-parts');
if (container) {
    container.style.setProperty('margin-left', '0', 'important');
    container.style.setProperty('margin-right', '0', 'important');
    container.style.setProperty('width', '100%', 'important');
    container.style.setProperty('transform', 'none', 'important');
    console.log('✅ Container positioning reset');
}`);

console.log('\n// Fix 2: Remove all full-width styling');
console.log(`const container = document.querySelector('.holder.fullwidth.full-nopad.out-banners-generator-parts');
if (container) {
    container.style.setProperty('position', 'static', 'important');
    container.style.setProperty('left', 'auto', 'important');
    container.style.setProperty('right', 'auto', 'important');
    container.style.setProperty('margin', '0 auto', 'important');
    container.style.setProperty('max-width', '1200px', 'important');
    console.log('✅ Full-width styling removed');
}`);

if (problems.length > 0) {
    console.log(`\n%c🎯 WORST ISSUE: ${problems[0].issue}`, 'color: #ff0000; font-size: 18px; font-weight: bold;');
    console.log('Check the highlighted element above ☝️');
} else {
    console.log('\n%c✅ NO MAJOR LAYOUT ISSUES FOUND', 'color: #2ecc71; font-size: 16px; font-weight: bold;');
}