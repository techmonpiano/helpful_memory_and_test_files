// CSS DEBUG ANALYZER - Comprehensive CSS Override Detection Bookmarklet
// Copy this code, wrap in javascript:( ... ), and save as bookmark

(function() {
    'use strict';
    
    // Remove existing debug panel
    const existingPanel = document.getElementById('css-debug-panel');
    if (existingPanel) {
        existingPanel.remove();
        return;
    }
    
    // Create debug panel
    const panel = document.createElement('div');
    panel.id = 'css-debug-panel';
    panel.style.cssText = `
        position: fixed !important;
        top: 10px !important;
        right: 10px !important;
        width: 400px !important;
        max-height: 80vh !important;
        overflow-y: auto !important;
        background: #1e1e1e !important;
        color: #fff !important;
        border: 2px solid #007acc !important;
        border-radius: 8px !important;
        padding: 15px !important;
        font-family: Monaco, Consolas, monospace !important;
        font-size: 12px !important;
        z-index: 999999 !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    `;
    
    // CSS Specificity Calculator
    function calculateSpecificity(selector) {
        let a = 0, b = 0, c = 0;
        
        // Remove pseudo-elements and pseudo-classes for counting
        const cleanSelector = selector.replace(/:+[\w-]+(\([^)]*\))?/g, '');
        
        // Count IDs
        a = (cleanSelector.match(/#[\w-]+/g) || []).length;
        
        // Count classes, attributes, pseudo-classes
        b = (cleanSelector.match(/\.[\w-]+/g) || []).length;
        b += (cleanSelector.match(/\[[^\]]*\]/g) || []).length;
        b += (selector.match(/:[\w-]+/g) || []).length;
        
        // Count elements
        c = (cleanSelector.match(/\b[a-zA-Z][\w-]*/g) || []).length;
        
        return {
            value: a * 100 + b * 10 + c,
            breakdown: `(${a},${b},${c})`
        };
    }
    
    // Find all stylesheets and rules affecting element
    function analyzeElement(element) {
        const computedStyle = window.getComputedStyle(element);
        const rules = [];
        
        // Get all stylesheets
        for (let sheet of document.styleSheets) {
            try {
                for (let rule of sheet.cssRules || []) {
                    if (rule.type === CSSRule.STYLE_RULE) {
                        try {
                            if (element.matches(rule.selectorText)) {
                                const specificity = calculateSpecificity(rule.selectorText);
                                rules.push({
                                    selector: rule.selectorText,
                                    specificity: specificity,
                                    cssText: rule.style.cssText,
                                    href: sheet.href || 'inline'
                                });
                            }
                        } catch (e) {
                            // Skip invalid selectors
                        }
                    }
                }
            } catch (e) {
                // Skip inaccessible stylesheets
            }
        }
        
        // Sort by specificity
        rules.sort((a, b) => b.specificity.value - a.specificity.value);
        
        return {
            element: element,
            tagName: element.tagName.toLowerCase(),
            id: element.id,
            classes: Array.from(element.classList),
            rules: rules,
            computedStyle: {
                position: computedStyle.position,
                display: computedStyle.display,
                width: computedStyle.width,
                height: computedStyle.height,
                margin: computedStyle.margin,
                padding: computedStyle.padding,
                backgroundColor: computedStyle.backgroundColor,
                zIndex: computedStyle.zIndex
            }
        };
    }
    
    // Find suspicious white block elements
    function findSuspiciousElements() {
        const suspicious = [];
        const allElements = document.querySelectorAll('*');
        
        allElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);
            
            // Look for large white elements or elements extending beyond viewport
            if ((rect.width > 500 || rect.height > 200) && 
                (style.backgroundColor === 'rgb(255, 255, 255)' || 
                 style.backgroundColor === 'white' ||
                 rect.left < -100 || rect.right > window.innerWidth + 100)) {
                
                suspicious.push({
                    element: el,
                    reason: rect.left < -100 ? 'Extends left' : 
                           rect.right > window.innerWidth + 100 ? 'Extends right' :
                           'Large white background',
                    width: rect.width,
                    height: rect.height,
                    left: rect.left,
                    backgroundColor: style.backgroundColor
                });
            }
        });
        
        return suspicious.slice(0, 10); // Top 10
    }
    
    // Main analysis
    let selectedElement = null;
    let suspiciousElements = findSuspiciousElements();
    
    // Create panel content
    function updatePanel() {
        panel.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="margin: 0; color: #007acc;">CSS Debug Analyzer</h3>
                <button onclick="this.parentElement.parentElement.remove()" style="background: #e74c3c; color: white; border: none; border-radius: 3px; padding: 5px 10px; cursor: pointer;">×</button>
            </div>
            
            <div style="margin-bottom: 15px;">
                <h4 style="color: #f39c12; margin: 5px 0;">🔍 Click any element to analyze</h4>
                <div style="font-size: 11px; color: #bbb;">
                    Hover over elements and click to see CSS hierarchy and overrides
                </div>
            </div>
            
            <div style="margin-bottom: 15px;">
                <h4 style="color: #e74c3c; margin: 5px 0;">⚠️ Suspicious Elements (${suspiciousElements.length})</h4>
                ${suspiciousElements.map((item, i) => `
                    <div style="background: rgba(231,76,60,0.1); padding: 8px; margin: 5px 0; border-radius: 4px; cursor: pointer;" onclick="document.getElementById('css-debug-panel').highlightElement(this, ${i})">
                        <strong>${item.element.tagName.toLowerCase()}${item.element.id ? '#' + item.element.id : ''}</strong>
                        <div style="font-size: 10px; color: #ccc;">
                            ${item.reason} | ${Math.round(item.width)}×${Math.round(item.height)}px | Left: ${Math.round(item.left)}px
                        </div>
                    </div>
                `).join('')}
            </div>
            
            <div id="selected-analysis" style="display: none;">
                <h4 style="color: #2ecc71; margin: 5px 0;">📋 Selected Element Analysis</h4>
                <div id="analysis-content"></div>
            </div>
        `;
    }
    
    // Highlight element function
    panel.highlightElement = function(clickedDiv, index) {
        const suspicious = suspiciousElements[index];
        suspicious.element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        suspicious.element.style.outline = '3px solid #e74c3c';
        setTimeout(() => {
            suspicious.element.style.outline = '';
        }, 3000);
        
        // Show analysis
        selectedElement = suspicious.element;
        showElementAnalysis(suspicious.element);
    };
    
    // Show element analysis
    function showElementAnalysis(element) {
        const analysis = analyzeElement(element);
        const analysisDiv = document.getElementById('selected-analysis');
        const contentDiv = document.getElementById('analysis-content');
        
        contentDiv.innerHTML = `
            <div style="background: rgba(46,204,113,0.1); padding: 10px; border-radius: 4px; margin-bottom: 10px;">
                <strong>${analysis.tagName}${analysis.id ? '#' + analysis.id : ''}${analysis.classes.length ? '.' + analysis.classes.join('.') : ''}</strong>
            </div>
            
            <h5 style="color: #3498db; margin: 10px 0 5px 0;">Computed Styles:</h5>
            <div style="background: rgba(52,152,219,0.1); padding: 8px; border-radius: 4px; font-size: 11px;">
                ${Object.entries(analysis.computedStyle).map(([prop, value]) => 
                    `<div><span style="color: #3498db;">${prop}:</span> ${value}</div>`
                ).join('')}
            </div>
            
            <h5 style="color: #9b59b6; margin: 10px 0 5px 0;">CSS Rules (by specificity):</h5>
            ${analysis.rules.slice(0, 10).map(rule => `
                <div style="background: rgba(155,89,182,0.1); padding: 8px; margin: 5px 0; border-radius: 4px; font-size: 11px;">
                    <div style="color: #9b59b6;"><strong>${rule.selector}</strong> <span style="color: #f39c12;">${rule.specificity.breakdown}</span></div>
                    <div style="color: #bbb; font-size: 10px;">${rule.href.split('/').pop()}</div>
                    ${rule.cssText ? `<div style="color: #2ecc71; margin-top: 3px;">${rule.cssText.substring(0, 100)}${rule.cssText.length > 100 ? '...' : ''}</div>` : ''}
                </div>
            `).join('')}
        `;
        
        analysisDiv.style.display = 'block';
    }
    
    // Element selection handler
    let isSelecting = false;
    let highlightedElement = null;
    
    function highlightElement(e) {
        if (highlightedElement) {
            highlightedElement.style.outline = '';
        }
        if (e.target !== panel && !panel.contains(e.target)) {
            highlightedElement = e.target;
            e.target.style.outline = '2px solid #007acc';
        }
    }
    
    function selectElement(e) {
        if (e.target !== panel && !panel.contains(e.target)) {
            e.preventDefault();
            e.stopPropagation();
            selectedElement = e.target;
            showElementAnalysis(e.target);
            
            // Scroll to analysis
            document.getElementById('selected-analysis').scrollIntoView({ 
                behavior: 'smooth', 
                block: 'nearest' 
            });
        }
    }
    
    // Add event listeners
    document.addEventListener('mouseover', highlightElement);
    document.addEventListener('click', selectElement);
    
    updatePanel();
    document.body.appendChild(panel);
    
    // Instructions
    console.log('%c🔍 CSS Debug Analyzer Active!', 'color: #007acc; font-size: 16px; font-weight: bold;');
    console.log('• Hover over elements to highlight them');
    console.log('• Click any element to see its CSS hierarchy and overrides');
    console.log('• Check the debug panel for suspicious elements');
    console.log('• Click × to close the analyzer');
    
})();